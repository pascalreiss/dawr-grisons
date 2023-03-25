
import requests
import pandas as pd
import wikipediaapi
from bs4 import BeautifulSoup as bs
from typing import List

from util import getPathDynamically
from util import read_csv
from util import create_csv
from util import create_csv_path

wiki = wikipediaapi.Wikipedia(
    language='de',
    extract_format=wikipediaapi.ExtractFormat.WIKI
)

def getListOfMuncipalities() -> List[str]:
    municpalities_path = getPathDynamically('raw_data', 'muncipalities.csv', check_exists=False)
    municpality_df: pd.DataFrame
    if (municpalities_path.exists()):
        municpality_df = pd.read_csv(municpalities_path)
    else:
        url = 'https://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Graub%C3%BCnden'
        req = requests.get(url)
        soup = bs(req.text, "html.parser")
        muncipalities = []
        for tr in soup.find_all('td')[1::8]:
            a = tr.find('a')
            muncipalities.append(a.text)
    
        municpality_df = pd.DataFrame(muncipalities, columns=['name'])
        create_csv_path(municpalities_path, municpality_df)
    
    return municpality_df.name.tolist()




def main() -> None:
    famous_people_path = getPathDynamically('raw_data', 'famous_people.csv', check_exists=False)
    if famous_people_path.exists():
        return
    muncipalities = getListOfMuncipalities()
    muncipality_of_famous_person = []
    famous_person = []
    for muncipality in muncipalities:
        content = wiki.page(muncipality)
        if (not content.exists):
            continue
        
        if content.section_by_title('Persönlichkeiten') is not None:
            people = content.section_by_title('Persönlichkeiten').full_text().split('\n')
            for person in people:
                if person not in ['Persönlichkeiten', '', 'Wissenschaft:', 'Sport:', 'Ehrenbürger'
                                  , 'Weitere Persönlichkeiten', '(Sortierung nach Geburtsjahr)', 'Kunst/Kultur:'
                                  , 'Politik und Unternehmertum:', 'Wissenschaft: ', 'Kunst/Kultur/Medien:', 'Sport: '
                                  , 'Politik und Unternehmertum: ', 'Söhne und Töchter der Stadt', 'Söhne und Töchter Maienfelds']:
                    famous_person.append(person)
                    # change all instances as the gemeinde_allgemein file uses another name
                    if (muncipality == 'Roveredo'):
                        muncipality = 'Roveredo (GR)'
                    muncipality_of_famous_person.append(muncipality)

    famous_people_df = pd.DataFrame({'Famous_Person': famous_person, 'Gemeinde_Name': muncipality_of_famous_person})
    create_csv('raw_data', 'famous_people.csv', famous_people_df, index=True)

    # after getting all muncipality pages from wikipedia we can now update it to match the name in all ofther files
    muncipalities_df = read_csv('raw_data', 'muncipalities.csv')
    muncipalities_df.loc[muncipalities_df['name'] == 'Roveredo', 'name'] = 'Roveredo (GR)'
    create_csv('raw_data', 'muncipalities.csv', muncipalities_df, index=False, overwrite=True)


main()