
import pandas as pd
from io import BytesIO

def process_files(file_dict):
    # Load uploaded files
    kcb = pd.read_excel(file_dict.get("KCB"))
    equity = pd.read_excel(file_dict.get("EQUITY"))
    aspire = pd.read_csv(file_dict.get("ASPIRE"))
    key = pd.read_excel(file_dict.get("CARD_KEY"))

    # === Start of original notebook logic ===

    # Example transformation (add your full logic here)
    kcb['Source'] = 'KCB'
    equity['Source'] = 'EQUITY'
    aspire['Source'] = 'ASPIRE'

    # Normalize column names
    for df in [kcb, equity, aspire]:
        df.columns = df.columns.str.strip().str.upper()

    # Combine all sources
    merged_cards = pd.concat([kcb, equity, aspire], ignore_index=True)

    # Create 'card_check' for matching
    merged_cards['CARD_NUMBER'] = merged_cards['CARD_NUMBER'].astype(str)
    merged_cards['CARD_CHECK'] = merged_cards['CARD_NUMBER'].str[:4] + merged_cards['CARD_NUMBER'].str[-4:]

    # Clean 'key' file for VLOOKUP
    key['COL_1'] = key['COL_1'].astype(str).str.strip().str.upper()
    key['COL_2'] = key['COL_2'].astype(str).str.strip()

    # VLOOKUP branch using card_key
    merged_cards['STORE'] = merged_cards['STORE'].astype(str).str.strip().str.upper()
    merged_cards.drop(columns=['BRANCH'], errors='ignore', inplace=True)

    merged_cards = merged_cards.merge(
        key[['COL_1', 'COL_2']],
        how='left',
        left_on='STORE',
        right_on='COL_1'
    )
    merged_cards.rename(columns={'COL_2': 'BRANCH'}, inplace=True)
    merged_cards.drop(columns=['COL_1'], inplace=True)

    # Drop duplicates
    merged_cards.drop_duplicates(inplace=True)

    # === End of logic ===

    # Create downloadable Excel
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        merged_cards.to_excel(writer, index=False, sheet_name="Final_Report")

    output.seek(0)
    return merged_cards, output
