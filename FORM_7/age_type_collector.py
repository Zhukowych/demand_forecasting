import os
import pandas as pd


CATEGORY_FIRST_INDEX = 9
VD = 29
NUMBER_OF_CATEGORIES = 113


def create_data_frame(year:int, category_title: str, df: pd.DataFrame) -> pd.DataFrame:

    rows = []
    for i in range(df.shape[0]):
        for j in range(df.shape[1]):  
            rows.append(
                (year, category_title, regions.iloc[i], age_groups.iloc[j], df.iloc[i, j])
            )
    return pd.DataFrame(rows, columns=["year", "category", "region", "age_group", "incidence"])


df = pd.read_excel("2008.xls", engine="xlrd", names=range(24))

regions = df.iloc[11:38,1]
age_groups = df.iloc[7, 3:23]

dataframes = []

for file in os.listdir('.'):
    if not file.endswith("xls"):
        continue

    year = int(file.split('.')[0])
    print("Year", year)

    df = pd.read_excel(file, engine="xlrd", names=range(24))

    current_regions = df.iloc[11:38,1]
    current_age_groups = df.iloc[7, 3:23]

    current_regions = list(current_regions)
    current_regions[0] = 'Автономна pеспубліка Крим'
    current_regions[-1] = current_regions[-1].replace(' ', '')

    if list(current_regions) != list(regions):
        print("Base", list(regions))
        print("Current", list(current_regions))
        raise Exception(f"{year} regions are not consistent")

    for i in range(NUMBER_OF_CATEGORIES):
        category_title = df.iloc[CATEGORY_FIRST_INDEX + i * VD, 1]

        start_ind = CATEGORY_FIRST_INDEX + i * VD + 2
        end_ind = CATEGORY_FIRST_INDEX + (i+1) * VD 
    
        category_data = df.iloc[start_ind:end_ind, 3:23]

        dataframes.append(create_data_frame(year=year, category_title=category_title, df=category_data))

full_data_frame = pd.concat(dataframes)
full_data_frame.to_csv("incidence.csv", index_label=False)
