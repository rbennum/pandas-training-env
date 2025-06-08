import pandas as pd
from pathlib import Path

def find_project_root(marker_files=['.git', 'requirements.txt']):
    '''
    Find project root by looking for marker files.
    '''
    current = Path.cwd()
    for parent in [current] + list(current.parents):
        for marker in marker_files:
            if (parent / marker).exists():
                return parent
    
    return current # fallback to current directory

PROJECT_ROOT = find_project_root()
DATA_DIR = PROJECT_ROOT / 'datasets'

def load_data(filename: str) -> pd.DataFrame:
    '''
    Load .csv data from the data directory.

    Parameters:
    filename: name of the .csv file to load

    Returns:
    pandas.DataFrame: Loaded dataframe
    '''
    file_path = DATA_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(f'File not found: {file_path}')
    
    try:
        try:
            df = pd.read_csv(file_path)
        except UnicodeDecodeError:
            df = pd.read_csv(file_path, encoding='latin-1')
    except Exception as e:
        raise Exception(f'Error loading {filename}: {str(e)}')
    
    return df

def display_result(result):
    '''Display the result in a formatted way'''
    print('\nResult:')
    print('-' * 50)
    print(result)
    print('-' * 50)