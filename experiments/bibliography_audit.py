import re
from pathlib import Path

BIB_PATH = Path("paper/references.bib")

MANUSCRIPT_PATH = Path("paper/manuscript.md")


EXPECTED_DOIS = {
    "kuhn2008beyond": ("10.1109/MITP.2008.54"),
    "nie2011survey": ("10.1145/1883612.1883618"),
    "nie2011mfs": ("10.1145/2000799.2000801"),
    "zhang2011fic": ("10.1145/2001420.2001460"),
    "shakya2012isolating": ("10.1109/ICST.2012.149"),
    "yilmaz2014masking": ("10.1109/TSE.2013.53"),
    "niu2020multiple": ("10.1109/TSE.2018.2844259"),
    "niu2020interleaving": ("10.1109/TSE.2018.2865772"),
    "niu2022pending": ("10.1109/TSE.2021.3113920"),
    "nishiura2024frog": ("10.1007/s11219-024-09677-1"),
    "xie2026nopend": ("10.1145/3811916"),
    "wang2019pfs": ("10.23940/ijpe.19.10.p17.27092717"),
    "ji2023bayesflo": ("10.1109/QRS-C60940.2023.00019"),
    "zeller2002delta": ("10.1109/32.988498"),
    "martinez2009ela": ("10.1137/080730706"),
    "trevino2025failtalms": ("10.18653/v1/2025.naacl-long.149"),
    "sun2024toolsfail": ("10.18653/v1/2024.emnlp-main.790"),
}


def parse_entries(
    text: str,
) -> dict[str, str]:
    pattern = re.compile(
        r"@(?P<type>\w+)"
        r"\{(?P<key>[^,]+),"
        r"(?P<body>.*?)"
        r"\n\}",
        re.DOTALL,
    )

    entries = {}

    for match in pattern.finditer(text):
        key = match.group("key").strip()

        entries[key] = match.group("body")

    return entries


def get_field(
    body: str,
    field: str,
) -> str | None:
    pattern = re.compile(
        rf"^\s*{re.escape(field)}"
        rf"\s*=\s*\{{(.*?)\}}\s*,?\s*$",
        re.MULTILINE,
    )

    match = pattern.search(body)

    if match is None:
        return None

    return match.group(1).strip()


bib_text = BIB_PATH.read_text(encoding="utf-8")

manuscript = MANUSCRIPT_PATH.read_text(encoding="utf-8")

entries = parse_entries(bib_text)


print("=== Entry count ===")

if len(entries) != 17:
    raise RuntimeError(f"Expected 17 bibliography entries, found {len(entries)}")

print("PASS: 17 bibliography entries")


print()
print("=== Expected keys ===")

actual_keys = set(entries)

expected_keys = set(EXPECTED_DOIS)

missing_entries = sorted(expected_keys - actual_keys)

unexpected_entries = sorted(actual_keys - expected_keys)

if missing_entries:
    raise RuntimeError(f"Missing bibliography entries: {missing_entries}")

if unexpected_entries:
    raise RuntimeError(f"Unexpected bibliography entries: {unexpected_entries}")

print("PASS: bibliography key set")


print()
print("=== DOI audit ===")

observed_dois = []

for key in sorted(EXPECTED_DOIS):
    body = entries[key]

    doi = get_field(
        body,
        "doi",
    )

    expected = EXPECTED_DOIS[key]

    if doi is None:
        raise RuntimeError(f"{key}: DOI missing")

    if doi.lower() != expected.lower():
        raise RuntimeError(f"{key}: DOI mismatch: {doi!r} != {expected!r}")

    observed_dois.append(doi.lower())

    print(f"PASS: {key}: {doi}")


if len(observed_dois) != len(set(observed_dois)):
    raise RuntimeError("Duplicate DOI detected")

print("PASS: all DOIs unique")


print()
print("=== Required metadata ===")

for key, body in sorted(entries.items()):
    for field in (
        "author",
        "title",
        "year",
        "doi",
    ):
        value = get_field(
            body,
            field,
        )

        if not value:
            raise RuntimeError(f"{key}: missing {field}")

    if (
        get_field(
            body,
            "journal",
        )
        is None
        and get_field(
            body,
            "booktitle",
        )
        is None
    ):
        raise RuntimeError(f"{key}: neither journal nor booktitle present")

    print(f"PASS: {key}")


print()
print("=== Citation resolution ===")

citation_keys = set(
    re.findall(
        r"@([A-Za-z0-9_-]+)",
        manuscript,
    )
)

missing_citations = sorted(citation_keys - actual_keys)

unused_references = sorted(actual_keys - citation_keys)

if missing_citations:
    raise RuntimeError(f"Unresolved manuscript citations: {missing_citations}")

print("PASS: all manuscript citations resolve")

print(
    "Cited references:",
    len(citation_keys),
)

print(
    "Unused references:",
    unused_references,
)


print()
print("=== Duplicate title audit ===")

titles: dict[
    str,
    str,
] = {}

for key, body in entries.items():
    title = get_field(
        body,
        "title",
    )

    if title is None:
        continue

    normalized = re.sub(
        r"\W+",
        "",
        title.lower(),
    )

    if normalized in titles:
        raise RuntimeError(f"Duplicate title: {key} and {titles[normalized]}")

    titles[normalized] = key

print("PASS: no duplicate titles")


print()
print("BIBLIOGRAPHY AUDIT PASSED")
