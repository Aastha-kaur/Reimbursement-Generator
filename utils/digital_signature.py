# utils/digital_signature.py
import pandas as pd

def sign_claim(visit_id, approver):
    df = pd.read_excel("data/reimbursements.xlsx")
    df.loc[df["visit_id"] == visit_id, "status"] = "Approved"
    df.loc[df["visit_id"] == visit_id, "approved_by"] = approver
    df.to_excel("data/reimbursements.xlsx", index=False)
