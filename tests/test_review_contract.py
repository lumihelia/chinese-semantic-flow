"""Synthetic reporting-contract fixtures; these are not semantic assessments."""

from contextlib import redirect_stderr, redirect_stdout
from copy import deepcopy
import io
import json
from pathlib import Path
import tempfile
import unittest

from evaluation import harness as h
from evaluation import review_contract as r


class ReviewContractTests(unittest.TestCase):
    def setUp(self):
        self.packet = {"schema_version": 2, "request": "保留原意。",
                       "instructions": ["分开记录保真与风格，不推断作者采用。"],
                       "items": [{"candidate_id": "c-001", "source_frame_quote": "叙述中的猜测。",
                                  "frame_note": "Synthetic test fixture.", "context_before": "",
                                  "context_after": "", "source": "他可能会来。", "candidate": "他也许会来。"},
                                 {"candidate_id": "c-002", "source_frame_quote": "另一个猜测。",
                                  "frame_note": "Synthetic test fixture.", "context_before": "",
                                  "context_after": "", "source": "她可能会来。", "candidate": "她也许会来。"}]}
        self.reviews = [{"candidate_id": item["candidate_id"], "overall_fidelity": "preserved",
                         "fidelity_findings": [], "style_observations": [],
                         "author_acceptability": "unjudged"} for item in self.packet["items"]]
        self.quote = {"source_quote": "可能", "candidate_quote": "也许", "note": "Synthetic fixture note."}

    def finding(self, severity):
        return {"severity": severity, **self.quote}

    def test_article_title_context_is_supported_without_narrative_frame(self):
        for item in self.packet["items"]:
            del item["source_frame_quote"]
            del item["frame_note"]
            item["title"] = "一篇真实文章的标题"
        self.assertEqual(r.validate_reviews(self.packet, self.reviews)["review_count"], 2)
        self.assertEqual(self.packet["items"][0]["title"], "一篇真实文章的标题")

    def test_optional_context_does_not_allow_condition_or_answer_leakage(self):
        for field, value in (("condition", "core"), ("expected", "preserved"),
                             ("title", None), ("frame_note", "")):
            with self.subTest(field=field):
                packet = deepcopy(self.packet)
                packet["items"][0][field] = value
                with self.assertRaises(h.DiagnosticError):
                    r.validate_reviews(packet, self.reviews)

    def test_style_only_stays_preserved_despite_unknown_acceptance(self):
        self.reviews[0]["style_observations"] = [{**self.quote, "note": "作者是否喜欢这种风格尚不清楚。"}]
        self.assertEqual(r.validate_reviews(self.packet, self.reviews)["review_count"], 2)
        before = deepcopy(self.reviews)
        self.reviews[0]["overall_fidelity"] = "uncertain"
        with self.assertRaisesRegex(h.DiagnosticError, "must be 'preserved'"):
            r.validate_reviews(self.packet, self.reviews)
        self.assertEqual(self.reviews[0]["overall_fidelity"], "uncertain")
        self.assertEqual(self.reviews[0]["style_observations"], before[0]["style_observations"])

    def test_definite_issue_cannot_hide_under_preserved_or_uncertain(self):
        self.reviews[0]["fidelity_findings"] = [self.finding("possible"), self.finding("definite")]
        for label in ("preserved", "uncertain"):
            with self.subTest(label=label):
                self.reviews[0]["overall_fidelity"] = label
                with self.assertRaisesRegex(h.DiagnosticError, "must be 'violated'"):
                    r.validate_reviews(self.packet, self.reviews)
        self.reviews[0]["overall_fidelity"] = "violated"
        self.assertEqual(r.validate_reviews(self.packet, self.reviews)["reported_overall_fidelity"]["violated"], 1)

    def test_only_possible_findings_require_uncertain(self):
        self.reviews[0].update(fidelity_findings=[self.finding("possible")], overall_fidelity="uncertain")
        r.validate_reviews(self.packet, self.reviews)
        for label in ("preserved", "violated"):
            with self.subTest(label=label):
                self.reviews[0]["overall_fidelity"] = label
                with self.assertRaisesRegex(h.DiagnosticError, "must be 'uncertain'"):
                    r.validate_reviews(self.packet, self.reviews)

    def test_forged_or_non_target_quotes_rejected_for_both_observation_types(self):
        for field in ("fidelity_findings", "style_observations"):
            for quote_field in ("source_quote", "candidate_quote"):
                for fake in ("编造的引文", "叙述中的猜测。", "可能 ", ""):
                    with self.subTest(field=field, quote_field=quote_field, fake=fake):
                        rows = deepcopy(self.reviews)
                        observation = self.finding("possible") if field == "fidelity_findings" else deepcopy(self.quote)
                        observation[quote_field] = fake
                        rows[0][field] = [observation]
                        rows[0]["overall_fidelity"] = "uncertain" if field == "fidelity_findings" else "preserved"
                        with self.assertRaises(h.DiagnosticError):
                            r.validate_reviews(self.packet, rows)

    def test_duplicate_missing_unknown_and_reordered_ids(self):
        r.validate_reviews(self.packet, list(reversed(self.reviews)))
        invalid = [(self.reviews[:1], "missing candidate IDs"),
                   ([], "missing candidate IDs"),
                   (self.reviews + [deepcopy(self.reviews[0])], "duplicate candidate ID"),
                   ([{**self.reviews[0], "candidate_id": "absent"}, self.reviews[1]], "unknown candidate ID")]
        for rows, message in invalid:
            with self.subTest(message=message), self.assertRaisesRegex(h.DiagnosticError, message):
                r.validate_reviews(self.packet, rows)
        self.packet["items"].append(deepcopy(self.packet["items"][0]))
        with self.assertRaisesRegex(h.DiagnosticError, "duplicate candidate ID"):
            r.validate_reviews(self.packet, self.reviews)

    def test_invented_author_acceptance_and_invalid_fields_fail_closed(self):
        mutations = [lambda row: row.update(author_acceptability="accepted"),
                     lambda row: row.update(author_acceptability=True),
                     lambda row: row.update(overall_fidelity=None),
                     lambda row: row.update(fidelity_findings={}),
                     lambda row: row.update(style_observations="none"),
                     lambda row: row.update(author_note="approved"),
                     lambda row: row.update(fidelity_findings=[self.finding("minor")]),
                     lambda row: row.update(style_observations=[self.finding("possible")]),
                     lambda row: row.update(style_observations=[{**self.quote, "note": 7}]),
                     lambda row: row.update(style_observations=[{**self.quote, "source_quote": None}])]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                rows = deepcopy(self.reviews)
                mutate(rows[0])
                with self.assertRaises(h.DiagnosticError):
                    r.validate_reviews(self.packet, rows)

    def test_packet_rejects_old_version_wrong_types_and_unknown_fields(self):
        mutations = [lambda packet: packet.update(schema_version=1),
                     lambda packet: packet.update(schema_version=True),
                     lambda packet: packet.update(items=[]),
                     lambda packet: packet.update(instructions="instructions"),
                     lambda packet: packet.update(extra="value"),
                     lambda packet: packet["items"][0].update(context_before=None),
                     lambda packet: packet["items"][0].update(candidate="")]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                packet = deepcopy(self.packet)
                mutate(packet)
                with self.assertRaises(h.DiagnosticError):
                    r.validate_reviews(packet, self.reviews)

    def test_cli_hashes_raw_bytes_leaves_files_unchanged_and_fails_without_report(self):
        with tempfile.TemporaryDirectory(prefix="csf-review-contract-") as directory:
            packet_path, results_path = Path(directory) / "packet.json", Path(directory) / "results.jsonl"
            packet_raw = h.encoded(self.packet)
            results_raw = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in self.reviews).encode("utf-8")
            packet_path.write_bytes(packet_raw)
            results_path.write_bytes(results_raw)
            args = ["--packet", str(packet_path), "--results", str(results_path)]
            stdout, stderr = io.StringIO(), io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                self.assertEqual(r.main(args), 0)
            report = json.loads(stdout.getvalue())
            self.assertTrue(report["complete"])
            self.assertEqual(report["digests"], {"packet_sha256": h.digest(packet_raw),
                                                 "results_sha256": h.digest(results_raw)})
            self.assertEqual(packet_path.read_bytes(), packet_raw)
            self.assertEqual(results_path.read_bytes(), results_raw)
            self.assertEqual(stderr.getvalue(), "")
            invalid_inputs = [results_raw.splitlines(keepends=True)[0], results_raw + b"\n",
                              b'{"candidate_id":"c-001","candidate_id":"c-002"}\n', b'{"x": NaN}\n']
            for invalid_raw in invalid_inputs:
                with self.subTest(raw=invalid_raw):
                    results_path.write_bytes(invalid_raw)
                    stdout, stderr = io.StringIO(), io.StringIO()
                    with redirect_stdout(stdout), redirect_stderr(stderr):
                        self.assertEqual(r.main(args), 2)
                    self.assertEqual(stdout.getvalue(), "")
                    self.assertTrue(stderr.getvalue().startswith("error: "))
                    self.assertEqual(results_path.read_bytes(), invalid_raw)


if __name__ == "__main__":
    unittest.main()
