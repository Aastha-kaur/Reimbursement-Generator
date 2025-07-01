import pandas as pd
import os

# === SAFE LOAD FUNCTIONS ===
def load_participants():
    try:
        df = pd.read_excel("data/participants.xlsx")
        df.columns = df.columns.str.strip()

        # Auto-fix common typo
        if 'partipant_address' in df.columns:
            df.rename(columns={'partipant_address': 'participant_address'}, inplace=True)

        return df
    except PermissionError:
        raise PermissionError("Permission denied: Close 'participants.xlsx' if open in Excel.")
    except Exception as e:
        raise RuntimeError(f"Error loading participants.xlsx: {e}")

def load_reimbursements():
    try:
        df = pd.read_excel("data/reimbursements.xlsx")
        df.columns = df.columns.str.strip()
        return df
    except PermissionError:
        raise PermissionError("Permission denied: Close 'reimbursements.xlsx' if open.")
    except Exception as e:
        raise RuntimeError(f"Error loading reimbursements.xlsx: {e}")

def load_studies():
    try:
        df = pd.read_excel("data/studies.xlsx")
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        raise RuntimeError(f"Error loading studies.xlsx: {e}")

def load_study_caps():
    try:
        df = pd.read_excel("data/studies_caps.xlsx")
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        raise RuntimeError(f"Error loading studies_caps.xlsx: {e}")

# === ATTENDANCE / CLAIM UPDATES ===
def mark_attendance(visit_id):
    df = load_participants()
    df.loc[df['visit_id'] == visit_id, 'attended'] = True
    df.to_excel("data/participants.xlsx", index=False)

def save_reimbursement(participant_id, visit_id, total_reimbursement):
    df = load_reimbursements()

    new_row = {
        "participant_id": participant_id,
        "visit_id": visit_id,
        "total_reimbursement": total_reimbursement,
        "status": "Submitted",
        "receipt_uploaded": True,
        "approved_by": "",
        "approval_date": ""
    }

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_excel("data/reimbursements.xlsx", index=False)

# === MERGED VIEW FOR DASHBOARD USE ===
def get_merged_reimbursements():
    reimbursements = load_reimbursements()
    participants = load_participants()

    print("📄 reimbursements.columns:", reimbursements.columns.tolist())
    print("📄 participants.columns:", participants.columns.tolist())

    merged = pd.merge(
    load_reimbursements(),
    load_participants(),
    on=['participant_id', 'visit_id'],
    how='left'
)

    # Optionally fix study_name column collision
    merged['study_name'] = merged['study_name_x'].combine_first(merged['study_name_y'])


    print("📄 merged.columns:", merged.columns.tolist())
    print("🔍 Preview merged data:")
    print(merged.head())

    required = ['participant_name', 'participant_address', 'distance']
    for col in required:
        if col not in merged.columns:
            raise KeyError(f"'{col}' column is missing in merged dataset — check input files.")

    return merged
