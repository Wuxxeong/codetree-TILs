'''
탐색 -> 가장 남쪽의 칸으로 갈 때까지
1) 남쪽으로 한 칸 내려감 (초록색 칸 비어있는 경우에만)
2) 안되면 서쪽으로 (초록색 칸 비어있는 경우에만)
    - 출구 반시계 방향으로 이동
3) 안되면 동쪽으로 (초록색 칸 비어있는 경우에만)
    - 출구 시계 방향 이동
정령의 이동
1) 남쪽으로 이동
2) 출구가 연결되어있으면 이동 가능

전략 => 골렘의 번호를 각각 다르게 설정하고, 출구를 저장해둔다.
'''

R,C,K = map(int,input().split())
unit = [list(map(int,input().split())) for _ in range(K)]
arr = [[1]+[0]*C+[1] for _ in range(R+3)] + [[1]*(C+2)]
exit_set = set()
ei,ej = [-1,0,1,0],[0,1,0,-1] #북동남서




def bfs(ci, cj):
    q = []
    v = [[0]*(C+2) for _ in range(R+4)]

    q.append((ci,cj))
    v[ci][cj]=1

    mx_i = 0
    while q:
        si,sj = q.pop(0)
        mx_i = max(mx_i,si)
        for i in range(4):
            ni,nj = si+ei[i],sj+ej[i]
            if v[ni][nj]==0 and (arr[ni][nj]==arr[si][sj] or ((si,sj) in exit_set) and arr[ni][nj]>1):
                q.append((ni,nj))
                v[ni][nj]=1

    return mx_i-2

ans = 0
cnt = 2 #골렘 체크용
for cj,dr in unit:
    # [1] 골렘 이동
    ci = 1
    while True:
        if arr[ci + 1][cj - 1] == 0 and arr[ci + 2][cj] == 0 and arr[ci + 1][cj + 1] == 0:
            ci += 1
        elif arr[ci][cj - 2] == 0 and arr[ci - 1][cj - 1] == 0 and arr[ci + 1][cj - 1] == 0 and arr[ci + 1][
            cj - 2] == 0 and arr[ci + 2][cj - 1] == 0:
            ci += 1
            cj -= 1
            dr = (dr - 1) % 4
        elif arr[ci][cj + 2] == 0 and arr[ci - 1][cj + 1] == 0 and arr[ci + 1][cj + 1] == 0 and arr[ci + 2][
            cj + 1] == 0 and arr[ci + 1][cj + 2] == 0:
            ci += 1
            cj += 1
            dr = (dr + 1) % 4
        else:
            break

    if ci<4:
        arr = [[1] + [0] * C + [1] for _ in range(R + 3)] + [[1] * (C + 2)]
        exit_set = set()
        cnt = 2
    else:
        # [2] 정령의 이동
        arr[ci][cj-1:cj+2] = [cnt]*3
        arr[ci-1][cj] = arr[ci+1][cj] = cnt
        cnt += 1
        exit_set.add((ci+ei[dr],cj+ej[dr]))
        ans += bfs(ci,cj)
print(ans)