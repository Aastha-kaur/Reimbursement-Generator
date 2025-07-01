# main_app.py

import streamlit as st

# Import the page views
from pages import admin_finance, coordinator_data, invoice_generator

# Configure Streamlit page
st.set_page_config(
    page_title="ARA Clinical Trial Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# App Title & Logo
st.sidebar.image("assets/logo.png", use_column_width=True)
st.sidebar.title("Clinical Trial Dashboard")

# Sidebar Navigation
pages = {
    "Admin / Finance": admin_finance.show_admin_finance,
    "Coordinator / Participant Data View": coordinator_data.show_coordinator_view,
    "Reimbursement Invoice Generator": invoice_generator.show_invoice_generator
}

selection = st.sidebar.radio("Navigate to", list(pages.keys()))
st.sidebar.markdown("---")
st.sidebar.caption("Developed for ARA | Secure Internal Tool")

# Call the selected page
pages[selection]()
