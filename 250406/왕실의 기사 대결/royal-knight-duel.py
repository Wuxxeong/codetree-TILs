L,N,Q = map(int,input().split())
arr = [[2]*(L+2)] + [[2]+list(map(int,input().split()))+[2] for _ in range(L)] + [[2]*(L+2)]
king = [list(map(int,input().split())) for _ in range(N)] #(r,c,h,w,k) cnt=3부터 시작
commands = [list(map(int,input().split())) for _ in range(Q)] #(i,d) i번 기사 , d방향으로 이동

di,dj = [-1,0,1,0],[0,1,0,-1]

alive = [1]*N #살아있는 i-1 번 기사
damage = [0]*N

arr_king = [[2]*(L+2)] + [[2]+[0]*L+[2] for _ in range(L)] + [[2]*(L+2)]

cnt = 3
for r,c,h,w,k in king:
    for i in range(r,r+h):
        for j in range(c,c+w):
            arr_king[i][j] = cnt
    cnt += 1

# for command in commands:
#     i,d = command
#     narr_king = [x[:] for x in arr_king]

def get_chain(i, d, king_pos):
    # i번 기사부터 시작해 연쇄적으로 밀릴 기사들 반환
    visited = set()
    q = [i]
    while q:
        curr = q.pop()
        visited.add(curr)
        r, c, h, w, k = king[curr]
        for nr in range(r, r+h):
            for nc in range(c, c+w):
                ni, nj = nr+di[d], nc+dj[d]
                if arr_king[ni][nj] >= 3 and arr_king[ni][nj]-3 not in visited:
                    q.append(arr_king[ni][nj]-3)
    return list(visited)

def can_move(chain, d):
    for idx in chain:
        r, c, h, w, _ = king[idx]
        for i in range(r, r+h):
            for j in range(c, c+w):
                ni, nj = i+di[d], j+dj[d]
                if arr[ni][nj] == 2:  # 벽
                    return False
    return True

def move_chain(chain, d):
    # 1. 기존 자리 지움
    for idx in chain:
        r, c, h, w, _ = king[idx]
        for i in range(r, r+h):
            for j in range(c, c+w):
                arr_king[i][j] = 0

    # 2. 위치 이동
    for idx in chain:
        king[idx][0] += di[d]  # r
        king[idx][1] += dj[d]  # c

    # 3. 새로운 위치 표시
    for idx in chain:
        r, c, h, w, _ = king[idx]
        for i in range(r, r+h):
            for j in range(c, c+w):
                arr_king[i][j] = idx + 3


def apply_damage(moved_idx, pusher_idx):
    for idx in moved_idx:
        if idx == pusher_idx: continue
        r, c, h, w, hp = king[idx]
        dmg = 0
        for i in range(r, r+h):
            for j in range(c, c+w):
                if arr[i][j] == 1:
                    dmg += 1
        damage[idx] += dmg
        king[idx][4] -= dmg  # 체력 감소
        if king[idx][4] <= 0:
            alive[idx] = 0
            # 죽은 기사 제거
            for i in range(r, r+h):
                for j in range(c, c+w):
                    arr_king[i][j] = 0


for i, d in commands:
    i -= 1
    if not alive[i]:
        continue

    chain = get_chain(i, d, king)
    if not can_move(chain, d):
        continue

    move_chain(chain, d)
    apply_damage(chain, i)

ans = 0
for i in range(N):
    if alive[i]:
        ans+=damage[i]
print(ans)