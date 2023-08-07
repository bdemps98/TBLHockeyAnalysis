import pandas as pd
import datetime as dt

# The year in which the Tampa Bay Lightning were founded
FOUNDED = 1993

# Used to get the current year
TODAY = dt.datetime.now()

# Path to the raw data
RAW_PATH = r"C:\Users\braed\Desktop\TBL Hockey Analysis\Raw Data\player_data.xlsx"

# Path to the cleaned data
CLEAN_PATH = r"C:\Users\braed\Desktop\TBL Hockey Analysis\Cleaned Data\player_data.xlsx"

# Load the Excel file into a DataFrame
df = pd.read_excel(RAW_PATH, sheet_name=None)

# Loop through the specified years processes the DataFrames
scrubbed_df = {}
for year in range(FOUNDED, TODAY.year() + 1):
    sheet = str(year)
    if sheet in df:
        # Remove rows with all zeros in specific columns
        df = df[sheet]
        columns_to_check = ['games_played', 'goals', 'assists', 'points', 'plus_minus', 'pen_min']
        mask = (df[columns_to_check] != 0).any(axis=1)
        scrubbed_df = df[mask]
        
        # Trunctuating the DataFrame from "Team Total" row and beyond
        try:
            total_row_index = scrubbed_df[scrubbed_df['player'] == 'Team Total'].index[0]
            scrubbed_df = scrubbed_df.iloc[:total_row_index]
        except IndexError:
            pass
        
        scrubbed_df[sheet] = scrubbed_df

# Update the Excel file with the scrubbed data
with pd.ExcelWriter(CLEAN_PATH, engine='xlsxwriter') as excel_writer:
    for sheet, scrubbed_df in scrubbed_df.items():
        scrubbed_df.to_excel(excel_writer, sheet_name=sheet, index=False)

print(f"Data has been scrubbed and updated in '{CLEAN_PATH}'.")
