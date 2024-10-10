'''
좌상단 = (1,1)
빈칸 = 0
벽 = 1~9

디버깅용으로
출구좌표 = 10
참가자 = 11, 12, 13 ...

K초 동안
    [1] 각 초마다 참가자 이동
        출구와 가까워지는 방향(좌표값 차들의 합)으로 상하좌우, 벽없는 곳 (한 칸에 2명 이상의 참가자 가능)
            여러군데이면? => 상하 우선시
            움직일 곳 없으면? => 움직이지 않음
    [2] 미로 회전
        [2-1] 출구와 최소 1명의 참가자를 포함한 최소 정사각형 잡기
            r작 -> c작
        [2-2] 정사각형 시계방향 90도 회전
            벽 -= 1
            0이 되면 -> 빈칸 변경
    [3] 모든 참가자가 미로 탈출 시 종료

print(모든 참가자들의 이동 거리 합, 출구 좌표)
'''
def rotate(arr, exit, sr, sc, w,units): #90도로 회전, 내구도 모두 -1씩
    narr = [x[:] for x in arr]
    new_exit = exit
    new_units = units
    for i in range(w):
        for j in range(w):
            narr[sr+i][sc+j] = arr[sr+w-j-1][sc+i]
            if 0<narr[sr+i][sc+j]<10:
                narr[sr+i][sc+j] -= 1
            if narr[sr+i][sc+j]==-1:
                new_exit = [sr+i,sc+j]
            if narr[sr+i][sc+j]>=10: #유닛이면 유닛도 회전
                old_position = [sr+w-j-1,sc+i]
                if old_position in units:
                    idx1 = units.index(old_position)
                    units[idx1] = [sr+i,sc+j]

    return narr, new_exit, new_units

def find_rectangle(N, arr):
    for w in range(2, N + 1):
        for sr in range(1, N - w + 2):
            for sc in range(1, N - w + 2):
                is_exit = False
                is_unit = False
                for r in range(sr, sr + w):
                    for c in range(sc, sc + w):
                        if arr[r][c] == -1: is_exit = True  # 출구 찾음
                        if arr[r][c] >= 10: is_unit = True  # 사람 찾음
                if is_exit and is_unit:
                    return sr,sc,w


N, M, K = map(int, input().split())
arr = [[0]*(N+2)]+[[0]+list(map(int,input().split()))+[0] for _ in range(N)]+[[0]*(N+2)]
units = [list(map(int, input().split())) for _ in range(M)] #arr에 대입할 때 -1 해줘야함
exit = list(map(int, input().split()))
out = [0]*M #탈출 시 1로
cnt = 0
ucnt = 10
arr[exit[0]][exit[1]]=-1


for ui, uj in units:
    arr[ui][uj] = ucnt
    ucnt += 1

for turn in range(1,K+1):
    #[1] 참가자 이동 arr == 0인 곳으로만 이동 가능
    # print(turn)
    # print("이동 전 :", arr)
    to_go = []
    for idx in range(M):
        if out[idx] == 1:
            continue
        si,sj = units[idx]
        ti,tj = exit
        cur_dist = abs(si-ti) + abs(sj-tj) #이동 전 출구와의 거리
        mn_dist = cur_dist
        # to_go = []
        # 각각의 참가자 이동 방향 결정
        for di,dj in ((-1,0),(1,0),(0,-1),(0,1)): #상하좌우
            ni,nj = si+di, sj+dj
            dist = abs(ti-ni)+abs(tj-nj) #이동 했을 시 출구와의 거리
            #범위 내 + 빈칸 + 가까워지는 방향 => 출구에 도착하면 참가자 탈출 !!
            if 1<=ni<=N and 1<=nj<=N and (arr[ni][nj]==0 or arr[ni][nj]==-1):
                if mn_dist>=dist:
                    mn_dist = dist
                    to_go.append([si,sj,ni,nj])
                    break
        # print("to_go:", si,sj,"->", to_go)
        #이동할 수 있을 경우 이동
    to_go.sort(key=lambda x: (x[0],x[1]))
    # print("to_go: ", to_go)
    for tg in to_go:
        si,sj,ni,nj = tg
        idx = units.index([si, sj])
        if exit!=[ni,nj]: #출구가 아닐때만
            arr[ni][nj] = arr[si][sj]
            units[idx] = [ni,nj]
        else:
            out[idx] = 1
        arr[si][sj] = 0
        cnt+=1

    # print("이동 후 : ", arr)
    # print("cnt : ", cnt)
    #[2-1] 최소 정사각형 잡기 r작->c작
    sr, sc, w = find_rectangle(N,arr)



    # print("기준 점 sr,sc, w" ,sr,sc,w)
    #[2-2] 미로 회전
    narr = [x[:] for x in arr]
    arr, exit, units = rotate(arr, exit, sr,sc,w,units) #내구도 -1
    # print("회전 후 : " , arr)
    # print()
    # print(turn, cnt, arr)
    #[3] 모든 참가자 미로 탈출 시 종료
    if out.count(0)==0: break

print(cnt)
print(*exit)