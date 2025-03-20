import os
import pandas as pd


CATEGORY_FIRST_INDEX = 10
VD = 29
NUMBER_OF_CATEGORIES = 29


df = pd.read_excel("2008.xls", engine="xlrd", names=range(20), sheet_name="F470100")

regions = df.iloc[12:39,1]
dataframes = []

for file in os.listdir('.'):
    if not file.endswith("xls"):
        continue

    year = int(file.split('.')[0])
    print("Year", year)

    df = pd.read_excel(file, engine="xlrd", names=range(20), sheet_name="F470100")

    current_regions = list(df.iloc[12:39,1])

    current_regions[0] = 'Автономна pеспубліка Крим'
    current_regions[-1] = current_regions[-1].replace(' ', '')

    if list(current_regions) != list(regions):
        print("Base", list(regions))
        print("Current", list(current_regions))
        raise Exception(f"{year} regions are not consistent")

    for i in range(NUMBER_OF_CATEGORIES):
        try:
            category_title = df.iloc[CATEGORY_FIRST_INDEX + i * VD, 1]
            if isinstance(category_title, float): continue

            start_ind = CATEGORY_FIRST_INDEX + i * VD + 2
            end_ind = CATEGORY_FIRST_INDEX + (i+1) * VD 

            category_data = df.iloc[start_ind:end_ind, 2:23]
            category_df = pd.DataFrame(columns=["year", "category", "region", "nhospotal", "nbeds", "ybeds", "nill", 
                                                "nvillage_ill", "bed_days", "dvisits",
                                                "hvisits", 'ndoctors', 'nnursing'])

            category_df["region"] = regions.values
            category_df["nhospotal"] = category_data.iloc[:, 0].values
            category_df["nbeds"] = category_data.iloc[:, 1].values
            category_df["ybeds"] = category_data.iloc[:, 2].values
            category_df["nill"] = category_data.iloc[:, 3].values
            category_df["nvillage_ill"] = category_data.iloc[:, 4].values
            category_df["bed_days"] = category_data.iloc[:, 5].values
            category_df["dvisits"] = category_data.iloc[:, 6].values
            category_df["hvisits"] = category_data.iloc[:, 7].values
            category_df['ndoctors'] = category_data.iloc[:, 9].values
            category_df['nnursing'] = category_data.iloc[:, 14].values      
            category_df["year"] = year
            category_df["category"] = category_title
        except Exception as ex:
            print(ex)

        dataframes.append(category_df)


full_data_frame = pd.concat(dataframes)
full_data_frame.to_csv("F470100.csv", index=False)

