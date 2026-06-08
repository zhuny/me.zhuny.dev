---
title: '치킨너겟정리'
description: ''
pubDate: 'Jun 7 2026'
youtube:
  url: 'https://www.youtube.com/watch?v=3WEfQGHb46w'
  title: "why you can't order 43 nuggets."
  subtitle: '@MichaelPennMath'
---

## 문제
치킨너겟을 각각 6, 9, 20개 담은 박스를 소중대 3가지 사이즈의 박스로 판매한다.
그렇다면 박스 단위로 구매할 때, 구매할 수 없는 가장 많은 치킨너겟의 갯수는 몇개일까?
(판매하는 너겟 갯수는 서로소이다. Pairwise 할 필요는 없다.)

예로 들면 치킨너겟을 1개만 구매하는 것은 불가능하다. 최소 6개가 든 박스를 사야 하기 때문이다.
대신 15개는 구매 가능하다. 6개짜리 하나 9개짜리 하나를 구매하면 되기 때문이다.

여기서 존재성 여부에 대한 (수학적인) 내용과 답을 어떻게 찾을지에 대한 (알고리즘) 내용을 담고 있다.

## 존재성
치킨 너겟이 갯수 종류를 $x_i$로 표현하기로 하자.
일반성을 잃지않고 $x_i$는 strict increasing sequence 라고 해도 좋다.
여기서는 $x_1=6$, $x_2=9$, $x_3=20$이다.
또한 가정에 의해 $\gcd(x_i) = 1$이다.

존재성을 보인다는 것은 어떤 값 $N$을 찾아서 $N$ 이상의 모든 자연수에 대해서 조합이 가능하다는 것을 보이는 것이다.
그래서 조합이 가능하지 않은 수들은 $N$이하이고 1이상의 자연수라는 것을 알 수 있다.

GCD가 1이기 때문에 $\sum_i{c_i x_i} = 1$을 만족하는 $c_i$를 찾을 수 있다.
여기서 $c_i^+=\max(c_i, 0)$, $c_i^-=-\min(c_i, 0)$ 으로 정의하자.
전자는 양수인 부분만 취하고, 후자는 음수인 부분만 취한 것이다.
그리고 $c_i=c_i^+-c_i^-$로 나타낼 수 있다.
그래서 $c_i^+$, $c_i^-$ 모두 0 혹은 양수가 된다.

$N=x_1 \sum_i c_i^-x_i$라고 하자. 여기서 $x_1=\min(x_i)$이다.
먼저 $N + kx_1$ 꼴의 모든 자연수($0 \le k$)에 대해서는 조합이 가능하다.
각 박스는 $c_i$만큼 제공하는데 가장 작은 박스만 $c_1 + k$개 만큼 제공하면 된다.

$0 \le j \lt x_1$인 $j$에 대해서,

$$
\begin{aligned}
N+j&=x_1 \sum_i c_i^-x_i+j\sum_i{c_i x_i} \\
&=(x_1 - j) \sum_i c_i^-x_i+j\sum_i c_i^+x_i
\end{aligned}
$$

모든 $x_i$에 대해서 양의 값을 가지게 된다.
그리고 이것은 $j \le x_1$인 경우에서만 가능하다.
다만 전에 $N + kx_1$ 꼴은 제공 가능하므로 $N + kx_1 + j$의 경우 같은 논리로 풀어갈 수 있다.

결과적으로 $L$ 이상의 모든 자연수에 대해서는 제공 가능하므로 $L$ 미만의 어떤 수에서 답을 찾을 수 있게 된다.

## 풀이
사실 2개에 대해서는 closed form이 존재하고, 3개 이상에서는 존재하지 않는다.
이것은 이하의 영상을 통해서 확인할 수 있다.

이 문제를 알고리즘을 통해서 해결해 보려고 한다.

HeapQueue인 q가 있고 처음에는 0만 들어간 상태라고 하자.
이 큐는 이미 값이 들어간 경우에는 추가로 크기를 증가시키지 않는다.

각 큐의 원소 하나 $e$마다 각각의 $e + x_i$를 큐에 넣는다.
언제 이 iteration을 멈추는지가 중요한데, 만약 큐에서 뺀 원소들이 연속해서 $x_1$만큼 지속된다면 더이상 확인할 필요가 없다.
정답은 지속된 sequence의 가장 작은 값 -1을 하면 된다.

슈도코드를 작성하면 다음과 같다.

```python
def find_min_nugget(num_list: list[int]) -> int:
    """
    :param num_list: 정렬된 자연수 리스트
    :return: 조합할 수 없는 가장 큰 자연수
    """

    # Queue Initialize
    queue = HeapQueue()
    queue.put(0)

    # 연속인지 확인 용
    start_num = 0
    consecutive_count = 0
    
    while True:
        current = queue.get()
        for num in num_list:
            queue.put(current + num)

        # 연속인지 확인 및 종료 여부 체크
        if current == start_num + consecutive_count:
            consecutive_count += 1
            if consecutive_count >= num_list[0]:
                return start_num - 1
        else:
            start_num = current
            consecutive_count = 1

def main():
    print(find_min_nugget([6, 9, 20]))  # 결과는 43
```

## 마무리
$x_i$의 값들이 작을 때에는 상관 없지만, 결국 답까지의 정수를 일일이 확인해야 한다.
더 빠른 알고리즘이 있을지에 대해서는 더 생각해 봐야 할 것 같다.
