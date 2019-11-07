# Чтение Имен учеников и ссылок
def read_mindmap_ids(sheet, point_names, point_links):
    if point_names == '':
        point_names = "A1"
    if point_links == '':
        point_links = "B1"

    arr = [[], []]
    column_names = ord(point_names[0]) - 65
    column_links = ord(point_links[0]) - 65
    str_row_names = point_names[1:]
    str_row_links = point_links[1:]

    for row in sheet.iter_rows(None, int(str_row_links), None, column_links):
        try:
            if row[column_links].value:
                arr[0].append(row[column_names].value.strip())
                arr[1].append(link_to_id(row[column_links].value.strip()))
            else:
                arr[0].append(None)
                arr[1].append(None)
        except Exception:
            return arr
    return arr


# Возврат ИДшника из ссылки
def link_to_id(link):
    first = link.find("/diagram/")
    last = link.find("/t/")
    return link[first + 9:last:1]