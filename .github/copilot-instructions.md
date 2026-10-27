# RFP Evaluation Desk

- Keep LLM judgement separate from deterministic business rules. LLM code only extracts criterion assessments; validation, weighted scores, benchmarks, PPI, tie-breaks, and ranking belong in Python.
- Active criterion weights must total 100%.
- Run the focused suite with `python -m pytest -q` after changes to scoring or validation.
- Generated supplier proposals are fictional and must remain clearly identified as synthetic.