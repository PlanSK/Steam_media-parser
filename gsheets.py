import gspread
import gspread_formatting

from gspread_formatting.models import TextFormat


GSHEETS_API_KEY = 'esports_cred.json'


def gsheets_save(table_key: str, data: dict):
    google_connect = gspread.service_account(filename=GSHEETS_API_KEY)
    gsheet = google_connect.open_by_key(table_key)
    worksheet = gsheet.sheet1

    write_list = []
    desc_list = []

    borders_style = gspread_formatting.Border(
        style='SOLID',
        color=gspread_formatting.Color(0, 0, 0),
        width=1
    )

    table_style = gspread_formatting.CellFormat(
        borders=gspread_formatting.Borders(
            top=borders_style,
            bottom=borders_style,
            left=borders_style,
            right=borders_style
        )
    )

    for id, data_list in data.items(): 
        first_data = [
            id,
            data_list['title'],
            data_list['title'],
            data_list['genres'],
            data_list['main_img'],
            data_list['icon'],
            data_list['tags'],
            data_list['screenshots'],
            '-', '-', '-', '-', '-', '-',
            data_list['description']
        ]

        write_list.append(first_data)

    range_table = 'O' + str(len(write_list) + 1)
    worksheet.update('A2:' + range_table, write_list)

    gspread_formatting.format_cell_range(
         worksheet,
         'A1:'+ range_table, table_style
    )
    # worksheet.format('D2:' + range_table, float_style)
