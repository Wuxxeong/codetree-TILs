# 출력 => 전사가 이동한 거리의 합, 돌이 된 수, 메두사 공격한 전사의 수
#   상0,우상1,우2,우하3,하4,좌하5,좌6,좌상7
di = [-1,-1,0,1,1,1,0,-1]
dj = [0,1,1,1,0,-1,-1,-1]

def find_route(si,sj,ei,ej):
    q = []
    v = [[0]*N for _ in range(N)]

    q.append((si,sj))
    v[si][sj]=((si,sj))          # 직전위치를 저장

    while q:
        ci,cj = q.pop(0)

        if (ci,cj)==(ei,ej):        # 목적지 도착! 경로 저장
            route = []
            ci,cj = v[ci][cj]
            while (ci,cj)!=(si,sj): # 출발지가 아니라면 저장
                route.append((ci,cj))
                ci,cj = v[ci][cj]
            return route[::-1]      # 역순(메두사 이동순서대로) 리턴

        # 네방향(상하좌우!), 범위내, 미방문, 조건(==0)
        for di,dj in ((-1,0),(1,0),(0,-1),(0,1)):
            ni,nj = ci+di, cj+dj
            if 0<=ni<N and 0<=nj<N and v[ni][nj]==0 and arr[ni][nj]==0:
                q.append((ni,nj))
                v[ni][nj]=(ci,cj)

    # 이곳까지 왔다는 얘기는?? 목적지 못찾음
    return -1

def mark_line(v,ci,cj,dr): # 전사를 만나서 2로 가려짐을 표시
    while 0<=ci<N and 0<=cj<N:
        v[ci][cj]=2
        ci,cj = ci+di[dr],cj+dj[dr]

def mark_safe(v,si,sj,dr,org_dr):
    ci,cj = si+di[dr],sj+dj[dr]
    mark_line(v,ci,cj,dr)

    ci,cj = si+di[org_dr],sj+dj[org_dr],
    while 0<=ci<N and 0<=cj<N:
        mark_line(v,ci,cj,dr)
        ci,cj = ci+di[org_dr], cj+dj[org_dr]
def make_stone(marr,mi,mj,dr): # return tv,tstone -> 시야배열과, 돌 된 개수
    # 현재 메두사가 dr 방향으로 바라봄
    v = [[0]*N for _ in range(N)]
    cnt = 0

    ni,nj = mi+di[dr],mj+dj[dr]
    while 0<=ni<N and 0<=nj<N:
        v[ni][nj]=1
        if marr[ni][nj]>0: #시야에 걸리는 놈 있으면
            cnt+=marr[ni][nj]
            ni,nj = ni+di[dr],nj+dj[dr]
            mark_line(v,ni,nj,dr) #그 뒤로는 v배열에 2 저장
            break
        ni,nj = ni+di[dr],nj+dj[dr]

    for org_dr in ((dr-1)%8,(dr+1)%8):
        si,sj = mi+di[org_dr],mj+dj[org_dr]
        while 0<=si<N and 0<=sj<N:
            if v[si][sj]==0 and marr[si][sj]>0:
                v[si][sj]=1
                cnt+=marr[si][sj]
                mark_safe(v,si,sj,dr,org_dr)
                break

            ci,cj = si,sj
            while 0<=ci<N and 0<=cj<N:
                if v[ci][cj]==0:
                    v[ci][cj]=1
                    if marr[ci][cj]>0:
                        cnt+=marr[ci][cj]
                        mark_safe(v,ci,cj,dr,org_dr)
                else:
                    break
                ci,cj = ci+di[dr],cj+dj[dr]

            si,sj = si+di[org_dr],sj+dj[org_dr]
    return v,cnt

def move_men(v,mi,mj):
    #(상하좌우),(좌우상하) 메두사 시야가 아니면
    move,attk = 0,0

    for dirs in (((-1,0),(1,0),(0,-1),(0,1)), ((0,-1),(0,1),(-1,0),(1,0))):
        for idx in range(len(men)-1,-1,-1):
            ci,cj = men[idx]
            if v[ci][cj]==1:
                continue

            dist = abs(mi-ci)+abs(mi+ci)
            for di,dj in dirs:
                ni,nj = ci+di,cj+dj
                if 0<=ni<N and 0<=nj<N and v[ni][nj]!=1 and dist>abs(mi-ni)+abs(mj-nj):
                    if (ni,nj)==(mi,mj):
                        attk+=1
                        men.pop(idx)
                    else:
                        men[idx] = [ni,nj]
                    move+=1
                    break
    return move,attk

N,M = map(int,input().split())
si,sj,ei,ej = map(int,input().split())
tlst = list(map(int,input().split()))
men = []
for i in range(0,M*2,2):
    men.append([tlst[i],tlst[i+1]])
arr = [list(map(int,input().split())) for _ in range(N)]


# [1] 메두사 최단거리 구하기
route = find_route(si,sj,ei,ej) # route 배열 반환

if route==-1:
    print(-1)
else:
    for mi,mj in route:
        move_cnt, attk_cnt = 0,0
        # [1-1] 메두사 이동에 의한 전사들 삭제
        for i in range(len(men)-1,-1,-1):
            if men[i]==[mi,mj]:
                men.pop(i)

        # 전사들 몇명인지 기록 용도
        marr = [[0]*N for _ in range(N)]
        for ti,tj in men:
            marr[ti][tj]+=1

        # [2] 시선 결정
        mx_stone = -1
        v = [] # 결정된 시야 범위 배열 (0:빈땅, 1:메두사 시선, 2:전사에 가려진 곳)
        for dr in (0,4,6,2): #상하좌우순으로 dr 방향으로 결정
            tv,tstone = make_stone(marr,mi,mj,dr)
            if tstone>mx_stone:
                mx_stone = tstone
                v = tv

        # [3] 전사들의 이동
        move_cnt, attk_cnt = move_men(v,mi,mj)

        print(move_cnt, mx_stone, attk_cnt)
print(0)