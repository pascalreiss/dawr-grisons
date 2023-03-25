import pandas as pd

from wikipedia_crawler import getListOfMuncipalities

from util import getPathDynamically
from util import read_csv
from util import create_csv

def merge_DataFrames_and_save() -> None:
    muncipalities_general_path = getPathDynamically('raw_data', 'gemeinde_allgemein.xlsx')

    df = pd.read_excel(muncipalities_general_path, header=None, skiprows=9, index_col=None, 
                       skipfooter=16, usecols=lambda column: column != 0, )
    df.columns = ['Gemeinde_Name', 'Einwohner', 'Einwohneraenderung', 'Bevoelkerungsdichte_pro_km2', 
                                'Auslaender_in_prozent', 'Zero_to_Nineteen', 'Twenty_to_Sixtyfour', 'Sixtyfive_and_more', 
                                'Marriage', ' Divorce', 'Birth', 'Death', 'Household', 'Household_size_average', 'area', 
                                'settled_area_percentage', 'settled_area_chagne_in_ha', 'agricultural_area_percentage', 
                                'agricultural_area_change_in_ha', 'woods_area_percentage', 'unproductive_area_percentage',
                                'Workers_total', 'first_sector_Workers_total', 'second_sector_Workers_total',
                                'third_sector_Workers_total', 'Workplaces_total', 'first_sector_Workplaces_total',
                                'second_sector_Workplaces_total', 'third_sector_Workplaces_total', 'Empty_Appartments_Number',
                                'New_homes_per_1000_inhabitants', 'Socialsecurity_in_Percent', 'FDP', 'CVP', 'SP', 'SVP', 'EVP_CSP',
                                'GLP', 'BDP', 'PdA_Sol', 'GPS', 'Small_parties']
    # In case the wikipedia_crawler wasnt run before i do not directly read the file containing the muncipalities as it could not exists yet in some casesd
    relevant_muncipalities = getListOfMuncipalities()
    df = df[df['Gemeinde_Name'].isin(relevant_muncipalities)]

    abstimmung_df = read_csv('raw_data', 'anderung-vom-19-maerz-2021-des-covid-19-gesetzes.csv')
    abstimmung_df = abstimmung_df.rename(columns={'name':'Gemeinde_Name'})
   
    famous_people_df = read_csv('generated_data', 'famous_people.csv')
    famous_people_df_grouped = famous_people_df.groupby('Gemeinde_Name')['Famous_Person'].agg([('Famous_Person_list', lambda x: '|'.join(x)), ('Famous_Person_count', 'count')]).reset_index()

    dfs = [df, abstimmung_df, famous_people_df_grouped]
    big_boy_df = dfs[0]
    for df in dfs[1:]:
        big_boy_df = pd.merge(big_boy_df, df, on='Gemeinde_Name', how='outer')

    create_csv('data', 'combined_data_set.csv', big_boy_df, index=False, overwrite=True)