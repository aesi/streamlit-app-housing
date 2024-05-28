import streamlit as st
st.write('# Power BI Dashboard')

dashboard_file_path = "housing_dashboard.pbix"

def download_dashboard():
    with open(dashboard_file_path, 'rb') as f:
        dashboard_data = f.read()
    st.download_button(label="Download Dashboard", data=dashboard_data, file_name="dashboard.pbix", mime="application/octet-stream")

download_dashboard()

st.image('housing_dashboard.png')