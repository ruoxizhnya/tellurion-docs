#!/usr/bin/env python3
"""docs/guides/ 跨仓引用检查（DOC-08）。

为什么需要它：三份 guide（`local-dev` / `deploy-config` / `data-dependencies`）
从单仓口径改成 12 仓口径后，正文里会有大量 `repo:path` 形式的**纯文本**跨仓引用
（如 `tellurion:pkg/storage/postgres.go`、`tellurion-agent:pkg/ai/client.go`）。
`check_doc_links.py` 只认 Markdown 链接 `[x](y)`，**看不见**这种写法 ——
于是两类失效都没有执法者：

  1. 仓名写错（`telliurion:docs/TASKS.md`）—— 读者会去一个不存在的仓里找；
  2. 路径在该仓已不存在（`tellurion:pkg/ai/pipeline`，2026-10-09 已迁 agent）
     —— 正是 DOC-08 要修的那类漂移。

判据分两层（与 DOC-07 的 `check_repo_docs.py` 同一套定位）：

  默认            仓名必须是 12 仓之一。**CI 可跑**（只需要本仓）。
  --workspace DIR 额外断言 path 在**该仓目录**里真实存在。**不进 CI** ——
                  CI 只 checkout 本仓，看不到另外 11 个仓。

两类刻意不判：

  - 不是「仓:路径」的冒号写法（`kernel:"nautilus"`、`status:failed`）——
    判据要求冒号右边含 `/`，即必须像一条路径；
  - 同一行或上一行出现否定词的引用（`cmd/strategy 已删除`）—— 历史说明
    合法地引用已不存在的路径，与 `check_doc_links.py` 的否定词窗口同源。

否定词是**按行文本**匹配的启发式（不是语义分析），两条边界如实写出：
  - 否定词落在**下一行**时不豁免 —— 写文档时把「不存在」放在同一行或上一行；
  - 被引用的**路径名本身**含否定词（如 `...删除...md`）时，会被一并放过。
    仓库里没有这种文件名，所以没为它加特例；真出现时再改判据。

用法：
    python tools/check_guide_refs.py                    # 只查仓名（CI 同款）
    python tools/check_guide_refs.py --workspace DIR    # 连路径存在性一起查
    python tools/check_guide_refs.py --dir docs/guides  # 换扫描目录
退出码：0 = 通过；1 = 有未登记仓名 / 路径不存在 / 扫描目录为空。
"""
import argparse
import os
import re
import sys

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(TOOLS_DIR)

# 12 仓清单的真相在 tellurion:docs/design/qt-decoupling/repo-inventory.md；
# 本仓已有一份代码副本在 check_repo_docs.py（DOC-07）。**import，不复制** ——
# 「同一个约定写两处、各改各的」正是这个仓反复收口过的那类失效。
# 加一条 sys.path 兜底，让脚本入口与 `python -m unittest` 两种跑法都解析得到。
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)

from check_repo_docs import REPOS  # noqa: E402

# `repo:path`。冒号右边**必须含 `/` 且以字母/下划线开头**，两条一起把非引用挡在外面：
#   - 含 `/` 挡掉 `status:failed` / `kernel:"nautilus"` / `{a}:{b}`；
#   - 不以数字开头挡掉 `localhost:5432/quant_trading` / `host.docker.internal:6379/x`
#     这类 **host:port/path** 写法（真仓实测：DSN 连接串就是这么被误判成仓名的）。
#
# ⚠️ 路径字符集包含 CJK（`\u4e00-\u9fff`）：两个库仓与六个服务仓的 ADR 文件名是中文
# （如 `0001-统一协议与-visible-at-第二道防线.md`）。只认 ASCII 时正则会停在第一个汉字，
# 把 `docs/adr/0001-编译期依赖-core-是过渡态.md` 截成 `docs/adr/0001-` ⇒ **误报缺失**
# （实测踩到过）。代价：引用后面紧跟中文且无分隔符时会把正文吞进路径 —— 所以
# 正文里一律用反引号包住引用。
REF = re.compile(
    r'(?<![A-Za-z0-9_./-])([a-z][a-z0-9-]*):([A-Za-z_][A-Za-z0-9_./\u4e00-\u9fff-]*)')

# 路径尾部可能粘上的标点（正文里 `tellurion:docs/TASKS.md`、`...，` 会连在一起）。
TRAILING = '）)，,。；;：:、'

# 否定词窗口 = 当前行 + 上一行（与 check_doc_links.py 同源）。
# 「已迁移 / 已删除」这类历史说明合法引用不存在的路径。
NEGATION_MARKERS = (
    '没有', '不存在', '并不存在', '已删除', '删除', '已删', '从未', '不许',
    '不再', '移除', '废弃', '退役', '已迁', '迁走', '空号',
)


def markdown_files(directory):
    return sorted(
        os.path.join(directory, n)
        for n in os.listdir(directory)
        if n.endswith('.md') and os.path.isfile(os.path.join(directory, n))
    )


def iter_refs(text):
    """产出 (行号, 仓名, 路径, 该行 + 上一行的窗口文本)。"""
    lines = text.split('\n')
    for idx, line in enumerate(lines):
        window = line + (lines[idx - 1] if idx >= 1 else '')
        for m in REF.finditer(line):
            repo, path = m.group(1), m.group(2)
            if '/' not in path:
                continue
            path = path.rstrip(TRAILING)
            # `cmd/...` 这种是省略号占位，不是一条可核对的路径 —— 跳过。
            # （实测：`tellurion-data:cmd/...` 会被当成缺失路径误报。）
            if '...' in path:
                continue
            if not path or '/' not in path:
                continue
            yield idx + 1, repo, path, window


def is_negated(window):
    return any(marker in window for marker in NEGATION_MARKERS)


def check(guides_dir, workspace):
    """返回 (errors, notes)。errors 非空即退出码 1。"""
    errors, notes = [], []

    if not os.path.isdir(guides_dir):
        return ['扫描目录不存在: %s' % guides_dir], notes

    files = markdown_files(guides_dir)
    if not files:
        return ['扫描目录里没有 .md 文件: %s' % guides_dir], notes

    for path in files:
        rel = os.path.relpath(path, REPO_ROOT).replace(os.sep, '/')
        with open(path, encoding='utf-8', errors='replace') as f:
            text = f.read()
        for lineno, repo, target, window in iter_refs(text):
            where = '%s:%d' % (rel, lineno)
            if repo not in REPOS:
                errors.append(
                    '%s 引用了未登记的仓 `%s` —— 12 仓清单见 repo-inventory.md'
                    % (where, repo))
                continue
            if workspace is None:
                continue
            root = os.path.join(workspace, repo)
            if not os.path.isdir(root):
                errors.append(
                    '%s 引用 `%s:%s`，但 workspace 里没有该仓目录（%s）'
                    % (where, repo, target, root))
                continue
            resolved = os.path.join(root, *target.split('/'))
            if os.path.exists(resolved):
                continue
            if is_negated(window):
                notes.append('%s  `%s:%s` 不存在，但同行/上行有否定词，按历史说明放过'
                             % (where, repo, target))
                continue
            errors.append(
                '%s 引用 `%s:%s`，该路径在 %s 仓里不存在 —— '
                '迁移过的路径要改指向，或就地写明「已迁到哪」'
                % (where, repo, target, repo))

    return errors, notes


def main(argv=None):
    parser = argparse.ArgumentParser(
        description='docs/guides/ 跨仓引用检查（只认 repo:path 纯文本引用）')
    parser.add_argument('--workspace', default=None,
                        help='12 仓所在目录；给了才校验路径存在性'
                             '（CI 只 checkout 本仓，故默认不查）')
    parser.add_argument('--dir', default=os.path.join(REPO_ROOT, 'docs', 'guides'),
                        help='扫描目录（默认 docs/guides）')
    args = parser.parse_args(argv)

    workspace = os.path.abspath(args.workspace) if args.workspace else None
    errors, notes = check(os.path.abspath(args.dir), workspace)

    scope = '仓名 + 路径存在性' if workspace else '只查仓名（未给 --workspace）'
    print('guides 跨仓引用检查：%s · %s' % (os.path.abspath(args.dir), scope))
    for n in notes:
        print('  · %s' % n)
    if errors:
        print('✗ %d 处引用失效：' % len(errors))
        for e in errors:
            print('  - %s' % e)
        return 1
    print('✓ 跨仓引用全部有效')
    return 0


if __name__ == '__main__':
    sys.exit(main())