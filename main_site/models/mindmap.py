import networkx as nx


class MindMap:
    def __init__(self, name: str, id: str, service: str):
        self.name = name
        self.id = id
        self.service = service
        self.similarity = 0
        self.plagiarism = 0
        self.graph = None

    # Метод преобразования сырых данных в граф формата NetworkX
    def create_graph_view(self, data: dict):
        if self.service == "Coggle":
            if 'error' in data:
                print("Coggle: don't add mindmap")
                return
            graph = nx.DiGraph()
            queue, passed_nodes = [], []
            for obj in data:
                graph.add_node(obj['_id'], text=obj['text'], offset=obj['offset'])
                queue.append(obj)
                passed_nodes.append(obj['_id'])

            passed_nodes = []
            while queue:
                node = queue.pop(0)
                if node['children']:
                    for child in node['children']:
                        try:
                            if passed_nodes.index(child['_id']):
                                continue
                        except ValueError:
                            queue.append(child)
                            passed_nodes.append(child['_id'])
                            graph.add_node(child['_id'], text=child['text'], offset=child['offset'])
                            graph.add_edge(node['_id'], child['_id'], color=child['colour'])
            self.graph = graph

        elif self.service == "Miro":
            if data['type'] == "error":
                print("MIRO: Don't add mindmap")
                return

            if data['type'] != "collection":
                print("MIRO: Incorrect miro info: " + str(data['type']))
                return

            graph = nx.DiGraph()
            for obj in data['data']:
                if obj['type'] == 'text':
                    text = obj['text'].replace("<p>", " ").replace("</p>", " ")
                    self.graph.add_node(obj['id'], text=text)
                elif obj['type'] == 'line':
                    parent = obj['startWidget']['id']
                    child = obj['endWidget']['id']
                    self.graph.add_edge(parent, child)
            self.graph = graph
        else:
            raise ValueError("Unexpected service name")

    def get_metrics(self) -> dict:
        if self.graph is not None:
            metrics = dict()
            metrics["max_height"] = self.calc_max_height()
            metrics["count_nodes"] = len(list(self.graph.nodes))
            metrics["count_first_layer_branches"] = len(list(self.graph.neighbors(list(self.graph.nodes)[0])))
            # metrics["images"] = images_count(nodes)
            metrics["avg_node_text_len"] = self.calc_text_length() / metrics["count_nodes"]
            return metrics
        else:
            return {
                'max_height': 0, 'avg_node_text_len': 0,
                'count_nodes': 0, 'count_first_layer_branches': 0
            }

    def calc_text_length(self) -> int:
        if self.graph is not None:
            text_length = 0
            head = list(self.graph.nodes)[0]
            queue = list()
            queue.append(head)
            while queue:
                node = queue.pop(0)
                text_length += len(self.graph.nodes[node]['text'].strip())
                for child in self.graph.neighbors(node):
                    queue.append(child)
            return text_length
        return 0

    def calc_max_height(self) -> int:
        def calc_max_height(node) -> int:
            nodes = []
            for v in self.graph.neighbors(node):
                nodes.append(calc_max_height(v))

            if len(nodes) == 0:
                return 0
            return max(nodes) + 1

        if self.graph is not None:
            head = list(self.graph.nodes)[0]
            arr = []
            for obj in self.graph.neighbors(head):
                arr.append(calc_max_height(obj))

            if len(arr) == 0:
                return 0
            return max(arr)
        return 0
