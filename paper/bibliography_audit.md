# Bibliography Metadata Audit

Audit status: 2026-08-11

## Scope

The current bibliography contains 17 references covering:

- combinatorial interaction testing;
- minimal failure-causing schemas;
- adaptive failure characterization;
- masking effects;
- multiple-fault localization;
- pending schemas;
- statistical and probabilistic localization;
- delta debugging;
- error-locating arrays;
- recent faulty-interaction localization;
- tool-augmented language-model reliability.

## Automated Checks

The artifact verifies:

- exactly 17 expected bibliography entries;
- expected citation keys;
- DOI values;
- DOI uniqueness;
- required title/author/year metadata;
- presence of journal or proceedings metadata;
- manuscript citation resolution;
- duplicate titles;
- unused references.

Run:

    uv run python experiments/bibliography_audit.py

## Metadata Sources

Metadata was checked preferentially against publisher,
conference, institutional, or author publication records.

Key authoritative sources included:

- NIST publication records;
- IEEE publication metadata;
- ACM publication metadata where available;
- Springer Nature;
- SIAM;
- ACL Anthology;
- institutional publication records;
- official author publication lists.

## 2026 Reference

The reference:

    Complete, Sound, and Scalable Identification of
    Minimal Failure-Causing Schema

is a 2026 ACM Transactions on Software Engineering and
Methodology publication with DOI:

    10.1145/3811916

At the time of this audit, the stable metadata available for the
reference includes authors, title, journal, year, publisher, and DOI.

The bibliography therefore does not fabricate volume, issue, or page
numbers when those values are not included in the currently verified
record.

## Citation Policy

The manuscript should not introduce references whose metadata has not
been checked.

Every new citation added after this audit should include, where
applicable:

- author;
- title;
- venue;
- publication year;
- pages or article number;
- DOI.

Absolute novelty claims must not be inferred merely from this
bibliography audit.
