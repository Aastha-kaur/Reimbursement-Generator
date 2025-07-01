import pandas as pd

def calculate_reimbursement(study_name, transport_method, distance, duration, scan_required=False, has_caregiver=False):
    caps_df = pd.read_excel("data/studies_caps.xlsx")
    caps_df.columns = caps_df.columns.str.strip()
    cap = caps_df[caps_df["study_name"] == study_name].squeeze()

    if pd.notna(cap.get("travel_cap_total")):
        return float(cap["travel_cap_total"])

    mileage_rate = float(cap.get("travel_cap_mileage", 0)) if transport_method != "public" else 0
    parking = float(cap.get("travel_cap_parking", 0)) if transport_method != "public" else 0
    meal = float(cap.get("meal_cap_pt", 0)) if duration > 3 else 0

    km_reimbursement = distance * mileage_rate
    total = km_reimbursement + parking + meal
    return round(total, 2)
