import prettytable as pt


def convert_table_html_telegram(columns: list, attributes: list, data):
    table = pt.PrettyTable(columns)
    for entry in data:
        row = []
        for attribute in attributes:
            row.append(entry.get(attribute))
        table.add_row(row)
    return table
