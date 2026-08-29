from __future__ import annotations
from dataclasses import asdict
from .report import build_risk_report

def critical_items(report: dict) -> list[dict]:
    return [item for item in report.get("items", []) if item.get("level") == "critical"]

def audit_summary(report: dict) -> dict:
    items=report.get("items", [])
    return {
        "decision": "BLOCK" if critical_items(report) else "REVIEW" if any(i.get("level") == "high" for i in items) else "PASS",
        "critical_count": len(critical_items(report)),
        "high_count": sum(i.get("level") == "high" for i in items),
        "total": len(items),
    }
