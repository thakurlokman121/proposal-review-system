from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from rfp_eval.evaluation import calculate_peer_results, validate_scorecard
from rfp_eval.llm import evaluate_demo
from generate_sample_pdfs import PROPOSALS


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    criteria = [
        {"criterion_id": 1, "name": "Technical Capability", "description": "Architecture and technical fit", "weight": 30, "max_score": 10},
        {"criterion_id": 2, "name": "Implementation Plan", "description": "Delivery plan and milestones", "weight": 20, "max_score": 10},
        {"criterion_id": 3, "name": "Commercial Value", "description": "Price and assumptions", "weight": 20, "max_score": 10},
        {"criterion_id": 4, "name": "Security & Compliance", "description": "Controls and assurance", "weight": 20, "max_score": 10},
        {"criterion_id": 5, "name": "Support & Experience", "description": "Support and track record", "weight": 10, "max_score": 10},
    ]
    suppliers = []
    scorecards = []
    for name, pages in PROPOSALS.items():
        document_text = "\n\n".join(pages)
        suppliers.append(
            {
                "supplier_name": name,
                "submission_date": date(2026, 10, 18).isoformat(),
                "experience_rating": {"Apex Systems": 3.5, "BrightPath Tech": 1.5, "NexaWorks": 4.0, "Orbit Digital": 5.0}[name],
                "filename": f"{name.replace(' ', '_')}.pdf",
            }
        )
        scorecards.append(validate_scorecard(evaluate_demo(name, document_text, criteria), criteria, name))
    results = calculate_peer_results(scorecards, suppliers)
    result = {
        "rfp_run_id": "SYNTHETIC-SAMPLE-RUN",
        "created_at": "2026-10-18T00:00:00+00:00",
        "status": "sample",
        "suppliers": results,
    }
    result["notes"] = "Generated with the local demo scorer; scores are illustrative, not procurement advice."
    (root / "samples" / "sample_run.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("Created samples/sample_run.json")


if __name__ == "__main__":
    main()