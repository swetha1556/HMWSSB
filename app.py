import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================================================
# HYDROVERSE
# Hyderabad Water & Sewerage Intelligence Prototype
# =========================================================

st.set_page_config(
    page_title="HYDROVERSE",
    page_icon="💧",
    layout="wide",
)

# =========================================================
# DATA
# Prototype/reference data only
# =========================================================

sources = pd.DataFrame({
    "Source": [
        "Osman Sagar",
        "Himayat Sagar",
        "Manjeera",
        "Singur",
        "Krishna / Akkampally",
        "Godavari / Sripada Yellampally",
    ],
    "Type": [
        "Reservoir",
        "Reservoir",
        "River / Reservoir System",
        "Reservoir",
        "River / Reservoir System",
        "River / Reservoir System",
    ],
    "Latitude": [
        17.379,
        17.318,
        18.000,
        17.735,
        16.430,
        18.920,
    ],
    "Longitude": [
        78.318,
        78.341,
        78.000,
        77.995,
        78.150,
        79.450,
    ],
    "Contribution": [8, 7, 15, 12, 27, 23],
})

groundwater = pd.DataFrame({
    "Source": [
        "Groundwater Zone 1",
        "Groundwater Zone 2",
        "Groundwater Zone 3",
        "Groundwater Zone 4",
        "Groundwater Zone 5",
    ],
    "Latitude": [17.45, 17.52, 17.40, 17.55, 17.32],
    "Longitude": [78.38, 78.43, 78.47, 78.50, 78.42],
})

mallanna = pd.DataFrame({
    "Source": ["Mallanna Sagar"],
    "Latitude": [18.06],
    "Longitude": [78.09],
})


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("💧 HYDROVERSE")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Water Source Map",
        "Water Journey",
        "Water Balance",
        "Source Analytics",
        "Source Register",
        "Architecture",
    ],
)

st.sidebar.markdown("---")

st.sidebar.info(
    "Prototype / reference data only.\n\n"
    "This is not a live operational monitoring system."
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div style="
        background: linear-gradient(135deg,#063970,#087ea4);
        padding: 30px;
        border-radius: 15px;
        color: white;
        margin-bottom: 25px;
    ">
        <h1 style="margin:0;">💧 HYDROVERSE</h1>
        <h3 style="margin-top:8px;">
            Hyderabad Water & Sewerage Intelligence Prototype
        </h3>
        <p>
            Integrated visualization of water sources, treatment,
            distribution, sewerage, STPs and water-balance analytics.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    st.header("Executive Dashboard")

    total_sources = len(sources)
    surface_total = sources["Contribution"].sum()
    groundwater_value = 8
    total_modeled = surface_total + groundwater_value

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Principal Water Sources",
        total_sources,
    )

    c2.metric(
        "Surface Water",
        f"{surface_total} units",
    )

    c3.metric(
        "Groundwater / Local",
        f"{groundwater_value} units",
    )

    c4.metric(
        "Modeled Total",
        f"{total_modeled} units",
    )

    st.markdown("---")

    left, right = st.columns(2)

    with left:

        fig = px.bar(
            sources,
            x="Source",
            y="Contribution",
            title="Indicative Source Contribution",
            color="Contribution",
            color_continuous_scale="Blues",
        )

        fig.update_layout(
            xaxis_title="",
            yaxis_title="Indicative Contribution",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    with right:

        st.subheader("HYDROVERSE Concept")

        st.info(
            """
            HYDROVERSE models Hyderabad's water system as a connected
            lifecycle rather than isolated datasets.

            **Source → Intake → Treatment → Distribution → Household**

            followed by:

            **Household → Sewerage → STP → Reuse / Discharge**
            """
        )

        st.subheader("Core Capabilities")

        st.write("🗺️ Spatial water-source visualization")
        st.write("💧 Water-source register")
        st.write("🚰 End-to-end water journey")
        st.write("♻️ Sewerage and STP lifecycle")
        st.write("⚖️ Water-balance simulation")
        st.write("📊 Source analytics")
        st.write("🏗️ Future BigQuery / GIS / IoT architecture")


# =========================================================
# WATER SOURCE MAP
# =========================================================

elif page == "Water Source Map":

    st.header("🗺️ Hyderabad Water Source Map")

    st.info(
        "The map separates principal physical water sources from "
        "augmentation and groundwater layers."
    )

    show_sources = st.checkbox(
        "Show Principal Sources",
        value=True,
    )

    show_mallanna = st.checkbox(
        "Show Mallanna Sagar Layer",
        value=True,
    )

    show_groundwater = st.checkbox(
        "Show Groundwater / Borewells",
        value=True,
    )

    fig = go.Figure()

    if show_sources:

        fig.add_trace(
            go.Scattergeo(
                lat=sources["Latitude"],
                lon=sources["Longitude"],
                mode="markers+text",
                text=sources["Source"],
                textposition="top center",
                marker=dict(
                    size=13,
                    color="#087ea4",
                    line=dict(
                        width=1,
                        color="white",
                    ),
                ),
                name="Principal Sources",
                hovertemplate=(
                    "<b>%{text}</b><br>"
                    "Latitude: %{lat}<br>"
                    "Longitude: %{lon}"
                    "<extra></extra>"
                ),
            )
        )

    if show_mallanna:

        fig.add_trace(
            go.Scattergeo(
                lat=mallanna["Latitude"],
                lon=mallanna["Longitude"],
                mode="markers+text",
                text=mallanna["Source"],
                textposition="top center",
                marker=dict(
                    size=16,
                    color="#f28e2b",
                    symbol="diamond",
                ),
                name="Mallanna Sagar",
            )
        )

    if show_groundwater:

        fig.add_trace(
            go.Scattergeo(
                lat=groundwater["Latitude"],
                lon=groundwater["Longitude"],
                mode="markers",
                marker=dict(
                    size=9,
                    color="#7b3fb5",
                ),
                text=groundwater["Source"],
                name="Groundwater",
                hovertemplate=(
                    "<b>%{text}</b>"
                    "<extra></extra>"
                ),
            )
        )

    fig.update_geos(
        projection_type="mercator",
        center=dict(
            lat=17.5,
            lon=78.5,
        ),
        lataxis_range=[15.5, 20.0],
        lonaxis_range=[75.5, 81.0],
        showcountries=True,
        showland=True,
        landcolor="#eef3f5",
        showocean=True,
        oceancolor="#dceff7",
        
    )

    fig.update_layout(
        height=650,
        margin=dict(
            l=0,
            r=0,
            t=30,
            b=0,
        ),
        title="Hyderabad Water Source Network",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    st.subheader("Principal Sources")

    st.dataframe(
        sources[
            [
                "Source",
                "Type",
                "Contribution",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )


# =========================================================
# WATER JOURNEY
# =========================================================

elif page == "Water Journey":

    st.header("🚰 Water Journey")

    st.info(
        "HYDROVERSE represents water as a complete urban lifecycle."
    )

    st.subheader("Drinking Water")

    stages = [
        ("💧", "SOURCE", "Reservoir / river system"),
        ("⬇️", "INTAKE", "Raw-water abstraction"),
        ("🧪", "TREATMENT", "Water treatment"),
        ("🚰", "DISTRIBUTION", "Network delivery"),
        ("🏠", "HOUSEHOLD", "Consumer"),
    ]

    cols = st.columns(5)

    for col, stage in zip(cols, stages):

        icon, title, description = stage

        with col:

            st.markdown(
                f"""
                <div style="
                    background:#ffffff;
                    padding:20px;
                    border-radius:12px;
                    border:1px solid #dce7ef;
                    text-align:center;
                    min-height:150px;
                ">
                    <div style="font-size:35px;">{icon}</div>
                    <b>{title}</b>
                    <p>{description}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("")

    st.subheader("Sewerage & Reuse")

    sewer = [
        ("🏠", "HOUSEHOLD", "Used water"),
        ("🕳️", "SEWERAGE", "Collection"),
        ("🏭", "STP", "Treatment"),
        ("♻️", "REUSE", "Treated water"),
        ("🌊", "DISCHARGE", "Permitted discharge"),
    ]

    cols = st.columns(5)

    for col, stage in zip(cols, sewer):

        icon, title, description = stage

        with col:

            st.markdown(
                f"""
                <div style="
                    background:#ffffff;
                    padding:20px;
                    border-radius:12px;
                    border:1px solid #dce7ef;
                    text-align:center;
                    min-height:150px;
                ">
                    <div style="font-size:35px;">{icon}</div>
                    <b>{title}</b>
                    <p>{description}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("---")

    st.subheader("Conceptual Flow")

    st.code(
        """
SOURCE
   ↓
INTAKE
   ↓
TREATMENT
   ↓
DISTRIBUTION
   ↓
HOUSEHOLDS
   ↓
SEWERAGE
   ↓
STP
   ↓
TREATED WATER
   ↓
REUSE / DISCHARGE
        """,
        language="text",
    )


# =========================================================
# WATER BALANCE
# =========================================================

elif page == "Water Balance":

    st.header("⚖️ Water Balance Simulator")

    st.info(
        "Adjust the parameters to see how supply, losses and demand "
        "affect the modeled balance."
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        availability = st.slider(
            "Source Availability",
            50,
            150,
            100,
            5,
        )

    with col2:

        losses = st.slider(
            "Distribution Losses (%)",
            0,
            40,
            15,
            1,
        )

    with col3:

        demand = st.slider(
            "Demand",
            40,
            140,
            80,
            5,
        )

    effective_supply = availability * (
        1 - losses / 100
    )

    balance = effective_supply - demand

    st.markdown("---")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Availability",
        f"{availability:.1f}",
    )

    c2.metric(
        "Effective Supply",
        f"{effective_supply:.1f}",
    )

    c3.metric(
        "Demand",
        f"{demand:.1f}",
    )

    c4.metric(
        "Balance",
        f"{balance:.1f}",
    )

    if balance > 0:

        st.success(
            f"Modeled surplus: {balance:.1f} units."
        )

    elif balance < 0:

        st.error(
            f"Modeled deficit: {abs(balance):.1f} units."
        )

    else:

        st.warning(
            "Supply and demand are balanced."
        )

    chart_data = pd.DataFrame({
        "Category": [
            "Source Availability",
            "Losses",
            "Effective Supply",
            "Demand",
        ],
        "Value": [
            availability,
            availability * losses / 100,
            effective_supply,
            demand,
        ],
    })

    fig = px.bar(
        chart_data,
        x="Category",
        y="Value",
        color="Category",
        title="Water Balance Components",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    st.caption(
        "All simulator values are illustrative."
    )


# =========================================================
# SOURCE ANALYTICS
# =========================================================

elif page == "Source Analytics":

    st.header("📊 Source Analytics")

    col1, col2 = st.columns(2)

    with col1:

        fig = px.pie(
            sources,
            names="Source",
            values="Contribution",
            title="Indicative Source Contribution",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    with col2:

        ordered = sources.sort_values(
            "Contribution"
        )

        fig = px.bar(
            ordered,
            x="Contribution",
            y="Source",
            orientation="h",
            title="Source Contribution",
            color="Contribution",
            color_continuous_scale="Blues",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    st.info(
        """
        In a production system, this analytics layer could consume
        validated historical and real-time measurements to support
        demand analysis, source dependency analysis, anomaly detection
        and operational planning.
        """
    )


# =========================================================
# SOURCE REGISTER
# =========================================================

elif page == "Source Register":

    st.header("🗂️ Source Register")

    register = sources.copy()

    register.insert(
        0,
        "Source ID",
        [
            "HYD-001",
            "HYD-002",
            "HYD-003",
            "HYD-004",
            "HYD-005",
            "HYD-006",
        ],
    )

    register["Data Status"] = "Prototype / Reference"

    st.dataframe(
        register,
        use_container_width=True,
        hide_index=True,
    )

    csv = register.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "⬇️ Download Source Register",
        csv,
        "hydroverse_source_register.csv",
        "text/csv",
    )

    st.subheader("Suggested Production Schema")

    st.code(
        """
source_id
source_name
source_type
latitude
longitude
project_phase
operator
capacity
status
data_source
data_quality
last_updated
geometry
        """,
        language="text",
    )


# =========================================================
# ARCHITECTURE
# =========================================================

elif page == "Architecture":

    st.header("🏗️ Future Production Architecture")

    st.info(
        "Streamlit represents the prototype presentation layer. "
        "A production implementation would separate ingestion, "
        "storage, spatial data, analytics and presentation."
    )

    st.code(
        """
              DATA SOURCES
                    │
        ┌───────────┼───────────┐
        │           │           │
       GIS       IoT/SCADA   APIs/CSV
        │           │           │
        └───────────┼───────────┘
                    ↓
             DATA INGESTION
                 ETL/ELT
                    ↓
                BIGQUERY
                    │
          ┌─────────┴─────────┐
          │                   │
       SPATIAL             TIME SERIES
        DATA                   DATA
          │                   │
          └─────────┬─────────┘
                    ↓
             ANALYTICS / ML
                    │
       ┌────────────┼────────────┐
       │            │            │
 Water Balance   Demand      Anomaly
                 Model      Detection
       │            │            │
       └────────────┼────────────┘
                    ↓
             HYDROVERSE UI
                STREAMLIT
        """,
        language="text",
    )

    st.subheader("Prototype → Production")

    architecture_data = pd.DataFrame({
        "Area": [
            "Frontend",
            "Data",
            "Spatial",
            "Real-time",
            "Analytics",
            "Data Quality",
        ],
        "Prototype": [
            "Streamlit",
            "Reference data",
            "Plotly map",
            "Not connected",
            "Rule-based simulation",
            "Manual classification",
        ],
        "Production Direction": [
            "Web application / Streamlit",
            "BigQuery",
            "GIS",
            "IoT / SCADA",
            "Forecasting / ML",
            "Automated validation",
        ],
    })

    st.dataframe(
        architecture_data,
        use_container_width=True,
        hide_index=True,
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "HYDROVERSE | Hyderabad Water & Sewerage Intelligence Prototype "
    "| Prototype/reference data only"
)
