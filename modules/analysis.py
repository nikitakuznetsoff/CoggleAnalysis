from openpyxl import load_workbook
from modules import readers, coggle, algorithm
from modules import graph_functions as gf


def mindmap_analysis(arr_ids, true_id):
    arr_diagrams = create_arr_diagrams(arr_ids)
    if true_id != '':
        true_diagram = create_diagram(true_id)
        #mass = [0] * len(arr_diagrams)
        mass = []
        if true_diagram is not None:
            for i in range(0, len(arr_diagrams)):
                if true_diagram == arr_diagrams[i]:
                    mass.append(1)
                elif (arr_diagrams[i] == None) or (true_diagram == None):
                    mass.append(None)
                else:
                    mass.append(algorithm.max_common_substree_rooted(true_diagram, arr_diagrams[i]))
        return mass

    else:
        #mass = [[0] * len(arr_diagrams)] * len(arr_diagrams)
        mass = []
        for i in range(0, len(arr_diagrams)):
            arr = []
            mass.append(arr)
            for j in range(0, len(arr_diagrams)):
                if (arr_diagrams[i] == arr_diagrams[j]):
                    mass[i].append(1)
                elif (arr_diagrams[i] == None) or (arr_diagrams[j] == None):
                    mass[i].append(None)
                else:
                    mass[i].append(algorithm.max_common_substree_rooted(arr_diagrams[i], arr_diagrams[j]))
        return mass


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


# Получение массива текстов каждой интеллект-карты
def take_text(arr_ids):
    arr_diagrams = create_arr_diagrams(arr_ids)
    arr_texts = []

    for i in range(0, len(arr_ids)):
        if arr_diagrams[i] is None:
            arr_texts.append("")
        else:
            graph = gf.transform_into_graph(arr_diagrams[i])
            arr_texts.append(gf.get_text(graph))
    return arr_texts