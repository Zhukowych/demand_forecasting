import os
import pandas as pd

village_dataframes = []
stage_dataframes = []

for file in os.listdir('.'):
    if not file.endswith("xls"):
        continue

    year = int(file.split('.')[0])
    print("Year", year)

    df = pd.read_excel(file, engine="xlrd", names=range(8), sheet_name="F071001")

    village_data = pd.DataFrame(columns=["year",  "region", "male", "female"])
    
    regions = df.iloc[9:35, 1]
    village_male_incidence = df.iloc[9:35, 2]
    village_female_incidence = df.iloc[9:35, 3]

    village_data["region"] = regions
    village_data["male"] = village_male_incidence
    village_data["female"] = village_female_incidence
    village_data["year"] = year

    village_dataframes.append(village_data)

    stage_data = pd.DataFrame(columns=["year",  "region", "mtumors", "syncmtumors", "insitu", "ncervix"])

    stage_data["region"] = regions
    stage_data["mtumors"] = df.iloc[9:35, 4]
    stage_data["syncmtumors"] = df.iloc[9:35, 5]
    stage_data["insitu"] = df.iloc[9:35, 6]
    stage_data["ncervix"] = df.iloc[9:35, 7]
    stage_data["year"] = year

    stage_dataframes.append(stage_data)

pd.concat(village_dataframes).to_csv("village_incidence.csv", index_label=False)
pd.concat(stage_dataframes).to_csv("stage_date.csv", index_label=False)