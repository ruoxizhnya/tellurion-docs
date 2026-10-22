#!/usr/bin/env python3
"""12 仓文档齐套巡检（DOC-07）。

为什么需要它：拆成 12 个仓之后，"每仓该有的文档是否都在"只能靠人眼一仓一仓看。
这个脚本只查**存在性与形状**，不读正文、不比对内容 —— 正文真相在各仓自己的三件套里，
本仓 AGENTS.md §3 的「不复制，只索引」同样适用于检查器。

每仓判据（默认 12 仓全查）：
  AGENTS.md                       全部仓
  docs/TASKS.md                   全部仓
  docs/db-schema.md               非豁免仓
  docs/api-schema.md              非豁免仓
  docs/dataflow.md                非豁免仓
  docs/adr/ 至少 1 个 .md          非豁免仓
  docs/adr/0001-*.md              非豁免仓
  docs/odr/ 或 docs/archive/odr/   非豁免仓（两处都是已登记的 ODR 家）

豁免是**具名**的（EXEMPT 表逐条写理由），不是"找不到就算过"：
  2026-10-21 spec 审查 H1/L3 裁决 core 与本仓豁免三件薄规格与 adr/0001-*；
  另有两条按实仓取证追加，写在同一张表里（core 的 ADR / ODR 已随文档拆分迁走）。

用法：
    python tools/check_repo_docs.py                    # workspace = 本仓父目录（12 仓同级）
    python tools/check_repo_docs.py --workspace DIR    # 显式指定 12 仓所在目录
    python tools/check_repo_docs.py --repos a,b        # 只查部分仓（默认要求 12 仓齐）
    python tools/check_repo_docs.py --explain          # 打印每仓的豁免理由
退出码：0 = 齐套；1 = 有缺件 / 仓目录不存在 / 仓名未登记。
"""
import argparse
import glob
import os
import sys

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(TOOLS_DIR)

# 仓名与 module path 的唯一真相源：tellurion:docs/design/qt-decoupling/repo-inventory.md。
REPOS = (
    'tellurion',
    'tellurion-contracts',
    'tellurion-kit',
    'tellurion-agent',
    'tellurion-ui',
    'tellurion-data',
    'tellurion-strategy',
    'tellurion-risk',
    'tellurion-analytics',
    'tellurion-orchestration',
    'tellurion-broker',
    'tellurion-docs',
)

SPEC_FILES = ('docs/db-schema.md', 'docs/api-schema.md', 'docs/dataflow.md')
ADR_DIR = 'docs/adr'
ODR_HOMES = ('docs/odr', 'docs/archive/odr')

# 豁免表：key = 仓名，value = {检查项: 理由}。
# 只登记**具名**豁免；没登记的项一律按必需处理（fail-closed）。
EXEMPT = {
    'tellurion': {
        'specs': '三件薄规格豁免（2026-10-21 H1/L3）：API/DB/流程真相由 docs/openapi.yaml / pkg/storage/postgres.go / docs/SPEC.md 直接承载',
        'adr_dir': 'core 的 ADR 已随文档拆分全部住在 tellurion-docs/docs/adr（core AGENTS.md §10 记录本仓已无 docs/adr）',
        'adr_0001': '同上：core 不再持有 ADR 文件',
        'odr': 'ODR 随文档拆分迁至 tellurion-docs/docs/archive/odr（core AGENTS.md §10 记录的既有漂移）',
    },
    'tellurion-docs': {
        'specs': '三件薄规格豁免（2026-10-21 H1/L3）：本仓只做索引、不复制各仓契约正文（AGENTS.md §3.1）',
        'adr_0001': '本仓 ADR 是跨仓 ADR（adr-001~），没有 0001-* 的编号惯例（2026-10-21 H1/L3 裁决）',
    },
}

CHECKS = (
    ('AGENTS.md', 'file'),
    ('docs/TASKS.md', 'file'),
    ('specs', 'specs'),
    ('adr_dir', 'adr_dir'),
    ('adr_0001', 'adr_0001'),
    ('odr', 'odr'),
)

CHECK_LABELS = {
    'AGENTS.md': 'AGENTS.md',
    'docs/TASKS.md': 'docs/TASKS.md',
    'specs': ' / '.join(SPEC_FILES),
    'adr_dir': 'docs/adr/（至少 1 个 .md）',
    'adr_0001': 'docs/adr/0001-*.md',
    'odr': ' / '.join(ODR_HOMES),
}


def check_repo(workspace, name):
    """返回 (missing: [str], exempted: [(check_key, reason)], details: dict)。"""
    root = os.path.join(workspace, name)
    if not os.path.isdir(root):
        return ['仓目录不存在: %s' % root], [], {}

    missing, exempted, details = [], [], {}
    rules = EXEMPT.get(name, {})

    def skip(key):
        if key in rules:
            exempted.append((key, rules[key]))
            return True
        return False

    for key, kind in CHECKS:
        if skip(key):
            continue
        if kind == 'file':
            if not os.path.isfile(os.path.join(root, key)):
                missing.append(CHECK_LABELS[key])
            continue
        if kind == 'specs':
            for rel in SPEC_FILES:
                if not os.path.isfile(os.path.join(root, rel)):
                    missing.append(rel)
            continue
        if kind == 'adr_dir':
            count = len(glob.glob(os.path.join(root, ADR_DIR, '*.md')))
            details['adr'] = count
            if count == 0:
                missing.append(CHECK_LABELS[key])
            continue
        if kind == 'adr_0001':
            if not glob.glob(os.path.join(root, ADR_DIR, '0001-*.md')):
                missing.append(CHECK_LABELS[key])
            continue
        if kind == 'odr':
            home = next((h for h in ODR_HOMES if os.path.isdir(os.path.join(root, h))), None)
            details['odr'] = home
            if home is None:
                missing.append(CHECK_LABELS[key])
            continue

    return missing, exempted, details


def main(argv=None):
    parser = argparse.ArgumentParser(
        description='12 仓文档齐套巡检（只查存在性与形状，不读正文）')
    parser.add_argument('--workspace', default=os.path.dirname(REPO_ROOT),
                        help='12 个仓所在目录（默认：本仓的父目录）')
    parser.add_argument('--repos', default='',
                        help='逗号分隔的仓名子集；缺省 = 12 仓全查')
    parser.add_argument('--explain', action='store_true',
                        help='打印每仓的豁免理由')
    args = parser.parse_args(argv)

    if args.repos.strip():
        names = [s.strip() for s in args.repos.split(',') if s.strip()]
    else:
        names = list(REPOS)

    unknown = [n for n in names if n not in REPOS]
    if unknown:
        print('未登记的仓名：%s（12 仓清单见本文件 REPOS 与 repo-inventory.md）' % ', '.join(unknown))
        return 1

    workspace = os.path.abspath(args.workspace)
    print('12 仓文档齐套巡检：workspace=%s' % workspace)

    failed = 0
    exempted_repos = 0
    for name in names:
        missing, exempted, details = check_repo(workspace, name)
        if exempted:
            exempted_repos += 1
        if missing:
            failed += 1
            print('[MISS] %-24s 缺: %s' % (name, ' / '.join(missing)))
        else:
            bits = []
            if 'adr' in details:
                bits.append('adr %d' % details['adr'])
            if details.get('odr'):
                bits.append('odr=%s' % details['odr'])
            suffix = ('  （豁免 %d 项）' % len(exempted)) if exempted else ''
            print('[OK]   %-24s %s%s' % (name, ' · '.join(bits) or '齐', suffix))
        if args.explain:
            for key, reason in exempted:
                print('       -> 豁免 %s：%s' % (key, reason))

    if failed:
        print('小结：%d 仓全查 · 齐套 %d · 缺件 %d · 豁免 %d 仓'
              % (len(names), len(names) - failed, failed, exempted_repos))
        return 1
    print('小结：%d 仓全查 · 齐套 %d · 缺件 0 · 豁免 %d 仓'
          % (len(names), len(names), exempted_repos))
    return 0


if __name__ == '__main__':
    sys.exit(main())
