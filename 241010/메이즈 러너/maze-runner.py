def rotate(arr, exit, sr, sc, w, units):  # 90도 회전, 내구도 모두 -1씩
    narr = [x[:] for x in arr]
    new_exit = exit[:]
    new_units = [u[:] for u in units]  # units 복사
    for i in range(w):
        for j in range(w):
            narr[sr + i][sc + j] = arr[sr + w - j - 1][sc + i]
            if 0 < narr[sr + i][sc + j] < 10:
                narr[sr + i][sc + j] -= 1
            if narr[sr + i][sc + j] == -1:
                new_exit = [sr + i, sc + j]
            if narr[sr + i][sc + j] >= 10:  # 유닛이면 유닛도 회전
                old_position = [sr + w - j - 1, sc + i]
                if old_position in units:  # 유효한 유닛인지 확인
                    idx1 = units.index(old_position)
                    new_units[idx1] = [sr + i, sc + j]

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
                    return sr, sc, w
    return -1, -1, -1  # 찾지 못한 경우


N, M, K = map(int, input().split())
arr = [[0] * (N + 2)] + [[0] + list(map(int, input().split())) + [0] for _ in range(N)] + [[0] * (N + 2)]
units = [list(map(int, input().split())) for _ in range(M)]  # arr에 대입할 때 -1 해줘야함
exit = list(map(int, input().split()))
out = [0] * M  # 탈출 시 1로
cnt = 0
ucnt = 10
arr[exit[0]][exit[1]] = -1

for ui, uj in units:
    arr[ui][uj] = ucnt
    ucnt += 1

for turn in range(1, K + 1):
    to_go = []
    for idx in range(M):
        if out[idx] == 1:
            continue
        si, sj = units[idx]
        ti, tj = exit
        cur_dist = abs(si - ti) + abs(sj - tj)  # 이동 전 출구와의 거리
        mn_dist = cur_dist

        # 각각의 참가자 이동 방향 결정
        best_move = None
        for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):  # 상하좌우
            ni, nj = si + di, sj + dj
            if 1 <= ni <= N and 1 <= nj <= N and (arr[ni][nj] == 0 or arr[ni][nj] == -1):
                dist = abs(ti - ni) + abs(tj - nj)  # 이동 후 출구와의 거리
                if dist < mn_dist:
                    mn_dist = dist
                    best_move = [si, sj, ni, nj]
                elif dist == mn_dist and best_move:  # 같은 거리가 여러 개일 때 상하 우선시
                    if (di, dj) == (-1, 0) or (di, dj) == (1, 0):
                        best_move = [si, sj, ni, nj]

        if best_move:
            to_go.append(best_move)

    to_go.sort(key=lambda x: (x[0], x[1]))  # 상하좌우 우선 순위 적용
    for tg in to_go:
        si, sj, ni, nj = tg
        idx = units.index([si, sj])
        if exit != [ni, nj]:  # 출구가 아닐 때만
            arr[ni][nj] = arr[si][sj]
            units[idx] = [ni, nj]
        else:
            out[idx] = 1
        arr[si][sj] = 0
        cnt += 1

    # 최소 정사각형 잡기
    sr, sc, w = find_rectangle(N, arr)
    if sr == -1 and sc == -1 and w == -1:  # 탈출 경로 없으면 중단
        break

    # 미로 회전
    arr, exit, units = rotate(arr, exit, sr, sc, w, units)  # 내구도 -1

    # 모든 참가자 탈출 시 종료
    if all(o == 1 for o in out):
        break

print(cnt)
print(*exit)