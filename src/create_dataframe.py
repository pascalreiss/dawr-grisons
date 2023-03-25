from pathlib import Path
import pandas as pd
import regex as re
from wikipedia_crawler import getListOfMuncipalities

def main() -> None:
    gov_file_path = Path('./raw_data/gemeinde_allgemein.xlsx')
    if not gov_file_path.exists():
        return

    df = pd.read_excel(gov_file_path, header=None, skiprows=9, index_col=None, 
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

    #Not consistant between wikipedia and admin dataset
    relevant_muncipalities.append('Roveredo (GR)')

    df['Gemeinde_Name'] = df['Gemeinde_Name'].apply(lambda x: re.sub(r'\p{C}', '', x))

    # Here regex matching is used so () are an issue, interestingly it works with the newly added entry, but does not if I add the others it can not find
    df = df[df['Gemeinde_Name'].isin(relevant_muncipalities)]


    erkannte_gemeinden = df['Gemeinde_Name'].tolist()
    rest = set(relevant_muncipalities) - set(erkannte_gemeinden)
    print(rest)
    ...




main()