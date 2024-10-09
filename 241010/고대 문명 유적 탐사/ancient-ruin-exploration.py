'''
유믈 조각이 흩어져있다.
K번의 턴
    탐사진행 -> 격자 찾기
        [1]중심좌표 기준으로 3X3 격자 선택 -> 회전(90,180,270도 회전) 중심좌표 9개*회전3개 ()
        [2]3가지 방식으로 모두 회전 해보면서 유물의 가치가 가장 높게 측정되게 끔 좌표를 돌린다.
            유물을 획득할 수 없다면 종료
            1.유물 1차 획득 가치 최대화
                상하좌우 인접한 조각 3개 이상 => 유물이 되고 사라짐. 유물의 가치+=모인 조각의 개수
                유물이 되어 사라짐 => 열작,행큰 순으로 벽면에 써 있는 숫자로 채워짐
                유물 연쇄 획득 => 유물의 가치 += 모인 조각의 개수
            2.회전 각도 작은 방법
            3.회전 중심 좌표의 열작->행작
'''


def rotate(arr, si, sj):
    narr = [x[:] for x in arr]
    for i in range(3):
        for j in range(3):
            narr[si + i][sj + j] = arr[si + 3 - j - 1][sj + i]
    return narr


def bfs(arr, si, sj, v, clr):
    q = []
    sset = set()
    cnt = 0

    q.append((si, sj))
    sset.add((si, sj))
    v[si][sj] = 1

    cnt += 1
    while q:
        ci, cj = q.pop(0)
        for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            ni, nj = ci + di, cj + dj
            # 범위 안 + 들리지 않은 곳 + 같은 숫자 => cnt 증가
            if 0 <= ni < 5 and 0 <= nj < 5 and v[ni][nj] == 0 and arr[ci][cj] == arr[ni][nj]:
                q.append((ni, nj))
                v[ni][nj] = 1
                sset.add((ni, nj))
                cnt += 1

    if cnt >= 3:
        if clr == 1:
            for i, j in sset:
                arr[i][j] = 0
        return cnt
    else:
        return 0


def count_clear(arr, clr):  # 유물의 개수 카운트
    cnt = 0
    v = [[0] * 5 for _ in range(5)]
    for i in range(5):
        for j in range(5):
            if v[i][j] == 0:
                k = bfs(arr, i, j, v, clr)
                cnt += k
    return cnt


K, M = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(5)]  # 유물 조각
lst = list(map(int, input().split()))  # M개
ans = []

for _ in range(K):
    # [0] 유물의 합이 최대가 되는 i,j,r 찾기
    mx_cnt = 0
    for rot in range(1, 4):  # 회전 순 -> 열 -> 행 순
        for sj in range(3):
            for si in range(3):
                narr = [x[:] for x in arr]
                for _ in range(rot):
                    narr = rotate(narr, si, sj)
                # 유물의 개수 카운트
                t = count_clear(narr, 0)  # 0이라는 flag 사용해서 clear을 할지말지 결정 1일때만 clear
                if mx_cnt < t:
                    mx_cnt = t
                    marr = narr

    # 유물이 없는 경우 턴 종료
    if mx_cnt == 0: break

    cnt = 0  # 연쇄 획득 개수
    arr = marr
    # [3] 연쇄 획득 불가능 -> 다음 턴/ 가능하면 계속
    while True:  # 더 이상 3개 이상 연결되지 않아 유물이 될 수 없을 때까지 반복
        t = count_clear(arr, 1)  # 이 함수 내부에서 유물의 개수를 카운트하고 clear -> 숫자 채워넣기
        if t==0: break
        cnt += t

        for j in range(5):
            for i in range(4, -1, -1):
                if arr[i][j] == 0:
                    arr[i][j] = lst.pop(0)

    ans.append(cnt)
print(*ans)