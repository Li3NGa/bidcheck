from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class DocumentPage:
    page_number: int
    text: str
    blocks: list[dict[str, Any]] = field(default_factory=list)

@dataclass(frozen=True)
class ParsedDocument:
    source_name: str
    source_type: str
    pages: list[DocumentPage]
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def text(self) -> str:
        return "\n\n".join(page.text for page in self.pages)

class DocumentParser:
    def parse(self, path: str) -> ParsedDocument:
        raise NotImplementedError
