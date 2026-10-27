# Agentic RFP Evaluation Desk

A Streamlit procurement evaluation workspace that extracts proposal text from PDF, requests criterion-level JSON assessments, normalizes malformed results, calculates peer metrics in Python, and persists completed runs to SQLite.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/generate_sample_pdfs.py
streamlit run app.py
```

Upload the four fictional PDFs in `samples/` for a first run. Without an API key the app uses a clearly labelled local keyword-based demo scorer; configure an LLM for content assessment. Copy `.env.example` to `.env` and set the values in your shell or Streamlit secrets. The app reads `OPENAI_API_KEY`, optional `OPENAI_BASE_URL`, and `OPENAI_MODEL`. It uses the OpenAI-compatible Chat Completions JSON response format.

## Architecture

- `app.py`: Streamlit criteria configuration, PDF upload, metadata input, leaderboard, scorecards, and JSON download.
- `rfp_eval/documents.py`: PDF text extraction with PyMuPDF.
- `rfp_eval/llm.py`: Dynamic criteria prompt and JSON-capable LLM adapter; offline demo fallback.
- `rfp_eval/evaluation.py`: schema normalization, scoring, peer metrics, and stable tie-break ordering.
- `rfp_eval/database.py`: SQLite criteria, run, and complete supplier-result persistence.
- `rfp_eval/orchestrator.py`: runs the tools in sequence and persists the evaluated batch.

## Scoring and assumptions

Absolute score is the sum of `(criterion score / criterion maximum) × criterion weight`, so the result is on a 0-100 scale when active weights total 100%. Each criterion benchmark is the highest supplier score observed. Gap is `supplier score - benchmark`. Relative performance is `(supplier score / benchmark) × 100`; when a criterion benchmark is zero, every supplier receives 100% relative parity for that criterion. PPI is the weighted average of criterion relative percentages.

Ranking is determined only by Python, in this order: higher PPI, earlier ISO submission date, higher historical experience rating, then supplier name ascending (case-insensitive). Missing or invalid LLM scores become zero; out-of-range finite scores are clipped to the configured maximum and warnings are retained. Evidence is displayed as returned and is not independently verified.

The demo scorer is a local keyword-based smoke-test aid, not an LLM and not suitable for purchasing decisions. For reproducibility, formula outputs and ranking are deterministic once scorecards are validated. LLM outputs themselves may vary by provider. The database defaults to `rfp_evaluation.db`; on Streamlit Community Cloud the filesystem may be ephemeral, so use an external persistent database for durable production records.

## Database and tests

The database is initialized automatically with five active sample criteria. Edit or deactivate criteria in the app; active weights must total exactly 100%. Run tests with:

```powershell
python -m pytest -q
```

Regenerate the artificial three-page proposals with `python scripts/generate_sample_pdfs.py`. Generate the sample JSON export with `python scripts/create_sample_run.py` after generating the PDFs.

## Deploy to Streamlit Community Cloud

Push this repository to GitHub, choose `app.py` as the app entry point in Streamlit Community Cloud, and add `OPENAI_API_KEY` (plus any optional model/base URL overrides) in the app's Secrets settings. Deploying and obtaining a public URL requires a GitHub repository and Streamlit Community Cloud account; those external account actions cannot be completed from this workspace. Treat cloud-local SQLite as temporary.

## Demonstration outline

1. Upload the four sample PDFs and complete their metadata; run the batch and inspect the leaderboard and evidence.
2. Download the complete run JSON or open `Previous run` to inspect the persisted result.
3. For a validation case, call `validate_scorecard` with a malformed payload or a score above its maximum; the tests verify zero-filling and clipping warnings.