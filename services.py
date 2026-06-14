import gspread
import pandas as pd
from datetime import datetime

def append_dataframe(df, spreadsheet_id, worksheet_name, credentials_file):
    gc = gspread.service_account(filename=credentials_file)
    spreadsheet = gc.open_by_key(spreadsheet_id)
    worksheet = spreadsheet.worksheet(worksheet_name)

    if not worksheet.get_all_values():
        worksheet.append_row(df.columns.tolist())

    worksheet.append_rows(
        df.values.tolist(),
        value_input_option="USER_ENTERED"
    )
    print(f"{len(df)} baris berhasil ditambahkan.")

def transform_og(path):
    df = pd.read_html(path, skiprows=5)[0]
    df.columns = [
        'Date',
        'Outlet',
        'SJ',
        'No. Cust',
        'Add Info',
        'Nett',
        'Disc',
        'Grand Total',
        'User Entry',
        'Date Entry',
        'Payment Type',
        'Payment Total',
        'Lunas',
        'Tgl Lunas'
    ]

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    df.dropna(inplace=True, how='all')
    df = df [['Date','Outlet','SJ','Nett','Payment Type','Payment Total']]
    df = df.dropna(subset=['SJ'])
    df['Timestamp'] = [timestamp for i in range(len(df))]

    id_sheet = "1ZGjn85gDAQjK4H5pTLr_Ho7T64C8sswQ5acU2X3_3cs"
    worksheet_name = "DATABASE"
    credentials_file = "credentials/wh-aoi.json"

    append_dataframe(df, id_sheet, worksheet_name, credentials_file)
    return df

def transform_gs(path):
    df = pd.read_html(path, skiprows=5)[0]
    df.columns = [
        'Date',
        'Supplier',
        'Purchase No.',
        'No. Supplier',
        'Add Info',
        'Nett',
        'Disc',
        'Grand Total',
        'User Entry',
        'Date Entry',
        'Payment Type',
        'Settled',
        'Settled Date'
    ]

    df.dropna(inplace=True, how='all')
    df = df [['Date','Supplier','Purchase No.','No. Supplier','Add Info','Nett', 'Grand Total']]
    df = df.dropna(subset=['Purchase No.'])

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    df['Timestamp'] = [timestamp for i in range(len(df))]

    id_sheet = "1AYejIgtwZKEOh9I17bM36SSQOWOcPcUumGqb4yA1uWE"
    worksheet_name = "DATABASE"
    credentials_file = "credentials/wh-aoi.json"

    append_dataframe(df, id_sheet, worksheet_name, credentials_file)

    return df
