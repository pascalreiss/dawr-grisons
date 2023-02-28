import wikipediaapi
import numpy

wiki_api =  wikipediaapi.Wikipedia(
        language='de',
        extract_format=wikipediaapi.ExtractFormat.WIKI
)


def getListOfMuncipalities() -> numpy.array(str):
    grisons_muncipalities = wiki_api.page('Gemeinden_des_Kantons_Graubünden')

    if (not grisons_muncipalities.exists()):
        raise Exception('Wikipedia page does not exist')

    print(grisons_muncipalities.page('Liste der Gemeinden'))


    return numpy.array()




def main() -> None:
    muncipalities = getListOfMuncipalities()

main()