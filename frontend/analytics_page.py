import plotly.express as px
import streamlit as st

from backend.analytics import (
    appliance_analysis,
    city_analysis,
    company_analysis
)


CHART_COLORS = [
    "#0F8F70",
    "#087A8A",
    "#6C63C9",
    "#F39C4A",
    "#3B82F6",
    "#14B8A6"
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
            font_size=13
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


def render_analytics(df, page: str):

    st.subheader(page)

    if page == "City Analysis":

        data = city_analysis(df)

        st.dataframe(
            data,
            use_container_width=True,
            hide_index=True
        )

        left, right = st.columns(2)

        with left:

            fig = px.bar(
                data,
                x="City",
                y="AverageBill",
                color="AverageBill",
                color_continuous_scale=[
                    "#DDF5EE",
                    "#0F8F70"
                ],
                title="Average Electricity Bill by City",
                labels={
                    "AverageBill":
                    "Average Bill"
                },
            )

            _style_figure(fig)

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={
                    "displaylogo": False
                }
            )

        with right:

            fig = px.bar(
                data.sort_values(
                    "AverageRisk",
                    ascending=False
                ),
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
                title="Average Risk Score by City",
                labels={
                    "AverageRisk":
                    "Risk Score"
                },
            )

            _style_figure(fig)

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={
                    "displaylogo": False
                }
            )


    elif page == "Company Analysis":

        data = company_analysis(df)

        choice = st.radio(
            "Companies to display",
            [
                "Top 5",
                "Top 10",
                "All"
            ],
            horizontal=True,
        )

        if choice == "Top 5":

            chart_data = data.head(5)

        elif choice == "Top 10":

            chart_data = data.head(10)

        else:

            chart_data = data

        st.dataframe(
            data,
            use_container_width=True,
            hide_index=True
        )

        fig = px.bar(
            chart_data,
            x="Company",
            y="AverageBill",
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
            title="Company Average Bill Comparison",
            labels={
                "AverageBill":
                "Average Bill",
                "AverageRisk":
                "Risk Score"
            },
        )

        fig.update_layout(
            xaxis_tickangle=-40
        )

        _style_figure(fig)

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displaylogo": False
            }
        )


    elif page == "Appliance Analysis":

        data = appliance_analysis(df)

        st.dataframe(
            data,
            use_container_width=True,
            hide_index=True
        )

        left, right = st.columns(2)

        with left:

            fig = px.bar(
                data,
                x="Appliance",
                y="Average Usage",
                color="Appliance",
                color_discrete_sequence=CHART_COLORS,
                title="Average Appliance Usage",
                labels={
                    "Average Usage":
                    "Average Usage"
                },
            )

            _style_figure(fig)

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={
                    "displaylogo": False
                }
            )

        with right:

            fig = px.bar(
                data,
                x="Appliance",
                y="Bill Correlation",
                color="Bill Correlation",
                color_continuous_scale=[
                    "#E85D5D",
                    "#F2A93B",
                    "#18A673"
                ],
                range_color=[
                    -1,
                    1
                ],
                title=(
                    "Appliance Correlation "
                    "with Electricity Bill"
                ),
                labels={
                    "Bill Correlation":
                    "Bill Correlation"
                },
            )

            _style_figure(fig)

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={
                    "displaylogo": False
                }
            )

        if df["MotorPump"].eq(0).all():

            st.info(
                "MotorPump values are 0 "
                "across the current dataset."
            )


    elif page == "Consumption Analysis":

        render_consumption_analysis(df)


def render_consumption_analysis(df):

    st.markdown(
        "### 🎛️ Consumption Filters"
    )

    first_filter, second_filter, third_filter = st.columns(3)

    with first_filter:

        cities = st.multiselect(
            "City",
            sorted(
                df["City"].unique()
            ),
            placeholder="All cities",
        )

    with second_filter:

        companies = st.multiselect(
            "Company",
            sorted(
                df["Company"].unique()
            ),
            placeholder="All companies",
        )

    with third_filter:

        months = st.multiselect(
            "Month",
            sorted(
                df["Month"].unique()
            ),
            placeholder="All months",
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

    if filtered.empty:

        st.warning(
            "No records match the selected filters."
        )

        return

    st.caption(
        f"Showing {len(filtered):,} records "
        "after applying the selected filters."
    )

    first, second = st.columns(2)

    with first:

        fig = px.scatter(
            filtered,
            x="MonthlyHours",
            y="ElectricityBill",
            color="Risk Level",
            color_discrete_map=RISK_COLORS,
            hover_data=[
                "Record ID",
                "City",
                "Company"
            ],
            title=(
                "Monthly Hours vs "
                "Electricity Bill"
            ),
            labels={
                "MonthlyHours":
                "Monthly Hours",
                "ElectricityBill":
                "Electricity Bill"
            },
        )

        _style_figure(
            fig,
            400
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displaylogo": False,
                "scrollZoom": True
            }
        )

    with second:

        fig = px.scatter(
            filtered,
            x="TariffRate",
            y="ElectricityBill",
            color="Risk Level",
            color_discrete_map=RISK_COLORS,
            hover_data=[
                "Record ID",
                "City",
                "Company"
            ],
            title=(
                "Tariff Rate vs "
                "Electricity Bill"
            ),
            labels={
                "TariffRate":
                "Tariff Rate",
                "ElectricityBill":
                "Electricity Bill"
            },
        )

        _style_figure(
            fig,
            400
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displaylogo": False,
                "scrollZoom": True
            }
        )


    first, second, third = st.columns(3)

    with first:

        fig = px.histogram(
            filtered,
            x="MonthlyHours",
            color_discrete_sequence=[
                CHART_COLORS[1]
            ],
            title="Monthly Hours Distribution",
        )

        _style_figure(
            fig,
            340
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displaylogo": False
            }
        )

    with second:

        fig = px.histogram(
            filtered,
            x="ElectricityBill",
            color_discrete_sequence=[
                CHART_COLORS[0]
            ],
            title="Electricity Bill Distribution",
        )

        _style_figure(
            fig,
            340
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displaylogo": False
            }
        )

    with third:

        fig = px.histogram(
            filtered,
            x="TariffRate",
            color_discrete_sequence=[
                CHART_COLORS[2]
            ],
            title="Tariff Rate Distribution",
        )

        _style_figure(
            fig,
            340
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displaylogo": False
            }
        )