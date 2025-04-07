di = [-1, 0, 1, 0]
dj = [ 0, 1, 0,-1]

L,N,Q = map(int,input().split())
arr = [[2]*(L+2)] + [[2]+list(map(int,input().split()))+[2] for _ in range(L)] +[[2]*(L+2)]
units = {}
init_k = [0]*(N+1)

for m in range(1,N+1):
    units[m] = list(map(int,input().split()))
    init_k[m] = units[m][4]

#start부터 dr 방향으로 밀기
def push_unit(start, dr):
    q = []
    pset = set() #밀린 놈들 저장
    damage = [0]*(N+1)

    q.append(start)
    pset.add(start)

    while q:
        curr = q.pop(0)
        ci,cj,h,w,k = units[curr]

        # [1] 이동
        ni,nj = ci+di[dr],cj+dj[dr]
        for i in range(ni,ni+h):
            for j in range(nj,nj+w):
                if arr[i][j]==2:
                    return
                if arr[i][j]==1:
                    damage[curr]+=1

        # [2] 모든 유닛들에 대해 겹침 여부 판단
        for idx in units:
            if idx in pset: continue
            ti,tj,th,tw,tk = units[idx]

            if ni<=ti+th-1 and nj<=tj+tw-1 and ti<=ni+h-1 and tj<=nj+w-1: #겹치면
                q.append(idx)
                pset.add(idx)

    # [3] damage 반영 및 실제 이동 처리
    damage[start] = 0

    for idx in pset:
        si,sj,sh,sw,sk = units[idx]
        if damage[idx]>=sk:
            units.pop(idx)
        else:
            ni,nj = si+di[dr],sj+dj[dr]
            units[idx] = [ni,nj,sh,sw,sk-damage[idx]]

for _ in range(Q):
    idx,dr = map(int,input().split())
    if idx in units:
        push_unit(idx,dr)

ans = 0
for idx in units:
    ans += init_k[idx]-units[idx][4]
print(ans)