"""Read-only validation of the Phase 2 v2 semantic-review reporting contract.

Checks complete candidate coverage, field types, verbatim target-text quotes,
and severity/overall consistency. It does not judge language, authenticate source
provenance or reviewer identity, or establish author acceptance. Raw reviews are
never normalized or rewritten; hashes identify only the supplied file bytes.
"""

import argparse
from collections import Counter
from pathlib import Path
import sys

from evaluation.harness import (DiagnosticError, digest, encoded, enum, exact_keys,
                                nonblank, parse_json, parse_jsonl, read_bytes, require)


PACKET_FIELDS = {"schema_version", "request", "instructions", "items"}
ITEM_FIELDS = {"candidate_id", "context_before", "context_after", "source", "candidate"}
CONTEXT_FIELDS = {"title", "source_frame_quote", "frame_note"}
REVIEW_FIELDS = {"candidate_id", "overall_fidelity", "fidelity_findings",
                 "style_observations", "author_acceptability"}
QUOTE_FIELDS = {"source_quote", "candidate_quote", "note"}
FIDELITY = {"preserved", "uncertain", "violated"}
SEVERITIES = {"possible", "definite"}


def validate_packet(packet):
    """Return the v2 packet's complete candidate index, without changing it."""
    exact_keys(packet, PACKET_FIELDS, "packet")
    require(type(packet["schema_version"]) is int and packet["schema_version"] == 2,
            "packet: unsupported schema_version (expected 2)")
    nonblank(packet["request"], "packet.request")
    instructions = packet["instructions"]
    require(isinstance(instructions, list) and instructions,
            "packet.instructions: expected a nonempty list")
    for index, instruction in enumerate(instructions):
        nonblank(instruction, f"packet.instructions[{index}]")
    require(isinstance(packet["items"], list) and packet["items"],
            "packet.items: expected a nonempty list")
    items = {}
    for index, item in enumerate(packet["items"]):
        where = f"packet.items[{index}]"
        require(isinstance(item, dict), f"{where}: expected an object")
        # Narrative frames and published-article titles are both legitimate
        # context forms. Keep the payload closed to unrelated metadata/keys.
        exact_keys(item, ITEM_FIELDS | (set(item) & CONTEXT_FIELDS), where)
        candidate_id = nonblank(item["candidate_id"], f"{where}.candidate_id")
        require(candidate_id not in items, f"{where}: duplicate candidate ID {candidate_id}")
        for field in ITEM_FIELDS - {"context_before", "context_after"}:
            nonblank(item[field], f"{where}.{field}")
        for field in set(item) & CONTEXT_FIELDS:
            nonblank(item[field], f"{where}.{field}")
        for field in ("context_before", "context_after"):
            # Empty boundary context is valid; other values must be UTF-8 text.
            if item[field] != "":
                nonblank(item[field], f"{where}.{field}")
        items[candidate_id] = item
    return items


def validate_observations(observations, item, where, fidelity=False):
    require(isinstance(observations, list), f"{where}: expected a list")
    severities = set()
    for index, observation in enumerate(observations):
        location = f"{where}[{index}]"
        exact_keys(observation, QUOTE_FIELDS | ({"severity"} if fidelity else set()), location)
        nonblank(observation["note"], f"{location}.note")
        for field in ("source", "candidate"):
            quote = nonblank(observation[f"{field}_quote"], f"{location}.{field}_quote")
            require(quote in item[field],
                    f"{location}.{field}_quote: quote is not verbatim in target {field}")
        if fidelity:
            enum(observation["severity"], SEVERITIES, f"{location}.severity")
            severities.add(observation["severity"])
    return severities


def validate_reviews(packet, reviews):
    """Validate all rows; return descriptive label counts only after completeness."""
    items = validate_packet(packet)
    require(isinstance(reviews, list), "results: expected a list of review objects")
    seen, counts = set(), Counter()
    for index, review in enumerate(reviews):
        where = f"results[{index}]"
        exact_keys(review, REVIEW_FIELDS, where)
        candidate_id = nonblank(review["candidate_id"], f"{where}.candidate_id")
        require(candidate_id not in seen, f"{where}: duplicate candidate ID {candidate_id}")
        require(candidate_id in items, f"{where}: unknown candidate ID {candidate_id}")
        seen.add(candidate_id)
        enum(review["overall_fidelity"], FIDELITY, f"{where}.overall_fidelity")
        enum(review["author_acceptability"], {"unjudged"}, f"{where}.author_acceptability")
        severities = validate_observations(review["fidelity_findings"], items[candidate_id],
                                          f"{where}.fidelity_findings", fidelity=True)
        validate_observations(review["style_observations"], items[candidate_id],
                              f"{where}.style_observations")
        expected = ("violated" if "definite" in severities else
                    "uncertain" if "possible" in severities else "preserved")
        require(review["overall_fidelity"] == expected,
                f"{where} ({candidate_id}): overall_fidelity must be {expected!r} "
                "for the reported fidelity_findings; style observations do not affect it")
        counts[review["overall_fidelity"]] += 1
    require(seen == set(items), f"results: missing candidate IDs {sorted(set(items) - seen)}")
    return {"candidate_count": len(items), "review_count": len(reviews),
            "reported_overall_fidelity": {label: counts[label] for label in sorted(FIDELITY)}}


def validate_files(packet_path, results_path):
    packet_raw, results_raw = read_bytes(packet_path), read_bytes(results_path)
    packet = parse_json(packet_raw, str(packet_path))
    reviews = parse_jsonl(results_raw, str(results_path))
    summary = validate_reviews(packet, reviews)
    return {"schema_version": 1, "contract": "phase2-semantic-review-v2",
            "status": "valid", "complete": True,
            "digests": {"packet_sha256": digest(packet_raw), "results_sha256": digest(results_raw)},
            **summary,
            "interpretation": [
                "Complete coverage, fields, exact target-text quotes, and reporting consistency validated.",
                "Reported labels are not independently verified semantic judgments or language scores.",
                "Source provenance and reviewer identity are not authenticated; author acceptability is unjudged.",
                "Raw input files were not normalized or rewritten."]}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", type=Path, required=True)
    parser.add_argument("--results", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        report = validate_files(args.packet, args.results)
    except DiagnosticError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(encoded(report).decode("utf-8"), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
