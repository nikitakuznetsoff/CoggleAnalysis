from networkx.algorithms import isomorphism
import networkx as nx
from modules import analysis_functions as af
from modules import graph_functions as gf
import copy


# Делаем поддерево от заданной точки
def subtree_by_node(graph, curr_node):
    new_graph = nx.DiGraph()
    new_graph.add_node(curr_node)
    for node in graph.neighbors(curr_node):
        new_graph.add_node(node, text=graph.node[node]['text'])
        #new_graph.node[node]['text'] = graph.node[node]['text']
        new_graph.add_edge(curr_node, node)
        subtree_by_node_rec(graph, node, new_graph)
    return new_graph


def subtree_by_node_rec(graph, curr_node, new_graph):
    for node in graph.neighbors(curr_node):
        new_graph.add_node(node, text=graph.node[node]['text'])
        new_graph.add_edge(curr_node, node)
        subtree_by_node_rec(graph, node, new_graph)


# Создание графа от заднного корня до конкретной вершины
def make_graph(graph, root, nd):
    list_nodes = nx.shortest_path(graph, source=root, target=nd)
    new_graph = nx.DiGraph()
    new_graph.add_nodes_from(list_nodes, text='')
    curr_node = list_nodes[list_nodes.index(root)]
    for obj in list_nodes:
        if obj == curr_node:
            new_graph.node[obj]['text'] = graph.node[obj]['text']
            continue
        new_graph.add_edge(curr_node, obj)
        curr_node = obj
        # obj = присваиваем метрики каждой вершине графа new_graph аналошичных вершин из graph
        # new_graph[curr_node][obj]['colour'] = graph[curr_node][obj]['colour']
        new_graph.node[obj]['text'] = graph.node[obj]['text']
    return new_graph


# Масимальное количество схожих вершин в двух одинаковых по длине графах
def max_count_isom_nodes(G, H):
    count = 0
    mass_G = list(G.nodes())
    mass_H = list(H.nodes())
    for i in range(len(mass_G)):
        if G.node[mass_G[i]]['text'] == H.node[mass_H[i]]['text']:
            count += 1
    return count


# Поиск максимального общего дерева
def max_isom_substree(G, H):
    #gm_one = isomorphism.DiGraphMatcher(G, H)
    #gm_two = isomorphism.DiGraphMatcher(H, G)
    nm = isomorphism.categorical_node_match('text', '')
    gm_one = isomorphism.DiGraphMatcher(G, H, node_match=nm)
    gm_two = isomorphism.DiGraphMatcher(H, G, node_match=nm)
    if gm_one.subgraph_is_isomorphic():
        return af.count_nodes(H)
    if gm_two.subgraph_is_isomorphic():
        return af.count_nodes(G)
    return 0


# Поиск максимального весового совпадения (MWM) в заданной матрице
def max_mwm(arr):
    if len(arr) == 0:
        return 0
    if len(arr) > len(arr[0]):
        mass = copy.deepcopy(arr)
        arr.clear()
        for i in range(len(mass[0])):
            arr.append([])
            for j in range(len(mass)):
                arr[i].append(mass[j][i])

    arr_summ = []
    for i in range(len(arr)):
        # Массив для посещенных/не посещенных вершин
        nodes = []
        for k in range(len(arr[0])):
            nodes.append(False)
        for j in range(len(arr[0])):
            if arr[i][j] != 0:
                sum = 0
                sum += arr[i][j]
                max_mwm_rec(arr, nodes, i, j, sum, arr_summ)
    if not arr_summ:
        return 0
    return max(arr_summ)


# Рекурсивная часть алгоритма
def max_mwm_rec(arr, nodes, ni, nj, sum, arr_summ):
    nodes[nj] = True
    for i in range(ni + 1, len(arr)):
        for j in range(len(arr[0])):
            if (nodes[j] != True) & (arr[i][j] != 0):
                sum += arr[i][j]
                max_mwm_rec(arr, nodes, i, j, sum, arr_summ)
    arr_summ.append(sum)


# Алгоритм для направленных деревьев
def max_common_substree_rooted(G, H):
    G_graph = gf.transform_into_graph(G)
    H_graph = gf.transform_into_graph(H)
    matrix = []
    i = 0
    for G_node in G_graph.neighbors(G[0]['_id']):
        matrix.append([])
        for H_node in H_graph.neighbors(H[0]['_id']):
            g = subtree_by_node(G_graph, G_node)
            h = subtree_by_node(H_graph, H_node)
            if max_isom_substree(g, h) == af.count_nodes(g):
                matrix[i].append(af.count_nodes(g))
            if max_isom_substree(g, h) == af.count_nodes(h):
                matrix[i].append(af.count_nodes(h))
            if max_isom_substree(g, h) == 0:
                matrix[i].append(max_common_substree_rooted_rec(
                    G_graph, H_graph, G_node, H_node, G[0]['_id'], H[0]['_id'])
                )
        i += 1
    return af.similarity_sub_algo(max_mwm(matrix), G_graph, H_graph)


# Рекурсивная часть алгоритма
def max_common_substree_rooted_rec(G_graph, H_graph, nG_node, nH_node, root_G, root_H):
    matrix = []
    i = 0
    for G_node in G_graph.neighbors(nG_node):
        matrix.append([])
        for H_node in H_graph.neighbors(nH_node):
            matrix[i].append(max_common_substree_rooted_rec(
                G_graph, H_graph, G_node, H_node, root_G, root_H)
            )
        i += 1
    root_to_GNode = make_graph(G_graph, root_G, nG_node)
    root_to_HNode = make_graph(H_graph, root_H, nH_node)
    max_count_isom_nodes(root_to_GNode, root_to_HNode)
    return max_mwm(matrix) + max_count_isom_nodes(root_to_GNode, root_to_HNode)


# Алгоритм для ненаправоенных деревьев
def max_common_substree_unrooted(G, H):
    G_graph = gf.transform_into_graph(G)
    H_graph = gf.transform_into_graph(H)
    nodes_of_G = list(G_graph.nodes())
    nodes_of_G.remove(G[0]['_id'])
    D = []
    history_arr = []
    for node_G in nodes_of_G:
        for node_H in H_graph.nodes():
            arr_of_node = list(H_graph.neighbors(node_H))
            arr_of_node.append(node_H)
            for s in arr_of_node:
                arr = []
                i = 0
                for u in G_graph.neighbors(node_G):
                    graph_form_root_G = make_graph(G_graph, node_G, u)
                    node_substree_G = subtree_by_node(G_graph, u)
                    arr.append([])
                    for v in H_graph.neighbors(node_H):
                        graph_form_root_H = make_graph(H_graph, node_H, v)
                        node_substree_H = subtree_by_node(H_graph, v)
                        summ = max_isom_substree(graph_form_root_G, graph_form_root_H) \
                               + max_isom_substree(node_substree_G, node_substree_H)
                        arr[i].append(summ)
                    i += 1
                graph_form_root_r = make_graph(G_graph, G[0]['_id'], node_G)
                graph_form_root_s = make_graph(H_graph, node_H, s)
                D.append(max_isom_substree(graph_form_root_r, graph_form_root_s) + max_mwm(arr))
                history_arr.append(arr)
    return max(D) - 1


