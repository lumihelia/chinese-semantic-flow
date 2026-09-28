"""Adversarial mechanics tests; fixture judgments are not model evaluation.

Each test creates an isolated git source snapshot. No test calls a provider or
writes purported quality findings into repository evidence.
"""

from copy import deepcopy
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

from evaluation import harness as h


class HarnessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.snapshot = tempfile.TemporaryDirectory(prefix="csf-source-fixture-")
        cls.snapshot_root = Path(cls.snapshot.name)
        cls.git("init", "-q")
        (cls.snapshot_root / "constraint.md").write_text("# 测试来源\n不补充未提供的原因。\n保持原句的确定程度。\n", encoding="utf-8")
        cls.git("add", "constraint.md")
        cls.git("-c", "user.name=Diagnostic Fixture", "-c", "user.email=fixture@example.invalid",
                "-c", "commit.gpgsign=false", "commit", "-qm", "Local test source fixture")
        cls.commit = cls.git("rev-parse", "HEAD").strip()

    @classmethod
    def tearDownClass(cls):
        cls.snapshot.cleanup()

    @classmethod
    def git(cls, *args):
        result = subprocess.run(["git", "-C", str(cls.snapshot_root), *args],
                                capture_output=True, text=True, check=True)
        return result.stdout

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="csf-harness-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        # The fixture shares read-only git objects, not the tested repository.
        (self.root / ".git").write_text(f"gitdir: {self.snapshot_root / '.git'}\n", encoding="utf-8")
        (self.root / "benchmarks/data").mkdir(parents=True)
        (self.root / "evaluation").mkdir()
        self.sources = {"schema_version": 1, "baseline_commit": self.commit, "sources": [{
            "id": "fixture-private-source", "path": "constraint.md", "start_line": 2, "end_line": 2,
            "quote": "不补充未提供的原因。", "sha256": h.digest("不补充未提供的原因。".encode("utf-8"))}]}
        self.cases = [self.case("one", "contract", "b", "core", "family-alpha"),
                      self.case("two", "contract", "tie", "house-language", "family-alpha"),
                      self.case("three", "hypothesis", "a", "house-writing", "family-beta"),
                      self.case("four", "unresolved", "abstain", "persona-dialogue", "family-gamma")]
        self.write_inputs()
        self.rubric_path.write_text("比较给定语境中的两个候选。引用可见证据；证据不足时弃答。\n", encoding="utf-8")
        self.run = self.root / "run"
        self.judgments_path = self.root / "judgments.jsonl"

    @staticmethod
    def case(name, status, verdict, profile, family):
        return {"id": f"private-case-{name}", "family": family, "kind": "minimal_pair",
                "mode": "rewrite", "profile": profile, "context": "只提供这一句，不补充事实。",
                "prompt": f"改写第{name}句，使意思保持清楚。", "candidates": {"a": "他可能会来。", "b": "他一定会来。"},
                "criteria": ["grounding", "stance"], "failure_tags": ["stance_drift"],
                "expected": {"status": status, "verdict": verdict, "reason": "PRIVATE-KEY-REASON"},
                "provenance": {"origin": "synthetic", "source_refs": ["fixture-private-source"],
                               "hypothesis": "PRIVATE-HYPOTHESIS", "changes": "PRIVATE-CONSTRUCTION"}}

    @property
    def sources_path(self):
        return self.root / "benchmarks/data/sources.json"

    @property
    def cases_path(self):
        return self.root / "benchmarks/data/cases.jsonl"

    @property
    def rubric_path(self):
        return self.root / "evaluation/RUBRIC.md"

    def write_inputs(self):
        self.sources_path.write_bytes(h.encoded(self.sources))
        self.write_jsonl(self.cases_path, self.cases)

    @staticmethod
    def write_jsonl(path, rows):
        path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")

    def packet(self, seed=17):
        self.public, self.private = h.create_packet(self.root, seed, self.run)
        return self.public, self.private

    def judgments(self, outcomes=None, label=None):
        """Fabricated mechanical fixtures, never a real evaluator's judgments."""
        outcomes = outcomes or {case["id"]: case["expected"]["verdict"] for case in self.cases}
        mapping = {trial["trial_id"]: trial for trial in self.private["trials"]}
        rows = []
        for trial in self.public["trials"]:
            stable = outcomes[mapping[trial["trial_id"]]["case_id"]]
            verdict = label or next((key for key, value in mapping[trial["trial_id"]]["mapping"].items()
                                    if value == stable), stable)
            rows.append({"trial_id": trial["trial_id"], "verdict": verdict,
                         "evidence": [] if verdict == "abstain" else [
                             {"candidate": candidate, "quote": trial["candidates"][candidate], "criterion": "stance"}
                             for candidate in ("A", "B")],
                         "reason": "MECHANICS FIXTURE: 测试映射与引用验证；此处没有模型判断。"})
        self.write_jsonl(self.judgments_path, rows)
        return rows

    def report(self):
        return h.make_report(self.root, self.run, self.judgments_path)

    def test_valid_source_snapshot_and_changed_worktree_are_independent(self):
        inputs = h.load_inputs(self.root)
        self.assertEqual(len(inputs.cases), 4)
        (self.root / "constraint.md").write_text("当前工作区已改写，不应替换历史证据。", encoding="utf-8")
        self.assertEqual(h.load_inputs(self.root).sources, inputs.sources)

    def test_source_quote_digest_does_not_prove_quote_is_authentic(self):
        self.sources["sources"][0]["quote"] = "编造的来源。"
        self.sources["sources"][0]["sha256"] = h.digest("编造的来源。".encode("utf-8"))
        self.write_inputs()
        with self.assertRaisesRegex(h.DiagnosticError, "pinned source snapshot"):
            h.load_inputs(self.root)

    def test_source_ranges_paths_and_commit_types_fail_closed(self):
        baseline = deepcopy(self.sources)
        mutations = [lambda s: s.update(baseline_commit="0" * 40),
                     lambda s: s.update(baseline_commit=True),
                     lambda s: s["sources"][0].update(start_line=True),
                     lambda s: s["sources"][0].update(end_line=200),
                     lambda s: s["sources"][0].update(path="../constraint.md"),
                     lambda s: s["sources"][0].update(path="/constraint.md"),
                     lambda s: s["sources"][0].update(path="./constraint.md"),
                     lambda s: s["sources"][0].update(sha256="0" * 64),
                     lambda s: s["sources"].append(deepcopy(s["sources"][0])),
                     lambda s: s.update(schema_version=True)]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                self.sources = deepcopy(baseline)
                mutate(self.sources)
                self.write_inputs()
                with self.assertRaises(h.DiagnosticError):
                    h.load_inputs(self.root)

    def test_case_schema_provenance_and_labels_fail_closed(self):
        baseline = deepcopy(self.cases)
        mutations = [lambda c: c.update(extra="private key"),
                     lambda c: c.update(context="  "),
                     lambda c: c.update(profile="Secret Profile"),
                     lambda c: c.update(criteria=["stance", "stance"]),
                     lambda c: c.update(criteria=["pretty"]),
                     lambda c: c.update(failure_tags=[]),
                     lambda c: c.update(candidates={"a": "  ", "b": "你好。"}),
                     lambda c: c["candidates"].update(c="多余候选。"),
                     lambda c: c["expected"].update(status="gold"),
                     lambda c: c["expected"].update(status="unresolved", verdict="a"),
                     lambda c: c["provenance"].update(source_refs=["missing"]),
                     lambda c: c["provenance"].update(source_refs=["fixture-private-source"] * 2),
                     lambda c: c["provenance"].update(changes=""),
                     lambda c: c["provenance"].update(origin="real_user_data"),
                     lambda c: c.update(id=[])]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                self.cases = deepcopy(baseline)
                mutate(self.cases[0])
                self.write_inputs()
                with self.assertRaises(h.DiagnosticError):
                    h.load_inputs(self.root)

    def test_duplicate_cases_rejected(self):
        self.cases.append(deepcopy(self.cases[0]))
        self.write_inputs()
        with self.assertRaisesRegex(h.DiagnosticError, "duplicate case ID"):
            h.load_inputs(self.root)

    def test_punctuation_only_and_mixed_script_dialogue_candidates_are_valid(self):
        self.cases[0].update(mode="dialogue", profile="persona-dialogue",
                             candidates={"a": "？", "b": "TA？"})
        self.write_inputs()
        self.assertEqual(h.load_inputs(self.root).cases[0]["candidates"], {"a": "？", "b": "TA？"})
        self.packet()
        self.judgments()
        self.assertEqual(self.report()["summary"]["cases"], 4)

    def test_json_parser_rejects_duplicate_keys_and_nonstandard_values(self):
        for raw in (b'{"x": 1, "x": 2}', b'{"x": NaN}', b'{"x": Infinity}', b'{"x":', b'\xff'):
            with self.subTest(raw=raw), self.assertRaises(h.DiagnosticError):
                h.parse_json(raw, "fixture")
        with self.assertRaises(h.DiagnosticError):
            h.parse_jsonl(b'{}\n\n{}\n', "fixture")

    def test_packet_contains_only_blind_fields_and_both_orientations(self):
        packet, manifest = self.packet()
        self.assertEqual(len(packet["trials"]), 8)
        public_text = h.encoded(packet).decode("utf-8")
        for secret in ("private-case", "family-alpha", "stance_drift", "PRIVATE-KEY-REASON",
                       "fixture-private-source", "PRIVATE-HYPOTHESIS", "PRIVATE-CONSTRUCTION",
                       "source_refs", "expected", "mapping", "key_status"):
            self.assertNotIn(secret, public_text)
        by_id = {trial["trial_id"]: trial for trial in packet["trials"]}
        for trial in packet["trials"]:
            self.assertEqual(set(trial), h.TRIAL_FIELDS)
            self.assertEqual(set(trial["candidates"]), {"A", "B"})
        manifest_pairs = []
        for case in self.cases:
            trials = [trial for trial in manifest["trials"] if trial["case_id"] == case["id"]]
            self.assertEqual(len(trials), 2)
            self.assertEqual({trial["mapping"]["A"] for trial in trials}, {"a", "b"})
            for trial in trials:
                for label, stable in trial["mapping"].items():
                    self.assertEqual(by_id[trial["trial_id"]]["candidates"][label], case["candidates"][stable])
            manifest_pairs.extend(trial["trial_id"] for trial in trials)
        self.assertNotEqual([trial["trial_id"] for trial in manifest["trials"]], manifest_pairs)
        self.assertEqual(manifest["digests"]["packet"], h.digest((self.run / "packet.json").read_bytes()))

    def test_packet_is_reproducible_and_ids_change_with_inputs_or_seed(self):
        inputs = h.load_inputs(self.root)
        packet, manifest = h.build_packet(inputs, 17)
        self.assertEqual((packet, manifest), h.build_packet(inputs, 17))
        different_seed, _ = h.build_packet(inputs, 18)
        self.assertNotEqual(packet, different_seed)
        self.rubric_path.write_text("新评审说明。", encoding="utf-8")
        changed_packet, _ = h.build_packet(h.load_inputs(self.root), 17)
        self.assertNotEqual(packet["packet_id"], changed_packet["packet_id"])
        self.assertFalse({trial["trial_id"] for trial in packet["trials"]}
                         & {trial["trial_id"] for trial in changed_packet["trials"]})

    def test_swapped_visible_winners_map_to_same_stable_choice(self):
        self.packet()
        self.judgments()
        report = self.report()
        self.assertEqual([row["outcome"] for row in report["cases"]], ["b", "tie", "a", "abstain"])
        summary = report["summary"]
        self.assertEqual(summary["contract_key_agreement_all_cases"], h.ratio(2, 2))
        self.assertEqual(summary["contract_key_agreement_substantive_consistent"], h.ratio(2, 2))
        self.assertEqual(summary["unresolved_case_abstentions"], h.ratio(1, 1))
        self.assertEqual(summary["substantive_coverage"], h.ratio(3, 4))
        self.assertEqual(report["strata"]["family"]["family-alpha"]["cases"], 2)
        self.assertEqual(report["strata"]["key_status"]["hypothesis"]["contract_key_agreement_all_cases"], h.ratio(0, 0))

    def test_constant_position_choice_is_inconsistent_never_a_tie(self):
        self.packet()
        self.judgments(label="A")
        summary = self.report()["summary"]
        self.assertEqual(summary["inconsistent_cases"], 4)
        self.assertEqual(summary["tie_cases"], 0)
        self.assertEqual(summary["consistent_substantive_cases"], 0)
        self.assertEqual(summary["contract_key_agreement_all_cases"], h.ratio(0, 2))

    def test_any_unequal_mapped_verdicts_are_inconsistent(self):
        self.packet()
        rows = self.judgments(label="tie")
        rows[0]["verdict"] = "abstain"
        rows[0]["evidence"] = []
        self.write_jsonl(self.judgments_path, rows)
        summary = self.report()["summary"]
        self.assertEqual(summary["inconsistent_cases"], 1)
        self.assertEqual(summary["tie_cases"], 3)
        self.assertEqual(summary["consistent_abstention_cases"], 0)
        self.assertEqual(summary["abstention_trials"], 1)

    def test_all_abstain_has_zero_substantive_coverage_and_null_conditional_agreement(self):
        self.packet()
        self.judgments(label="abstain")
        summary = self.report()["summary"]
        self.assertEqual(summary["consistent_cases"], 4)
        self.assertEqual(summary["consistent_abstention_cases"], 4)
        self.assertEqual(summary["abstention_trials"], 8)
        self.assertEqual(summary["substantive_coverage"], h.ratio(0, 4))
        self.assertEqual(summary["contract_key_agreement_all_cases"], h.ratio(0, 2))
        self.assertEqual(summary["contract_key_agreement_substantive_consistent"], h.ratio(0, 0))
        self.assertEqual(summary["unresolved_case_abstentions"], h.ratio(1, 1))

    def test_contract_abstention_match_remains_separate_from_substantive_agreement(self):
        self.cases[0]["expected"]["verdict"] = "abstain"
        self.write_inputs()
        self.packet()
        self.judgments(label="abstain")
        summary = self.report()["summary"]
        self.assertEqual(summary["contract_key_abstention_matches"], 1)
        self.assertEqual(summary["contract_key_agreement_all_cases"], h.ratio(0, 2))

    def test_missing_duplicate_extra_and_empty_trials_fail_instead_of_scoring_subset(self):
        self.packet()
        rows = self.judgments()
        extra = deepcopy(rows[0])
        extra["trial_id"] = "unknown-trial"
        for invalid in (rows[:-1], rows + [rows[0]], rows + [extra], []):
            with self.subTest(count=len(invalid)):
                self.write_jsonl(self.judgments_path, invalid)
                with self.assertRaises(h.DiagnosticError):
                    self.report()

    def test_judgments_reject_invented_quotes_unknown_criteria_and_key_leakage(self):
        self.packet()
        baseline = self.judgments(label="A")
        mutations = [lambda row: row["evidence"][0].update(quote="文本中没有的细节。"),
                     lambda row: row["evidence"][0].update(criterion="relation"),
                     lambda row: row["evidence"][0].update(candidate="a"),
                     lambda row: row["evidence"][0].update(key="b"),
                     lambda row: row.update(evidence=[]),
                     lambda row: row.update(evidence=row["evidence"][:1]),
                     lambda row: row.update(verdict="a"),
                     lambda row: row.update(reason=" \n "),
                     lambda row: row.update(reason="\ud800"),
                     lambda row: row.update(expected="b"),
                     lambda row: row.update(evidence={}),
                     lambda row: row.update(trial_id=["wrong type"])]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                rows = deepcopy(baseline)
                mutate(rows[0])
                # ASCII escapes allow malformed Unicode to reach the validator.
                self.judgments_path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
                with self.assertRaises(h.DiagnosticError):
                    self.report()

    def test_evidence_is_checked_even_for_abstention(self):
        self.packet()
        rows = self.judgments(label="abstain")
        rows[0]["evidence"] = [{"candidate": "A", "quote": "编造", "criterion": "grounding"}]
        self.write_jsonl(self.judgments_path, rows)
        with self.assertRaisesRegex(h.DiagnosticError, "invented evidence"):
            self.report()

    def test_reordered_judgments_do_not_change_report_counts(self):
        self.packet()
        rows = self.judgments()
        original = self.report()
        self.write_jsonl(self.judgments_path, list(reversed(rows)))
        reordered = self.report()
        self.assertEqual(original["summary"], reordered["summary"])
        self.assertEqual(original["cases"], reordered["cases"])
        self.assertNotEqual(original["digests"]["judgments"], reordered["digests"]["judgments"])

    def test_modified_dataset_sources_or_rubric_invalidate_old_run(self):
        self.packet()
        self.judgments()
        for path in (self.cases_path, self.sources_path, self.rubric_path):
            with self.subTest(path=path.name):
                original = path.read_bytes()
                # Semantically harmless whitespace still changes the pinned bytes.
                path.write_bytes(b" " + original)
                with self.assertRaisesRegex(h.DiagnosticError, "digest mismatch"):
                    self.report()
                path.write_bytes(original)

    def test_changed_baseline_snapshot_cannot_be_hidden_by_manifest_digest_update(self):
        self.packet()
        self.judgments()
        self.sources["sources"][0].update(quote="伪造来源。", sha256=h.digest("伪造来源。".encode("utf-8")))
        self.sources_path.write_bytes(h.encoded(self.sources))
        self.private["digests"]["sources"] = h.digest(self.sources_path.read_bytes())
        (self.run / "manifest.json").write_bytes(h.encoded(self.private))
        with self.assertRaisesRegex(h.DiagnosticError, "source snapshot"):
            self.report()

    def test_changed_mapping_is_rejected_even_when_other_integrity_fields_are_valid(self):
        self.packet()
        self.judgments()
        self.private["trials"][0]["mapping"] = {"A": "b", "B": "a"} if self.private["trials"][0]["mapping"]["A"] == "a" else {"A": "a", "B": "b"}
        (self.run / "manifest.json").write_bytes(h.encoded(self.private))
        with self.assertRaisesRegex(h.DiagnosticError, "deterministic trial mappings"):
            self.report()

    def test_packet_tampering_cannot_be_hidden_by_recomputing_its_digest(self):
        self.packet()
        self.judgments()
        baseline = deepcopy(self.public)
        mutations = [lambda p: p["trials"][0].update(expected="b"),
                     lambda p: p["trials"][0]["candidates"].update(A="替换候选。"),
                     lambda p: p["trials"].pop(),
                     lambda p: p["trials"].append(deepcopy(p["trials"][0])),
                     lambda p: p.update(rubric="被替换的评审规则。"),
                     lambda p: p.update(schema_version=True)]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                packet = deepcopy(baseline)
                mutate(packet)
                raw = h.encoded(packet)
                (self.run / "packet.json").write_bytes(raw)
                self.private["digests"]["packet"] = h.digest(raw)
                (self.run / "manifest.json").write_bytes(h.encoded(self.private))
                with self.assertRaises(h.DiagnosticError):
                    self.report()

    def test_packet_raw_byte_change_fails_digest(self):
        self.packet()
        self.judgments()
        with (self.run / "packet.json").open("ab") as stream:
            stream.write(b" ")
        with self.assertRaisesRegex(h.DiagnosticError, "packet: digest mismatch"):
            self.report()

    def test_existing_runs_and_reports_are_not_overwritten(self):
        self.packet()
        original = (self.run / "packet.json").read_bytes()
        with self.assertRaisesRegex(h.DiagnosticError, "already exist"):
            h.create_packet(self.root, 18, self.run)
        self.assertEqual((self.run / "packet.json").read_bytes(), original)
        with self.assertRaises(h.DiagnosticError):
            h.write_new(self.run / "packet.json", b"overwritten")

    def test_cli_outputs_readable_errors_nonzero_and_no_report_on_invalid_run(self):
        self.packet()
        rows = self.judgments()
        self.write_jsonl(self.judgments_path, rows[:-1])
        report_path = self.root / "report.json"
        stderr = io.StringIO()
        with redirect_stderr(stderr):
            status = h.main(["--root", str(self.root), "report", "--run", str(self.run),
                             "--judgments", str(self.judgments_path), "--out", str(report_path)])
        self.assertEqual(status, 2)
        self.assertIn("missing 1 trial", stderr.getvalue())
        self.assertNotIn("Traceback", stderr.getvalue())
        self.assertFalse(report_path.exists())

    def test_cli_validates_and_writes_complete_report(self):
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            self.assertEqual(h.main(["--root", str(self.root), "validate"]), 0)
        self.assertIn("no judgments executed", stdout.getvalue())
        self.packet()
        self.judgments()
        report_path = self.root / "report.json"
        with redirect_stdout(io.StringIO()):
            self.assertEqual(h.main(["--root", str(self.root), "report", "--run", str(self.run),
                                     "--judgments", str(self.judgments_path), "--out", str(report_path)]), 0)
        report = json.loads(report_path.read_text(encoding="utf-8"))
        self.assertEqual(report["summary"]["trials"], 8)
        self.assertEqual(report["report_implementation"]["harness_sha256"],
                         h.digest(Path(h.__file__).read_bytes()))
        self.assertTrue(report["report_implementation"]["python_version"])


if __name__ == "__main__":
    unittest.main()
