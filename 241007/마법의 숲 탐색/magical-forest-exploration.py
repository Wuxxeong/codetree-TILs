R, C, K = map(int, input().split())
unit = [list(map(int, input().split())) for _ in range(K)]
arr = [[1]+[0]*C+[1] for _ in range(R+3)] + [[1]*(C+2)]
exit_set = set()

di, dj = [-1, 0, 1, 0], [0, 1, 0, -1]

def bfs(si,sj): #숫자가 같은 칸 or 나의 출구 인접 = 다른 골렘
    q = []
    visited = [[0]*(C+2) for _ in range(R+4)]
    mx_i = 0

    q.append((si,sj))
    visited[si][sj] = 1

    while q:
        ci,cj = q.pop(0)
        mx_i = max(mx_i, ci)
        for i in range(4):
            ni, nj = ci+di[i], cj+dj[i]
            if visited[ni][nj]==0 and (arr[ni][nj] == arr[ci][cj] or ((ci,cj) in exit_set) and arr[ni][nj] > 1):
                visited[ni][nj] = 1
                q.append((ni,nj))
    return mx_i-2


ans = 0
cnt = 2

for cj, dr in unit:
    ci = 1
    # [1]골렘을 최대한 남쪽으로 이동시키기
    while True:
        if arr[ci+1][cj-1]==0 and arr[ci+2][cj]==0 and arr[ci+1][cj+1]==0:
            ci += 1
        elif arr[ci][cj-2]==0 and arr[ci-1][cj-1]==0 and arr[ci+1][cj-1]==0 and arr[ci+1][cj-2]==0 and arr[ci+2][cj-1]==0:
            ci += 1
            cj -= 1
            dr = (dr-1)%4
        elif arr[ci][cj+2]==0 and arr[ci-1][cj+1]==0 and arr[ci+1][cj+1]==0 and arr[ci+2][cj+1]==0 and arr[ci+1][cj+2]==0:
            ci += 1
            cj += 1
            dr = (dr+1)%4
        else:
            break

    if ci < 4: #범위 밖으로 나갈 경우 arr 재배열
        arr = [[1] + [0] * C + [1] for _ in range(R + 3)] + [[1] * (C + 2)]
        exit_set = set() ###
        cnt = 2
    # [2] 정령 이동
    else:
        arr[ci-1][cj] = arr[ci+1][cj] = cnt
        arr[ci][cj-1:cj+2] = [cnt]*3 ###
        exit_set.add((ci+di[dr], cj+dj[dr])) ###
        cnt += 1
        ans += bfs(ci,cj)

print(ans)