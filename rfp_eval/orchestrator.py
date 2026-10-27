from __future__ import annotations

from rfp_eval.database import persist_run
from rfp_eval.evaluation import calculate_peer_results, validate_scorecard
from rfp_eval.llm import evaluate_with_llm


def evaluate_batch(suppliers: list[dict], criteria: list[dict]) -> dict:
    if not suppliers:
        raise ValueError("Add at least one supplier proposal.")
    if not criteria:
        raise ValueError("No active evaluation criteria are configured.")
    weight_total = sum(float(item["weight"]) for item in criteria)
    if round(weight_total, 6) != 100:
        raise ValueError(f"Active criteria weights must total 100%; current total is {weight_total:g}%.")
    scorecards = []
    for supplier in suppliers:
        raw, mode = evaluate_with_llm(supplier["supplier_name"], supplier["document_text"], criteria)
        scorecard = validate_scorecard(raw, criteria, supplier["supplier_name"])
        scorecard["evaluation_mode"] = mode
        scorecards.append(scorecard)
    results = calculate_peer_results(scorecards, suppliers)
    return persist_run(results)