import pandas as pd
from io import BytesIO

def process_files(file_dict):
    kcb = pd.read_excel(file_dict.get("KCB"))
    equity = pd.read_excel(file_dict.get("EQUITY"))
    aspire = pd.read_excel(file_dict.get("ASPIRE"))
    card_key = pd.read_excel(file_dict.get("CARD_KEY"))

    # --- Place your FinalCards.ipynb logic here ---
    # For demonstration, this part returns dummy merged data
    merged = pd.concat([kcb, equity, aspire], ignore_index=True)
    merged["source"] = ["KCB"] * len(kcb) + ["EQUITY"] * len(equity) + ["ASPIRE"] * len(aspire)

    # Example Excel output
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        merged.to_excel(writer, index=False, sheet_name="Merged_Recs")

    output.seek(0)
    return merged, output
