#!/usr/bin/env python3
"""check_repo_docs.py 的夹具测试（stdlib unittest，无依赖）。

跑法：
    python tools/test_check_repo_docs.py        # 或 python -m unittest discover -s tools -p 'test_*.py'

为什么要有夹具：这个检查器的价值全在「缺件会不会红」与「豁免会不会误红」两条腿上。
真实 12 仓今天恰好是齐的 —— 只跑真仓，删掉任何一个判据都照样绿（假护栏）。
"""
import contextlib
import io
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_repo_docs as subject  # noqa: E402


def write(path, text='x'):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


def make_normal_repo(workspace, name, *, odr_home='docs/odr'):
    """一个齐套的业务仓：AGENTS + TASKS + 三件套 + adr(含 0001) + odr。"""
    root = os.path.join(workspace, name)
    write(os.path.join(root, 'AGENTS.md'))
    write(os.path.join(root, 'docs', 'TASKS.md'))
    for rel in subject.SPEC_FILES:
        write(os.path.join(root, rel))
    write(os.path.join(root, 'docs', 'adr', 'README.md'))
    write(os.path.join(root, 'docs', 'adr', '0001-first-decision.md'))
    os.makedirs(os.path.join(root, odr_home), exist_ok=True)
    write(os.path.join(root, odr_home, 'README.md'))
    return root


def make_core_like(workspace, name):
    """core：只有 AGENTS + TASKS；三件套 / adr / odr 都按豁免不要求。"""
    root = os.path.join(workspace, name)
    write(os.path.join(root, 'AGENTS.md'))
    write(os.path.join(root, 'docs', 'TASKS.md'))
    return root


def make_docs_like(workspace, name):
    """本仓：有 docs/adr（跨仓 ADR，无 0001-*），ODR 在 docs/archive/odr。"""
    root = os.path.join(workspace, name)
    write(os.path.join(root, 'AGENTS.md'))
    write(os.path.join(root, 'docs', 'TASKS.md'))
    write(os.path.join(root, 'docs', 'adr', 'adr-001-cross-repo.md'))
    os.makedirs(os.path.join(root, 'docs', 'archive', 'odr'), exist_ok=True)
    write(os.path.join(root, 'docs', 'archive', 'odr', 'odr-001-x.md'))
    return root


def make_workspace(tmp, *, skip=()):
    for name in subject.REPOS:
        if name in skip:
            continue
        if name == 'tellurion':
            make_core_like(tmp, name)
        elif name == 'tellurion-docs':
            make_docs_like(tmp, name)
        else:
            make_normal_repo(tmp, name)
    return tmp


def run_cli(argv):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = subject.main(argv)
    return code, buf.getvalue()


class CheckRepoDocsTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.ws = self._tmp.name
        make_workspace(self.ws)

    def tearDown(self):
        self._tmp.cleanup()

    def missing_of(self, name):
        missing, exempted, _ = subject.check_repo(self.ws, name)
        return missing, exempted

    # --- 绿色基线 ---------------------------------------------------------

    def test_full_workspace_is_green(self):
        for name in subject.REPOS:
            missing, _ = self.missing_of(name)
            self.assertEqual(missing, [], '%s 不该缺件' % name)

    def test_cli_exit_code_is_zero_on_complete_workspace(self):
        code, out = run_cli(['--workspace', self.ws])
        self.assertEqual(code, 0, out)
        self.assertIn('缺件 0', out)

    # --- 缺件必须红（每条判据各一条，不参数化打天下） ----------------------

    def test_missing_agents_is_red(self):
        os.remove(os.path.join(self.ws, 'tellurion-kit', 'AGENTS.md'))
        missing, _ = self.missing_of('tellurion-kit')
        self.assertEqual(missing, ['AGENTS.md'])

    def test_missing_tasks_is_red(self):
        os.remove(os.path.join(self.ws, 'tellurion-agent', 'docs', 'TASKS.md'))
        missing, _ = self.missing_of('tellurion-agent')
        self.assertEqual(missing, ['docs/TASKS.md'])

    def test_missing_spec_is_red(self):
        os.remove(os.path.join(self.ws, 'tellurion-risk', 'docs', 'api-schema.md'))
        missing, _ = self.missing_of('tellurion-risk')
        self.assertEqual(missing, ['docs/api-schema.md'])

    def test_missing_adr_dir_is_red(self):
        import shutil
        shutil.rmtree(os.path.join(self.ws, 'tellurion-broker', 'docs', 'adr'))
        missing, _ = self.missing_of('tellurion-broker')
        self.assertIn('docs/adr/（至少 1 个 .md）', missing)

    def test_missing_adr_0001_is_red(self):
        os.remove(os.path.join(self.ws, 'tellurion-data', 'docs', 'adr', '0001-first-decision.md'))
        missing, _ = self.missing_of('tellurion-data')
        self.assertEqual(missing, ['docs/adr/0001-*.md'])

    def test_missing_odr_home_is_red(self):
        import shutil
        shutil.rmtree(os.path.join(self.ws, 'tellurion-strategy', 'docs', 'odr'))
        missing, _ = self.missing_of('tellurion-strategy')
        self.assertEqual(missing, [subject.CHECK_LABELS['odr']])

    def test_odr_under_archive_is_accepted(self):
        import shutil
        root = os.path.join(self.ws, 'tellurion-analytics')
        shutil.rmtree(os.path.join(root, 'docs', 'odr'))
        os.makedirs(os.path.join(root, 'docs', 'archive', 'odr'))
        write(os.path.join(root, 'docs', 'archive', 'odr', 'odr-001-x.md'))
        missing, _ = self.missing_of('tellurion-analytics')
        self.assertEqual(missing, [])

    def test_missing_repo_directory_is_red(self):
        import shutil
        shutil.rmtree(os.path.join(self.ws, 'tellurion-orchestration'))
        missing, _ = self.missing_of('tellurion-orchestration')
        self.assertEqual(len(missing), 1)
        self.assertIn('仓目录不存在', missing[0])
        code, out = run_cli(['--workspace', self.ws])
        self.assertEqual(code, 1, out)

    # --- 豁免分支（不得对两仓报缺件） -------------------------------------

    def test_core_exemptions_do_not_report_missing(self):
        missing, exempted = self.missing_of('tellurion')
        self.assertEqual(missing, [])
        keys = [k for k, _ in exempted]
        self.assertEqual(keys, ['specs', 'adr_dir', 'adr_0001', 'odr'])

    def test_docs_repo_exemptions_do_not_report_missing(self):
        missing, exempted = self.missing_of('tellurion-docs')
        self.assertEqual(missing, [])
        keys = [k for k, _ in exempted]
        self.assertEqual(keys, ['specs', 'adr_0001'])

    def test_exemption_reasons_are_not_empty(self):
        for name, rules in subject.EXEMPT.items():
            for key, reason in rules.items():
                self.assertGreater(len(reason), 10, '%s 的 %s 豁免理由没写清楚' % (name, key))

    def test_explain_prints_reasons(self):
        code, out = run_cli(['--workspace', self.ws, '--explain'])
        self.assertEqual(code, 0, out)
        self.assertIn('core 的 ADR 已随文档拆分', out)

    # --- 抽查范围与参数校验 -----------------------------------------------

    def test_repos_subset_only_checks_listed(self):
        import shutil
        shutil.rmtree(os.path.join(self.ws, 'tellurion-ui'))  # 不在抽查范围内
        code, out = run_cli(['--workspace', self.ws, '--repos', 'tellurion-kit,tellurion-broker'])
        self.assertEqual(code, 0, out)
        self.assertIn('2 仓全查', out)
        self.assertNotIn('tellurion-ui', out)

    def test_unknown_repo_name_is_red(self):
        code, out = run_cli(['--workspace', self.ws, '--repos', 'tellurion-typo'])
        self.assertEqual(code, 1, out)
        self.assertIn('未登记的仓名', out)

    # --- 破坏验证：完整夹具 → 删件红 → 还原绿 ------------------------------

    def test_destruction_and_restore(self):
        code, out = run_cli(['--workspace', self.ws])
        self.assertEqual(code, 0, out)

        victim = os.path.join(self.ws, 'tellurion-ui', 'docs', 'dataflow.md')
        with open(victim, 'rb') as f:
            saved = f.read()
        os.remove(victim)

        code, out = run_cli(['--workspace', self.ws])
        self.assertEqual(code, 1, out)
        self.assertIn('tellurion-ui', out)
        self.assertIn('docs/dataflow.md', out)

        with open(victim, 'wb') as f:
            f.write(saved)
        code, out = run_cli(['--workspace', self.ws])
        self.assertEqual(code, 0, out)


if __name__ == '__main__':
    unittest.main(verbosity=2)
