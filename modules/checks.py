# Проверка на наличие конкретной таблицы в файле
def check_correct_tablename(wb, name):
    arr = wb.sheetnames
    try:
        if arr.index(name) != -1:
            return True
    except Exception:
        return False


# Проверка на кооректный формат ячейки для начала считывания
def check_correct_cellname(name):
    if name == "":
        return True
    if name[0].isupper() and name[1:].isdigit():
        return True
    return False


# Проверка на кооректный формат ячейки для начала считывания
def column_name_is_correct(name):
    if name == "":
        return True
    if name.isupper():
        return True
    return False


# Проверка на кооректный формат ячейки для начала считывания
def check_correct_row_name(name):
    if name == "":
        return True
    if name.isdigit():
        return True
    return False
