import streamlit as st
import pandas as pd
from io import StringIO
from snowflake.snowpark.context import get_active_session
#from get_detection_summary import get_detection_summary

# Snowflake connection
session = get_active_session()

st.title("Detection Summary")

# Load study codes
# with open("study_codes.txt", "r") as f:
all_codes = []
all_codes.append("all")

study_code = st.selectbox("Select a study code", all_codes)

accessioning_fields = [
    "indication",
    "cohort",
    "timepoint",
    "timepoint_description",
    "collection_date",
    "received_date",
    "approve_date",
]
accessioning_details = st.multiselect(
    "Select accessioning fields to include in the final report", accessioning_fields
)
exclude_no_detection = st.checkbox("Exclude samples without detection results")
minimum_targets = st.number_input(
    "Minimum number of targets for detection", min_value=1, value=500
)

if "raw_report" not in st.session_state:
    st.session_state.raw_report = None
    st.session_state.filtered_report = None

generate_report = st.button("Generate report")

if generate_report:
    with st.spinner("Generating report... please wait"):
        # with open("detection_results.sql", encoding="utf-8") as f:
        #     query = f.read()
        # query = query.replace("study_code_placeholder", f"'{study_code}'")

        # detection_data = session.sql(query).to_pandas()

        filtered_reportIO = StringIO('''
        "Month", "1958", "1959", "1960"
        "JAN",  340,  360,  417
        "FEB",  318,  342,  391
        "MAR",  362,  406,  419
        "APR",  348,  396,  461
        ''')
        filtered_report = pd.read_csv(filtered_reportIO)

        raw_reportIO = StringIO('''
        "Month", "1958", "1959", "1960"
        "MAY",  363,  420,  472
        "JUN",  435,  472,  535
        "JUL",  491,  548,  622
        "AUG",  505,  559,  606
        ''')
        raw_report = pd.read_csv(raw_reportIO)
        st.session_state.raw_report = raw_report
        st.session_state.filtered_report = filtered_report

if st.session_state.raw_report is not None:
    st.success("Report generated!")
    
    raw_csv = st.session_state.raw_report.to_csv(index=False).encode("utf-8")
    filtered_csv = st.session_state.filtered_report.to_csv(index=False).encode("utf-8")

    st.download_button("Download raw report", raw_csv, "raw_report.csv", mime="text/csv")
    st.download_button("Download filtered report", filtered_csv, "filtered_report.csv", mime="text/csv")
 
