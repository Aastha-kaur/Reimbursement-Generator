import streamlit as st
from utils.data_loader import get_merged_reimbursements
from utils.invoice_pdf import generate_invoice_pdf

def show_invoice_generator():
    st.title("📄 Reimbursement Invoice Generator")

    try:
        df = get_merged_reimbursements()
    except Exception as e:
        st.error(f"Error loading merged data: {e}")
        return

    participants = df['participant_id'].dropna().unique()
    selected_pid = st.selectbox("Select Participant", participants)

    visit_ids = df[df['participant_id'] == selected_pid]['visit_id'].unique()
    selected_vid = st.selectbox("Select Visit", visit_ids)

    visit = df[(df['participant_id'] == selected_pid) & (df['visit_id'] == selected_vid)].iloc[0]

    st.subheader(f"Invoice Preview for Visit {visit['visit_id']}")
    st.write(f"**Participant:** {visit.get('participant_name', 'N/A')}")
    st.write(f"**Study:** {visit.get('study_name', 'N/A')}")
    st.write(f"**Date:** {visit.get('visit_date', 'N/A')}")
    st.write(f"**Distance:** {visit.get('distance', 'N/A')} km")
    st.write(f"**Claimed Amount:** ${visit.get('total_reimbursement', 0.00):.2f}")

    if st.button("🧾 Generate Invoice PDF"):
        pdf = generate_invoice_pdf(visit)
        st.download_button(
            label="📥 Download Invoice",
            data=pdf,
            file_name=f"invoice_{visit['visit_id']}.pdf",
            mime="application/pdf"
        )
