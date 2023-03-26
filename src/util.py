from pathlib import Path
import pandas as pd
import os

def getPathDynamically(folder: str, file: str, check_exists=True) -> Path:

    current_directory = os.getcwd()
    parent_directory = os.path.dirname(current_directory)
    current_folder = os.path.basename(current_directory)
    parent_folder = os.path.basename(parent_directory)

    path: Path
    # Check in what dir the code is executed
    if (current_folder == 'dawr-grisons'):
        path = Path(os.path.join('.', folder, file))
    elif (current_folder == 'src' and parent_folder == 'dawr-grisons'):
        path = Path(os.path.join('..', folder, file))
    else:
        # code uses dynamic paths so only these two directories work
        raise Exception(f'Please execute .py files while your working directory is either /dawr-grisons or /dawr-grisons/src. Currently it is {current_folder}, which will not work.')
    
    # checks if file exists unless you specifically declare check_exists=False
    if (check_exists and not path.exists()):
        raise FileNotFoundError(f'The file {path} could not be found.')
    return path


def create_csv(folder: str, file:str, df: pd.DataFrame, index=False, overwrite=False) -> None:
    path = getPathDynamically(folder, file, check_exists=False)
    if (not overwrite and not path.exists()):
        df.to_csv(path, index=index, na_rep='0')
    elif (overwrite):
        df.to_csv(path, mode='w', index=index, na_rep='0')

def create_csv_path(path: Path, df: pd.DataFrame, index=False, overwrite=False) -> None:
    if (not overwrite and not path.exists()):
        df.to_csv(path, index=index, na_rep='0')
    if (overwrite):
        df.to_csv(path, mode='w', index=index, na_rep='0')
    

def read_csv(folder: str, file: str) -> pd.DataFrame:
    path = getPathDynamically(folder, file)
    df = pd.read_csv(path, na_values=['---', ''])
    df.replace('---', pd.np.nan, inplace=True)
    df.fillna(value=0, inplace=True)
    return df
