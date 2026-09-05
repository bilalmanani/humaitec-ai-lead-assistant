import pandas as pd
import streamlit as st

from app.database.leads_db import Lead, SessionLocal


st.set_page_config(
    page_title="HUMAITEC Lead Dashboard",
    page_icon="📊",
    layout="wide",
)


def get_leads():
    session = SessionLocal()

    leads = session.query(Lead).order_by(
        Lead.created_at.desc()
    ).all()

    session.close()

    return [
        {
            "ID": lead.id,
            "Business": lead.business,
            "Requirement": lead.requirement,
            "Recommended Service": lead.recommended_service,
            "Timeline": lead.timeline,
            "Budget": lead.budget,
            "Status": lead.lead_status,
            "Summary": lead.summary,
            "Next Action": lead.next_action,
            "Created At": lead.created_at,
        }
        for lead in leads
    ]


st.title("HUMAITEC AI Lead Dashboard")
st.caption("AI-qualified client leads")

leads = get_leads()
dataframe = pd.DataFrame(leads)

if dataframe.empty:
    st.warning("No leads are available yet.")
    st.stop()

total_leads = len(dataframe)
hot_leads = len(dataframe[dataframe["Status"] == "HOT"])
warm_leads = len(dataframe[dataframe["Status"] == "WARM"])
cold_leads = len(dataframe[dataframe["Status"] == "COLD"])

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Leads", total_leads)
col2.metric("HOT Leads", hot_leads)
col3.metric("WARM Leads", warm_leads)
col4.metric("COLD Leads", cold_leads)

st.divider()

selected_statuses = st.multiselect(
    "Filter by lead status",
    options=["HOT", "WARM", "COLD"],
    default=["HOT", "WARM", "COLD"],
)

filtered_data = dataframe[
    dataframe["Status"].isin(selected_statuses)
]

st.subheader("Recent Leads")

st.dataframe(
    filtered_data[
        [
            "Business",
            "Requirement",
            "Recommended Service",
            "Timeline",
            "Budget",
            "Status",
            "Next Action",
        ]
    ],
    use_container_width=True,
)

st.subheader("Most Requested Services")

service_counts = (
    dataframe["Recommended Service"]
    .value_counts()
    .reset_index()
)

service_counts.columns = ["Service", "Number of Leads"]

st.bar_chart(
    service_counts.set_index("Service")
)

st.subheader("Lead Details")

selected_business = st.selectbox(
    "Select a lead",
    options=dataframe["Business"].tolist(),
)

selected_lead = dataframe[
    dataframe["Business"] == selected_business
].iloc[0]

st.write("**Requirement:**", selected_lead["Requirement"])
st.write("**Recommended Service:**", selected_lead["Recommended Service"])
st.write("**Timeline:**", selected_lead["Timeline"])
st.write("**Budget:**", selected_lead["Budget"])
st.write("**Lead Status:**", selected_lead["Status"])
st.write("**Summary:**", selected_lead["Summary"])
st.write("**Next Action:**", selected_lead["Next Action"])