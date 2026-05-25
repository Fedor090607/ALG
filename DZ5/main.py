
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from typing import Dict, List, Tuple
import math
import heapq
import time

def haversine(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
    """Вычисляет расстояние между двумя точками на Земле (в км)"""
    lon1, lat1 = coord1
    lon2, lat2 = coord2
    R = 6371  # Радиус Земли в км

    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def dijkstra(graph: Dict[Tuple[float, float], List[Tuple[Tuple[float, float], float]]],
             start: Tuple[float, float],
             end: Tuple[float, float],
             raw_edges: List[Tuple[Tuple[float, float], Tuple[float, float], str]]) -> Tuple[List[Tuple[float, float]], float, List[str]]:

    queue = [(0.0, start)]
    distances = {start: 0.0}
    backtrack_map = {start: None}
    visited = set()
    while queue:
        current_dist, current_node = heapq.heappop(queue)

        if current_node in visited:
            continue
        
        if current_node == end:
            break

        visited.add(current_node)

        for neighbor, weight in graph.get(current_node, []):
            if neighbor in visited:
                continue
            
            new_dist = current_dist + weight
            if new_dist < distances.get(neighbor, float('inf')):
                distances[neighbor] = new_dist
                backtrack_map[neighbor] = current_node
                heapq.heappush(queue, (new_dist, neighbor))
    path = []
    total_distance = 0.0
    street_names = []

    if end in distances:
        total_distance = distances[end]
        step = end
        while step is not None:
            path.append(step)
            step = backtrack_map[step]
        path.reverse()

        edge_to_name = {}
        for s_coord, e_coord, name in raw_edges:
            edge_to_name[(s_coord, e_coord)] = name
            edge_to_name[(e_coord, s_coord)] = name  

        for i in range(len(path) - 1):
            segment = (path[i], path[i+1])
            street = edge_to_name.get(segment)
            if street and (not street_names or street_names[-1] != street):
                street_names.append(street)

    return path, total_distance, street_names


def build_graph(edges: List[Tuple[Tuple[float, float], Tuple[float, float], str]]) -> Dict[Tuple[float, float], List[Tuple[Tuple[float, float], float]]]:
    graph = {}
    for start, end, _ in edges:
        dist = haversine(start, end)
        graph.setdefault(start, []).append((end, dist))
        graph.setdefault(end, []).append((start, dist))  
    return graph


def read_graphml(file_path: str) -> Tuple[Dict[str, Tuple[float, float]], List[Tuple[Tuple[float, float], Tuple[float, float], str]]]:
    tree = ET.parse(file_path)
    root = tree.getroot()
    

    ns_url = root.tag.split('}')[0].strip('{') if '}' in root.tag else 'http://graphml.graphdrawing.org/xmlns'
    ns = {'g': ns_url}


    key_x, key_y, key_name = None, None, None
    for key in root.findall('.//g:key', ns):
        attr_name = key.get('attr.name')
        if attr_name == 'x':
            key_x = key.get('id')
        elif attr_name == 'y':
            key_y = key.get('id')
        elif attr_name == 'name':
            key_name = key.get('id')


    if not key_x: key_x = 'd4'
    if not key_y: key_y = 'd5'
    if not key_name: key_name = 'd18'

    nodes = {}
    for node in root.findall('.//g:node', ns):
        node_id = node.get('id')
        x, y = None, None
        for data in node.findall('.//g:data', ns):
            data_key = data.get('key')
            if data_key == key_x:
                x = float(data.text)
            elif data_key == key_y:
                y = float(data.text)
        if x is not None and y is not None:
            nodes[node_id] = (x, y)

    edges = []
    for edge in root.findall('.//g:edge', ns):
        source = edge.get('source')
        target = edge.get('target')
        street_name = None

        for data in edge.findall('.//g:data', ns):
            if data.get('key') == key_name:
                street_name = data.text if data.text else None

        if source in nodes and target in nodes:
            edges.append((nodes[source], nodes[target], street_name))

    return nodes, edges


def find_street_index(edges: List[Tuple[Tuple[float, float], Tuple[float, float], str]], 
                      street_name_query: str) -> Tuple[int, str]:
    for i, (_, _, name) in enumerate(edges):
        if name and street_name_query.lower() in name.lower():
            return i, name
    return -1, None


def visualize_path_with_network(nodes, edges, path, street_names=None, figsize=(15, 15)):
    plt.figure(figsize=figsize)
    ax = plt.gca()

    all_lines = [(start, end) for start, end, _ in edges]
    lc = LineCollection(all_lines, linewidths=0.3, colors='gray', alpha=0.4)
    ax.add_collection(lc)

    if path and len(path) > 1:
        path_lines = [(path[i], path[i+1]) for i in range(len(path)-1)]
        lc_path = LineCollection(path_lines, linewidths=2.5, colors='red', alpha=1.0)
        ax.add_collection(lc_path)

    ax.autoscale()
    plt.axis('equal')
    plt.title('Дорожная сеть Бухареста и кратчайший маршрут (Вариант 15)')
    plt.xlabel('Долгота')
    plt.ylabel('Широта')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    nodes, edges = read_graphml("buharest_road_network.graphml")
    print(f"Количество вершин: {len(nodes)}")
    print(f"Количество рёбер: {len(edges)}")


    start_street_query = "Șoseaua Colentina"
    end_street_query = "Bulevardul Ghencea"      

    start_index, start_street = find_street_index(edges, start_street_query)
    end_index, end_street = find_street_index(edges, end_street_query)

    if start_index == -1 or end_index == -1:
        print("Не удалось найти заданную улицу для начала или конца маршрута.")
        print("Попробуй более общие названия, например 'Unirii' или 'Aviation'.")
    else:
        start_node = edges[start_index][0]
        end_node = edges[end_index][1]

        graph = build_graph(edges)
        
  
        start_time = time.perf_counter()
        path, distance, street_names = dijkstra(graph, start_node, end_node, edges)
        end_time = time.perf_counter()

        if not path:
            print("Путь не найден.")
        else:
            execution_time = end_time - start_time
            print(f"\nУспешно рассчитвно!")
            print(f"Время работы алгоритма: {execution_time:.5f} сек")
            print(f"Найден путь длиной {distance:.2f} км")
            print("Улицы на пути:", ", ".join(filter(None, street_names)))
            visualize_path_with_network(nodes, edges, path, street_names)
