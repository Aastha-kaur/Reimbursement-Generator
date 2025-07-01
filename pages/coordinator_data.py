import streamlit as st
import os
from utils.data_loader import load_participants, mark_attendance, save_reimbursement
from utils.reimbursement import calculate_reimbursement
from utils.maps import generate_google_maps_link

def show_coordinator_view():
    st.title("Coordinator / Participant Visit Management")

    participants_df = load_participants()
    st.header("📅 Calendar View by Study")
    selected_study = st.selectbox("Choose Study", participants_df['study_name'].unique())
    filtered = participants_df[participants_df['study_name'] == selected_study]

    for idx, row in filtered.iterrows():
        with st.expander(f"{row['participant_name']} | Visit {row['visit_id']}"):
            st.write(f"**Hospital:** {row['hospital_name']}")
            st.write(f"**Transport:** {row['transport_method']}")
            st.write(f"**Distance:** {row['distance']} km")

            st.markdown(f"[🗺️ View Route]({generate_google_maps_link(row['participant_address'], row['hospital_address'])})")

            if st.checkbox("Mark as Attended", key=f"attended_{row['visit_id']}_{idx}"):
                mark_attendance(row['visit_id'])

                reimbursement = calculate_reimbursement(
                    row['study_name'],
                    row['transport_method'],
                    row['distance'],
                    row['visit_duration'],
                    row['scan_required'],
                    row['has_caregiver']
                )

                st.success(f"Reimbursement: ${reimbursement:.2f}")

                # Receipt Upload Section
                st.markdown("### Upload Receipts (Meal / Parking / Accommodation)")
                files = st.file_uploader("Upload receipt files", type=['pdf', 'jpg', 'png'], accept_multiple_files=True)

                if files:
                    receipt_dir = f"receipts/{row['participant_id']}"
                    os.makedirs(receipt_dir, exist_ok=True)
                    for file in files:
                        ext = file.name.split('.')[-1]
                        out_path = os.path.join(receipt_dir, f"{row['visit_id']}_{file.name}")
                        with open(out_path, "wb") as f:
                            f.write(file.getbuffer())
                    st.success("Receipts uploaded.")

                if st.button("Submit Claim", key=f"submit_{row['visit_id']}_{idx}"):
                    save_reimbursement(row['participant_id'], row['visit_id'], reimbursement)
                    st.success("Claim submitted to Admin.")
