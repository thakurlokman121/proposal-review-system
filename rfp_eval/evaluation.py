from __future__ import annotations

import json
import math
from datetime import date
from typing import Any


def validate_scorecard(payload: Any, criteria: list[dict], supplier_name: str) -> dict:
    warnings: list[str] = []
    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except json.JSONDecodeError:
            payload = {}
            warnings.append("LLM response was not valid JSON; all criterion scores defaulted to zero.")
    if not isinstance(payload, dict):
        payload = {}
        warnings.append("Scorecard response was not a JSON object; all criterion scores defaulted to zero.")
    received = payload.get("criteria", [])
    if not isinstance(received, list):
        received = []
        warnings.append("Criteria response was not a list; all criterion scores defaulted to zero.")
    by_id = {}
    for item in received:
        if isinstance(item, dict):
            try:
                by_id[int(item.get("criterion_id"))] = item
            except (TypeError, ValueError):
                warnings.append("Ignored a criterion result with a missing or invalid criterion_id.")
    normalized = []
    for criterion in criteria:
        criterion_id = int(criterion["criterion_id"])
        item = by_id.get(criterion_id)
        if item is None:
            warnings.append(f"Missing result for {criterion['name']}; score defaulted to zero.")
            item = {}
        raw_score = item.get("score", 0)
        try:
            score = float(raw_score)
            if not math.isfinite(score):
                raise ValueError
        except (TypeError, ValueError):
            score = 0.0
            warnings.append(f"Invalid score for {criterion['name']}; score defaulted to zero.")
        max_score = float(criterion["max_score"])
        clipped = min(max(score, 0.0), max_score)
        if clipped != score:
            warnings.append(f"Score for {criterion['name']} was outside its allowed range and was clipped.")
        normalized.append(
            {
                "criterion_id": criterion_id,
                "criterion_name": criterion["name"],
                "score": clipped,
                "max_score": max_score,
                "weight": float(criterion["weight"]),
                "justification": str(item.get("justification", "No justification provided.")).strip() or "No justification provided.",
                "evidence": str(item.get("evidence", "")).strip(),
            }
        )
    risks = payload.get("risks", [])
    if not isinstance(risks, list):
        risks = [str(risks)]
        warnings.append("Risks field was not a list and was normalized.")
    return {
        "supplier_name": supplier_name,
        "criteria": normalized,
        "risks": [str(risk) for risk in risks],
        "overall_summary": str(payload.get("overall_summary", "")).strip(),
        "warnings": warnings,
    }


def calculate_peer_results(scorecards: list[dict], suppliers: list[dict]) -> list[dict]:
    results = []
    for scorecard, supplier in zip(scorecards, suppliers):
        absolute = 0.0
        relative_weight_sum = 0.0
        for item in scorecard["criteria"]:
            benchmark = max(
                (other["score"] for card in scorecards for other in card["criteria"] if other["criterion_id"] == item["criterion_id"]),
                default=0.0,
            )
            item["benchmark"] = benchmark
            item["gap"] = item["score"] - benchmark
            item["relative_pct"] = item["score"] / benchmark * 100 if benchmark else 100.0
            absolute += item["score"] / item["max_score"] * item["weight"]
            relative_weight_sum += item["relative_pct"] * item["weight"]
        scorecard["absolute_score"] = absolute
        scorecard["ppi"] = relative_weight_sum / 100 if relative_weight_sum else 0.0
        scorecard["submission_date"] = supplier["submission_date"]
        scorecard["experience_rating"] = float(supplier["experience_rating"])
        scorecard["filename"] = supplier.get("filename", "")
        scorecard["risks"] = scorecard.get("risks", [])
        results.append(scorecard)
    results.sort(
        key=lambda item: (
            -item["ppi"],
            _date_key(item["submission_date"]),
            -item["experience_rating"],
            item["supplier_name"].casefold(),
        )
    )
    for rank, item in enumerate(results, start=1):
        item["final_rank"] = rank
    return results


def _date_key(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError):
        return date.max