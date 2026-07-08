from collections import Counter

from fastapi import APIRouter
from fastapi.routing import APIRoute


def build_endpoint_summary(router: APIRouter) -> str:
    """Auto-generowana tabelka "ile endpointów per tag", liczona przy starcie
    (wzorzec: docs/ARCHITEKTURA.md 7.8)."""
    counts: Counter[str] = Counter()

    for route in router.routes:
        if not isinstance(route, APIRoute):
            continue
        tags = route.tags or ["(bez taga)"]
        for tag in tags:
            counts[str(tag)] += 1

    total = sum(counts.values())

    lines = [
        f"**Endpointy: {total}**",
        "",
        "| Tag | Liczba endpointów |",
        "|-----|-------------------|",
    ]
    for tag, count in sorted(counts.items()):
        lines.append(f"| {tag} | {count} |")
    lines.append("")

    return "\n".join(lines)
