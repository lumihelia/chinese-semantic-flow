# Semantic review v2: separate meaning from style

An earlier research round exposed an ambiguous reporting axis: the first reviewer used `overall_fidelity=uncertain` for both potential semantic change and unknown style acceptance. That is not evidence that all such candidates have semantic problems. Original v1 reviews remain unchanged; v2 defines the axis explicitly.

## Fields and interpretation

Each review has:

- `fidelity_findings`: possible or definite changes to meaning, source scope, relationships, modality or knowledge. Quote source and output, and explain the concrete issue.
- `style_observations`: observable wording, emphasis, punctuation or rhythm differences. An unjudged stylistic change alone does not establish semantic loss.
- `overall_fidelity`: `violated` if any definite finding; `uncertain` if there are possible findings but no definite ones; otherwise `preserved`.
- `author_acceptability`: `unjudged`. Actual author replies are separate evidence events, not a model inference.

`preserved` means this reviewer identified no qualifying semantic finding. It is not proof of quality, successful completion of every stylistic instruction, factual truth outside the source, or author approval. `uncertain` is not a failure score. Context can support a natural paraphrase even when isolated words differ, and reviewers can disagree.

The packet carries exact target source/candidate text and before/after context. A published article can also have `title`; a narrative can have `source_frame_quote` and `frame_note`. These are known optional context fields, not permission to add condition labels or answer keys.

## Validation

```sh
python3 -m evaluation.review_contract --packet <packet.json> --results <results.jsonl>
```

The checker verifies complete IDs, exact target-text quotation, allowed fields, author-unjudged status and consistent severity/overall labels. It does not determine whether a quoted span actually entails the reviewer's explanation. Failures and missing model outputs must be recorded as execution state, not filled with invented review rows.

A real integration defect was repaired: the first validator required the narrative frame fields and rejected the already-frozen article-title packets. It now accepts the two documented context forms without rewriting either packet or opening the schema to arbitrary metadata. Tests also reject concealed definite findings, style-only semantic uncertainty, fabricated author acceptance and missing candidates.

## Evidence over time

Keep initial and subsequent reviews separate. A later author explanation may support a reading the original source alone left unclear; do not insert that explanation into earlier inputs and pretend the generator or first reviewer saw it. Author permission to use a variant also does not necessarily establish exact semantic equivalence or preference ranking.

Source-only reviews, root reviews, retries and later author evidence are different evidence events; keep them as separate records rather than interchangeable labels.
