from __future__ import annotations


def normalize_evidence_reference(source_uri: str, title: str, excerpt: str, availability_status: str = "available") -> dict:
    return {
        "source_uri": source_uri,
        "title": title,
        "excerpt": excerpt,
        "availability_status": availability_status,
    }
