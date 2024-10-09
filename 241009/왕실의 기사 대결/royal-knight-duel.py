L,N,Q = map(int, input().split())
arr = [[2]*(L+2)] + [[2]+list(map(int,input().split()))+[2]for _ in range(L)] + [[2]*(L+2)]
units = {}
init_k = [0]*(N+1)

for i in range(1,N+1):
    r,c,h,w,k = map(int, input().split())
    units[i] = [r,c,h,w,k]
    init_k[i] = k

dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]
damage = [0]*(N+1)
def bfs(start, d):
    q = []
    visited = set()

    q.append(start)
    visited.add(start)

    while q:
        cur = q.pop(0)
        sr,sc,sh,sw,sk = units[cur]
        nr, nc = sr+dr[d], sc+dc[d]
        for i in range(nr, nr+h):
            for j in range(nc, nc+w):
                if arr[i][j] == 2:
                    return
                if arr[i][j] == 1:
                    damage[cur] += 1
        #밀려나가는 기사들을 저장
        for idx in units:
            if idx in visited: continue
            tr,tc,th,tw,tk = units[idx]
            if nr <= tr+th-1 and nr+sh-1>=tr and tc<=nc+sw-1 and nc<=tc+tw-1:
                q.append(idx)
                visited.add(idx)
    
    damage[start] = 0
    for idx in visited:
        vr,vc,vh,vw,vk = units[idx]

        if vk<=damage[idx]:
            units.pop(idx)
        else:
            nr, nc = vr+dr[d], vc+dc[d]
            units[idx] = [nr,nc,vh,vw,vk-damage[idx]]

for _ in range(Q):
    i,d = map(int, input().split())
    bfs(i,d) #기사 이동 + 데미지 감소

ans = 0
for idx in units:
    ans += init_k[idx]-units[idx][4]
print(ans)