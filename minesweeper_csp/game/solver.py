from typing import Dict, List, Set, Tuple
import random
from .board import Minesweeper

Coord = Tuple[int, int]

def build_constraints(game: Minesweeper):
    constraints = []
    variables: Set[Coord] = set()
    for (r, c) in game.frontier_numbered():
        neigh = game.neighbors(r, c)
        hidden = [(rr, cc) for (rr, cc) in neigh if not game.grid[rr][cc].revealed and not game.grid[rr][cc].flagged]
        if not hidden:
            continue
        flags = sum(1 for (rr, cc) in neigh if game.grid[rr][cc].flagged)
        req = max(0, game.grid[r][c].number - flags)
        s = set(hidden)
        constraints.append((s, req))
        variables |= s
    return constraints, variables

def connected_components(variables: Set[Coord], constraints: List[Tuple[Set[Coord], int]]):
    if not variables:
        return []
    var_list = list(variables)
    var_index = {v: i for i, v in enumerate(var_list)}
    adj = [set() for _ in var_list]
    for s, _ in constraints:
        ids = [var_index[v] for v in s if v in var_index]
        for i in ids:
            adj[i].update(ids)
    seen = set()
    comps = []
    for i in range(len(var_list)):
        if i in seen: 
            continue
        stack = [i]; seen.add(i); idxs = {i}
        while stack:
            cur = stack.pop()
            for nb in adj[cur]:
                if nb not in seen:
                    seen.add(nb); stack.append(nb); idxs.add(nb)
        vset = {var_list[j] for j in idxs}
        clist = [(s & vset, req) for (s, req) in constraints if s & vset]
        comps.append((vset, clist))
    return comps

def enumerate_component(vars_set: Set[Coord], constraints: List[Tuple[Set[Coord], int]], limit_solutions: int = 300000):
    vars_list = list(vars_set)
    cons = [(set(s), req) for (s, req) in constraints]
    order = sorted(range(len(vars_list)), key=lambda i: sum(1 for (s, _) in cons if vars_list[i] in s), reverse=True)

    assign = [None] * len(vars_list)
    cons_state = [[req, len(s), set(s)] for (s, req) in cons]
    solutions = 0
    true_count = [0] * len(vars_list)

    def consistent(idx, val):
        v = vars_list[idx]
        for (req, rem, sset) in cons_state:
            if v in sset:
                nr = req - (1 if val == 1 else 0)
                nm = rem - 1
                if nr < 0 or nr > nm:
                    return False
        return True

    def snap():
        return [(req, rem, set(sset)) for (req, rem, sset) in cons_state]

    def push(idx, val):
        v = vars_list[idx]
        for k in range(len(cons_state)):
            req, rem, sset = cons_state[k]
            if v in sset:
                cons_state[k][0] = req - (1 if val == 1 else 0)
                cons_state[k][1] = rem - 1
                sset.remove(v)

    def pop(s):
        for k in range(len(cons_state)):
            cons_state[k][0], cons_state[k][1], cons_state[k][2] = s[k]

    def bt(pos):
        nonlocal solutions
        if solutions >= limit_solutions:
            return
        if pos == len(vars_list):
            solutions += 1
            for i, a in enumerate(assign):
                if a == 1: true_count[i] += 1
            return
        idx = order[pos]
        for val in (0, 1):
            if not consistent(idx, val): 
                continue
            s = snap()
            assign[idx] = val
            push(idx, val)
            bt(pos + 1)
            assign[idx] = None
            pop(s)

    bt(0)
    return solutions, vars_list, true_count

def compute_probabilities(game: Minesweeper):
    constraints, variables = build_constraints(game)
    if not variables:
        hidden = game.hidden_unflagged()
        p = game.mines_remaining_estimate() / max(1, len(hidden))
        return {cell: p for cell in hidden}, p

    probs: Dict[Coord, float] = {}
    for vset, cons in connected_components(variables, constraints):
        sol, vlist, tcount = enumerate_component(vset, cons)
        if sol == 0:
            for v in vset: probs[v] = 0.5
        else:
            for i, v in enumerate(vlist):
                probs[v] = tcount[i] / sol

    frontier = set(probs.keys())
    others = [c for c in game.hidden_unflagged() if c not in frontier]
    remaining = game.mines_remaining_estimate() - sum(1 for v, p in probs.items() if p == 1.0)
    rem_hidden = len(others) + sum(1 for p in probs.values() if p not in (0.0, 1.0))
    back_p = max(0.0, min(1.0, remaining / rem_hidden)) if rem_hidden > 0 else 0.0
    for c in others: probs[c] = back_p
    return probs, back_p

def next_actions(game: Minesweeper):
    probs, _ = compute_probabilities(game)
    forced_safe = [v for v, p in probs.items() if p == 0.0]
    forced_mine = [v for v, p in probs.items() if p == 1.0]
    if forced_safe or forced_mine:
        return forced_safe, forced_mine, None
    if not probs:
        return [], [], None
    minp = min(probs.values())
    candidates = [v for v, p in probs.items() if p == minp]
    return [], [], random.choice(candidates)

def apply_actions(game: Minesweeper, safe_to_reveal: List[Coord], mines_to_flag: List[Coord], guess: Coord):
    changed = False
    for r, c in safe_to_reveal:
        if not game.grid[r][c].revealed and not game.grid[r][c].flagged and not game.game_over:
            game.reveal(r, c); changed = True
            if game.game_over: return changed
    for r, c in mines_to_flag:
        if not game.grid[r][c].revealed and not game.grid[r][c].flagged and not game.game_over:
            game.toggle_flag(r, c); changed = True
    if guess and not game.game_over:
        r, c = guess
        if not game.grid[r][c].revealed and not game.grid[r][c].flagged:
            game.reveal(r, c); changed = True
    return changed
