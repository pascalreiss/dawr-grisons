from pathlib import Path
import pandas as pd
import regex as re
from wikipedia_crawler import getListOfMuncipalities

def main() -> None:
    muncipalities_general_path = Path('./raw_data/gemeinde_allgemein.xlsx')
    if not muncipalities_general_path.exists():
        raise FileNotFoundError(f'The file {muncipalities_general_path} could not be found.')

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
    relevant_muncipalities = getListOfMuncipalities()

    df['Gemeinde_Name'] = df['Gemeinde_Name'].apply(lambda x: re.sub(r'\p{C}', '', x))

    # Here regex matching is used so () are an issue, interestingly it works with the newly added entry, but does not if I add the others it can not find
    df = df[df['Gemeinde_Name'].isin(relevant_muncipalities)]

    abstimmung_path = Path('./raw_data/anderung-vom-19-maerz-2021-des-covid-19-gesetzes.csv')
    if not abstimmung_path.exists():
        raise FileNotFoundError(f'The file {muncipalities_general_path} could not be found.')
    abstimmung_df = pd.read_csv(abstimmung_path)
    abstimmung_df = abstimmung_df.rename(columns={'name':'Gemeinde_Name'})
   
    famous_people_path = Path('./raw_data/famous_people.csv')
    if not famous_people_path.exists():
        raise FileNotFoundError(f'The file {famous_people_path} could not be found.')
    famous_people_df = pd.read_csv(famous_people_path)
    famous_people_df_grouped = famous_people_df.groupby('Gemeinde_Name')['Famous_Person'].agg([('Famous_Person_list', lambda x: '|'.join(x)), ('Famous_Person_count', 'count')]).reset_index()

    dfs = [df, abstimmung_df, famous_people_df_grouped]
    big_boy_df = dfs[0]
    for df in dfs[1:]:
        big_boy_df = pd.merge(big_boy_df, df, on='Gemeinde_Name', how='outer')
    big_boy_df_path = Path('./raw_data/combined_data_set.csv')
    big_boy_df.to_csv(big_boy_df_path, mode='w', index=False)




main()