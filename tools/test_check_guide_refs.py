#!/usr/bin/env python3
"""check_guide_refs.py 的夹具测试（stdlib unittest，无依赖）。

跑法：
    python tools/test_check_guide_refs.py
    python -m unittest discover -s tools -p 'test_*.py'

为什么要有夹具：这个检查器的价值全在两条腿上 ——「路径不存在会不会红」与
「历史说明会不会误红」。真仓今天恰好全绿，只跑真仓的话，把路径存在性判据
整段删掉也照样绿（假护栏）。
"""
import contextlib
import io
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_guide_refs as subject  # noqa: E402


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


def make_workspace(tmp):
    """最小 workspace：每个登记仓一个目录 + 一条真实存在的文件。"""
    for name in subject.REPOS:
        write(os.path.join(tmp, name, 'docs', 'TASKS.md'), '# tasks\n')
    return tmp


def make_guides(tmp, body):
    d = os.path.join(tmp, 'guides')
    write(os.path.join(d, 'local-dev.md'), body)
    return d


def run(guides_dir, workspace=None):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        argv = ['--dir', guides_dir]
        if workspace is not None:
            argv += ['--workspace', workspace]
        code = subject.main(argv)
    return code, buf.getvalue()


class GuideRefsTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.ws = self._tmp.name
        make_workspace(self.ws)

    def tearDown(self):
        self._tmp.cleanup()

    # --- 绿色基线 ---------------------------------------------------------

    def test_valid_ref_is_green_with_workspace(self):
        d = make_guides(self.ws, '看 `tellurion:docs/TASKS.md` 的台账。\n')
        code, out = run(d, self.ws)
        self.assertEqual(code, 0, out)
        self.assertIn('跨仓引用全部有效', out)

    def test_all_twelve_repos_are_recognised(self):
        """仓清单是 import 来的（不是复制），这条同时钉住它的内容与条数。

        「12 仓」这个数字写在十几份文档里；清单被误删或误加一条时要当场红，
        而不是让所有引用悄悄变成「未登记的仓」。
        """
        self.assertEqual(len(subject.REPOS), 12, subject.REPOS)
        self.assertIn('tellurion-docs', subject.REPOS)
        body = ''.join('`%s:docs/TASKS.md`\n' % r for r in subject.REPOS)
        d = make_guides(self.ws, body)
        code, out = run(d, self.ws)
        self.assertEqual(code, 0, out)

    # --- 仓名腿 -----------------------------------------------------------

    def test_unknown_repo_name_is_red(self):
        d = make_guides(self.ws, '看 `telliurion:docs/TASKS.md`。\n')
        code, out = run(d, self.ws)
        self.assertEqual(code, 1, out)
        self.assertIn('未登记的仓', out)
        self.assertIn('telliurion', out)

    def test_unknown_repo_name_is_red_even_without_workspace(self):
        """仓名腿不需要 workspace —— 这一条是它能进 CI 的依据。"""
        d = make_guides(self.ws, '看 `tellurion-typo:docs/x.md`。\n')
        code, out = run(d)
        self.assertEqual(code, 1, out)
        self.assertIn('未登记的仓', out)

    # --- 路径腿 -----------------------------------------------------------

    def test_missing_path_is_red_with_workspace(self):
        d = make_guides(self.ws, '见 `tellurion-agent:pkg/ai/pipeline`。\n')
        code, out = run(d, self.ws)
        self.assertEqual(code, 1, out)
        self.assertIn('pkg/ai/pipeline', out)
        self.assertIn('不存在', out)

    def test_missing_path_is_green_without_workspace(self):
        """两层判据必须真的分层：不给 workspace 就查不到磁盘。"""
        d = make_guides(self.ws, '见 `tellurion-agent:pkg/ai/pipeline`。\n')
        code, out = run(d)
        self.assertEqual(code, 0, out)
        self.assertIn('只查仓名', out)

    def test_missing_repo_directory_is_red(self):
        import shutil
        shutil.rmtree(os.path.join(self.ws, 'tellurion-risk'))
        d = make_guides(self.ws, '见 `tellurion-risk:docs/TASKS.md`。\n')
        code, out = run(d, self.ws)
        self.assertEqual(code, 1, out)
        self.assertIn('没有该仓目录', out)

    # --- 否定词豁免（不得误红历史说明） -----------------------------------

    def test_negation_on_same_line_is_exempt(self):
        d = make_guides(self.ws, '`tellurion:cmd/strategy` 已于 REV-16 删除。\n')
        code, out = run(d, self.ws)
        self.assertEqual(code, 0, out)
        self.assertIn('否定词', out)

    def test_negation_on_previous_line_is_exempt(self):
        # 散文会换行：否定词常常落在被引用路径的上一行。
        d = make_guides(self.ws, '下面这条路径已经不存在了：\n'
                                 '`tellurion:cmd/risk`。\n')
        code, out = run(d, self.ws)
        self.assertEqual(code, 0, out)

    def test_negation_exemption_is_line_scoped_not_global(self):
        """上一行的否定词不能豁免下一行的**另一条**引用 —— 否则一处
        「已删除」就能把整篇的坏引用洗绿。"""
        d = make_guides(self.ws, '这一段讲的是别的：旧路径不存在。\n'
                                 '\n'
                                 '`tellurion-agent:cmd/gone`\n')
        code, out = run(d, self.ws)
        self.assertEqual(code, 1, out)
        self.assertIn('cmd/gone', out)

    # --- 非路径的冒号写法不算引用 -----------------------------------------

    def test_non_path_colon_writes_are_ignored(self):
        body = ('请求 `kernel:"nautilus"` 时返回 `status:failed`；\n'
                '模板里写 `{a}:{b}`，比例是 `1:2`。\n')
        d = make_guides(self.ws, body)
        code, out = run(d, self.ws)
        self.assertEqual(code, 0, out)

    def test_url_is_not_treated_as_ref(self):
        d = make_guides(
            self.ws,
            '见 [台账](https://github.com/ruoxizhnya/tellurion/blob/main/docs/TASKS.md)。\n')
        code, out = run(d, self.ws)
        self.assertEqual(code, 0, out)

    def test_trailing_punctuation_is_stripped(self):
        d = make_guides(self.ws, '看 `tellurion:docs/TASKS.md`，再看 `tellurion-kit:docs/TASKS.md`。\n')
        code, out = run(d, self.ws)
        self.assertEqual(code, 0, out)

    # --- 两条实测踩到的截断 bug（回归腿） ---------------------------------

    def test_ellipsis_placeholder_is_not_a_path_claim(self):
        """`cmd/...` 是省略号，不是可核对的路径 —— 不得报缺失。

        真仓实测：本文原写「不要提前按目标态写 `tellurion-data:cmd/...`」，
        第一版检查器把它当成缺失路径报了红。
        """
        d = make_guides(self.ws, '别提前写 `tellurion-data:cmd/...`。\n')
        code, out = run(d, self.ws)
        self.assertEqual(code, 0, out)

    def test_chinese_filename_is_matched_whole(self):
        """中文文件名必须整条匹配，不能截成 `docs/adr/0001-` 而误报缺失。

        真仓实测：两个库仓与六个服务仓的 ADR 文件名是中文。
        """
        rel = 'docs/adr/0001-统一协议与-visible-at-第二道防线.md'
        write(os.path.join(self.ws, 'tellurion-data', *rel.split('/')), '# adr\n')
        d = make_guides(self.ws, '见 `tellurion-data:%s`。\n' % rel)
        code, out = run(d, self.ws)
        self.assertEqual(code, 0, out)

    def test_chinese_filename_missing_is_still_red(self):
        """整条匹配不能变成「中文就放过」—— 真缺失仍须红。"""
        d = make_guides(self.ws, '见 `tellurion-data:docs/adr/0001-缺失的裁决.md`。\n')
        code, out = run(d, self.ws)
        self.assertEqual(code, 1, out)
        self.assertIn('0001-缺失的裁决.md', out)

    # --- 参数校验 ---------------------------------------------------------

    def test_missing_directory_is_red(self):
        code, out = run(os.path.join(self.ws, 'nope'))
        self.assertEqual(code, 1, out)
        self.assertIn('扫描目录不存在', out)

    def test_empty_directory_is_red(self):
        d = os.path.join(self.ws, 'empty-guides')
        os.makedirs(d, exist_ok=True)
        code, out = run(d)
        self.assertEqual(code, 1, out)
        self.assertIn('没有 .md 文件', out)

    # --- 破坏验证：完整夹具 → 删件红 → 还原绿 ------------------------------

    def test_destruction_and_restore(self):
        d = make_guides(self.ws, '见 `tellurion:docs/ARCHITECTURE.md`。\n')
        victim = os.path.join(self.ws, 'tellurion', 'docs', 'ARCHITECTURE.md')
        write(victim, '# arch\n')

        code, out = run(d, self.ws)
        self.assertEqual(code, 0, out)

        os.remove(victim)
        code, out = run(d, self.ws)
        self.assertEqual(code, 1, out)
        self.assertIn('docs/ARCHITECTURE.md', out)

        write(victim, '# arch\n')
        code, out = run(d, self.ws)
        self.assertEqual(code, 0, out)


class RealGuidesTest(unittest.TestCase):
    """真仓自检：本仓 docs/guides 的引用必须有效。

    这两条不是「再跑一遍上面」——它们钉的是**本仓真实内容**：
    没有它们，夹具全绿而真 guide 里写着 `tellurion:pkg/ai/pipeline` 也不会红。
    """

    def test_real_guides_repo_names_are_valid(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = subject.main([])
        self.assertEqual(code, 0, buf.getvalue())

    def test_real_guides_paths_exist_on_this_workspace(self):
        workspace = os.path.dirname(subject.REPO_ROOT)
        if not os.path.isdir(os.path.join(workspace, 'tellurion')):
            self.skipTest('兄弟仓不在同级目录，跳过路径腿（CI 即此形态）')
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = subject.main(['--workspace', workspace])
        self.assertEqual(code, 0, buf.getvalue())


if __name__ == '__main__':
    unittest.main(verbosity=2)