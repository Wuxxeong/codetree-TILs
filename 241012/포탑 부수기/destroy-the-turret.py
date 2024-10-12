N,M,K = map(int, input().split())
arr = [list(map(int,input().split())) for _ in range(N)]
turn = [[0]*M for _ in range(N)]

#레이저 공격 가능하면 공격하고 True 반환 안되면 False 반환
def bfs(si,sj,ei,ej):
    v = [[[]for _ in range(M)] for _ in range(N)]
    v[si][sj] = (si,sj)

    q = []
    q.append((si,sj))
    
    d = arr[si][sj]
    
    while q:
        ci,cj = q.pop(0)
        
        if (ci,cj)==(ei,ej):
            arr[ci][cj] = max(0, arr[ci][cj]-d)
            while True:
                ci,cj = v[ci][cj] #직전좌표
                if (ci,cj)==(si,sj):
                    return True
                arr[ci][cj] = max(0, arr[ci][cj]-d//2)
                fset.add((ci,cj))
        
        for di,dj in ((-1,0),(1,0),(0,-1),(0,1)):
            ni,nj = (ci+di)%N, (cj+dj)%M
            if arr[ni][nj]>0 and len(v[ni][nj])==0:
                q.append((ni,nj))
                v[ni][nj] = (ci,cj)

    return False

def bomb(si,sj,ei,ej):
    d = arr[si][sj]
    arr[ei][ej] = max(0,arr[ei][ej]-d)
    for di,dj in range((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)):
        ni,nj=(ci+di)%N, (cj+dj)%M
        if arr[ni][nj]>0 and (ni,nj)!=(si,sj):
            arr[ni][nj] = max(0, arr[ni][nj]-d//2)
            fset.add((ni,nj))

for T in range(K): 
    mn, mx_turn,si,sj = 5001, 0, -1, -1
    #1 공격자 선정
    for i in range(N):
        for j in range(M):
            if arr[i][j]<=0: continue
            if mn>arr[i][j] or (mn==arr[i][j] and mx_turn<turn[i][j]) or \
            (mn==arr[i][j] and mx_turn==turn[i][j] and si+sj<i+j) or \
            (mn==arr[i][j] and mx_turn==turn[i][j] and si+sj==i+j and sj<j):
                mn,mx_turn,si,sj = arr[i][j],turn[i][j],i,j
    #2 대상자 선정
    mx,mn_turn,ei,ej = 0, T, N, M
    for i in range(N):
        for j in range(M):
            if arr[i][j]<=0: continue
            if mx<arr[i][j] or (mx==arr[i][j] and mn_turn>turn[i][j]) or \
            (mn==arr[i][j] and mn_turn==turn[i][j] and ei+ej>i+j) or \
            (mn==arr[i][j] and mn_turn==turn[i][j] and ei+ej==i+j and sj>j):
                mx,mn_turn,ei,ej  = arr[i][j],turn[i][j],i,j
    
    arr[si][sj]+=(N+M)
    turn[si][sj]=T

    fset = set()
    fset.add((si,sj))
    fset.add((ei,ej))

    #3 공격
    if not bfs(si,sj,ei,ej):
        bomb(si,sj,ei,ej)
    
    #4 포탑 정비
    for i in range(N):
        for j in range(N):
            if (i,j) not in fset:
                arr[i][j]+=1

    cnt = N*M
    for lst in arr:
        cnt -= lst.count(0)
    if cnt<=1:
        break

print(max(map(max,arr)))