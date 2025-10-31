# ALGORITHM: CSP Minesweeper Solver

**INPUT:** board, revealed_cells, flagged_cells  
**OUTPUT:** safe_cells, mine_cells

## FUNCTION BuildConstraints(board, revealed, flagged)
- constraints ← empty list
- For each cell (r, c) in revealed:
  - number ← board[r][c]
  - If number > 0:
    - hidden ← neighbors of (r,c) that are NOT revealed AND NOT flagged
    - If hidden is not empty:
      - flagged_count ← count of neighbors that ARE flagged
      - required_mines ← number - flagged_count
      - constraints.add((hidden, required_mines))
- Return constraints

## FUNCTION SolveConstraints(constraints)
- safe ← empty set  
- mines ← empty set
- For each (variables, required) in constraints:
  - If required = 0:
    - safe.add_all(variables)  // All safe
  - Else if required = len(variables):
    - mines.add_all(variables) // All mines
- Return (safe, mines)

## FUNCTION CSP_Step(board, revealed, flagged)
- constraints ← BuildConstraints(board, revealed, flagged)
- (safe, mines) ← SolveConstraints(constraints)
- changed ← (safe is not empty OR mines is not empty)
- Return (safe, mines, changed)

## FUNCTION AutoSolve(board, revealed, flagged)  // Main solver loop
- While game not over:
  - (safe, mines, changed) ← CSP_Step(board, revealed, flagged)
  - For each cell in safe:
    - Reveal(cell)
  - For each cell in mines:
    - Flag(cell)
  - If not changed:
    - hidden ← all cells NOT revealed AND NOT flagged
    - If hidden not empty:
      - Reveal(random cell from hidden)
    - Else:
      - Break
