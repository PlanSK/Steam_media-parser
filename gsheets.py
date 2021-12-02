import gspread
import gspread_formatting

from gspread_formatting.models import TextFormat
from main import status_operation


@status_operation(title='Google sheets read data')
def gsheets_read(api: str, table_key: str) -> list:
    google_connect = gspread.service_account(filename=api)
    gsheet = google_connect.open_by_key(table_key)

    return gsheet.sheet1.col_values(1)[1:]

@status_operation(title='Google sheets export data')
def gsheets_save(
    api: str, table_key: str, data: dict, 
    title_colorize: bool = False) -> None:

    google_connect = gspread.service_account(filename=api)
    gsheet = google_connect.open_by_key(table_key)
    worksheet = gsheet.sheet1

    write_list = []

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

    title_format = gspread_formatting.CellFormat(
        backgroundColor=gspread_formatting.color(0.7, 0.7, 0.7),
        horizontalAlignment='CENTER',
        textFormat=TextFormat(
            foregroundColor=gspread_formatting.color(0, 0, 0),
            bold=True,
            fontSize=10
        )
    )

    for data_list in data.values(): 
        game_data_list = [
            data_list['title'],
            data_list['title'],
            data_list['genres'],
            data_list['main_img'],
            data_list['icon'],
            data_list['tags'],
            data_list['screenshots'],
            data_list['description']
        ]

        write_list.append(game_data_list)

    range_table = str(len(write_list) + 1)
    worksheet.update('B2:I' + range_table, write_list)

    if title_colorize:
        gspread_formatting.format_cell_range(
            worksheet,
            'A1:O1', title_format
        )

    gspread_formatting.format_cell_range(
         worksheet,
         'A1:O'+ range_table, table_style
    )
