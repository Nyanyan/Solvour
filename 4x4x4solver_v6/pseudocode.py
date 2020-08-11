def phase_search(phase, indexes, depth, h_i): # phase: フェーズ, indexes: パズルの状態インデックス, depth: 残り回せる手数, h_i: indexesの状態でのh(indexes)
    global path
    if depth == 0: # 残り手数0の場合には解にたどり着いたかを返す
        return h_i == 0
    twist = successor[phase].next() # twistは回す手
    while twist < len(successor[phase]): # successorは回転の候補
        if skip(twist, path): # 前の手で回したのと同じ面を回すなどはしない
            twist = skip_axis[phase][twist] # 同じ面を回さなくなるまでtwistを進める
            continue
        next_indexes = move(indexes, phase, twist) # 配列参照によってパズルを動かす。indexesの定義はフェーズによって異なるのでフェーズを引数にとる
        next_h_i = h(indexes, phase) # h(i)を返す。h(i)もフェーズごとに定義が異なるのでフェーズを引数に取る。
        if next_h_i > depth or next_h_i > h_i + 1: # 明らかに遠回りをしようとしている場合はスキップ
            twist = skip_axis[phase][twist]
        path.append(twist) # ここまで回してきた手順にtwistを追加する
        if phase_search(phase, next_indexes, depth - 1, next_h_i): # 再帰で次の手を探索する
            return True # 解が見つかった
        path.pop() # ここまで回してきた手順から今回した手順を取り除く
        twist = next_twist(twist, phase) # 次の手
    return False

def solver(puzzle): # puzzle: パズルのすべての状態を表したクラスのオブジェクトなど
    global path
    solution = [] # 解
    for phase in range(6): # フェーズを回す
        indexes = initialize_indexes(puzzle, phase) # パズルの状態をインデックスに変換
        h_i = h(indexes, phase)
        for depth in range(60): # depthを回す。なお60は適当
            path = []
            if phase_search(phase, indexes, depth, h_i):
                for twist in path: # フェーズが終わった状態までパズルをシミュレート
                    puzzle = puzzle.move(twist)
                solution.extend(path) # solutionに今のフェーズの解を付け加える
                break
    return solution
