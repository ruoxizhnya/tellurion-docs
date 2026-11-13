#!/usr/bin/env python3
"""归档层可信索引校验（DOC-22 / R2）。

`docs/archive/README.md` 的「归档清单」是归档层唯一的可信索引。这个脚本保证
它不会烂成一张只列了三五个文件的旧目录树：

  1. **覆盖**：`docs/archive/` 下每个文件（README.md 自身除外）都必须被清单
     某一行的条目命中；
  2. **反向**：清单每一行必须至少命中一个真实文件（防止条目指向已删除的东西）；
  3. **status 语义**：归档层 .md 的 frontmatter `status:` 只允许 `archived`；
     全仓不得出现未定义的 `status: historical`。

条目写法：表格第一列里的反引号路径，相对 `docs/archive/`。
  - 文件：`IMPLEMENTATION_PLAN.md`（精确匹配）；
  - 目录：`odr/`（前缀匹配，覆盖其下全部文件）。

用法：python tools/check_archive_index.py
退出码：0 = 一致；1 = 有未覆盖 / 空条目 / status 违规。
"""
import fnmatch
import os
import re
import sys

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(TOOLS_DIR)
DOCS = os.path.join(REPO_ROOT, 'docs')
ARCHIVE = os.path.join(DOCS, 'archive')
INDEX = os.path.join(ARCHIVE, 'README.md')

BLOCK = re.compile(r'<!-- archive:begin -->\s*(.*?)\s*<!-- archive:end -->', re.S)
BACKTICK = re.compile(r'`([^`]+)`')
FRONTMATTER = re.compile(r'\A---\s*\n(.*?)\n---\s*\n', re.S)
STATUS = re.compile(r'^status:\s*(\S+)\s*$', re.M)


def rel_files():
    out = []
    for base, _, files in os.walk(ARCHIVE):
        for name in files:
            path = os.path.join(base, name)
            rel = os.path.relpath(path, ARCHIVE).replace(os.sep, '/')
            if rel != 'README.md':
                out.append(rel)
    return sorted(out)


def patterns_from_index(text):
    block = BLOCK.search(text)
    if not block:
        return None
    pats = []
    for line in block.group(1).splitlines():
        line = line.strip()
        if not line.startswith('|'):
            continue
        first_cell = line.strip('|').split('|')[0]
        for token in BACKTICK.findall(first_cell):
            token = token.strip()
            if token and token not in pats:
                pats.append(token)
    return pats


def matches(pattern, rel):
    if pattern.endswith('/'):
        return rel.startswith(pattern)
    return fnmatch.fnmatchcase(rel, pattern)


def check_status(errors):
    for rel in rel_files():
        if not rel.endswith('.md'):
            continue
        path = os.path.join(ARCHIVE, rel)
        with open(path, encoding='utf-8', errors='replace') as f:
            text = f.read()
        m = FRONTMATTER.match(text)
        if not m:
            continue
        s = STATUS.search(m.group(1))
        if s and s.group(1) != 'archived':
            errors.append('%s 的 frontmatter status=%s（归档层只允许 archived）'
                          % (rel, s.group(1)))
    for base, _, files in os.walk(DOCS):
        if os.sep + 'archive' in base:
            continue
        for name in files:
            if not name.endswith('.md'):
                continue
            path = os.path.join(base, name)
            with open(path, encoding='utf-8', errors='replace') as f:
                if re.search(r'^status:\s*historical\s*$', f.read(), re.M):
                    errors.append('%s 使用了未定义的 status: historical'
                                  % os.path.relpath(path, REPO_ROOT))


def main():
    files = rel_files()
    if not os.path.isfile(INDEX):
        print('✗ 缺 docs/archive/README.md')
        return 1
    with open(INDEX, encoding='utf-8') as f:
        text = f.read()
    pats = patterns_from_index(text)
    if pats is None:
        print('✗ docs/archive/README.md 缺 <!-- archive:begin --> … <!-- archive:end --> 清单块')
        return 1
    if not pats:
        print('✗ 归档清单未解析到任何反引号条目')
        return 1

    errors = []
    uncovered = [rel for rel in files if not any(matches(p, rel) for p in pats)]
    for rel in uncovered:
        errors.append('未覆盖：%s' % rel)
    for p in pats:
        if not any(matches(p, rel) for rel in files):
            errors.append('空条目：`%s` 没有命中任何文件' % p)

    check_status(errors)

    print('归档索引校验：%d 个文件 / %d 条条目' % (len(files), len(pats)))
    if errors:
        print('✗ %d 处问题：' % len(errors))
        for e in errors:
            print('  - %s' % e)
        return 1
    print('✓ 归档清单覆盖完整，status 语义正确')
    return 0


if __name__ == '__main__':
    sys.exit(main())
