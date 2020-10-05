# Чтение Имен учеников и ссылок
def read_mindmap_ids(sheet, names_column, links_column, start_row):
    if names_column == '':
        names_column = "A"
    if links_column == '':
        links_column = "B"
    if start_row == '':
        start_row = 1

    arr = [[], []]
    names_column_index = ord(names_column) - 65
    links_column_index = ord(links_column) - 65

    for row in sheet.iter_rows(min_row=start_row):
        try:
            if row[names_column_index].value:
                arr[0].append(row[names_column_index].value.strip())
                arr[1].append(link_to_id(row[links_column_index].value.strip()))
            else:
                arr[0].append(None)
                arr[1].append(None)
        except Exception as e:
            print("[SHEET ERROR]" + str(e))
            return arr
    return arr


# Возврат ИДшника из ссылки
def link_to_id(link):
    first = link.find("/diagram/")
    last = link.find("/t/")
    return link[first + 9:last:1]