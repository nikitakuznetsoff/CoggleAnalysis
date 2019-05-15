from openpyxl import load_workbook
from modules import readers, coggle, algorithm
from modules import graph_functions as gf

from fuzzywuzzy import fuzz
from fuzzywuzzy import process


def mindmap_analysis(arr_ids, true_id):
    arr_diagrams = create_arr_diagrams(arr_ids)

    if true_id != '':
        true_diagram = create_diagram(true_id)
        mass = [0] * len(arr_diagrams) 
        if true_diagram is not None:
            for i in range(0, len(arr_diagrams)):
                if arr_diagrams[i] is None or true_diagram is None:
                    mass[i] = None
                else:
                    mass[i] = algorithm.max_common_substree_rooted(true_diagram, arr_diagrams[i])
        return mass

    else:
        mass = [[0] * len(arr_diagrams)] * len(arr_diagrams)
        for i in range(0, len(arr_diagrams)):
            for j in range(0, len(arr_diagrams)):
                if arr_diagrams[i] is None or arr_diagrams[j] is None:
                    mass[i][j] = None
                else:
                    mass[i][j] = algorithm.max_common_substree_rooted(arr_diagrams[i], arr_diagrams[j])
        return mass


# Получение степени плагиата для каждого ученика и номер с которым наибольшее сходство
def plagiarism_rating(arr_ids):
    arr_diagrams = create_arr_diagrams(arr_ids)
    arr_texts = []
    temp_rating = []

    for i in range(0, len(arr_ids)):
        graph = gf.transform_into_graph(arr_diagrams[i])
        arr_texts.append(gf.get_text(graph))

    for i in range(0, len(arr_ids)):
        arr = []
        temp_rating.append(arr)
        for j in range(0, len(arr_ids)):
            temp_rating[i].append(fuzz.ratio(arr_texts[i], arr_texts[j]))

    rating = []
    for i in range(0, len(arr_ids)):
        arr = []
        rating.append(arr)
        temp_rating[i].remove(max(temp_rating[i]))
        rating[i].append(max(temp_rating[i]))
        rating[i].append(temp_rating[i].index(rating[i][0]))

    return rating


# Создание диаграммы из ID и проверка закрыта / открыта карта
def create_diagram(id):
    if id is None:
        return None
    diag = coggle.coggle_user.nodes(id)
    for obj in diag:
        if obj == 'error':
            return None
        break
    return diag


# Создание массива диаграмм из массива айдишников
def create_arr_diagrams(arr):
    new_arr = []
    for obj in arr:
        new_arr.append(create_diagram(obj))
    return new_arr


def information_for_algo(id_diagram):
    arr = {'diagram': '', 'graph': ''}
    arr['diagram'] = coggle.coggle_user.nodes(id_diagram)
    arr['graph'] = gf.transform_into_graph(arr['diagram'])
    return arr