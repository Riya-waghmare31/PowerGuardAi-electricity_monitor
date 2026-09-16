import plotly.express as px
import streamlit as st


DISPLAY_COLUMNS = [
    "Record ID",
    "City",
    "Company",
    "Month",
    "MonthlyHours",
    "TariffRate",
    "ElectricityBill",
    "Risk Score",
    "Risk Level",
    "Anomaly Status",
    "anomaly_reason",
]


RISK_COLORS = {
    "LOW": "#18A673",
    "MODERATE": "#F2A93B",
    "HIGH": "#E85D5D",
}


def _style_figure(fig, height=390):

    fig.update_layout(
        template="plotly_white",
        height=height,
        margin=dict(
            l=10,
            r=10,
            t=55,
            b=20
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#ffffff",
        font=dict(
            color="#334155",
            family="Arial"
        ),
        title=dict(
            font=dict(
                size=17,
                color="#172033"
            )
        ),
        hoverlabel=dict(
            bgcolor="#172033",
            font_color="white",
            font_size=13,
        ),
    )

    fig.update_xaxes(
        showgrid=False,
        linecolor="#dbe5e2"
    )

    fig.update_yaxes(
        gridcolor="#edf2f0",
        zeroline=False
    )

    return fig


def render_anomaly_page(df):

    st.subheader(
        "AI Anomaly Detection"
    )

    st.caption(
        "Isolation Forest with supporting "
        "statistical analysis"
    )


    # =====================================================
    # SUMMARY
    # =====================================================

    normal = int(
        (df["Risk Level"] == "LOW").sum()
    )

    review = int(
        (df["Risk Level"] == "MODERATE").sum()
    )

    high = int(
        (df["Risk Level"] == "HIGH").sum()
    )


    columns = st.columns(4)

    columns[0].metric(
        "Total Records",
        f"{len(df):,}"
    )

    columns[1].metric(
        "Normal Records",
        f"{normal:,}"
    )

    columns[2].metric(
        "Records Requiring Review",
        f"{review:,}"
    )

    columns[3].metric(
        "High-Risk Anomalies",
        f"{high:,}"
    )


    # =====================================================
    # RISK DISTRIBUTION
    # =====================================================

    distribution = (
        df["Risk Level"]
        .value_counts()
        .reindex(
            [
                "LOW",
                "MODERATE",
                "HIGH"
            ],
            fill_value=0
        )
        .rename_axis(
            "Risk Level"
        )
        .reset_index(
            name="Records"
        )
    )


    figure = px.bar(
        distribution,
        x="Risk Level",
        y="Records",
        color="Risk Level",
        color_discrete_map=RISK_COLORS,
        title="Risk Distribution",
        labels={
            "Records":
            "Number of Records"
        },
    )


    figure.update_traces(
        hovertemplate=(
            "<b>%{x}</b>"
            "<br>Records: %{y:,}"
            "<extra></extra>"
        )
    )


    _style_figure(
        figure,
        400
    )


    st.plotly_chart(
        figure,
        use_container_width=True,
        config={
            "displaylogo": False
        }
    )


    # =====================================================
    # FILTERS
    # =====================================================

    st.markdown(
        "### 🔎 Explore Highest-Risk Records"
    )


    first, second, third, fourth = st.columns(4)


    with first:

        risk_levels = st.multiselect(
            "Risk level",
            [
                "LOW",
                "MODERATE",
                "HIGH"
            ],
            default=[
                "HIGH",
                "MODERATE"
            ],
        )


    with second:

        cities = st.multiselect(
            "City",
            sorted(
                df["City"].unique()
            )
        )


    with third:

        companies = st.multiselect(
            "Company",
            sorted(
                df["Company"].unique()
            )
        )


    with fourth:

        months = st.multiselect(
            "Month",
            sorted(
                df["Month"].unique()
            )
        )


    filtered = df.copy()


    if risk_levels:

        filtered = filtered[
            filtered["Risk Level"].isin(
                risk_levels
            )
        ]


    if cities:

        filtered = filtered[
            filtered["City"].isin(
                cities
            )
        ]


    if companies:

        filtered = filtered[
            filtered["Company"].isin(
                companies
            )
        ]


    if months:

        filtered = filtered[
            filtered["Month"].isin(
                months
            )
        ]


    st.caption(
        f"{len(filtered):,} records "
        "match the selected filters."
    )


    # =====================================================
    # RECORD TABLE
    # =====================================================

    display = (
        filtered
        .sort_values(
            "Risk Score",
            ascending=False
        )
        [DISPLAY_COLUMNS]
        .head(250)
    )


    st.dataframe(
        display,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Risk Score":
                st.column_config.ProgressColumn(
                    "Risk Score",
                    min_value=0,
                    max_value=100,
                    format="%.2f",
                )
        },
    )


    # =====================================================
    # RECORD DETAILS
    # =====================================================

    if not filtered.empty:

        selected_id = st.selectbox(
            "Select a record for details",
            filtered
            .sort_values(
                "Risk Score",
                ascending=False
            )
            ["Record ID"]
            .tolist(),
        )


        record = filtered[
            filtered["Record ID"] == selected_id
        ].iloc[0]


        st.markdown(
            "### 📄 Record Details"
        )


        details = [
            (
                "Record ID",
                record["Record ID"]
            ),
            (
                "City",
                record["City"]
            ),
            (
                "Company",
                record["Company"]
            ),
            (
                "Month",
                record["Month"]
            ),
            (
                "Monthly Hours",
                record["MonthlyHours"]
            ),
            (
                "Tariff Rate",
                record["TariffRate"]
            ),
            (
                "Electricity Bill",
                record["ElectricityBill"]
            ),
            (
                "Fan",
                record["Fan"]
            ),
            (
                "Refrigerator",
                record["Refrigerator"]
            ),
            (
                "AirConditioner",
                record["AirConditioner"]
            ),
            (
                "Television",
                record["Television"]
            ),
            (
                "Monitor",
                record["Monitor"]
            ),
            (
                "MotorPump",
                record["MotorPump"]
            ),
            (
                "Risk Score",
                record["Risk Score"]
            ),
            (
                "Risk Level",
                record["Risk Level"]
            ),
            (
                "Anomaly Status",
                record["Anomaly Status"]
            ),
        ]


        columns = st.columns(4)


        for index, (label, value) in enumerate(
            details
        ):

            columns[
                index % 4
            ].write(
                f"**{label}**\n\n{value}"
            )


        st.info(
            "Why this record was flagged: "
            f"{record['anomaly_reason']}"
        )