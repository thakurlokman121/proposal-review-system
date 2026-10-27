from __future__ import annotations

import json
from datetime import date

import pandas as pd
import streamlit as st

from rfp_eval.database import get_active_criteria, get_latest_run, initialize_database, save_criteria
from rfp_eval.documents import extract_pdf_text
from rfp_eval.orchestrator import evaluate_batch


st.set_page_config(page_title="RFP Evaluation Desk", page_icon="R", layout="wide")
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500;600;700&family=Newsreader:opsz,wght@6..72,500;6..72,600&display=swap');
    :root { --forest:#173b32; --leaf:#b8d94b; --paper:#f5f5ef; --ink:#1d2925; --muted:#64716a; --rule:#d9ded5; }
    html, body, [class*="css"] { font-family:'DM Sans', sans-serif; color:var(--ink); }
    .stApp { background:var(--paper); }
    [data-testid="stSidebar"] { background:#e8ece3; border-right:1px solid var(--rule); }
    [data-testid="stSidebar"] h1 { font-family:'Newsreader', Georgia, serif; color:var(--forest); }
    h1, h2, h3 { font-family:'Newsreader', Georgia, serif !important; color:var(--forest); letter-spacing:0 !important; }
    h1 { font-size:2.55rem !important; }
    .eyebrow { font:500 11px 'DM Mono', monospace; color:#64716a; text-transform:uppercase; letter-spacing:1px; }
    .masthead { padding:4px 0 18px; border-bottom:1px solid var(--rule); margin-bottom:24px; }
    .stButton > button[kind="primary"] { background:var(--forest); color:white; border:0; border-radius:4px; font-weight:600; }
    .stButton > button[kind="primary"]:hover { background:#285b4c; color:white; }
    [data-testid="stMetric"] { background:#fff; padding:16px; border:1px solid var(--rule); border-radius:4px; }
    [data-testid="stMetricLabel"] { color:var(--muted); }
    div[data-testid="stExpander"] { border:1px solid var(--rule); border-radius:4px; background:#fff; }
    .stTabs [data-baseweb="tab-list"] { gap:8px; border-bottom:1px solid var(--rule); }
    .stTabs [data-baseweb="tab"] { padding:10px 16px; }
    .stCaption, [data-testid="stCaptionContainer"] { color:var(--muted); }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def setup_database() -> None:
    initialize_database()


setup_database()
with st.sidebar:
    st.markdown("# RFP Desk")
    st.caption("PROCUREMENT INTELLIGENCE / 01")
    page = st.radio("Workspace", ["Evaluate proposals", "Evaluation criteria", "Previous run"], label_visibility="collapsed")
    st.divider()
    criteria = get_active_criteria()
    st.markdown(f"**{len(criteria)} active criteria**")
    st.caption(f"Combined weight: {sum(item['weight'] for item in criteria):.0f}%")
    st.markdown("---")
    st.caption("LLM mode is selected automatically from environment credentials. Scores, benchmarks and ranking remain deterministic Python calculations.")


def show_results(run: dict) -> None:
    suppliers = run["suppliers"]
    st.markdown('<div class="eyebrow">Completed evaluation / Supplier comparison</div>', unsafe_allow_html=True)
    st.subheader("Final leaderboard")
    leaderboard = pd.DataFrame(
        [
            {
                "Rank": item["final_rank"],
                "Supplier": item["supplier_name"],
                "Absolute score": round(item["absolute_score"], 2),
                "Peer index": f"{item['ppi']:.1f}%",
                "Submitted": item["submission_date"],
                "Experience": f"{item['experience_rating']:.1f} / 5",
            }
            for item in suppliers
        ]
    )
    st.dataframe(leaderboard, use_container_width=True, hide_index=True)
    st.caption(f"Run ID: `{run['rfp_run_id']}` · Ranking: PPI, earlier submission, experience rating, supplier name.")
    modes = sorted({item.get("evaluation_mode", "unknown") for item in suppliers})
    st.caption("Assessment mode: " + ", ".join(modes) + (" · Demo scores are illustrative." if "demo" in modes else ""))
    for item in suppliers:
        with st.expander(f"#{item['final_rank']}  {item['supplier_name']}  ·  {item['absolute_score']:.2f} points  ·  PPI {item['ppi']:.1f}%"):
            st.write(item.get("overall_summary") or "No overall summary was returned.")
            score_rows = []
            for score in item["criteria"]:
                score_rows.append(
                    {
                        "Criterion": score["criterion_name"],
                        "Score": f"{score['score']:.1f} / {score['max_score']:.1f}",
                        "Weight": f"{score['weight']:.0f}%",
                        "Benchmark": f"{score['benchmark']:.1f}",
                        "Gap": f"{score['gap']:+.1f}",
                        "Relative": f"{score['relative_pct']:.1f}%",
                    }
                )
            st.dataframe(pd.DataFrame(score_rows), use_container_width=True, hide_index=True)
            for score in item["criteria"]:
                st.markdown(f"**{score['criterion_name']}** · {score['score']:.1f}/{score['max_score']:.1f}")
                st.write(score["justification"])
                st.caption(f"Evidence: {score['evidence'] or 'No supporting evidence found.'}")
            if item["warnings"]:
                st.warning("Validation notes: " + "; ".join(item["warnings"]))
            if item.get("risks"):
                st.info("Proposal risks: " + "; ".join(item["risks"]))
    st.download_button(
        "Download complete run as JSON",
        data=json.dumps(run, indent=2, ensure_ascii=False),
        file_name=f"rfp-run-{run['rfp_run_id']}.json",
        mime="application/json",
        type="primary",
    )


if page == "Evaluate proposals":
    st.markdown('<div class="masthead"><div class="eyebrow">Supplier due diligence / Evaluation workspace</div><h1>Proposal evaluation</h1><div>Assess each submission against the active scorecard. Python computes peer results and final rank.</div></div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("#### Active scorecard")
        st.dataframe(
            pd.DataFrame([{"Criterion": c["name"], "Weight": f"{c['weight']:.0f}%", "Maximum": c["max_score"], "What to inspect": c["description"]} for c in criteria]),
            use_container_width=True,
            hide_index=True,
        )
    st.markdown("### Supplier submissions")
    uploads = st.file_uploader("Upload supplier RFP PDFs", type=["pdf"], accept_multiple_files=True, help="One PDF per supplier; synthetic sample proposals are in the samples folder.")
    submissions = []
    if uploads:
        with st.form("submission_metadata"):
            st.caption("Enter the metadata used in the ranking tie-break sequence.")
            for index, uploaded in enumerate(uploads):
                default_name = uploaded.name.rsplit(".", 1)[0].replace("_", " ").replace("-", " ").title()
                with st.expander(uploaded.name, expanded=True):
                    col_a, col_b, col_c = st.columns([2, 1, 1])
                    name = col_a.text_input("Supplier name", value=default_name, key=f"supplier_name_{index}")
                    submitted = col_b.date_input("Submission date", value=date.today(), key=f"submission_date_{index}")
                    experience = col_c.number_input("Experience rating (0-5)", min_value=0.0, max_value=5.0, value=3.0, step=0.5, key=f"experience_{index}")
                    submissions.append({"supplier_name": name.strip(), "submission_date": submitted.isoformat(), "experience_rating": experience, "filename": uploaded.name, "pdf_bytes": uploaded.getvalue()})
            evaluate_clicked = st.form_submit_button("Evaluate supplier batch", type="primary", use_container_width=True)
        if evaluate_clicked:
            if len({s["supplier_name"].casefold() for s in submissions}) != len(submissions) or any(not s["supplier_name"] for s in submissions):
                st.error("Supplier names must be present and unique within a batch.")
            else:
                try:
                    with st.spinner("Extracting proposals, validating scorecards and calculating peer results..."):
                        documents = []
                        for supplier in submissions:
                            text = extract_pdf_text(supplier["pdf_bytes"])
                            documents.append({**supplier, "document_text": text})
                        result = evaluate_batch(documents, criteria)
                    st.session_state["latest_run"] = result
                    st.success(f"Evaluation complete. Run ID: {result['rfp_run_id']}")
                except Exception as exc:
                    st.error(f"The batch could not be completed: {exc}")
    latest = st.session_state.get("latest_run")
    if latest:
        show_results(latest)
elif page == "Evaluation criteria":
    st.markdown('<div class="masthead"><div class="eyebrow">Configuration / Business rules</div><h1>Evaluation criteria</h1><div>Active weights must total exactly 100%. Changes are stored in SQLite and used on the next run.</div></div>', unsafe_allow_html=True)
    all_criteria = get_active_criteria(include_inactive=True)
    edited = pd.DataFrame(all_criteria)
    edited = edited[["criterion_id", "name", "description", "weight", "max_score", "is_active"]]
    edited.columns = ["ID", "Criterion", "Description", "Weight", "Maximum score", "Active"]
    changed = st.data_editor(edited, use_container_width=True, hide_index=True, num_rows="dynamic", column_config={"ID": None, "Weight": st.column_config.NumberColumn(min_value=0, max_value=100, step=1), "Maximum score": st.column_config.NumberColumn(min_value=1, step=1), "Active": st.column_config.CheckboxColumn()})
    if st.button("Save criteria", type="primary"):
        active_weight = sum(float(row["Weight"]) for _, row in changed.iterrows() if bool(row["Active"]))
        if round(active_weight, 6) != 100:
            st.error(f"Active criteria weights must total 100%; current total is {active_weight:g}%.")
        else:
            try:
                save_criteria(changed.to_dict("records"))
                st.success("Criteria saved.")
                st.rerun()
            except ValueError as exc:
                st.error(str(exc))
elif page == "Previous run":
    st.markdown('<div class="masthead"><div class="eyebrow">Run history / SQLite</div><h1>Previous evaluation</h1><div>The most recently completed batch persisted in the local evaluation database.</div></div>', unsafe_allow_html=True)
    saved = get_latest_run()
    if saved:
        show_results(saved)
    else:
        st.info("No completed runs yet. Evaluate a supplier batch to create the first run.")