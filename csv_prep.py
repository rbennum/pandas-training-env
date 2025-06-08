import pandas as pd

excel_file = 'supply-chain.xlsx'

excel = pd.ExcelFile(excel_file)

sheet_names = excel.sheet_names

for sheet in sheet_names:
    df = pd.read_excel(excel_file, sheet_name=sheet)
    csv_filename = f'{sheet}.csv'
    df.to_csv(csv_filename, index=False)
    print(f'Saved {sheet} to {csv_filename}')

print('Conversion complete!')