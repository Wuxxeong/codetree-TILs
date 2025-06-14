from collections import deque

N, Q = map(int, input().split())
bug = [list(map(int, input().split())) for _ in range(Q)]
arr = [[0]*N for _ in range(N)]

dy = [-1, 0, 1, 0]
dx = [0, -1, 0, 1]

def in_range(r, c):
    return 0 <= r < N and 0 <= c < N

def get_connected_cnt(k):
    visited = [[0]*N for _ in range(N)]
    cnt = 0
    for i in range(N):
        for j in range(N):
            if arr[i][j] == k and visited[i][j] == 0:
                cnt += 1
                q = deque([(i,j)])
                visited[i][j] = 1
                while q:
                    y,x = q.popleft()
                    for d in range(4):
                        ny, nx = y+dy[d], x+dx[d]
                        if in_range(ny,nx) and arr[ny][nx]==k and visited[ny][nx]==0:
                            visited[ny][nx] = 1
                            q.append((ny,nx))
    return cnt

def find_seperate(turn):
    # get_connected_cnt을 재활용
    for k in range(1, turn+1):
        if get_connected_cnt(k) >= 2:
            for i in range(N):
                for j in range(N):
                    if arr[i][j] == k:
                        arr[i][j] = 0
    return arr

def find_extent(k):
    return sum(1 for i in range(N) for j in range(N) if arr[i][j]==k)

def make_order(extents):
    order = [(extents[i], i+1) for i in range(len(extents))]
    order.sort(key=lambda x:(-x[0], x[1]))
    return [oid for _, oid in order]

def move(narr, insert_idx):
    marr = [[0]*N for _ in range(N)]
    for k in insert_idx:
        cells = [(i,j) for i in range(N) for j in range(N) if narr[i][j]==k]
        if not cells:
            continue
        origin = cells[0]
        rel = [(i-origin[0], j-origin[1]) for i,j in cells]
        placed = False
        for si in range(N):
            if placed: break
            for sj in range(N):
                ok = True
                for di,dj in rel:
                    ni, nj = si+di, sj+dj
                    if not (0<=ni<N and 0<=nj<N and marr[ni][nj]==0):
                        ok = False
                        break
                if ok:
                    for di,dj in rel:
                        marr[si+di][sj+dj] = k
                    placed = True
                    break
    return marr

def calculate(arr):
    visited = [[0]*N for _ in range(N)]
    gmap = [[0]*N for _ in range(N)]
    garea = {}
    gid = 1
    for i in range(N):
        for j in range(N):
            if arr[i][j]>0 and visited[i][j]==0:
                q = deque([(i,j)])
                visited[i][j] = 1
                gmap[i][j] = gid
                cnt = 1
                while q:
                    y,x = q.popleft()
                    for d in range(4):
                        ny, nx = y+dy[d], x+dx[d]
                        if in_range(ny,nx) and visited[ny][nx]==0 and arr[ny][nx]==arr[i][j]:
                            visited[ny][nx] = 1
                            gmap[ny][nx] = gid
                            cnt += 1
                            q.append((ny,nx))
                garea[gid] = cnt
                gid += 1

    total = 0
    seen = set()
    for i in range(N):
        for j in range(N):
            a = gmap[i][j]
            if a == 0: continue
            for d in range(4):
                ni, nj = i+dy[d], j+dx[d]
                if in_range(ni,nj):
                    b = gmap[ni][nj]
                    if b>0 and a<b and (a,b) not in seen:
                        total += garea[a]*garea[b]
                        seen.add((a,b))
    return total

# —————— 사용자가 원하시는 루프 ——————
for turn in range(1, Q+1):
    # [1] 미생물 투입
    si, sj, ei, ej = bug[turn-1]
    for i in range(si,ei):
        for j in range(sj,ej):
            arr[i][j] = turn

    # [1-1] 분리된 무리 제거
    arr = find_seperate(turn)

    # [1-2] 투입 순서 결정
    extents = [ find_extent(i+1) for i in range(turn) ]
    insert_idx = make_order(extents)

    # [2-2] 옮기기
    narr = [row[:] for row in arr]
    dag = move(narr, insert_idx)
    arr = dag

    # [3] 인접 넓이 계산 및 출력
    print(calculate(arr))
