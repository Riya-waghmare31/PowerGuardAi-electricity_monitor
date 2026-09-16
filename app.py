from pathlib import Path
import io

import streamlit as st

from backend.anomaly_detection import detect_anomalies
from backend.data_processing import load_csv, clean_dataframe
from backend.database import initialize_database, log_processing
from backend.risk_scoring import calculate_risk_scores

from frontend.analytics_page import render_analytics
from frontend.anomaly_page import render_anomaly_page
from frontend.dashboard import render_dashboard
from frontend.reports_page import render_reports
from frontend.settings_page import render_settings


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="PowerGuard AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# CUSTOM LIGHT UI
# =========================================================

st.markdown(
    """
    <style>
    /* =====================================================
       REFERENCE-INSPIRED VISUAL SYSTEM
       Visual-only changes: existing content and navigation
       are intentionally preserved.
       ===================================================== */

    :root {
        --surface: #ffffff;
        --surface-soft: #f8faff;
        --page: #f5f7fb;
        --line: #e6eaf2;
        --text: #172033;
        --muted: #748096;
        --accent: #5b5ce2;
        --accent-2: #23c7bd;
        --green: #0f8f70;
    }

    [data-testid="stAppViewContainer"] {
        background: var(--page);
        color: var(--text);
    }

    [data-testid="stHeader"] {
        background: rgba(245,247,251,0.88);
    }

    .block-container {
        padding-top: 1.05rem;
        padding-bottom: 3rem;
        max-width: 1480px;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid var(--line);
        box-shadow: 5px 0 24px rgba(38, 48, 77, 0.035);
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1rem;
    }

    [data-testid="stSidebar"] * {
        color: #475166;
    }

    .sidebar-title {
        color: var(--text);
        font-weight: 850;
        font-size: 1.28rem;
        letter-spacing: -0.025em;
        margin-bottom: 1rem;
        padding: 0.35rem 0.2rem 0.9rem;
        border-bottom: 1px solid var(--line);
    }

    [data-testid="stSidebar"] .stRadio > div {
        gap: 0.28rem;
    }

    [data-testid="stSidebar"] .stRadio label {
        color: #667085;
        font-weight: 550;
        border-radius: 10px;
        padding: 8px 10px;
        transition: all 0.16s ease;
    }

    [data-testid="stSidebar"] .stRadio label:hover {
        background: #f2f4ff;
        color: #5557d9;
    }

    [data-testid="stSidebar"] .stRadio [aria-checked="true"] + div {
        color: #5557d9;
    }

    .status-box {
        background: linear-gradient(145deg, #f8f9ff, #f6fffd);
        border: 1px solid #e4e7f3;
        border-radius: 14px;
        padding: 14px;
        margin-top: 18px;
        font-size: 0.84rem;
        line-height: 1.85;
        box-shadow: 0 6px 18px rgba(38, 48, 77, 0.045);
    }

    /* Main page header */
    .powerguard-title {
        color: var(--text);
        font-size: 1.85rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        margin: 0.25rem 0 0.15rem;
    }

    .powerguard-subtitle {
        color: var(--muted);
        font-size: 0.92rem;
        margin-bottom: 0.9rem;
    }

    .stCaption {
        color: var(--muted);
    }

    h1, h2, h3, h4, h5, h6 {
        color: var(--text);
        letter-spacing: -0.02em;
    }

    /* Inputs */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    div[data-baseweb="textarea"] > div {
        background: #ffffff;
        border: 1px solid #e0e5ef;
        border-radius: 10px;
        box-shadow: none;
    }

    input {
        color: var(--text);
    }

    [data-testid="stFileUploader"] {
        background: #fafbfe;
        border: 1px dashed #cbd2e2;
        border-radius: 12px;
        padding: 6px;
    }

    /* Buttons */
    .stButton > button {
        background: #5b5ce2;
        color: #ffffff;
        border: 1px solid #5b5ce2;
        border-radius: 10px;
        font-weight: 650;
        padding: 0.45rem 1rem;
        box-shadow: 0 5px 14px rgba(91, 92, 226, 0.16);
        transition: all 0.16s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 18px rgba(91, 92, 226, 0.22);
        color: #ffffff;
    }

    .stDownloadButton > button {
        background: #ffffff;
        color: #5557d9;
        border: 1px solid #cfd4e4;
        border-radius: 10px;
        font-weight: 650;
    }

    /* Native bordered containers become the dashboard cards. */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255,255,255,0.96);
        border: 1px solid var(--line);
        border-radius: 17px;
        box-shadow: 0 7px 24px rgba(38, 48, 77, 0.045);
    }

    /* Metrics used on secondary pages */
    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid var(--line);
        border-radius: 15px;
        padding: 15px 17px;
        box-shadow: 0 5px 18px rgba(38, 48, 77, 0.045);
    }

    div[data-testid="stMetricLabel"] {
        color: var(--muted);
        font-weight: 600;
    }

    div[data-testid="stMetricValue"] {
        color: var(--text);
        font-weight: 800;
    }

    /* Data tables / alerts */
    .stDataFrame {
        border: 1px solid var(--line);
        border-radius: 12px;
        overflow: hidden;
    }

    [data-testid="stAlert"] {
        border-radius: 12px;
        border: 1px solid var(--line);
    }

    hr {
        border-color: var(--line);
    }

    /* Dashboard decorative hero: shapes only, no new content. */
    .dashboard-visual-hero {
        position: relative;
        overflow: hidden;
        background: linear-gradient(135deg, #eef6ff 0%, #eefbfa 100%);
        border: 1px solid #e1eaf4;
        border-radius: 18px;
        min-height: 150px;
        box-shadow: 0 8px 25px rgba(38, 48, 77, 0.045);
    }

    .dashboard-visual-hero::before,
    .dashboard-visual-hero::after {
        content: "";
        position: absolute;
        border-radius: 50%;
        pointer-events: none;
    }

    .dashboard-visual-hero::before {
        width: 250px;
        height: 250px;
        right: 5%;
        top: -135px;
        background: rgba(119, 183, 255, 0.18);
        box-shadow: 150px 80px 0 rgba(103, 91, 225, 0.10);
    }

    .dashboard-visual-hero::after {
        width: 170px;
        height: 170px;
        right: 27%;
        bottom: -120px;
        background: rgba(40, 199, 189, 0.13);
    }

    /* Plotly cards */
    div[data-testid="stPlotlyChart"] {
        background: #ffffff;
        border-radius: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# DATASET PATH
# =========================================================

DATASET_PATH = Path(__file__).parent / "electricity_bill_dataset.csv"


# =========================================================
# LOAD AND ANALYZE DATA
# =========================================================

@st.cache_data(show_spinner="Loading and analyzing electricity data...")
def load_and_analyze(source_bytes=None):

    if source_bytes is None:
        df = load_csv(DATASET_PATH)

    else:
        df = load_csv_from_bytes(source_bytes)

    analyzed_df, _ = detect_anomalies(df)

    analyzed_df = calculate_risk_scores(analyzed_df)

    return analyzed_df


# =========================================================
# LOAD UPLOADED CSV
# =========================================================

def load_csv_from_bytes(source_bytes):

    df = clean_dataframe(
        __import__("pandas").read_csv(
            io.BytesIO(source_bytes)
        )
    )

    return df


# =========================================================
# MAIN APPLICATION
# =========================================================

def main():

    initialize_database()

    if not DATASET_PATH.exists():

        st.error(
            "electricity_bill_dataset.csv was not found. "
            "Please place the dataset in the project root folder."
        )

        st.stop()


    # =====================================================
    # SIDEBAR
    # =====================================================

    with st.sidebar:

        st.markdown(
            '<div class="sidebar-title">⚡ POWERGUARD AI</div>',
            unsafe_allow_html=True
        )

        st.markdown("### Dataset")

        uploaded_file = st.file_uploader(
            "Optional replacement CSV",
            type=["csv"],
            help=(
                "Upload another electricity dataset. "
                "The file must contain the required columns."
            ),
        )

        try:

            if uploaded_file is not None:

                df = load_and_analyze(
                    uploaded_file.getvalue()
                )

                st.success(
                    "Uploaded dataset connected."
                )

            else:

                df = load_and_analyze()

                st.success(
                    "Default dataset connected."
                )

        except ValueError as error:

            st.error(str(error))
            st.stop()

        except Exception as error:

            st.error(
                f"Unable to process the dataset: {error}"
            )
            st.stop()

        log_processing(len(df))

        st.markdown("### Navigation")

        page = st.radio(
            "Select a page",
            [
                "Dashboard",
                "Electricity Bills",
                "Consumption Analysis",
                "AI Anomaly Detection",
                "City Analysis",
                "Company Analysis",
                "Appliance Analysis",
                "Reports",
                "Settings",
            ],
            label_visibility="collapsed",
        )



    # =====================================================
    # MAIN HEADER
    # =====================================================

    st.markdown(
        """
        <div class="powerguard-title">
            AI Electricity Consumption & Anomaly Detection System
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="powerguard-subtitle">
            Smart Electricity Monitoring Dashboard
        </div>
        """,
        unsafe_allow_html=True,
    )



    # =====================================================
    # PAGE ROUTING
    # =====================================================

    if page == "Dashboard":

        render_dashboard(df)

    elif page == "Electricity Bills":

        render_electricity_bills(df)

    elif page == "Consumption Analysis":

        render_analytics(
            df,
            "Consumption Analysis"
        )

    elif page == "AI Anomaly Detection":

        render_anomaly_page(df)

    elif page == "City Analysis":

        render_analytics(
            df,
            "City Analysis"
        )

    elif page == "Company Analysis":

        render_analytics(
            df,
            "Company Analysis"
        )

    elif page == "Appliance Analysis":

        render_analytics(
            df,
            "Appliance Analysis"
        )

    elif page == "Reports":

        render_reports(df)

    elif page == "Settings":

        render_settings()


# =========================================================
# ELECTRICITY BILLS PAGE
# =========================================================

def render_electricity_bills(df):

    st.subheader("Electricity Bills")

    st.caption(
        "Search, filter and analyze electricity consumption records."
    )

    left, right = st.columns(2)

    with left:

        cities = st.multiselect(
            "City",
            sorted(
                df["City"].unique()
            )
        )

        companies = st.multiselect(
            "Company",
            sorted(
                df["Company"].unique()
            )
        )

        months = st.multiselect(
            "Month",
            sorted(
                df["Month"].unique()
            )
        )

    with right:

        risks = st.multiselect(
            "Risk Level",
            [
                "LOW",
                "MODERATE",
                "HIGH",
            ],
        )

        bill_min = float(
            df["ElectricityBill"].min()
        )

        bill_max = float(
            df["ElectricityBill"].max()
        )

        bill_range = st.slider(
            "Electricity Bill Range",
            min_value=bill_min,
            max_value=bill_max,
            value=(
                bill_min,
                bill_max,
            ),
        )

    filtered = df.copy()

    if cities:

        filtered = filtered[
            filtered["City"].isin(cities)
        ]

    if companies:

        filtered = filtered[
            filtered["Company"].isin(companies)
        ]

    if months:

        filtered = filtered[
            filtered["Month"].isin(months)
        ]

    if risks:

        filtered = filtered[
            filtered["Risk Level"].isin(risks)
        ]

    filtered = filtered[
        filtered["ElectricityBill"].between(
            bill_range[0],
            bill_range[1]
        )
    ]

    search = st.text_input(
        "Search Record ID, City or Company"
    ).strip().lower()

    if search:

        filtered = filtered[
            filtered.apply(
                lambda row:
                search in (
                    str(row["Record ID"])
                    + " "
                    + str(row["City"])
                    + " "
                    + str(row["Company"])
                ).lower(),
                axis=1,
            )
        ]

    columns = [
        "Record ID",
        "City",
        "Company",
        "Month",
        "MonthlyHours",
        "TariffRate",
        "ElectricityBill",
        "Risk Score",
        "Risk Level",
    ]

    st.write(
        f"Showing {len(filtered):,} records"
    )

    st.dataframe(
        filtered[columns]
        .sort_values(
            "Risk Score",
            ascending=False
        )
        .head(1000),
        use_container_width=True,
        hide_index=True,
    )

    st.download_button(
        "Download Filtered CSV",

        filtered.to_csv(
            index=False
        ).encode("utf-8"),

        file_name="filtered_electricity_bills.csv",

        mime="text/csv",
    )


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":
    main()