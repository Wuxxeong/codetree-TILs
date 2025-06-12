N,M,K = map(int, input().split()) #사람 최대 10명
arr = [list(map(int,input().split())) for _ in range(N)]
units = [list(map(int,input().split())) for _ in range(M)]
alive = [1]*M
for r,c in units:
    arr[r-1][c-1]-=1

ei,ej = list(map(int,input().split()))
ei,ej = ei-1, ej-1
arr[ei][ej]=-11

# 출구 탐색을 함수로 분리
def find_exit(arr):
    for i in range(N):
        for j in range(N):
            if arr[i][j] == -11:
                return i, j

def find_units(arr):
    units = []
    for i in range(N):
        for j in range(N):
            if -10 <= arr[i][j] <= -1:
                units.append((i, j))
    return units

def move(arr,ei,ej): # 동시 이동!!
    mv_cnt = 0
    units = find_units(arr)
    narr = [x[:] for x in arr]
    for ci,cj in units:
        dist = abs(ci-ei)+abs(cj-ej)
        for di,dj in ((-1,0),(1,0),(0,-1),(0,1)):
            ni,nj = ci+di,cj+dj
            if (ni,nj)==(ei,ej):
                mv_cnt+=arr[ci][cj]
                narr[ci][cj]-=arr[ci][cj]
                break
            elif 0<=ni<N and 0<=nj<N and arr[ni][nj]<=0 and dist>abs(ni-ei)+abs(nj-ej):
                mv_cnt+=arr[ci][cj]
                narr[ni][nj]+=arr[ci][cj]
                narr[ci][cj]-=arr[ci][cj]
                break
    return mv_cnt, narr

def make_rectangle():
    for w in range(2,N+1):
        for sr in range(N-w+1):
            for sc in range(N-w+1):
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
                narr[i+si][j+sj] = arr[w-j-1+si][i+sj]-1

    return narr

# for x in arr:
#     print(x)

cnt = 0 # 이동 횟수
for k in range(K):
    # [1] 참가자 이동
    t, arr = move(arr,ei,ej)
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
    ei,ej = find_exit(arr)
print(-cnt)
print(ei+1,ej+1)