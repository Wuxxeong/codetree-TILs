def find_3d_start():
    for i in range(M):
        for j in range(M):
            if arr3[4][i][j]==2:
                return 4,i,j

def find_2d_end():
    for i in range(N):
        for j in range(N):
            if arr[i][j]==4:
                arr[i][j]=0 ##############kick
                return i,j

def find_3d_base():
    for i in range(N):
        for j in range(M):
            if arr[i][j]==3:
                return i,j
def find_3d_end_2d_start(): #하나씩 나누어서 생각해볼 수 있다.###############3
    bi,bj = find_3d_base()

    for i in range(bi,bi+M):
        for j in range(bj,bj+M):
            if arr[i][j]!=3: continue
            if arr[i][j+1]==0: #동
                return 0, M-1, (M-1)-(i-bi), i, j+1
            elif arr[i][j-1]==0: #서
                return 1, M-1, i-bi, i, j-1
            elif arr[i+1][j]==0: #남
                return 2, M-1, j-bj, i+1, j
            elif arr[i-1][j]==0: #북
                return 3, M-1,  (M-1)-(j-bj), i-1, j
def bfs_3d(sk,si,sj,ek,ei,ej):
    left_nxt = {0:2,2:1,1:3,3:0,4:1}
    right_nxt = {0:3,3:1,1:2,2:0,4:0}

    q = []
    v = [[[0]*M for _ in range(M)] for _ in range(5)]

    q.append((sk, si, sj))
    v[sk][si][sj] = 1

    while q:
        ck,ci,cj = q.pop(0)
        if (ck,ci,cj)==(ek,ei,ej):
            return v[ck][ci][cj]

        for di,dj in ((-1,0),(0,1),(1,0),(0,-1)):
            ni,nj = ci+di,cj+dj
            if nj>=M: #동쪽으로 벗어남
                if ck==4:   nk,ni,nj = 0,0,(M-1)-ci
                else:       nk,ni,nj = right_nxt[ck],ci,0
            elif nj<0: #서쪽으로 벗어남
                if ck==4:   nk,ni,nj = 1,0,ci
                else:       nk,ni,nj = left_nxt[ck],ci,(M-1)
            elif ni>=M: #남쪽으로 벗어남
                if ck==4:   nk,ni,nj = 2, 0, cj
                else: continue
            elif ni<0: #북쪽으로 벗어남
                if ck==0:   nk,ni,nj = 4,(M-1)-ci,M-1
                elif ck==1: nk,ni,nj = 4,cj,0
                elif ck==2: nk,ni,nj = 4,M-1,cj
                elif ck==3: nk,ni,nj = 4,0,(M-1)-cj
                elif ck==4: nk,ni,nj = 3,0,(M-1)-cj
            else:
                nk=ck

            if arr3[nk][ni][nj]==0 and v[nk][ni][nj]==0: #길이고, 미방문이면
                q.append((nk,ni,nj))
                v[nk][ni][nj] = v[ck][ci][cj]+1


def bfs_2d(v,dist,si,sj,ei,ej):
    q = []
    q.append((si,sj))

    v[si][sj] = dist

    while q:
        ci,cj = q.pop(0)
        if (ci,cj)==(ei,ej):
            return v[ci][cj]

        for di,dj in ((-1,0),(0,1),(1,0),(0,-1)):
            ni,nj = ci+di, cj+dj
            if 0<=ni<N and 0<=nj<N and arr[ni][nj]==0 and v[ci][cj]+1<v[ni][nj]:
                q.append((ni,nj))
                v[ni][nj] = v[ci][cj]+1
    return -1
##############################################################################################
##############################################################################################
N, M, F = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]
arr3 = [[list(map(int, input().split())) for _ in range(M)] for _ in range(5)] # 동 서 남 북 위
wall = [list(map(int,input().split())) for _ in range(F)]

# [1] 각각의 좌표 찾기
sk,si_3d,sj_3d = find_3d_start() #3d 출발 좌표
ei_2d,ej_2d = find_2d_end() #2d 끝 좌표
ek,ei_3d,ej_3d,si_2d,sj_2d = find_3d_end_2d_start() #3d 끝, 2d 출발 좌표

# [2] bfs_3d 하기
dist = bfs_3d(sk,si_3d,sj_3d,ek,ei_3d,ej_3d)
# 동 서 남 북
di=[ 0, 0, 1,-1]
dj=[ 1,-1, 0, 0]
if dist != -1:
    # [3] 미리 이상 현상 진행 세팅해놓기 (시간에 맞게끔 확산되는 것이 아니라) arr에 세팅
    v = [[401]*N for _ in range(N)]
    for wi,wj,wd,wv in wall:
        v[wi][wj]=1
        for mul in range(1,N+1):
            wi,wj = wi+di[wd], wj+dj[wd]
            if 0<=wi<N and 0<=wj<N and arr[wi][wj]==0 and (wi,wj)!=(ei_2d,ej_2d):
                if v[wi][wj]>wv*mul:  # 더 큰 값 일때만 갱신(겹칠수있으니)
                    v[wi][wj]=wv*mul
            else:
                break
    # [4] bfs_2d 돌리기
    dist = bfs_2d(v,dist,si_2d,sj_2d,ei_2d,ej_2d)
print(dist)