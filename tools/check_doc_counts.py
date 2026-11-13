#!/usr/bin/env python3
"""入口页关键计数校验（DOC-18 · R5 机械门）。

为什么需要它：`docs/README.md` 是唯一入口，手写的「ADR 41 条 / 至 ADR-041、
ODR 001–073、12 仓服务卡已落地」一改台账就会腐烂（2026-11-13 五角审查 H1
实测过一次：页面同时写着 31 条 / 001–064 / 12 仓未落地）。这个脚本把入口页
的计数从「人肉同步」变成「改错即红」。

判据（全部 fail-closed，任一条不符退出码 1）：

  1. `docs/ADR.md` 索引表行数 == `docs/adr/adr-*.md` + `docs/archive/superseded-adr/adr-*.md`；
  2. 索引最大编号 == README 写的「至 ADR-NNN」；
  3. `docs/archive/odr/odr-*.md` 的编号区间 == README 写的「ODR NNN–NNN」；
  4. README 的「NNN 条」「已归档」清单与实测一致（清单 = superseded-adr/ 文件名编号）；
  5. README 的「N 仓已全部落地」== `check_repo_docs.REPOS` 长度（12）；给了
     `--workspace` 时再逐仓断言 `SERVICE.md` 真的存在。

CI 边界与 `check_guide_refs.py` 同款：CI 只 checkout 本仓，所以第 5 条的磁盘腿
只在 `--workspace` 下执行；仓数腿（12）始终执行 —— 把「12」改成别的数字仍会红。

用法：
    python tools/check_doc_counts.py                       # CI 同款
    python tools/check_doc_counts.py --workspace DIR       # 连 SERVICE.md 存在性一起查
退出码：0 = 一致；1 = 有计数漂移。
"""
import argparse
import glob
import os
import re
import sys

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(TOOLS_DIR)

if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)

from check_repo_docs import REPOS  # noqa: E402

DOCS = os.path.join(REPO_ROOT, 'docs')
ADR_MD = os.path.join(DOCS, 'ADR.md')
README_MD = os.path.join(DOCS, 'README.md')
ADR_DIR = os.path.join(DOCS, 'adr')
SUPERSEDED_DIR = os.path.join(DOCS, 'archive', 'superseded-adr')
ODR_DIR = os.path.join(DOCS, 'archive', 'odr')

# `| [ADR-001](adr/adr-001-plugin-loading.md) | ...`
ADR_ROW = re.compile(r'^\|\s*\[ADR-(\d{3})\]\(([^)]+)\)', re.M)
# `现行（41 条；编号至 ADR-041，009/010/012/021/022 已归档）`
README_ADR = re.compile(r'(\d+) 条；编号至 ADR-(\d{3})，([0-9/]+) 已归档')
# `ODR 001–073`
README_ODR = re.compile(r'ODR (\d{3})[–-](\d{3})')
# `12 仓已全部落地`
README_SERVICE = re.compile(r'(\d+) 仓已全部落地')

FILE_NO = re.compile(r'^adr-(\d{3})-')
ODR_NO = re.compile(r'^odr-(\d{3})-', re.I)


def ids_of(pattern, directory):
    ids = []
    for path in glob.glob(os.path.join(directory, '*.md')):
        m = pattern.match(os.path.basename(path))
        if m:
            ids.append(m.group(1))
    return sorted(ids)


def read_text(path):
    with open(path, encoding='utf-8', errors='replace') as f:
        return f.read()


def check(workspace):
    errors, notes = [], []

    adr_text = read_text(ADR_MD)
    rows = [(m.group(1), m.group(2)) for m in ADR_ROW.finditer(adr_text)]
    index_ids = [r[0] for r in rows]
    live_ids = ids_of(FILE_NO, ADR_DIR)
    superseded_ids = ids_of(FILE_NO, SUPERSEDED_DIR)

    if not rows:
        errors.append('docs/ADR.md 索引表未解析到任何 `| [ADR-NNN](...)` 行')
    if len(index_ids) != len(live_ids) + len(superseded_ids):
        errors.append(
            'ADR 计数漂移：索引 %d 条 ≠ adr/ %d 份 + superseded-adr/ %d 份 = %d'
            % (len(index_ids), len(live_ids), len(superseded_ids),
               len(live_ids) + len(superseded_ids)))
    if sorted(index_ids) != sorted(live_ids + superseded_ids):
        missing_files = sorted(set(index_ids) - set(live_ids + superseded_ids))
        missing_rows = sorted(set(live_ids + superseded_ids) - set(index_ids))
        errors.append(
            'ADR 编号不对齐：索引有而文件无 %s；文件有而索引无 %s'
            % (missing_files or '无', missing_rows or '无'))

    odr_ids = ids_of(ODR_NO, ODR_DIR)
    if not odr_ids:
        errors.append('docs/archive/odr/ 未找到 odr-NNN-*.md')

    readme = read_text(README_MD)

    m = README_ADR.search(readme)
    if not m:
        errors.append('docs/README.md 未匹配到「N 条；编号至 ADR-NNN，… 已归档」')
    else:
        declared_count, declared_max, declared_archived = (
            int(m.group(1)), m.group(2), sorted(m.group(3).split('/')))
        if declared_count != len(index_ids):
            errors.append('README 写 %d 条，ADR.md 索引实测 %d 条'
                          % (declared_count, len(index_ids)))
        if index_ids and declared_max != max(index_ids):
            errors.append('README 写至 ADR-%s，ADR.md 索引实测至 ADR-%s'
                          % (declared_max, max(index_ids)))
        if declared_archived != superseded_ids:
            errors.append('README 已归档清单 %s ≠ superseded-adr/ 实测 %s'
                          % ('/'.join(declared_archived), '/'.join(superseded_ids)))

    m = README_ODR.search(readme)
    if not m:
        errors.append('docs/README.md 未匹配到「ODR NNN–NNN」')
    elif odr_ids and (m.group(1), m.group(2)) != (odr_ids[0], odr_ids[-1]):
        errors.append('README 写 ODR %s–%s，archive/odr/ 实测 %s–%s'
                      % (m.group(1), m.group(2), odr_ids[0], odr_ids[-1]))

    m = README_SERVICE.search(readme)
    if not m:
        errors.append('docs/README.md 未匹配到「N 仓已全部落地」')
    elif int(m.group(1)) != len(REPOS):
        errors.append('README 写 %s 仓，仓清单实测 %d 仓'
                      % (m.group(1), len(REPOS)))

    if workspace is None:
        notes.append('未给 --workspace：跳过 12 份 SERVICE.md 存在性（CI 只 checkout 本仓）')
    else:
        for repo in REPOS:
            path = os.path.join(workspace, repo, 'SERVICE.md')
            if not os.path.isfile(path):
                errors.append('缺服务卡：%s' % path)
        notes.append('12 仓 SERVICE.md 存在性已核对：%s' % workspace)

    return errors, notes


def main(argv=None):
    parser = argparse.ArgumentParser(
        description='docs/README.md 关键计数与 ADR/ODR 台账对齐校验')
    parser.add_argument('--workspace', default=None,
                        help='12 仓所在目录；给了才校验每仓 SERVICE.md 存在性')
    args = parser.parse_args(argv)

    workspace = os.path.abspath(args.workspace) if args.workspace else None
    errors, notes = check(workspace)

    print('入口页计数校验：ADR 索引 / ADR 文件 / ODR 范围 / 12 仓服务卡')
    for n in notes:
        print('  · %s' % n)
    if errors:
        print('✗ %d 处计数漂移：' % len(errors))
        for e in errors:
            print('  - %s' % e)
        return 1
    print('✓ 入口页计数与台账一致')
    return 0


if __name__ == '__main__':
    sys.exit(main())
