def is_safe(v, graph, color, c, n):
    for i in range(n):
        if graph[v][i] == 1 and color[i] == c:
            return False
    return True

def backtrack(v, graph, k, color, n):
    if v == n:
        return True

    for c in range(1, k + 1):
        if is_safe(v, graph, color, c, n):
            color[v] = c
            if backtrack(v + 1, graph, k, color, n):
                return True
            color[v] = 0

    return False

def main():
    with open("input4.txt", "r") as f:
        lines = f.read().splitlines()
    
    if not lines:
        return

    n, k = map(int, lines[0].split())
    
    graph = []
    for i in range(1, n + 1):
        graph.append([int(x) for x in lines[i].strip()])

    color = [0] * n

    if backtrack(0, graph, k, color, n):
        print("YES")
        print(*(color))
    else:
        print("NO")

if __name__ == '__main__':
    main()