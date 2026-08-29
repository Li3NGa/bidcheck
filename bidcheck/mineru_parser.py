from __future__ import annotations
import json, subprocess
from pathlib import Path
from typing import Any
from .document import DocumentPage, DocumentParser, ParsedDocument

class MinerUParser(DocumentParser):
    def __init__(self, command: str = "mineru") -> None:
        self.command = command
    def parse(self, path: str) -> ParsedDocument:
        source = Path(path); output_dir = source.parent / f".{source.stem}_mineru"; output_dir.mkdir(parents=True, exist_ok=True)
        subprocess.run([self.command, "-p", str(source), "-o", str(output_dir)], check=True, capture_output=True, text=True)
        return self._load_output(source, output_dir)
    def _load_output(self, source: Path, output_dir: Path) -> ParsedDocument:
        files = list(output_dir.rglob("*.json"))
        if files:
            pages = self._pages_from_json(json.loads(files[0].read_text(encoding="utf-8")))
            if pages: return ParsedDocument(source.name, source.suffix.lower(), pages, {"parser":"mineru"})
        files = list(output_dir.rglob("*.md"))
        if files: return ParsedDocument(source.name, source.suffix.lower(), [DocumentPage(1, files[0].read_text(encoding="utf-8"))], {"parser":"mineru","fallback":"markdown"})
        raise RuntimeError(f"MinerU produced no readable output for {source}")
    @staticmethod
    def _pages_from_json(data: Any) -> list[DocumentPage]:
        candidates = data.get("pages") or data.get("content_list") or data.get("content") if isinstance(data, dict) else data
        if not isinstance(candidates, list): return []
        pages=[]
        for i,item in enumerate(candidates,1):
            if isinstance(item,dict): pages.append(DocumentPage(int(item.get("page_idx",i-1))+1,str(item.get("text") or item.get("content") or ""),item.get("blocks") or []))
            else: pages.append(DocumentPage(i,str(item)))
        return pages
