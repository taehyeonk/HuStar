import sys
import heapq

# dictionary를 활용한 graph 작성 (Linked List와 유사)
def getGraph(N, M):
    graph = {}
    for i in range(N):
        graph[i] = {}
    for _ in range(M):
        i, j, k = map(int, sys.stdin.readline().split())
        graph[i][j] = k
    
    return graph

def dijkstra(graph, root):
    dist = {node: float('inf') for node in graph}  # start로 부터의 거리 값을 저장하기 위함
    dist[root] = 0  # 시작 값은 0이어야 함
    queue = []
    heapq.heappush(queue, [dist[root], root])  # 시작 노드부터 탐색 시작 하기 위함.

    while queue:  # queue에 남아 있는 노드가 없으면 끝
        current_dist, current_node = heapq.heappop(queue)  # 탐색 할 노드, 거리를 가져옴.

        if current_dist > dist[current_node]:  # 기존에 있는 거리보다 길다면, 볼 필요도 없음
            continue

        for new_node, new_dist in graph[current_node].items():
            distance = current_dist + new_dist  # 해당 노드를 거쳐 갈 때 거리
            if distance < dist[new_node]:  # 알고 있는 거리 보다 작으면 갱신
                dist[new_node] = distance
                heapq.heappush(queue, [distance, new_node])  # 다음 인접 거리를 계산 하기 위해 큐에 삽입

    return dist

t = int(sys.stdin.readline())

for _ in range(t):
    N, M = map(int, sys.stdin.readline().split())
    graph = getGraph(N, M)
    result = dijkstra(graph, 0)[N-1]

    if result == float('inf'):
        print(-1)
    else:
        print(result)