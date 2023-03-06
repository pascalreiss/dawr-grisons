import os
import requests
import pandas as pd
import wikipediaapi
from bs4 import BeautifulSoup as bs
from typing import List
from pathlib import Path

wiki = wikipediaapi.Wikipedia(
    language='de',
    extract_format=wikipediaapi.ExtractFormat.WIKI
)

def getListOfMuncipalities() -> List[str]:
    url = 'https://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Graub%C3%BCnden'
    req = requests.get(url)
    soup = bs(req.text, "html.parser")
    muncipalities = []
    for tr in soup.find_all('td')[1::8]:
        a = tr.find('a')
        muncipalities.append(a.text)
    
    municpalities_file = Path('./data/muncipalities.csv')
    if (not municpalities_file.exists()):
        df = pd.DataFrame(muncipalities, columns=['name'])
        df.to_csv('./data/muncipalities.csv', index=False)
    
    return muncipalities




def main() -> None:
    muncipalities = getListOfMuncipalities()
    for municpality in muncipalities:
        content = wiki.page(municpality)
        if (not content.exists):
            continue
        
        print(content.section_by_title('Persönlichkeiten').text)
main()