# Чтение Имен учеников и ссылок
def read_mindmaps_info(sheet, names_column, links_column, start_row) -> dict:
    if names_column == '':
        names_column = "A"
    if links_column == '':
        links_column = "B"
    if start_row == '':
        start_row = 1

    names, links = [], []
    names_column_index = ord(names_column) - 65
    links_column_index = ord(links_column) - 65

    for row in sheet.iter_rows(min_row=start_row):
        try:
            if row[names_column_index].value:
                names.append(row[names_column_index].value.strip())
                links.append(link_to_id(row[links_column_index].value.strip()))
            else:
                names.append(None)
                links.append(None)
        except Exception as e:
            print("[SHEET ERROR]" + str(e))
    return {'names': names, 'mindmaps_id': links}


# Возврат ИДшника из ссылки
def link_to_id(link: str) -> str:
    left, right = -1, -1
    if link.find("miro.com") != -1:
        left = link.find("/app/board/") + 11
        right = len(link)-1
    elif link.find("coggle.it") != -1:
        left = link.find("/diagram/") + 9
        right = link.find("/t/")
    if left == -1 or right == -1:
        raise ValueError('incorrect mindmap link')
    return link[left:right]
