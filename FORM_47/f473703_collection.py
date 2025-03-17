import os
import sys
import pandas as pd


CATEGORY_FIRST_INDEX = 9
VD = 29
NUMBER_OF_CATEGORIES = 2
SHEET_NAME = "F473703"
N_COLUMNS = 4


df = pd.read_excel("2008.xls", engine="xlrd", names=range(N_COLUMNS), sheet_name=SHEET_NAME)

regions = df.iloc[11:38,1]
dataframes = []


for file in os.listdir('.'):
    if not file.endswith("xls"):
        continue

    year = int(file.split('.')[0])
    print("Year", year)

    df = pd.read_excel(file, engine="xlrd", names=range(N_COLUMNS), sheet_name=SHEET_NAME)

    current_regions = list(df.iloc[11:38,1])

    current_regions[0] = 'Автономна pеспубліка Крим'
    current_regions[-1] = current_regions[-1].replace(' ', '')

    if list(current_regions) != list(regions):
        print("Base", list(regions))
        print("Current", list(current_regions))
        raise Exception(f"{year} regions are not consistent")

    for i in range(NUMBER_OF_CATEGORIES):
        category_title = df.iloc[CATEGORY_FIRST_INDEX + i * VD, 1]
        if isinstance(category_title, float): continue

        start_ind = CATEGORY_FIRST_INDEX + i * VD + 2
        end_ind = CATEGORY_FIRST_INDEX + (i+1) * VD 

        category_data = df.iloc[start_ind:end_ind, 2:7]

        category_df = pd.DataFrame(columns=["nvisits", "nhome_visits"])

        category_df["region"] = regions.values
        category_df["year"] = year
        category_df["category"] = category_title
        
        category_df["nvisits"] = category_data.iloc[:, 0].values
        category_df["nhome_visits"] = category_data.iloc[:, 1].values

        dataframes.append(category_df)

full_data_frame = pd.concat(dataframes)
full_data_frame.to_csv("F473703.csv", index=False)

