# Максимальное число ребер от корня
def max_height(nodes):
    arr = []
    if nodes:
        for obj in nodes:
            arr.append(max_height_children(obj))
        return max(arr)
    else:
        return 0


def max_height_children(nodes):
    if nodes['children']:
        arr = []
        for obj in nodes['children']:
            arr.append(max_height_children(obj))
        return max(arr) + 1
    else:
        return 0


# Количество вершин через networkx
def count_nodes(graph):
    return len(graph.nodes)


# Количество узлов от корневых вершин
def count_first_layer_branches(nodes):
    count = 0
    for obj in nodes:
        count += len(obj['children'])
    return count


# Количество изображений
def images_count(nodes):
    count = 0
    if nodes:
        for obj in nodes:
            if obj['text'].find(r"!\[([a-zA-Z0-9 ]*)\]\(https?:") != -1:
                count += obj['text'].count("![")
            count += images_count_children(obj)
    else:
        return 0
    return count


def images_count_children(nodes):
    count = 0
    for obj in nodes['children']:
        if obj['text'].find(r"!\[([a-zA-Z0-9 ]*)\]\(https?:") != -1:
            count += obj['text'].count("![") + images_count_children(obj)
    return count


# Средняя длина текста
def avg_node_text_len(nodes, count_nodes) -> float:
    len_text = 0
    if nodes:
        for obj in nodes:
            if obj['text'].find("![") != -1:
                len_text += len(
                    obj['text'][0: obj['text'].find("![") - 2: 1]) + avg_node_text_len_children(obj)
            else:
                len_text += len(obj['text']) + avg_node_text_len_children(obj)
    else:
        return 0
    return len_text / count_nodes


def avg_node_text_len_children(nodes):
    len_text = 0
    if nodes['children']:
        for obj in nodes['children']:
            if obj['text'].find("![") != -1:
                len_text += len(
                    obj['text'][0: obj['text'].find("![") - 2: 1]) + avg_node_text_len_children(obj)
            else:
                len_text += len(obj['text']) + avg_node_text_len_children(obj)
    else:
        return 0
    return len_text


# Список метрик
def calculate_metrics(nodes, graph) -> dict:
    metrics = dict()
    metrics["max_height"] = max_height(nodes)
    metrics["count_nodes"] = count_nodes(graph)
    metrics["count_first_layer_branches"] = count_first_layer_branches(nodes)
    metrics["images"] = images_count(nodes)
    metrics["avg_node_text_len"] = avg_node_text_len(nodes, metrics["count_nodes"])
    return metrics


# Подсчет меры сходства для подструктурного подхода
def similarity_sub_algo(max_count, graph_1, graph_2) -> float:
    max_count -= 1
    return (max_count * max_count) / (count_nodes(graph_1) * count_nodes(graph_2))
