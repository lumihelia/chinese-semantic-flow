# Diagnostic data and judgment contract (v1)

This contract is an agent-proposed research artifact. Repository rules supply the constraints; synthetic cases and provisional keys test interpretations of those rules. No key is human gold.

`benchmarks/data/sources.json`: object with `schema_version: 1`, `baseline_commit` (40 hex), and `sources` array. Each source has unique `id`, repository-relative `path`, `start_line`, `end_line` (inclusive, 1-based), exact `quote`, and `sha256` of the UTF-8 quote. Resolve baseline paths using `git show <baseline_commit>:<path>`; do not validate historical quotes against a changed worktree.

`benchmarks/data/cases.jsonl`: one object per line, exactly these fields:

- `id`: unique opaque case ID, e.g. `csf-001`.
- `family`: related variants share a family; it is the unit of splitting and replication.
- `kind`: `minimal_pair`, `context_pair`, `negative_control`, or `reference_recheck`.
- `mode`: `rewrite`, `generation`, or `dialogue`.
- `profile`: `core`, or the slug of an extension the case requires (lowercase letters, digits and hyphens). The public dataset contains `core` cases only.
- `context`, `prompt`: nonempty strings; supplied context is the complete case evidence.
- `candidates`: exactly `a` and `b`, nonempty UTF-8 text strings (punctuation-only dialogue such as `？` is legal; language is not checked by a character whitelist).
- `criteria`: nonempty unique list drawn from `grounding`, `relation`, `stance`, `task_fit`, `scope`, `discourse`.
- `failure_tags`: nonempty unique list drawn from `unsupported_contrast`, `unsupported_detail`, `relation_drift`, `stance_drift`, `interaction_overreach`, `task_mismatch`, `scope_leak`, `template_overcorrection`, `unresolved_naturalness`.
- `expected`: exactly `status`, `verdict`, `reason`. Status is `contract`, `hypothesis`, or `unresolved`; verdict is `a`, `b`, `tie`, or `abstain`. `unresolved` requires `abstain`. Reason is a nonempty evidence-based explanation. `contract` means a provisional deduction from the stated task and repo constraint, not an externally validated gold label.
- `provenance`: exactly `origin`, `source_refs`, `hypothesis`, `changes`. Origin is `repository_excerpt`, `repository_adaptation`, or `synthetic`. Refs are a nonempty unique list of existing source IDs. `hypothesis` describes the proposed test, not a finding. `changes` states which text/context is constructed or modified and what is held constant. Even verbatim candidate text does not make constructed context authentic user data.

## Blind packet and private manifest

The packet has `schema_version`, `packet_id`, `rubric` (complete content of `evaluation/RUBRIC.md`), and `trials`. Each trial has opaque `trial_id`, `mode`, `profile`, `context`, `prompt`, `criteria`, `candidates` (`A`, `B`). Exclude case IDs, families, failure tags, keys, provenance, source labels, original Bad/Better headings, model identities, and pair orientation. Emit each case twice with candidates swapped, then deterministically shuffle trials using a seed. This reduces label and position cues; repeated-text recognition remains possible. Keep the manifest out of the evaluator's context and use separate sessions for stronger blinding.

Manifest records packet ID, seed, SHA-256 digests of the dataset, sources, rubric, and packet, plus each trial's case ID and exact A/B mapping. The packet digest covers the on-disk bytes. The manifest is a local integrity aid, not a security boundary against a party able to edit both files.

## Judgment JSONL

Exactly one row per trial, with exactly: `trial_id`, `verdict` (`A`, `B`, `tie`, `abstain`), `evidence`, `reason`. Evidence is a list of objects with exactly `candidate` (`A` or `B`), `quote` (nonempty exact substring of that candidate), `criterion` (one of the trial criteria). Include at least one quote from each candidate for A/B/tie judgments. Abstention can have an empty list when the missing evidence is in context; name the missing evidence in `reason`. Quotes establish traceability, not correctness of the explanation. Do not request private reasoning traces; give concise observable justification.

Reject unknown keys/labels/criteria, malformed JSON, duplicate IDs, missing or extra trials, invalid references, invented quotes, blank reasons, mismatched packet/manifest/dataset/rubric digests, and a changed source snapshot. Fail closed with a readable error and nonzero exit. Do not silently score a subset as a full run.

## Report semantics

Map judgments back to stable candidate IDs before comparison. Opposite winners or any unequal mapped verdicts are `inconsistent`, never silently a tie. Two `tie` judgments are a tie. Two `abstain` judgments are an abstention, never a successful substantive decision.

Report exact denominators: trials, cases, consistent/inconsistent cases, consistent substantive cases (`a`, `b`, `tie`), abstentions, contract-key agreements / all contract cases, agreements / substantive consistent contract cases (null if denominator zero), and unresolved-case abstentions separately. Stratify by family, profile, and key status. Do not merge hypothesis agreement into contract agreement. Missing results fail validation; abstaining everywhere must yield zero substantive coverage. No aggregate language-quality score, calibrated confidence, statistical generalization, or generation-quality claim follows from this small authored diagnostic set.

CLI target (Python standard library, no model/network dependency):

```sh
python3 -m evaluation.harness validate
python3 -m evaluation.harness packet --seed 17 --out /tmp/csf-run
python3 -m evaluation.harness report --run /tmp/csf-run --judgments /tmp/csf-judgments.jsonl --out /tmp/csf-report.json
python3 -m unittest discover -s tests -v
```

Reports also record the report-time harness SHA-256 and Python implementation/version. This identifies the aggregation implementation; it is not a record of model-provider configuration. Preserve a separate run note for evaluator identity, authorized input scope, execution method, and blinding limitations.
