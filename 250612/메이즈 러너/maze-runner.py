'''
미로 구성
    빈칸 = 0
    벽 = 1~9 회전시 1감소
    출구

while K초 동안:
    **모든 참가자들이 탈출시 종료**
    1. 참가자 이동 1칸씩
        상하좌우,벽 없는 곳으로 이동
        출구가 가까워지는 방향
        상하 우선
    2. 미로 회전
        1) 정사각형 잡기
            출구와 한명 이상의 참가자 포함.  v
            r작 c작   v
        2) 90도 회전.  v
            내구도-=1  v

출력 : 모든 참가자들의 이동 거리 합, 출구 좌표

출구 = -11
사람 = -1로 표현. -2,-3은 겹친는 것
'''

N,M,K = map(int, input().split()) #사람 최대 10명
arr = [list(map(int,input().split())) for _ in range(N)]
units = [list(map(int,input().split())) for _ in range(M)]
alive = [1]*M
for r,c in units:
    arr[r-1][c-1]-=1

ei,ej = list(map(int,input().split()))
ei,ej = ei-1, ej-1
arr[ei][ej]=-11

def find_units(arr):
    units = []
    for i in range(N):
        for j in range(N):
            if -10 <= arr[i][j] <= -1:
                units.append((i, j))
    return units

def move1(arr,ei,ej):
    mv_cnt = 0
    units = find_units(arr)

    narr = [x[:] for x in arr]
    for ci,cj in units:

        dist = abs(ci-ei)+abs(cj-ej)
        for di,dj in ((-1,0),(1,0),(0,-1),(0,1)):
            ni,nj = ci+di,cj+dj
            if (ni,nj)==(ei,ej):
                mv_cnt+=narr[ci][cj]
                narr[ci][cj]=0
                break
            elif 0<=ni<N and 0<=nj<N and narr[ni][nj]<=0 and dist>abs(ni-ei)+abs(nj-ej):
                mv_cnt+=narr[ci][cj]
                narr[ni][nj]+=narr[ci][cj]
                narr[ci][cj]=0

                break
    return mv_cnt, narr

def move(arr,units,ei,ej):
    mv_cnt = 0
    narr = [x[:] for x in arr]
    # units이 어디서 어디로?
    for idx in range(M):
        if not alive[idx]: continue
        ci,cj = units[idx][0]-1, units[idx][1]-1
        dist = abs(ci-ei)+abs(cj-ej)
        for di,dj in ((-1,0),(1,0),(0,-1),(0,1)):
            ni,nj = ci+di, cj+dj
            if 0<=ni<N and 0<=nj<N and narr[ni][nj]<=0 and dist>abs(ni-ei)+abs(nj-ej):
                if (ni,nj)==(ei,ej):
                    alive[idx]=0
                else:
                    narr[ni][nj] -= 1
                narr[ci][cj]=0
                mv_cnt+=1
                break
    return mv_cnt, narr

def make_rectangle():
    for w in range(2,N+1):
        for sr in range(N-w):
            for sc in range(N-w):
                isExit, isAny = False,False
                for r in range(sr,sr+w):
                    for c in range(sc,sc+w):
                        if arr[r][c]==-11:
                            isExit = True
                        if -10<=arr[r][c]<=-1:
                            isAny = True
                if isExit and isAny:
                    return sr,sc,w
    return -1

def rotate(arr,si,sj,w): # 내구도 1 감소
    narr = [x[:] for x in arr]
    for i in range(w):
        for j in range(w):
            if -11<=arr[w-j-1+si][i+sj]<=0:
                narr[i+si][j+sj] = arr[w-j-1+si][i+sj]
            else:
                narr[i + si][j + sj] = arr[w - j - 1 + si][i + sj]-1

    return narr

# for x in arr:
#     print(x)

cnt = 0 # 이동 횟수
for k in range(K):
    # [1] 참가자 이동
    t, arr = move1(arr,ei,ej)
    cnt += t
    u = find_units(arr)
    if len(u)==0:
        break
    # [2] 정사각형 설정
    sr,sc,w = make_rectangle()

    # [3] 90도 회전
    narr = [x[:] for x in arr]
    narr = rotate(narr,sr,sc,w)
    arr = narr
    # [4] 출구 좌표 갱신
    for i in range(N):
        for j in range(N):
            if arr[i][j]==-11:
                ei,ej = i,j
                break
print(-cnt)
print(ei+1,ej+1)