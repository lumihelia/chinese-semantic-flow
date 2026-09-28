"""Validate authored diagnostics, create blind trials, and audit judgments.

This module never calls a model. Keys are provisional repository deductions or
hypotheses, not human gold. See FORMAT.md for the input and judgment contract.
"""

import argparse
from collections import Counter
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import random
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
CRITERIA = {"grounding", "relation", "stance", "task_fit", "scope", "discourse"}
TAGS = {"unsupported_contrast", "unsupported_detail", "relation_drift",
        "stance_drift", "interaction_overreach", "task_mismatch", "scope_leak",
        "template_overcorrection", "unresolved_naturalness"}
CASE_FIELDS = {"id", "family", "kind", "mode", "profile", "context", "prompt",
               "candidates", "criteria", "failure_tags", "expected", "provenance"}
TRIAL_FIELDS = {"trial_id", "mode", "profile", "context", "prompt", "criteria", "candidates"}
SHA256 = re.compile(r"[0-9a-f]{64}\Z")
PROFILE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
COMMIT = re.compile(r"[0-9a-f]{40}\Z")


class DiagnosticError(ValueError):
    """A fail-closed input or integrity failure, suitable for CLI display."""


def require(condition, message):
    if not condition:
        raise DiagnosticError(message)


def exact_keys(value, keys, where):
    require(isinstance(value, dict), f"{where}: expected an object")
    require(set(value) == set(keys),
            f"{where}: invalid fields (missing {sorted(set(keys) - set(value))}; "
            f"unknown {sorted(set(value) - set(keys))})")


def nonblank(value, where):
    require(isinstance(value, str) and bool(value.strip()), f"{where}: expected nonblank text")
    # JSON escape sequences can represent lone surrogates, which are not UTF-8 text.
    try:
        value.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise DiagnosticError(f"{where}: text is not valid UTF-8") from exc
    return value


def enum(value, choices, where):
    require(isinstance(value, str) and value in choices, f"{where}: unknown label")


def unique_list(value, where, choices=None):
    require(isinstance(value, list) and value, f"{where}: expected a nonempty list")
    for item in value:
        nonblank(item, where)
        if choices is not None:
            enum(item, choices, where)
    require(len(set(value)) == len(value), f"{where}: duplicate values")


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")


def read_bytes(path):
    try:
        return Path(path).read_bytes()
    except OSError as exc:
        raise DiagnosticError(f"Cannot read {path}: {exc.strerror}") from exc


def decode(raw, where):
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise DiagnosticError(f"{where}: invalid UTF-8") from exc


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"JSON: duplicate object key {key!r}")
        result[key] = value
    return result


def _constant(value):
    raise DiagnosticError(f"JSON: nonfinite number {value!r} is not allowed")


def parse_json(raw, where):
    try:
        return json.loads(decode(raw, where), object_pairs_hook=_pairs, parse_constant=_constant)
    except DiagnosticError as exc:
        raise DiagnosticError(f"{where}: {exc}") from exc
    except (ValueError, RecursionError) as exc:
        raise DiagnosticError(f"{where}: malformed JSON ({exc})") from exc


def parse_jsonl(raw, where):
    lines = decode(raw, where).splitlines()
    require(bool(lines), f"{where}: empty JSONL")
    rows = []
    for number, line in enumerate(lines, 1):
        require(bool(line.strip()), f"{where}:{number}: blank JSONL row")
        rows.append(parse_json(line.encode("utf-8"), f"{where}:{number}"))
    return rows


def git_bytes(root, *args):
    # Fixed argument vectors, full commit IDs, and no replacement objects keep
    # provenance reads local and independent of shell interpretation/worktree edits.
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    env["GIT_NO_REPLACE_OBJECTS"] = "1"
    try:
        process = subprocess.run(["git", "--no-pager", "-C", str(root), *args],
                                 capture_output=True, timeout=15, env=env, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise DiagnosticError(f"Source snapshot: cannot read local git objects ({exc})") from exc
    require(process.returncode == 0, "Source snapshot: git object or path is unavailable")
    return process.stdout


@dataclass
class Inputs:
    root: Path
    sources: dict
    cases: list
    rubric: str
    digests: dict


def load_inputs(root=ROOT):
    """Validate all inputs, including quotes against the pinned git commit."""
    root = Path(root)
    sources_raw = read_bytes(root / "benchmarks/data/sources.json")
    cases_raw = read_bytes(root / "benchmarks/data/cases.jsonl")
    rubric_raw = read_bytes(root / "evaluation/RUBRIC.md")
    sources = parse_json(sources_raw, "sources.json")
    exact_keys(sources, {"schema_version", "baseline_commit", "sources"}, "sources.json")
    require(type(sources["schema_version"]) is int and sources["schema_version"] == 1,
            "sources.json: unsupported schema_version")
    commit = nonblank(sources["baseline_commit"], "baseline_commit")
    require(bool(COMMIT.fullmatch(commit)), "baseline_commit: expected a full lowercase commit SHA")
    require(git_bytes(root, "cat-file", "-t", commit).strip() == b"commit",
            "baseline_commit: object is not a commit")
    entries = sources["sources"]
    require(isinstance(entries, list) and entries, "sources: expected a nonempty list")
    source_ids, snapshots = set(), {}
    for index, source in enumerate(entries):
        where = f"sources[{index}]"
        exact_keys(source, {"id", "path", "start_line", "end_line", "quote", "sha256"}, where)
        source_id = nonblank(source["id"], f"{where}.id")
        require(source_id not in source_ids, f"{where}: duplicate source ID")
        source_ids.add(source_id)
        path = nonblank(source["path"], f"{where}.path")
        parsed_path = PurePosixPath(path)
        require(not parsed_path.is_absolute() and ".." not in parsed_path.parts
                and path == parsed_path.as_posix() and "\\" not in path and "\x00" not in path
                and path != ".", f"{where}: path must be canonical and repository-relative")
        start, end = source["start_line"], source["end_line"]
        require(type(start) is int and type(end) is int and 1 <= start <= end,
                f"{where}: invalid line range")
        quote = nonblank(source["quote"], f"{where}.quote")
        require(isinstance(source["sha256"], str) and bool(SHA256.fullmatch(source["sha256"])),
                f"{where}: invalid sha256")
        require(digest(quote.encode("utf-8")) == source["sha256"], f"{where}: quote digest mismatch")
        if path not in snapshots:
            snapshots[path] = decode(git_bytes(root, "show", "--no-ext-diff", "--no-textconv",
                                              f"{commit}:{path}"), f"baseline:{path}").splitlines()
        lines = snapshots[path]
        require(end <= len(lines), f"{where}: line range exceeds source snapshot")
        require("\n".join(lines[start - 1:end]) == quote,
                f"{where}: quote differs from pinned source snapshot")
    cases = parse_jsonl(cases_raw, "cases.jsonl")
    case_ids = set()
    for index, case in enumerate(cases):
        where = f"cases[{index}]"
        exact_keys(case, CASE_FIELDS, where)
        case_id = nonblank(case["id"], f"{where}.id")
        require(case_id not in case_ids, f"{where}: duplicate case ID")
        case_ids.add(case_id)
        for field in ("family", "context", "prompt"):
            nonblank(case[field], f"{where}.{field}")
        enum(case["kind"], {"minimal_pair", "context_pair", "negative_control", "reference_recheck"}, where)
        enum(case["mode"], {"rewrite", "generation", "dialogue"}, where)
        profile = nonblank(case["profile"], f"{where}.profile")
        require(profile == "core" or bool(PROFILE.fullmatch(profile)), f"{where}.profile: expected core or an extension slug")
        exact_keys(case["candidates"], {"a", "b"}, f"{where}.candidates")
        for value in case["candidates"].values():
            nonblank(value, f"{where}.candidates")
        unique_list(case["criteria"], f"{where}.criteria", CRITERIA)
        unique_list(case["failure_tags"], f"{where}.failure_tags", TAGS)
        expected = case["expected"]
        exact_keys(expected, {"status", "verdict", "reason"}, f"{where}.expected")
        enum(expected["status"], {"contract", "hypothesis", "unresolved"}, f"{where}.expected.status")
        enum(expected["verdict"], {"a", "b", "tie", "abstain"}, f"{where}.expected.verdict")
        require(expected["status"] != "unresolved" or expected["verdict"] == "abstain",
                f"{where}: unresolved keys require abstain")
        nonblank(expected["reason"], f"{where}.expected.reason")
        provenance = case["provenance"]
        exact_keys(provenance, {"origin", "source_refs", "hypothesis", "changes"}, f"{where}.provenance")
        enum(provenance["origin"], {"repository_excerpt", "repository_adaptation", "synthetic"}, where)
        unique_list(provenance["source_refs"], f"{where}.source_refs", source_ids)
        nonblank(provenance["hypothesis"], f"{where}.provenance.hypothesis")
        nonblank(provenance["changes"], f"{where}.provenance.changes")
    rubric = nonblank(decode(rubric_raw, "RUBRIC.md"), "RUBRIC.md")
    return Inputs(root, sources, cases, rubric,
                  {"dataset": digest(cases_raw), "sources": digest(sources_raw), "rubric": digest(rubric_raw)})


def build_packet(inputs, seed):
    """Return deterministic public packet and private orientation manifest."""
    require(type(seed) is int, "seed: expected an integer")
    identity = encoded({"seed": seed, "digests": inputs.digests})
    rng = random.Random(digest(identity))
    packet_id = "p-" + digest(identity)[:24]
    pairs = []
    for case in inputs.cases:
        for mapping in ({"A": "a", "B": "b"}, {"A": "b", "B": "a"}):
            trial_id = f"t-{rng.getrandbits(128):032x}"
            trial = {"trial_id": trial_id,
                     **{key: case[key] for key in ("mode", "profile", "context", "prompt", "criteria")},
                     "candidates": {label: case["candidates"][stable] for label, stable in mapping.items()}}
            pairs.append((trial, {"trial_id": trial_id, "case_id": case["id"], "mapping": mapping}))
    rng.shuffle(pairs)
    packet = {"schema_version": 1, "packet_id": packet_id, "rubric": inputs.rubric,
              "trials": [pair[0] for pair in pairs]}
    manifest = {"schema_version": 1, "packet_id": packet_id, "seed": seed,
                "digests": {**inputs.digests, "packet": digest(encoded(packet))},
                "trials": [pair[1] for pair in pairs]}
    return packet, manifest


def write_new(path, raw):
    """Never overwrite an existing run or report; private artifacts get mode 0600."""
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "wb") as stream:
            stream.write(raw)
    except OSError as exc:
        raise DiagnosticError(f"Cannot create {path}: {exc.strerror}") from exc


def create_packet(root, seed, out):
    inputs = load_inputs(root)
    packet, manifest = build_packet(inputs, seed)
    out = Path(out)
    try:
        out.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise DiagnosticError(f"Cannot create run directory {out}: {exc.strerror}") from exc
    require(not (out / "packet.json").exists() and not (out / "manifest.json").exists(),
            "Run files already exist; choose a new output directory")
    write_new(out / "manifest.json", encoded(manifest))
    write_new(out / "packet.json", encoded(packet))
    return packet, manifest


def load_run(root, run):
    inputs = load_inputs(root)
    run = Path(run)
    packet_raw = read_bytes(run / "packet.json")
    packet = parse_json(packet_raw, "packet.json")
    manifest = parse_json(read_bytes(run / "manifest.json"), "manifest.json")
    exact_keys(packet, {"schema_version", "packet_id", "rubric", "trials"}, "packet")
    exact_keys(manifest, {"schema_version", "packet_id", "seed", "digests", "trials"}, "manifest")
    require(type(manifest["seed"]) is int, "manifest.seed: expected an integer")
    for label, document in (("packet", packet), ("manifest", manifest)):
        require(type(document["schema_version"]) is int and document["schema_version"] == 1,
                f"{label}: unsupported schema_version")
        nonblank(document["packet_id"], f"{label}.packet_id")
        require(isinstance(document["trials"], list), f"{label}.trials: expected a list")
    exact_keys(manifest["digests"], {"dataset", "sources", "rubric", "packet"}, "manifest.digests")
    for label, value in manifest["digests"].items():
        require(isinstance(value, str) and bool(SHA256.fullmatch(value)), f"{label}: invalid digest")
        expected_digest = digest(packet_raw) if label == "packet" else inputs.digests[label]
        require(value == expected_digest, f"{label}: digest mismatch; run inputs are stale or modified")
    expected_packet, expected_manifest = build_packet(inputs, manifest["seed"])
    # Equality against regenerated artifacts validates all fields, trial coverage,
    # both orientations, opaque IDs, exact candidate text, and mapping. Digests
    # alone would accept a self-consistent but incorrectly edited manifest.
    require(packet == expected_packet, "packet: differs from deterministic packet for the validated inputs/seed")
    require(manifest == expected_manifest, "manifest: differs from deterministic trial mappings")
    return inputs, packet, manifest


def load_judgments(path, packet):
    raw = read_bytes(path)
    rows = parse_jsonl(raw, "judgments")
    trials = {trial["trial_id"]: trial for trial in packet["trials"]}
    judgments = {}
    for index, row in enumerate(rows):
        where = f"judgments[{index}]"
        exact_keys(row, {"trial_id", "verdict", "evidence", "reason"}, where)
        trial_id = nonblank(row["trial_id"], f"{where}.trial_id")
        require(trial_id in trials, f"{where}: unknown trial ID")
        require(trial_id not in judgments, f"{where}: duplicate trial ID")
        trial = trials[trial_id]
        enum(row["verdict"], {"A", "B", "tie", "abstain"}, f"{where}.verdict")
        nonblank(row["reason"], f"{where}.reason")
        require(isinstance(row["evidence"], list), f"{where}.evidence: expected a list")
        quoted = set()
        for evidence in row["evidence"]:
            exact_keys(evidence, {"candidate", "quote", "criterion"}, f"{where}.evidence")
            enum(evidence["candidate"], {"A", "B"}, f"{where}.evidence.candidate")
            enum(evidence["criterion"], trial["criteria"], f"{where}.evidence.criterion")
            quote = nonblank(evidence["quote"], f"{where}.evidence.quote")
            require(quote in trial["candidates"][evidence["candidate"]], f"{where}: invented evidence quote")
            quoted.add(evidence["candidate"])
        require(row["verdict"] == "abstain" or quoted == {"A", "B"},
                f"{where}: substantive judgments require evidence from both candidates")
        judgments[trial_id] = row
    missing = set(trials) - set(judgments)
    require(not missing, f"judgments: missing {len(missing)} trial(s); partial runs cannot be scored")
    return judgments, digest(raw)


def ratio(numerator, denominator):
    return {"numerator": numerator, "denominator": denominator,
            "rate": numerator / denominator if denominator else None}


def summarize(rows):
    substantive = [row for row in rows if row["outcome"] in {"a", "b", "tie"}]
    contract = [row for row in rows if row["key_status"] == "contract"]
    contract_substantive = [row for row in substantive if row["key_status"] == "contract"]
    agreements = sum(row["outcome"] == row["key_verdict"] for row in contract_substantive)
    unresolved = [row for row in rows if row["key_status"] == "unresolved"]
    counts = Counter(row["outcome"] for row in rows)
    return {
        "trials": 2 * len(rows), "cases": len(rows),
        "consistent_cases": len(rows) - counts["inconsistent"],
        "inconsistent_cases": counts["inconsistent"],
        "consistent_substantive_cases": len(substantive),
        "consistent_abstention_cases": counts["abstain"],
        "abstention_trials": sum(verdict == "abstain" for row in rows for verdict in row["mapped_verdicts"]),
        "tie_cases": counts["tie"],
        "outcomes": {label: counts[label] for label in ("a", "b", "tie", "abstain", "inconsistent")},
        "substantive_coverage": ratio(len(substantive), len(rows)),
        "contract_key_agreement_all_cases": ratio(agreements, len(contract)),
        "contract_key_agreement_substantive_consistent": ratio(agreements, len(contract_substantive)),
        "contract_key_abstention_matches": sum(row["outcome"] == row["key_verdict"] == "abstain" for row in contract),
        "unresolved_case_abstentions": ratio(sum(row["outcome"] == "abstain" for row in unresolved), len(unresolved)),
    }


def make_report(root, run, judgments_path):
    inputs, packet, manifest = load_run(root, run)
    judgments, judgments_digest = load_judgments(judgments_path, packet)
    grouped = {case["id"]: [] for case in inputs.cases}
    for trial in manifest["trials"]:
        verdict = judgments[trial["trial_id"]]["verdict"]
        grouped[trial["case_id"]].append({"trial_id": trial["trial_id"],
                                         "verdict": trial["mapping"].get(verdict, verdict)})
    rows = []
    for case in inputs.cases:
        trials = grouped[case["id"]]
        mapped = [trial["verdict"] for trial in trials]
        outcome = mapped[0] if mapped[0] == mapped[1] else "inconsistent"
        key = case["expected"]
        rows.append({"case_id": case["id"], "family": case["family"], "profile": case["profile"],
                     "key_status": key["status"], "key_verdict": key["verdict"],
                     "trial_ids": [trial["trial_id"] for trial in trials], "mapped_verdicts": mapped,
                     "outcome": outcome,
                     "provisional_key_match": outcome == key["verdict"] if key["status"] != "unresolved" else None})
    strata = {}
    for dimension in ("family", "profile", "key_status"):
        strata[dimension] = {value: summarize([row for row in rows if row[dimension] == value])
                             for value in sorted({row[dimension] for row in rows})}
    return {"schema_version": 1, "packet_id": packet["packet_id"],
            "digests": {**manifest["digests"], "judgments": judgments_digest},
            "report_implementation": {"harness_sha256": digest(read_bytes(Path(__file__))),
                                      "python_version": sys.version,
                                      "python_implementation": sys.implementation.name},
            "interpretation": [
                "Authored diagnostic judgments; provisional keys are not human gold.",
                "Contract agreement counts substantive consistent decisions; abstention matches are separate.",
                "Hypothesis key matches are descriptive per-case observations, excluded from contract agreement.",
                "Quoted evidence is checked for traceability, not semantic correctness.",
                "No aggregate language-quality, calibration, generalization, or generation-quality claim is supported."],
            "summary": summarize(rows), "strata": strata, "cases": rows}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="repository root (defaults to this checkout)")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("validate", help="validate data, provenance, and rubric")
    packet_parser = commands.add_parser("packet", help="write blind packet.json and private manifest.json")
    packet_parser.add_argument("--seed", type=int, required=True)
    packet_parser.add_argument("--out", type=Path, required=True)
    report_parser = commands.add_parser("report", help="validate a complete judgment run and report counts")
    report_parser.add_argument("--run", type=Path, required=True)
    report_parser.add_argument("--judgments", type=Path, required=True)
    report_parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "validate":
            inputs = load_inputs(args.root)
            print(f"Valid: {len(inputs.cases)} cases; {len(inputs.sources['sources'])} pinned sources; no judgments executed.")
        elif args.command == "packet":
            packet, _ = create_packet(args.root, args.seed, args.out)
            print(f"Created {len(packet['trials'])} blind trials in {args.out / 'packet.json'}.")
            print("Keep manifest.json private and outside the evaluator context.")
        else:
            report = make_report(args.root, args.run, args.judgments)
            write_new(args.out, encoded(report))
            print(f"Validated {report['summary']['trials']} judgments; report written to {args.out}.")
    except DiagnosticError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
