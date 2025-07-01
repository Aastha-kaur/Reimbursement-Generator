import streamlit as st
import os
from utils.data_loader import get_merged_reimbursements, load_study_caps
from utils.maps import generate_google_maps_link
from utils.digital_signature import sign_claim

def show_admin_finance():
    st.title("🧾 Admin / Finance Dashboard")

    st.subheader("📊 Study Caps Overview")
    try:
        study_caps = load_study_caps()
        st.dataframe(study_caps, use_container_width=True)
    except Exception as e:
        st.error(f"Failed to load study caps: {e}")

    st.subheader("📋 Reimbursement Claims for Approval")
    try:
        claims_df = get_merged_reimbursements()
        pending_claims = claims_df[claims_df['status'] == 'Submitted']

        if pending_claims.empty:
            st.info("✅ No pending claims to approve.")
            return

        for idx, row in pending_claims.iterrows():
            with st.expander(f"{row.get('participant_name', 'Unknown')} | Visit {row.get('visit_id')} | {row.get('study_name', 'N/A')}"):
                st.write(f"**Distance:** {row.get('distance', 'N/A')} km")
                st.write(f"**Claimed Amount:** ${row.get('total_reimbursement', 0):.2f}")
                st.write(f"**Hospital:** {row.get('hospital_name', 'N/A')}")
                st.markdown(f"[📍 Google Maps Link]({generate_google_maps_link(row.get('participant_address'), row.get('hospital_address'))})")

                # Show uploaded receipts
                receipt_folder = f"receipts/{row['participant_id']}"
                st.markdown("### 📎 Uploaded Receipts")
                if os.path.exists(receipt_folder):
                    visit_files = [f for f in os.listdir(receipt_folder) if row['visit_id'] in f]
                    if visit_files:
                        for file in visit_files:
                            file_path = f"{receipt_folder}/{file}"
                            if file.lower().endswith((".png", ".jpg", ".jpeg")):
                                st.image(file_path, width=300)
                            elif file.lower().endswith(".pdf"):
                                with open(file_path, "rb") as f:
                                    st.download_button("📄 View PDF", f, file_name=file, mime="application/pdf", key=file)
                    else:
                        st.info("No receipts found for this visit.")
                else:
                    st.info("No receipt folder for this participant.")

                if st.button(f"✅ Approve Visit {row['visit_id']}", key=f"approve_{row['visit_id']}_{idx}"):
                    sign_claim(row['participant_id'], row['visit_id'])
                    st.success("Approved and signed!")
    except Exception as e:
        st.error(f"Error loading claims: {e}")
