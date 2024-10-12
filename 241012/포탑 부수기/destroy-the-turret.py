N, M, K = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]
turn = [[0] * M for _ in range(N)]  # 공격한 턴수를 기록(최근공격 체크)

from collections import deque
def bfs(si,sj,ei,ej):
    q = deque()
    v = [[[] for _ in range(M)] for _ in range(N)]  # 경로를 표시하기 위한 visited

    q.append((si,sj))
    v[si][sj]=(si,sj)
    d = arr[si][sj]             # demage

    while q:
        ci,cj = q.popleft()
        if (ci,cj)==(ei,ej):            # 목적지 좌표 도달
            arr[ei][ej]=max(0, arr[ei][ej]-d)   # 목표 d만큼 타격
            while True:
                ci,cj = v[ci][cj]       # 직전좌표
                if (ci,cj)==(si,sj):    # 시작(공격자)까지 되집어 왔으면 종료
                    return True
                arr[ci][cj]=max(0,arr[ci][cj]-d//2)
                fset.add((ci,cj))

        # 우선순위: 우/하/좌/상 (미방문, 조건: >0 포탑있고)
        for di,dj in ((0,1),(1,0),(0,-1),(-1,0)):
            ni,nj = (ci+di)%N, (cj+dj)%M    # 반대편으로 연결
            if len(v[ni][nj])==0 and arr[ni][nj]>0:
                q.append((ni,nj))
                v[ni][nj]=(ci,cj)
    # 목적지 찾지 못함!!!
    return False

def bomb(si,sj,ei,ej):
    d = arr[si][sj]                         # demage
    # print(ei,ej)
    arr[ei][ej] = max(0, arr[ei][ej] - d)   # 목표 d만큼 타격
    # 목표좌료 주변 8개에 1/2피해 (나를 제외한)
    for di,dj in ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)):
        ni, nj = (ei+di) % N, (ej+dj) % M  # 반대편으로 연결
        if (ni,nj)!=(si,sj):
            arr[ni][nj] = max(0, arr[ni][nj]-d//2)
            fset.add((ni,nj))

for T in range(1, K + 1):
    # [1] 공격자 선정: 공격력 낮은->가장 최근 공격자->행+열(큰)->열(큰)
    mn, mx_turn, si, sj = 5001, 0, -1, -1
    for i in range(N):
        for j in range(M):
            if arr[i][j]<=0:    continue    # 포탑이 아니면 skip
            if mn>arr[i][j] or (mn==arr[i][j] and mx_turn<turn[i][j]) or \
                (mn==arr[i][j] and mx_turn==turn[i][j] and si+sj<i+j) or \
                (mn==arr[i][j] and mx_turn==turn[i][j] and si+sj==i+j and sj<j):
                mn, mx_turn, si, sj = arr[i][j], turn[i][j], i, j   # si,sj 공격자

    # [2] 공격(공격당할 포탑선정) & 포탑부서짐
    # 2-1) 공격 당할 포탑 선정: 공격력 높은->가장 오래전 공격->행+열(작은)->열(작은)
    mx, mn_turn, ei, ej = 0, T, N, M
    for i in range(N):
        for j in range(M):
            if arr[i][j]<=0:    continue    # 포탑이 아니면 skip
            if mx<arr[i][j] or (mx==arr[i][j] and mn_turn>turn[i][j]) or \
                (mx==arr[i][j] and mn_turn==turn[i][j] and ei+ej>i+j) or \
                (mx==arr[i][j] and mn_turn==turn[i][j] and ei+ej==i+j and ej>j):
                mx, mn_turn, ei, ej = arr[i][j], turn[i][j], i, j   # ei,ej 공격대상자

    # 2-2) 레이저공격 (우하좌상 순서로 최단거리이동-BFS, %N, %M 처리 필요(양끝연결))
    arr[si][sj]+=(N+M)  # 공격력 상승        # 즉시반영시 가장 센 포탑이 될 수도 있음
    turn[si][sj]=T      # 이번턴에 공격
    fset = set()
    fset.add((si,sj))
    fset.add((ei,ej))
    if bfs(si,sj,ei,ej)==False:     # 레이저공격 실패

        # 2-3) 포탄공격(레이저로 목적지 도달 못할 경우)
        bomb(si,sj,ei,ej)

    # [3] 포탑정비(공격에 상관없었던 포탑들 +1)
    for i in range(N):
        for j in range(M):
            if arr[i][j]>0 and (i,j) not in fset:
                arr[i][j]+=1

    cnt = N*M
    for lst in arr:
        cnt-=lst.count(0)
    if cnt<=1:              # 남은 포탑이 1이하면 종료!
        break

print(max(map(max, arr)))