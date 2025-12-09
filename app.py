import os
import io
import time
import json

import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px

from pipeline.pipeline_graph import build_pipeline
from utils.data_loader import load_provider_with_pdf  # provider + PDF loader

# Optional PDF export
try:
    from fpdf import FPDF
    HAS_FPDF = True
except ImportError:
    HAS_FPDF = False


# ================================
# ---------- GLOBAL CSS ----------
# ================================

CUSTOM_CSS = """
<style>

html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
}

/* Smooth fade-in animation */
@keyframes fadeIn {
  from {opacity: 0; transform: translateY(10px);}
  to {opacity: 1; transform: translateY(0);}
}

.fade-in {
    animation: fadeIn 0.8s ease-in-out;
}

/* Top navbar hover effect (option_menu tabs) */
div[data-baseweb="tab"] {
    transition: all 0.25s ease;
}
div[data-baseweb="tab"]:hover {
    transform: translateY(-2px);
}

/* Generic card style */
.card {
    height:300px;
    width:600px;
    margin-left:80px;
    border-radius: 20px;
    padding: 20px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 4px 16px rgba(0,0,0,0.25);
    backdrop-filter: blur(10px);
    margin-bottom: 16px;
}
.card2 {
    height:70px;
    width:800px;
    margin-left:80px;
    border-radius: 20px;
    padding: 20px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 4px 16px rgba(0,0,0,0.25);
    backdrop-filter: blur(10px);
    margin-bottom: 16px;
}

/* Neon Buttons */
.neon-button {
  display: flex;
  align-items: center;
  padding: 10px 19px;
  border-radius: 8px;
  background-color: #475569;   /* Slate Gray */
  color: white !important;
  font-weight: 600;
  border: none;
  cursor: pointer;
  text-align: center;
  transition: 0.25s;
}

.neon-button:hover {
  transform: scale(1.04);
  box-shadow: 
      0 0 8px rgba(148, 163, 184, 0.9),
      0 0 18px rgba(148, 163, 184, 0.75),
      0 0 28px rgba(148, 163, 184, 0.55);
}

/* Small tag-style label */
.badge {
    display:inline-block;
    padding:4px 10px;
    border-radius:999px;
    font-size:11px;
    background:rgba(255,255,255,0.08);
    border:1px solid rgba(255,255,255,0.15);
    margin-bottom:6px;
}

/* Team member cards */
.team-card {
    height: 300px;
    width: 300px;
    border-radius: 14px;
    padding: 16px;
    background:#151824;
    text-align:center;
    box-shadow:0 4px 16px rgba(0,0,0,0.4);
}

</style>
"""


# ================================
# ---------- HELPERS ------------
# ================================

@st.cache_resource
def get_pipeline():
    """Cache LangGraph pipeline so it builds only once."""
    return build_pipeline()


@st.cache_data
def load_providers_csv(path: str = "data/providers.csv") -> pd.DataFrame:
    if not os.path.exists(path):
        return pd.DataFrame()
    return pd.read_csv(path)


@st.cache_data
def load_final_results(path: str = "data/final_results.csv") -> pd.DataFrame | None:
    if not os.path.exists(path):
        return None
    return pd.read_csv(path)


def run_pipeline_for_provider(provider: dict):
    """Run the full 4-agent pipeline with a progress animation."""
    app = get_pipeline()

    progress = st.progress(0)
    status = st.empty()

    status.write("🚀 Starting Data Validation Agent...")
    progress.progress(25)
    time.sleep(0.15)

    result = app.invoke({"provider": provider})

    status.write("📚 Running Information Enrichment Agent...")
    progress.progress(50)
    time.sleep(0.15)

    status.write("🛡️ Running Quality Assurance Agent...")
    progress.progress(75)
    time.sleep(0.15)

    status.write("📂 Finalizing Directory Management Agent...")
    progress.progress(100)
    time.sleep(0.1)

    status.empty()
    progress.empty()
    return result


def make_pdf(summary: dict) -> bytes:
    """Create simple PDF summary and return as bytes."""
    if not HAS_FPDF:
        return b""

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Provider Summary Report", ln=True)
    pdf.ln(6)

    pdf.set_font("Arial", size=11)
    for k, v in summary.items():
        pdf.multi_cell(0, 8, f"{k}: {v}")

    pdf_output = pdf.output(dest="S").encode("latin-1")
    return pdf_output


# ================================
# ---------- HOME PAGE ----------
# ================================

def render_home():
    st.markdown(
        "<h1 class='fade-in' style='text-align:center;'> Provider Data Validation & Directory Management</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<h4 class='fade-in' style='text-align:center;color:#424242;'>Agentic AI pipeline for healthcare payers - EY Techathon Challenge VI</h4>",
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            """
            <div class="card fade-in">
                <div class="badge">Multi-Agent Automation</div>
                <h3> What this system does</h3>
                <p>
                    Our solution automates provider directory validation using a <b>4-agent AI workflow</b>:
                    <br>✔ Validates phone, address & specialty (Google Maps + NPI Registry)
                    <br>✔ Enriches profiles with education, board certification & affiliations
                    <br>✔ Computes confidence scores & risk levels
                    <br>✔ Generates final directory entries ready for web / mobile / PDF
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            """
            <div class="card fade-in" style="font-size:20px;">
                <div class="badge">Impact</div>
                <h3> &nbsp;Target Outcomes</h3>
                    <h6> &nbsp; Reduce manual validation time by <b>70%+ </h6>
                    <h6> &nbsp; Raise provider contact accuracy to <b>90%+</h6>
                    <h6> &nbsp; Build audit-ready QA reports with risk flags </h6>
                    <h6> &nbsp; Provide a reusable, modular pipeline for payers </h6>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<h3 class='fade-in'> Project Resources</h3>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    ppt_path = "assets/EY_Projeect_Case Study.pdf"
    srf_path = "assets/EY_Projeect_SRS.pdf"
    cs_path = "https://shorturl.at/pRUj5"
    extra_path = "assets/extra_doc.pdf"

    def view_button(label, path):
        return f"""<a href="{path}" target="_blank" class="view-button">{label}</a>"""

    with col1:
        if os.path.exists(ppt_path):
            st.markdown(view_button("📊 View PPT", ppt_path), unsafe_allow_html=True)
        else:
            st.markdown("<button class='neon-button'>📊 PPT Slides (add file)</button>",
                        unsafe_allow_html=True)

    with col2:
        if os.path.exists(srf_path):
            st.markdown(view_button("📘 View SRS", srf_path), unsafe_allow_html=True)
        else:
            st.markdown("<button class='neon-button'>📘 SRF Document (add file)</button>",
                        unsafe_allow_html=True)

    with col3:
        if os.path.exists(cs_path):
            st.markdown(view_button("📑 View Case Study", cs_path), unsafe_allow_html=True)
        else:
            st.markdown("<button class='neon-button'>📑 Case Study (add file)</button>",
                        unsafe_allow_html=True)

    with col4:
        if os.path.exists(extra_path):
            st.markdown(view_button("📁 View Extra Material", extra_path), unsafe_allow_html=True)
        else:
            st.markdown("<button class='neon-button'> Extra Material (add file)</button>",
                        unsafe_allow_html=True)

    st.markdown("<br><h3> Architecture at a Glance</h3>", unsafe_allow_html=True)

    with st.container():
        col1, col2 = st.columns([1, 1])

        with col1:
            st.write("""
            **Pipeline Flow:**

            1️⃣ **Input Layer** – CSV provider list + scanned PDFs  
            2️⃣ **Agent 1 – Data Validation** (Google Maps API + NPI Registry)  
            3️⃣ **Agent 2 – Information Enrichment** (education, board certs, affiliations)  
            4️⃣ **Agent 3 – Quality Assurance** (confidence scoring, discrepancies, risk)  
            5️⃣ **Agent 4 – Directory Management** (final directory row + reports & exports)
            """)

        with col2:
            if os.path.exists("assets/arch.jpg"):
                st.image("assets/arch.jpg", width=600)


# ================================
# ---------- AGENTS PAGE ---------
# ================================

def render_agents():
    st.markdown("##  Agent Execution Studio")

    # Sidebar agent selection


    with st.sidebar:
        if os.path.exists("assets/semantic_coders_logo.png"):
            st.image("assets/semantic_coders_logo.png", width=200)
        
        st.markdown("### Our Agents")
        agent_choice = option_menu(
            None,
            [
                "Data Validation Agent",
                "Information Enrichment Agent",
                "Quality Assurance Agent",
                "Directory Management Agent",
                "Batch Processing",
            ],
            icons=["check2-circle", "journal-text", "shield-check", "folder-check", "lightning-charge"],
            menu_icon="people-fill",
            default_index=0,
            orientation="vertical",
        )

    # Handle Batch Processing separately
    if agent_choice == "Batch Processing":
        render_batch_processing()
        return

    # Single provider processing UI
    st.markdown("###  Provider Input")

    df_providers = load_providers_csv()
    default_name = default_address = default_phone = default_specialty = ""

    if not df_providers.empty:
        use_sample = st.checkbox("Use provider from dataset", value=True)
        if use_sample:
            sample_name = st.selectbox(
                "Choose provider from CSV",
                df_providers["name"].tolist(),
            )
            row = df_providers[df_providers["name"] == sample_name].iloc[0]
            default_name = row["name"]
            default_address = row["address"]
            default_phone = row["phone"]
            default_specialty = row["specialty"]

    name = st.text_input("Name", value=default_name)
    address = st.text_input("Address", value=default_address)
    phone = st.text_input("Phone", value=default_phone)
    specialty = st.text_input("Specialty", value=default_specialty)

    run_btn = st.button("🚀 Run Full 4-Agent Pipeline")

    if run_btn and name.strip():
        provider = {
            "name": name,
            "address": address,
            "phone": phone,
            "specialty": specialty,
        }
        result = run_pipeline_for_provider(provider)
        st.session_state["last_result"] = result

    result = st.session_state.get("last_result")

    if result is None:
        st.info("Run the pipeline to inspect agent outputs.")
        return

    st.markdown("---")
    st.markdown(f"### ⚙ Output • <code>{agent_choice}</code>", unsafe_allow_html=True)

    if agent_choice == "Data Validation Agent":
        st.markdown(
            "<div class='card2'><b>Role:</b> Validate phone, address & specialty using Google & NPI.</div>",
            unsafe_allow_html=True,
        )
        st.json(result.get("validated_data", {}))

    elif agent_choice == "Information Enrichment Agent":
        st.markdown(
            "<div class='card2'><b>Role:</b> Enrich profile with education, certifications & affiliations.</div>",
            unsafe_allow_html=True,
        )
        st.json(result.get("enriched_data", {}))

    elif agent_choice == "Quality Assurance Agent":
        qa = result.get("quality_data", {})
        st.markdown(
            "<div class='card2'><b>Role:</b> Compute confidence scores, flag discrepancies & risk.</div>",
            unsafe_allow_html=True,
        )

        scores = qa.get("confidence_scores", {})
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("☎ Phone", f"{scores.get('phone', 0):.1f}")
        with c2:
            st.metric("📍 Address", f"{scores.get('address', 0):.1f}")
        with c3:
            st.metric("🩺 Specialty", f"{scores.get('specialty', 0):.1f}")
        with c4:
            st.metric("⭐ Overall", f"{scores.get('overall', 0):.1f}")
        st.json(qa)

    else:  # Directory Management Agent
        final_profile = result.get("final_profile", {})
        summary = result.get("summary_report", {})

        st.markdown(
            "<div class='card2'><b>Role:</b> Produce final directory entry and summary report, ready for export.</div>",
            unsafe_allow_html=True,
        )

        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Overall Confidence", summary.get("Overall Confidence", "NA"))
        with c2:
            st.metric("Risk Level", summary.get("Risk Level", "NA"))
        with c3:
            st.metric("Manual Review", summary.get("Needs Manual Review", "NA"))

        st.markdown("#### Final Directory Row")
        st.json(final_profile)

        st.markdown("#### Summary Report")
        st.json(summary)

        # Download options
        st.markdown("##### 📥 Download Options")

        # JSON summary
        json_bytes = json.dumps(summary, indent=2).encode("utf-8")
        st.download_button(
            "🧾 Download Summary (JSON)",
            data=json_bytes,
            file_name="provider_summary.json",
            mime="application/json",
        )

        # CSV row
        csv_df = pd.DataFrame([final_profile])
        csv_bytes = csv_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📊 Download Directory Row (CSV)",
            data=csv_bytes,
            file_name="provider_directory_row.csv",
            mime="text/csv",
        )

        # PDF summary
        if HAS_FPDF:
            pdf_bytes = make_pdf(summary)
            st.download_button(
                "📄 Download Summary (PDF)",
                data=pdf_bytes,
                file_name="provider_summary.pdf",
                mime="application/pdf",
            )
        else:
            st.caption("Install `fpdf` to enable PDF export: `pip install fpdf`")

        


# ================================
# ------- BATCH PROCESSING -------
# ================================

def render_batch_processing():
    """Render the batch processing interface."""
    st.markdown("## ⚡ Batch Processing")

    st.markdown(
        "<div class='card2'><b>Mode:</b> Run the 4-agent pipeline across multiple providers "
        "to simulate daily directory cleansing.</div>",
        unsafe_allow_html=True,
    )

    df = load_providers_csv()
    if df.empty:
        st.warning("No `data/providers.csv` found. Please add providers.csv first.")
        return

    st.markdown("#### 🧪 Batch Configuration")

    col_info, col_controls = st.columns([2, 1])

    with col_info:
        st.info(f"📊 Total providers available: **{len(df)}**")
        st.caption(
            "Select how many providers you want to process in this batch run. "
            "Each provider is passed through all 4 agents."
        )

    with col_controls:
        max_n = len(df)
        batch_size = st.number_input(
            "Providers to process",
            min_value=1,
            max_value=max_n,
            value=min(50, max_n),
            step=10,
            key="batch_size_input"
        )

    st.markdown("---")

    col_preview, col_action = st.columns([3, 1])

    with col_preview:
        with st.expander("👀 Preview Batch Data", expanded=False):
            st.dataframe(df.head(batch_size), use_container_width=True)

    with col_action:
        run_batch_btn = st.button(
            "🚀 Start Batch Processing",
            type="primary",
            use_container_width=True,
            key="run_batch_button"
        )

    # RUN BATCH
    if run_batch_btn:

        st.markdown("---")
        st.markdown("### 📊 Processing Status")

        app = get_pipeline()
        results = []

        progress_bar = st.progress(0)
        status_text = st.empty()

        metrics_cols = st.columns(4)
        metric_processed = metrics_cols[0].empty()
        metric_success = metrics_cols[1].empty()
        metric_warnings = metrics_cols[2].empty()
        metric_errors = metrics_cols[3].empty()

        log_expander = st.expander("📋 Processing Log", expanded=True)

        success_count = 0
        warning_count = 0
        error_count = 0

        for i in range(batch_size):
            try:
                row = df.iloc[i]
                name_for_log = row["name"] if "name" in row else "Unknown"

                status_text.info(
                    f"🔄 Processing provider {i+1}/{batch_size}: **{name_for_log}**"
                )

                # ✅ Correct: pass full row object to loader
                provider = load_provider_with_pdf(row)

                result = app.invoke({"provider": provider})
                final_profile = result.get("final_profile", {})

                final_profile["provider_id"] = int(row.get("id", i + 1))
                if "name" not in final_profile and "name" in provider:
                    final_profile["name"] = provider["name"]

                results.append(final_profile)

                risk = final_profile.get("risk_level", "UNKNOWN")

                if risk == "HIGH":
                    warning_count += 1
                else:
                    success_count += 1

                with log_expander:
                    st.success(f"✅ {i+1}. {name_for_log} — Risk: {risk}")

            except Exception as e:
                error_count += 1
                with log_expander:
                    st.error(f"❌ {i+1}. {row.get('name','Unknown')} — Error: {str(e)}")

            progress = (i + 1) / batch_size
            progress_bar.progress(progress)

            metric_processed.metric("Processed", f"{i+1}/{batch_size}")
            metric_success.metric("Success", success_count)
            metric_warnings.metric("High Risk", warning_count)
            metric_errors.metric("Errors", error_count)

        progress_bar.empty()
        status_text.empty()

        if results:
            out_df = pd.DataFrame(results)
            os.makedirs("data", exist_ok=True)
            out_path = "data/final_results.csv"
            out_df.to_csv(out_path, index=False)

            st.success(f"✅ Batch processing completed! Results saved to `{out_path}`")

            st.markdown("### 📈 Batch Summary")
            c1, c2, c3, c4 = st.columns(4)

            with c1:
                st.metric("Total Processed", len(results))

            with c2:
                if "confidence_overall" in out_df.columns:
                    avg_conf = out_df["confidence_overall"].astype(float).mean()
                    st.metric("Avg Confidence", f"{avg_conf:.1f}")

            with c3:
                if "risk_level" in out_df.columns:
                    st.metric("High Risk", (out_df["risk_level"] == "HIGH").sum())

            with c4:
                if len(results) > 0:
                    sr = (success_count / len(results)) * 100
                    st.metric("Success Rate", f"{sr:.1f}%")

            st.markdown("### 📋 Results Preview")
            st.dataframe(out_df.head(20), use_container_width=True)

            st.markdown("### 📥 Download Results")

            col_d1, col_d2 = st.columns(2)

            with col_d1:
                st.download_button(
                    "⬇ Download CSV",
                    out_df.to_csv(index=False).encode("utf-8"),
                    file_name="batch_results.csv",
                    mime="text/csv",
                    use_container_width=True,
                )

            with col_d2:
                st.download_button(
                    "⬇ Download JSON",
                    json.dumps(out_df.to_dict(orient="records"), indent=2).encode("utf-8"),
                    file_name="batch_results.json",
                    mime="application/json",
                    use_container_width=True,
                )

            # Clear cache for dashboard
            if hasattr(load_final_results, "clear"):
                load_final_results.clear()

        else:
            st.error("❌ No results generated. Check logs for details.")


# ================================
# ----- GENERATED OUTPUT PAGE ----
# ================================

def compute_priority(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute a priority score for each provider based on risk level and confidence.
    Higher priority = needs more urgent attention.
    """
    df = df.copy()

    if df.empty:
        df["priority_score"] = []
        df["priority_category"] = []
        return df

    df["priority_score"] = 0.0

    # Risk level scoring
    if "risk_level" in df.columns:
        risk_map = {"HIGH": 100, "MEDIUM": 50, "LOW": 10}
        df["priority_score"] += df["risk_level"].map(risk_map).fillna(0)

    # Confidence scoring (lower confidence = higher priority)
    if "confidence_overall" in df.columns:
        df["confidence_overall"] = pd.to_numeric(df["confidence_overall"], errors="coerce").fillna(0)
        df["priority_score"] += (100 - df["confidence_overall"])

    # Manual review flag
    if "needs_manual_review" in df.columns:
        df["priority_score"] += df["needs_manual_review"].apply(
            lambda x: 50 if str(x).strip().upper() in {"YES", "Y", "TRUE"} else 0
        )

    # Normalize
    max_val = df["priority_score"].max()
    if max_val > 0:
        df["priority_score"] = (df["priority_score"] / max_val) * 100

    df["priority_category"] = pd.cut(
        df["priority_score"],
        bins=[0, 33, 66, 100],
        labels=["LOW", "MEDIUM", "HIGH"],
        include_lowest=True,
    )

    return df


def render_generated_output():
    st.markdown("##  Generated Output – Batch Level")

    fr = load_final_results()
    if fr is None or fr.empty:
        st.warning("No `data/final_results.csv` found. Run batch processing first.")
        return

    # Ensure numeric columns
    if "confidence_overall" in fr.columns:
        fr["confidence_overall"] = pd.to_numeric(
            fr["confidence_overall"], errors="coerce"
        ).fillna(0)

    # Top metrics
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Total Providers", len(fr))
    with c2:
        if "confidence_overall" in fr.columns:
            st.metric("Avg Confidence", f"{fr['confidence_overall'].mean():.1f}")
    with c3:
        if "risk_level" in fr.columns:
            high_risk = (fr["risk_level"] == "HIGH").sum()
            st.metric("High-Risk Providers", int(high_risk))

    # Filters
    st.markdown("###  Filters")
    with st.container():
        f1, f2, f3 = st.columns(3)
        with f1:
            selected_specialties = st.multiselect(
                "Specialty",
                sorted(fr["specialty"].dropna().unique()) if "specialty" in fr.columns else [],
                key="dash_spec_filter",
            )
        with f2:
            risk_levels = st.multiselect(
                "Risk Level",
                sorted(fr["risk_level"].dropna().unique()) if "risk_level" in fr.columns else [],
                key="dash_risk_filter",
            )
        with f3:
            min_conf = st.slider(
                "Min Confidence",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=5.0,
                key="dash_min_conf",
            )

    # Apply filters
    filtered = fr.copy()
    if selected_specialties and "specialty" in filtered.columns:
        filtered = filtered[filtered["specialty"].isin(selected_specialties)]
    if risk_levels and "risk_level" in filtered.columns:
        filtered = filtered[filtered["risk_level"].isin(risk_levels)]
    if "confidence_overall" in filtered.columns:
        filtered = filtered[filtered["confidence_overall"] >= min_conf]

    st.markdown(
        f"Showing **{len(filtered)}** providers after filtering "
        f"(out of {len(fr)} total)."
    )

    if filtered.empty:
        st.warning("No records after applying filters.")
        return

    # ==========================
    #      VISUAL ANALYTICS
    # ==========================

    st.markdown("### 📊 Visual Analytics")

    # ---- Row 1: Confidence Histogram + Risk Breakdown
    c1, c2 = st.columns(2)

    with c1:
        if "confidence_overall" in filtered.columns:
            st.markdown("####  Confidence Distribution")
            fig_conf = px.histogram(
                filtered,
                x="confidence_overall",
                nbins=20,
                title="Confidence Score Distribution",
                template="plotly_dark",
            )
            fig_conf.update_traces(marker_line_width=0.5, marker_line_color="#1f2933")
            fig_conf.update_layout(
                xaxis_title="Overall Confidence Score",
                yaxis_title="Providers",
                height=320,
                margin=dict(l=10, r=10, t=40, b=40),
            )
            st.plotly_chart(fig_conf, use_container_width=True)

    with c2:
        if "risk_level" in filtered.columns:
            st.markdown("####  Risk Level Breakdown")
            risk_counts = (
                filtered["risk_level"]
                .value_counts()
                .rename_axis("risk_level")
                .reset_index(name="provider_count")
            )
            fig_risk = px.bar(
                risk_counts,
                x="risk_level",
                y="provider_count",
                title="Risk Level Distribution",
                color="risk_level",
                template="plotly_dark",
            )
            fig_risk.update_layout(
                xaxis_title="Risk Level",
                yaxis_title="Providers",
                height=320,
                margin=dict(l=10, r=10, t=40, b=40),
                legend_title="Risk Level",
            )
            st.plotly_chart(fig_risk, use_container_width=True)

    # ---- Row 2: Specialty vs Avg Confidence + Priority Category Count
    c3, c4 = st.columns(2)

    with c3:
        if "specialty" in filtered.columns and "confidence_overall" in filtered.columns:
            st.markdown("#### 🩺 Specialty vs Avg Confidence")
            spec_df = (
                filtered.groupby("specialty")["confidence_overall"]
                .mean()
                .reset_index()
                .sort_values("confidence_overall", ascending=True)
            )
            fig_spec = px.bar(
                spec_df,
                x="confidence_overall",
                y="specialty",
                orientation="h",
                title="Average Confidence by Specialty",
                template="plotly_dark",
            )
            fig_spec.update_layout(
                xaxis_title="Avg Confidence",
                yaxis_title="Specialty",
                height=360,
                margin=dict(l=10, r=10, t=40, b=40),
            )
            st.plotly_chart(fig_spec, use_container_width=True)

    with c4:
        st.markdown("#### 🎯 Priority Bucket Distribution")
        ranked_for_chart = compute_priority(filtered)
        if "priority_category" in ranked_for_chart.columns:
            pri_counts = (
                ranked_for_chart["priority_category"]
                .value_counts()
                .rename_axis("priority_category")
                .reset_index(name="provider_count")
            )
            fig_pri = px.bar(
                pri_counts,
                x="priority_category",
                y="provider_count",
                title="Providers by Priority Category",
                template="plotly_dark",
            )
            fig_pri.update_layout(
                xaxis_title="Priority Category",
                yaxis_title="Providers",
                height=360,
                margin=dict(l=10, r=10, t=40, b=40),
            )
            st.plotly_chart(fig_pri, use_container_width=True)

    # ---- Row 3: Main Heatmap (Specialty x Risk Level)
    if "specialty" in filtered.columns and "risk_level" in filtered.columns:
        st.markdown("#### 🔥 Risk Heatmap (Specialty × Risk Level)")

        heatmap_data = (
            filtered.groupby(["specialty", "risk_level"])
            .size()
            .reset_index(name="provider_count")
        )
        if not heatmap_data.empty:
            heatmap_pivot = heatmap_data.pivot(
                index="specialty", columns="risk_level", values="provider_count"
            ).fillna(0)

            fig_heatmap = px.imshow(
                heatmap_pivot,
                labels=dict(x="Risk Level", y="Specialty", color="Providers"),
                x=heatmap_pivot.columns,
                y=heatmap_pivot.index,
                color_continuous_scale="Viridis",
                title="Provider Count by Specialty and Risk Level",
            )
            fig_heatmap.update_layout(
                template="plotly_dark",
                height=440,
                margin=dict(l=10, r=10, t=50, b=40),
            )
            st.plotly_chart(fig_heatmap, use_container_width=True)

    # Directory Table
    with st.expander(" View Filtered Table", expanded=False):
        st.dataframe(filtered, use_container_width=True)

    # Downloads
    st.markdown("### 📥 Download Results")

    col1, col2 = st.columns(2)

    records = filtered.to_dict(orient="records")
    csv_bytes = filtered.to_csv(index=False).encode("utf-8")
    json_bytes = json.dumps(records, indent=2).encode("utf-8")

    with col1:
        st.download_button(
            "⬇ Download CSV",
            data=csv_bytes,
            file_name="final_results_filtered.csv",
            mime="text/csv",
        )
    with col2:
        st.download_button(
            "⬇ Download JSON",
            data=json_bytes,
            file_name="final_results_filtered.json",
            mime="application/json",
        )

    #========================================================
    # Provider Priority Ranking (Fraud / QA Queue) + Email
    #========================================================
    st.markdown("---")
    st.markdown("### 🔥 Provider Priority Ranking (Fraud / QA Queue)")

    ranked = compute_priority(filtered)
    cols = [
        "provider_id",
        "name",
        "specialty",
        "risk_level",
        "confidence_overall",
        "priority_score",
        "needs_manual_review",
    ]
    present_cols = [c for c in cols if c in ranked.columns]
    ranked_display = ranked[present_cols].sort_values(
        "priority_score", ascending=False
    ).head(30)

    st.dataframe(ranked_display, use_container_width=True, height=400)

    st.caption(
        "Priority score combines risk level, confidence (inverted) and manual-review flags. "
        "Higher score → review earlier."
    )

    st.markdown("### ✉️ Auto-Generated Email for High-Risk Provider")
    if ranked_display.empty:
        st.info("No providers to generate email for yet.")
        return

    sample_row = ranked_display.iloc[0]
    name = sample_row.get("name", "Provider")
    risk = sample_row.get("risk_level", "HIGH")
    conf = float(sample_row.get("confidence_overall", 0.0))
    pid = int(sample_row.get("provider_id", 0))

    default_email = f"""
Dear {name},

As part of our routine quality review of the provider directory,
your profile (ID: {pid}) has been flagged for **{risk}-risk** due to data inconsistencies.

Our automated system recorded an overall confidence score of **{conf:.1f}%** for your entry.
We request your support in confirming your latest practice address, contact number,
specialty details and license information.

You can reply directly to this email with corrected details, or upload updated documents
through the secure portal shared with your network administrator.

Thank you for helping us keep member-facing information accurate and compliant.

Regards,
Provider Data Quality Team
""".strip()

    st.text_area("Email body", value=default_email, height=220, key="email_body")


# ================================
# --------- ABOUT US PAGE --------
# ================================

def render_about():
    st.markdown("##  About Us")
    st.write("Meet the team behind the Provider Data Automation System.")

    team = [
        {
            "name": "Muskan Kawadkar",
            "role": "Team Lead & Presentation",
            "desc": "Leads the team and delivers impactful presentations.",
        },
        {
            "name": "Musa Qureshi",
            "role": "Agentic Developer",
            "desc": "Leads multi-agent design, LangGraph orchestration and AI strategy.",
        },
        {
            "name": "Parag Tiwari",
            "role": "Research & QA Lead",
            "desc": "Owns research strategy and quality assurance.",
        },
        {
            "name": "Shruti Mehra",
            "role": "UI/UX Designer",
            "desc": "Transforms ideas into meaningful user experiences.",
        },
    ]

    c1, c2, c3, c4 = st.columns(4)
    cols = [c1, c2, c3, c4]

    for member, col in zip(team, cols):
        with col:
            st.markdown(
                f"""
                <div class="team-card fade-in">
                    <div style="font-size:40px;">👤</div>
                    <h4 style="margin-bottom:4px;color:white;">{member['name']}</h4>
                    <p style="font-weight:600;margin-bottom:6px;color:#ccc">{member['role']}</p>
                    <p style="font-size:13px;color:#ccc;margin:0;">{member['desc']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ================================
# --------- CONTACT PAGE ---------
# ================================

def render_contact():
    st.markdown("##  Contact Us")
    st.write("Choose a team member and drop a message. (Demo mode – no real email send.)")

    members = {
        "Musa Qureshi": "musa@example.com",
        "Muskan": "muskan@example.com",
        "Parag Tiwari": "parag@example.com",
        "Shruti": "shruti@example.com",
    }

    selected = st.selectbox("Select person to contact", list(members.keys()))

    st.markdown(f"### Message for {selected}")

    with st.form("contact_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        msg = st.text_area("Your Message", height=150)
        submitted = st.form_submit_button("Send")

    if submitted:
        st.success(f"✅ Your message to **{selected}** has been recorded (demo).")
        st.caption(f"Would be sent to: {members[selected]}")


# ================================
# ------------- MAIN -------------
# ================================

def main():
    st.set_page_config(
        page_title="Provider Agentic System",
        layout="wide",
        page_icon="🏥",
    )

    # Inject CSS once
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    st.markdown(
        """
<style>
.block-container {
    padding-top: 2rem !important;
}
</style>
""",
        unsafe_allow_html=True,
    )

    selected = option_menu(
        menu_title=None,
        options=["Home", "Agents", "Generated Output", "About Us", "Contact"],
        icons=["house", "people", "bar-chart", "info-circle", "telephone"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
    )

    if selected == "Home":
        render_home()
    elif selected == "Agents":
        render_agents()
    elif selected == "Generated Output":
        render_generated_output()
    elif selected == "About Us":
        render_about()
    else:
        render_contact()


if __name__ == "__main__":
    main()
