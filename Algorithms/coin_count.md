# 세금 징수

## 문제 정의

어느 외딴 곳에 있는 국가는 화폐가 모두 동전으로 되어 있습니다. 동전의 종류는 50,000원, 10,000원, 5,000원, 1,000원, 500원, 100원이 있으며 그 무게는 모두 같습니다. 이 국가는 세금 징수원이 온 집을 돌아다니며 세금을 징수하게 됩니다. 다만 국가에는 거스름돈 제도가 없고, 동전이 상당히 무겁기 때문에 징수원은 어찌됐든 동전의 개수를 최소한으로 가지는 것이 효율적입니다.

국민들은 이런 세금 징수원의 고충을 알기 때문에, 내야 될 세금이 주어지면 동전을 최소 개수만 납부하려고 합니다. 납부해야 하는 세금이 주어졌을 때, 이 세금을 납부하기 위해 필요한 최소의 동전 개수를 출력하는 프로그램을 작성하세요.

예를 들어, 53,200원을 납부해야 한다면, 50,000원 동전 1개, 1,000원 동전 3개, 100원 동전 2개로 금액을 납부하면 6개의 동전만 써도 세금을 납부할 수 있습니다.

# 입력 형식

- 입력의 첫 줄에 테스트 케이스의 숫자 TT가 주어진다.
- 각 테스트 케이스마다 입력은 아래와 같다.
  - 한 줄에 국민들이 납부해야 하는 세금이 주어진다. 세금은 10201020 이하의 자연수이며, 항상 100으로 나누어 떨어진다.

# 출력 형식[¶](https://domjudge.postech.ac.kr/domjudge/team/problems/44/text#출력-형식)

- 각 테스트 케이스에 대해 동전을 최소한으로 써서 세금을 납부할 때, 동전의 개수를 출력한다.

# 입력 예시

4
200
700
7900
53200

# 출력 예시

2
3
8
6