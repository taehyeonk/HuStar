# 이진 탐색2

## 문제 정의

정렬된 리스트와 찾고자 하는 숫자 리스트가 입력되었을 때, 리스트에서 찾고자 하는 숫자와 차이가 가장 작은 값을 출력하는 프로그램을 작성하세요. 만약 차이가 가장 작은 값이 두 개 이상이라면 그 중 작은 값을 출력하세요.

## Hint

리스트의 각 원소를 한 줄에 출력하기 위해서는 다음과 같이 실행하면 됩니다.
l = [1,2,3,4]
print(*l)

출력 결과: 1 2 3 4

## 입력 형식

- 입력의 첫 줄에 테스트 케이스의 숫자 *t*가 주어진다.
  - 각 테스트 케이스의 첫 번째 줄에는 n(n≤100,000)n(n≤100,000) 개의 숫자 리스트가 띄어쓰기로 구분되어 입력된다.
  - 다음 줄에는 찾고자 하는 m(m≤100,000)m(m≤100,000)개의 숫자 리스트가 입력된다.
- 각 테스트 케이스의 첫 번째 리스트에 있는 숫자는 모두 다르며 정렬되어 있다.

## 출력 형식

- 각 테스트 케이스에 대해 각각의 찾고자 하는 숫자와 차이가 가장 작은 값을 순서대로 출력하라.
- 각 테스트 케이스의 출력은 한 줄에 이루어져야한다.

## 입력 예제

3
2 4 6 8 10
1 3 7
1 3 5 7
2 3 6
3 7 11 17 21
9 8 4 100 16 17

## 출력 예제

2 2 6
1 3 5
7 7 3 21 17 17