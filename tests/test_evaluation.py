from rfp_eval.evaluation import calculate_peer_results, validate_scorecard


CRITERIA = [
    {"criterion_id": 1, "name": "Technical", "weight": 60, "max_score": 10},
    {"criterion_id": 2, "name": "Plan", "weight": 40, "max_score": 10},
]


def test_validation_fills_missing_and_clips_out_of_range_scores():
    result = validate_scorecard(
        {"criteria": [{"criterion_id": 1, "score": 14, "evidence": "API architecture"}]},
        CRITERIA,
        "Alpha",
    )
    assert [item["score"] for item in result["criteria"]] == [10, 0]
    assert any("clipped" in warning for warning in result["warnings"])
    assert any("Missing result" in warning for warning in result["warnings"])


def test_peer_math_and_tie_break_order_are_deterministic():
    cards = [
        validate_scorecard({"criteria": [{"criterion_id": 1, "score": 8}, {"criterion_id": 2, "score": 8}]}, CRITERIA, "Beta"),
        validate_scorecard({"criteria": [{"criterion_id": 1, "score": 8}, {"criterion_id": 2, "score": 8}]}, CRITERIA, "Alpha"),
        validate_scorecard({"criteria": [{"criterion_id": 1, "score": 10}, {"criterion_id": 2, "score": 10}]}, CRITERIA, "Leader"),
    ]
    suppliers = [
        {"supplier_name": "Beta", "submission_date": "2026-01-02", "experience_rating": 5},
        {"supplier_name": "Alpha", "submission_date": "2026-01-02", "experience_rating": 2},
        {"supplier_name": "Leader", "submission_date": "2026-01-03", "experience_rating": 1},
    ]
    ranked = calculate_peer_results(cards, suppliers)
    assert [item["supplier_name"] for item in ranked] == ["Leader", "Beta", "Alpha"]
    assert ranked[1]["absolute_score"] == 80
    assert ranked[1]["ppi"] == 80
    assert ranked[1]["criteria"][0]["gap"] == -2


def test_zero_benchmarks_have_safe_relative_value():
    cards = [validate_scorecard({"criteria": []}, CRITERIA, "Zero")]
    ranked = calculate_peer_results(cards, [{"supplier_name": "Zero", "submission_date": "2026-01-01", "experience_rating": 1}])
    assert all(item["relative_pct"] == 100 for item in ranked[0]["criteria"])