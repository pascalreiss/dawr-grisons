# dawr-grisons
Projekt für das Fach dawr, in welchem ich alle Gemeinden des Kantons Graubünden crawle und mir eine davon Aussuche und einen Bericht darüber schreibe

# Installing all dependencies
To install all dependencies execute `pip install -r requirements.txt` on your terminal in this folder.

# Raw data gathering
Raw data is collected from 3 sources (excel by admin.ch, wikipedia API, opendata.swiss) the data is then combined into a pandas dataframe and saved in the format of a csv file.

# Execute everything yourself
If you want to try all of it yourself, delete the files in the folder `generated_data` and execute the python file `create_complete_data.py` from either `dawr-grisons` or `dawr-grisons\src` it will not work otherwise.

## References
See `references.txt`

# Visualization
Visualizations are made using `matplotlib`


