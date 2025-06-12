'''
0인 공간으로만 이동 가능
0==빈칸, 1==장애물

초기 타임머신의 위치 == 2
시간의 벽위치 == 3
탈출구 == 4 -> 2차원

출구는 한개

2차원에서 시간 이상 현상
- (r,c)에서 시작 -> 매 v의 배수 턴마다 d 방향으로 한 칸씩 확산 d는 동서남북 순
- 빈공간으로만 확산. 확산 불가시 멈춤.
- 서로 독립적이며 동시에 확산

타임머신
- 시간 이상 현상이 이루어지고 난 이후에 타임머신이 작동함.-> 미리 시간 이상 현상
- 매 턴마다 상하좌우 한칸 이동
- 장애물과 시간 이상현상을 피해 탈출구까지 도달.

출력 : 탈출구까지 이동하는 데 필요한 최소 시간. 탈출 불가시 -1
'''


def find_3D_base():
    for i in range(N):
        for j in range(N):
            if arr2[i][j]==3:
                return i,j

def find_2D_start_3D_exit():
    bi,bj = find_3D_base()
    for i in range(bi,bi+M):
        for j in range(bj,bj+M):
            if arr2[i][j]!=3:continue
            if arr2[i+1][j]==0: #남
                return i+1,j,M-1,j-bj,2
            if arr2[i][j+1]==0: #동
                return i,j+1,M-1,bi+M-1-i,0
            if arr2[i-1][j]==0: #북
                return i-1,j,M-1,bj+M-1-j,3
            if arr2[i][j-1]==0: #서
                return i,j-1,M-1,i-bi,1
    return -1

def find_2D_exit():
    for i in range(N):
        for j in range(N):
            if arr2[i][j]==4:
                arr2[i][j]=0
                return i,j

def find_3D_start():
    for i in range(M):
        for j in range(M):
            if arr3[4][i][j]==2:
                return i,j

def bfs_2D(si, sj, ei, ej, cnt):
    q=[]
    q.append((si,sj,cnt))
    vset = set()
    vset.add((si,sj))

    while q:
        ci,cj,t = q.pop(0)
        if (ci,cj)==(ei,ej):
            return t
        for i in range(4):
            ni,nj = ci+di[i],cj+dj[i]
            if 0<=ni<N and 0<=nj<N and (ni,nj) not in vset and (arr2[ni][nj]==0 or arr2[ni][nj]>t+1):
                q.append((ni,nj,t+1))
                vset.add((ni,nj))
    return -1
def bfs_3D(si, sj, ei, ej, d): #arr3[4][si][sj] -> arr3[d][ei][ej]
    right_next = {0:3,1:2,2:0,3:1,4:0}
    left_next = {0:2,1:3,2:1,3:0,4:1}
    q = []
    q.append((4,si,sj,0)) #면,i,j,cnt
    vset = set()
    vset.add((4,si,sj))

    while q:
        p,ci,cj,t = q.pop(0)
        if (ci,cj,p)==(ei,ej,d):
            return t
        for i in range(4):
            ni,nj = ci+di[i],cj+dj[i]
            if nj>=M: #동쪽으로 벗어남.
                if p==4:    np,ni,nj = 0,0,M-1-ci
                else:       np,ni,nj = right_next[p],ci,0
            elif nj<0: #서쪽
                if p==4:    np,ni,nj = 1,0,ci
                else:       np,ni,nj = left_next[p],ci,M-1
            elif ni>=M: #남
                if p==4:    np,ni,nj = 2,0,cj
                else:       continue
            elif ni<0: #북
                if p==0:    np,ni,nj = 4,M-1-ci,M-1
                elif p==1:  np,ni,nj = 4,cj,0
                elif p==2:  np,ni,nj = 4,M-1,cj
                elif p==3:  np,ni,nj = 4,0,M-1-cj
                elif p==4:  np,ni,nj = 3,0,M-1-cj
            else:
                np = p
            if (np,ni,nj) not in vset and arr3[np][ni][nj]==0:
                q.append((np,ni,nj,t+1))
                vset.add((np,ni,nj))


    return -1

####################################################################################
N,M,F = map(int, input().split())
arr2 = [list(map(int, input().split())) for _ in range(N)]
# [방향][행][열] / 동,서,남,북,윗면 순
arr3 = [[list(map(int,input().split())) for _ in range(M)] for _ in range(5)]
times = [list(map(int,input().split())) for _ in range(F)]

# [0] 좌표 찾기
si2,sj2,ei3,ej3,dd = find_2D_start_3D_exit()
ei2,ej2 = find_2D_exit()
si3,sj3 = find_3D_start()

# [1] 시간 이상 현상 먼저
di,dj = [0,0,1,-1],[1,-1,0,0] #동서남북
for r,c,d,v in times:
    ci,cj = r,c
    for t in range(N):
        if 0<=ci<N and 0<=cj<N and arr2[ci][cj]==0:
            if (ci,cj)==(ei2,ej2):
                break
            arr2[ci][cj] = v*t
            ci,cj = ci+di[d],cj+dj[d]
    arr2[r][c]=1


# [2] 3D 출발점 -> 2D 출발점 최단시간
ans = 0
t3 = bfs_3D(si3,sj3,ei3,ej3,dd)
ans+=t3
# [3] 2D 출발점 -> 출구 최단시간
t2 = bfs_2D(si2,sj2,ei2,ej2,t3+1)
if t2==-1: #탈출 불가능시
    ans=-1
else:
    ans=t2
print(ans)