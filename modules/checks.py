# Проверка на наличие конкретной таблицы в файле
def check_correct_tablename(wb, name):
    arr = wb.sheetnames
    try:
        if arr.index(name) != -1:
            return True
    except Exception:
        return False


# Проверка на кооректный формат ячейки для начала считывания
def column_name_is_correct(name):
    if name == "":
        return True
    if name.isupper():
        return True
    return False
