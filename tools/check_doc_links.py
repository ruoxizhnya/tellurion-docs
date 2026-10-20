#!/usr/bin/env python3
"""tellurion-docs 链接检查。

为什么需要它：本仓从 monorepo 拆出后，历史文档里 300+ 条相对链接指向已迁往
其它仓的文件（`../TASKS.md`、`../design/kernel/...`、`file:///Users/.../quant-trading/...`）。
这些链接在本机"看起来能解析"（兄弟仓就在旁边），在 GitHub 上却一定 404 ——
所以检查器必须按**仓根**判界，不能只看本地磁盘。

判据分两层：
  活跃层（README / docs/*.md / docs/guides / docs/design）
      → **必须 0 断链**，否则退出码 1（CI 用）
  历史层（docs/adr / docs/archive）
      → 只统计不判红：决策记录是只读档案，链接指向已删除文件属预期

判定规则：
  1. 外链（http/https/mailto）→ 跳过；
  2. 链接目标逃出本仓根 → 断（即使本机存在兄弟仓）；
  3. 代码块（``` ... ```）内不解析（否则会把示例里的 `[x](y)` 当链接）。

用法：
    python tools/check_doc_links.py            # 只报活跃层，退出码 0/1
    python tools/check_doc_links.py --all      # 连同历史层明细一起打印
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEGACY_DIRS = ('docs/adr', 'docs/archive')

LINK = re.compile(r'(?<!\!)\[([^\]]*)\]\(([^)\s]+)(?:\s+"[^"]*")?\)')


def markdown_files():
    for dp, dns, fs in os.walk(ROOT):
        dns[:] = [d for d in dns if d not in ('.git', 'node_modules')]
        for f in fs:
            if f.endswith('.md'):
                yield os.path.join(dp, f)


def strip_fences(text):
    """把代码块内容替换成空行，保持行号不变。"""
    out, in_fence = [], False
    for line in text.split('\n'):
        if line.lstrip().startswith('```'):
            in_fence = not in_fence
            out.append('')
            continue
        out.append('' if in_fence else line)
    return '\n'.join(out)


def is_legacy(rel_path):
    rel = rel_path.replace(os.sep, '/')
    return any(rel == d or rel.startswith(d + '/') for d in LEGACY_DIRS)


def check():
    active_bad, legacy_bad = [], []
    active_total = legacy_total = 0

    for path in markdown_files():
        rel_file = os.path.relpath(path, ROOT)
        text = strip_fences(open(path, encoding='utf-8', errors='replace').read())
        for m in LINK.finditer(text):
            target = m.group(2).split('#')[0].split('?')[0].strip()
            if not target or target.startswith(('http://', 'https://', 'mailto:', '<')):
                continue
            resolved = os.path.normpath(os.path.join(os.path.dirname(path), target))
            inside = resolved == ROOT or resolved.startswith(ROOT + os.sep)
            broken = (not inside) or (not os.path.exists(resolved))

            if is_legacy(rel_file):
                legacy_total += 1
                if broken:
                    legacy_bad.append((rel_file, target))
            else:
                active_total += 1
                if broken:
                    active_bad.append((rel_file, target))

    print('活跃层：%d 条链接，%d 条断' % (active_total, len(active_bad)))
    for f, t in active_bad:
        print('  BROKEN  %s  ->  %s' % (f, t))
    print('历史层（%s）：%d 条链接，%d 条断（只统计，不判红）'
          % ('/'.join(LEGACY_DIRS), legacy_total, len(legacy_bad)))
    if '--all' in sys.argv:
        for f, t in legacy_bad:
            print('  legacy  %s  ->  %s' % (f, t))

    if active_bad:
        print('\n活跃层必须 0 断链：跨仓引用改绝对 URL'
              '（https://github.com/ruoxizhnya/<repo>/blob/main/<path>），'
              '仓内引用改相对路径。')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(check())
