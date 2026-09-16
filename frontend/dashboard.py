import plotly.express as px
import streamlit as st

from backend.analytics import (
    city_analysis,
    monthly_analysis,
    overall_summary
)


# =========================================================
# COLOR PALETTE
# =========================================================

MAIN_GREEN = "#0F8F70"
TEAL = "#087A8A"
BLUE = "#3B82F6"
PURPLE = "#6C63C9"
ORANGE = "#F39C4A"
RED = "#E85D5D"


RISK_COLORS = {
    "LOW": "#18A673",
    "MODERATE": "#F2A93B",
    "HIGH": "#E85D5D"
}


# =========================================================
# MONEY FORMAT
# =========================================================

def _money(value: float) -> str:
    return f"{value:,.2f}"


# =========================================================
# CHART STYLE
# =========================================================

def _style_figure(figure, height=390):

    figure.update_layout(
        template="plotly_white",

        height=height,

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=30
        ),

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="#FFFFFF",

        font=dict(
            family="Arial",
            color="#334155"
        ),

        title=dict(
            font=dict(
                size=18,
                color="#172033"
            )
        ),

        hoverlabel=dict(
            bgcolor="#172033",
            font_color="#FFFFFF",
            font_size=13
        ),

        legend=dict(
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="#E2E8F0",
            borderwidth=1
        )
    )

    figure.update_xaxes(
        showgrid=False,
        linecolor="#DCE7E3",
        tickfont=dict(
            color="#64748B"
        )
    )

    figure.update_yaxes(
        showgrid=True,
        gridcolor="#EDF2F0",
        zeroline=False,
        tickfont=dict(
            color="#64748B"
        )
    )

    return figure


# =========================================================
# KPI CARD
# =========================================================

def _kpi_card(
    column,
    icon,
    title,
    value
):

    with column:

        st.html(
            f"""
            <div style="
                background: #FFFFFF;
                border: 1px solid #E6EAF2;
                border-radius: 17px;
                padding: 18px 19px;
                min-height: 126px;
                box-shadow: 0 7px 24px rgba(38, 48, 77, 0.045);
                box-sizing: border-box;
                width: 100%;
                position: relative;
                overflow: hidden;
            ">

                <div style="
                    font-size: 26px;
                    margin-bottom: 8px;
                ">
                    {icon}
                </div>

                <div style="
                    color: #64748B;
                    font-size: 13px;
                    font-weight: 600;
                    margin-bottom: 6px;
                ">
                    {title}
                </div>

                <div style="
                    color: #172033;
                    font-size: 22px;
                    font-weight: 800;
                ">
                    {value}
                </div>

            </div>
            """
        )


# =========================================================
# DASHBOARD
# =========================================================

def render_dashboard(df):

    # =====================================================
    # HEADER
    # =====================================================

    st.html(
        """
        <div class="dashboard-visual-hero" style="padding: 25px 28px; margin-bottom: 22px; box-sizing: border-box; width: 100%;">

            <div style="
                position: relative;
                z-index: 1;
                color: #172033;
                font-size: 28px;
                font-weight: 800;
                letter-spacing: -0.04em;
                margin-bottom: 5px;
            ">
                PowerGuard AI Dashboard
            </div>

            <div style="
                position: relative;
                z-index: 1;
                color: #748096;
                font-size: 15px;
            ">
                Smart electricity monitoring,
                consumption analysis and AI-powered
                anomaly detection.
            </div>

        </div>
        """
    )


    # =====================================================
    # INTERACTIVE FILTERS
    # =====================================================

    st.markdown(
        "### Interactive Dashboard"
    )

    st.caption(
        "Use the filters below to dynamically explore "
        "your electricity data."
    )

    filter1, filter2, filter3 = st.columns(3)


    with filter1:

        selected_cities = st.multiselect(
            "Select City",

            sorted(
                df["City"]
                .dropna()
                .unique()
                .tolist()
            ),

            placeholder="All cities",

            key="dashboard_city_filter"
        )


    with filter2:

        selected_companies = st.multiselect(
            "Select Company",

            sorted(
                df["Company"]
                .dropna()
                .unique()
                .tolist()
            ),

            placeholder="All companies",

            key="dashboard_company_filter"
        )


    with filter3:

        selected_months = st.multiselect(
            "Select Month",

            sorted(
                df["Month"]
                .dropna()
                .unique()
                .tolist()
            ),

            placeholder="All months",

            key="dashboard_month_filter"
        )


    # =====================================================
    # APPLY FILTERS
    # =====================================================

    filtered_df = df.copy()


    if selected_cities:

        filtered_df = filtered_df[
            filtered_df["City"].isin(
                selected_cities
            )
        ]


    if selected_companies:

        filtered_df = filtered_df[
            filtered_df["Company"].isin(
                selected_companies
            )
        ]


    if selected_months:

        filtered_df = filtered_df[
            filtered_df["Month"].isin(
                selected_months
            )
        ]


    if filtered_df.empty:

        st.warning(
            "No records match the selected filters. "
            "Please try different filters."
        )

        return


    # =====================================================
    # SUMMARY
    # =====================================================

    summary = overall_summary(
        filtered_df
    )


    # =====================================================
    # KPI SECTION
    # =====================================================

    st.markdown(
        "### Performance Overview"
    )

    st.caption(
        "Live metrics based on the currently selected data."
    )


    # =====================================================
    # KPI ROW 1
    # =====================================================

    kpi1, kpi2, kpi3 = st.columns(3)


    _kpi_card(
        kpi1,
        "",
        "Total Records",
        f"{summary['total_records']:,}"
    )


    _kpi_card(
        kpi2,
        "",
        "Average Electricity Bill",
        f"₹{_money(summary['average_bill'])}"
    )


    _kpi_card(
        kpi3,
        "",
        "Average Monthly Hours",
        f"{summary['average_hours']:,.2f}"
    )


    st.write("")


    # =====================================================
    # KPI ROW 2
    # =====================================================

    kpi4, kpi5, kpi6 = st.columns(3)


    _kpi_card(
        kpi4,
        "",
        "Average Tariff Rate",
        f"{summary['average_tariff']:,.2f}"
    )


    _kpi_card(
        kpi5,
        "",
        "High-Risk Records",
        f"{summary['high_risk']:,}"
    )


    _kpi_card(
        kpi6,
        "",
        "Average Risk Score",
        f"{summary['average_risk']:,.2f}/100"
    )


    st.write("")


    # =====================================================
    # MONTHLY TREND
    # =====================================================

    st.markdown(
        "### 📈 Monthly Electricity Bill Trend"
    )


    trend1, trend2 = st.columns(
        [3, 1]
    )


    with trend1:

        st.caption(
            "Track how electricity bills change over time."
        )


    with trend2:

        measure = st.selectbox(
            "Trend Metric",

            [
                "Average",
                "Maximum",
                "Minimum"
            ],

            key="dashboard_month_metric"
        )


    monthly = monthly_analysis(
        filtered_df
    )


    figure = px.line(
        monthly,

        x="Month",

        y=measure,

        markers=True,

        labels={
            "Month": "Month",
            measure: "Electricity Bill"
        },

        color_discrete_sequence=[
            MAIN_GREEN
        ]
    )


    figure.update_traces(
        line=dict(
            width=3
        ),

        marker=dict(
            size=9
        ),

        hovertemplate=(
            "<b>%{x}</b>"
            "<br>Electricity Bill: %{y:,.2f}"
            "<extra></extra>"
        )
    )


    _style_figure(
        figure,
        420
    )


    st.plotly_chart(
        figure,

        width="stretch",

        config={
            "displaylogo": False,
            "scrollZoom": True,
            "responsive": True
        }
    )


    # =====================================================
    # CITY ANALYSIS
    # =====================================================

    cities = city_analysis(
        filtered_df
    )


    left, right = st.columns(2)


    # =====================================================
    # AVERAGE BILL BY CITY
    # =====================================================

    with left:

        st.markdown(
            "### 🏙️ Average Bill by City"
        )

        st.caption(
            "Comparison of average electricity bills."
        )


        bill_data = cities.sort_values(
            "AverageBill",
            ascending=False
        )


        figure = px.bar(
            bill_data,

            x="City",

            y="AverageBill",

            color="AverageBill",

            color_continuous_scale=[
                "#DDF5EE",
                MAIN_GREEN
            ],

            labels={
                "AverageBill":
                    "Average Electricity Bill"
            }
        )


        figure.update_traces(
            hovertemplate=(
                "<b>%{x}</b>"
                "<br>Average Bill: %{y:,.2f}"
                "<extra></extra>"
            )
        )


        _style_figure(
            figure,
            400
        )


        st.plotly_chart(
            figure,

            width="stretch",

            config={
                "displaylogo": False,
                "responsive": True
            }
        )


    # =====================================================
    # AVERAGE RISK BY CITY
    # =====================================================

    with right:

        st.markdown(
            "### Average Risk by City"
        )

        st.caption(
            "Compare average risk scores across cities."
        )


        risk_data = cities.sort_values(
            "AverageRisk",
            ascending=False
        )


        figure = px.bar(
            risk_data,

            x="City",

            y="AverageRisk",

            color="AverageRisk",

            color_continuous_scale=[
                "#18A673",
                "#F2A93B",
                "#E85D5D"
            ],

            range_color=[
                0,
                100
            ],

            labels={
                "AverageRisk":
                    "Average Risk Score"
            }
        )


        figure.update_traces(
            hovertemplate=(
                "<b>%{x}</b>"
                "<br>Risk Score: %{y:.2f}"
                "<extra></extra>"
            )
        )


        _style_figure(
            figure,
            400
        )


        st.plotly_chart(
            figure,

            width="stretch",

            config={
                "displaylogo": False,
                "responsive": True
            }
        )


    # =====================================================
    # QUICK INSIGHTS
    # =====================================================

    st.markdown(
        "### Quick Insights"
    )


    highest_bill_city = cities.loc[
        cities["AverageBill"].idxmax()
    ]


    highest_risk_city = cities.loc[
        cities["AverageRisk"].idxmax()
    ]


    insight1, insight2, insight3 = st.columns(3)


    with insight1:

        st.info(
            f"""
            **Records Analyzed**

            {len(filtered_df):,} records are currently
            included in the dashboard analysis.
            """
        )


    with insight2:

        st.info(
            f"""
            **Highest Average Bill**

            {highest_bill_city['City']} has the highest
            average electricity bill of
            ₹{highest_bill_city['AverageBill']:,.2f}.
            """
        )


    with insight3:

        st.warning(
            f"""
            **Highest Average Risk**

            {highest_risk_city['City']} has the highest
            average risk score of
            {highest_risk_city['AverageRisk']:.2f}.
            """
        )


    # =====================================================
    # DATA PREVIEW
    # =====================================================

    with st.expander(
        "🔍 View Filtered Dataset"
    ):

        st.caption(
            f"Showing {len(filtered_df):,} filtered records."
        )


        st.dataframe(
            filtered_df,

            width="stretch",

            hide_index=True
        )