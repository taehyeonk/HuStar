# BFS

## 문제 정의

방향성 그래프가 주어졌을 때, 정점 0부터 시작하여 그래프를 너비우선탐색(BFS)으로 순회하는 알고리즘을 작성하세요.

너비우선탐색에서 여러 선택지가 존재하게 된다면 항상 가장 번호가 낮은 정점을 우선적으로 선택해서 탐색합니다. 예를 들면 정점 0을 방문한 뒤에 정점 2 혹은 정점 5를 방문할 수 있다면, 낮은 번호인 2번 정점을 먼저 탐색합니다.

## 입력 형식

- 입력의 첫 줄에 테스트 케이스의 숫자 tt가 주어진다.
- 각 테스트 케이스마다 입력은 아래와 같다.
  - 첫 줄에 정점의 개수 NN과 간선의 개수 MM이 주어진다. (N≤1,000,M≤100,000)(N≤1,000,M≤100,000)
  - 그 다음 MM개의 줄에 걸쳐서 방향성 그래프의 간선 (u,v)(u,v)가 공백을 사이에 두고 입력된다. uu와 vv는 항상 00부터 N−1N−1 사이의 정수이고, uu에서 vv로 향하는 간선은 유일하다.

## 출력 형식

- 각 테스트 케이스에 대해 정점 0에서 시작하여 너비우선탐색으로 그래프를 탐색했을 때 정점이 방문되는 순서를 한 줄에 공백을 두고 출력한다.

## 입력 예시

3
4 4
0 1
0 3
1 2
1 3
5 7
0 1
0 2
0 4
1 3
1 4
2 4
3 4
6 5
0 5
5 4
1 4
1 3
2 3

## 출력 예시

0 1 3 2
0 1 2 4 3
0 5 4