# CO4 Assignment 4A – Algorithmic Design Through Pseudocode

**Course:** CSA06 Design and Analysis of Algorithms  
**Course Outcome:** CO4 – Solve optimization problems using Dynamic Programming and Greedy strategies  
**Student:** Vishnuvardhan Reddy L

This assignment is about designing algorithms *before* implementing them, so all solutions are
language-independent pseudocode (no C/C++/Java/Python source). The complete answers, traces,
test cases and explanations are in the report.

## Contents

| Task | Topic | Technique | Pseudocode folder |
|------|-------|-----------|-------------------|
| 1 | Diagnose and repair LoadVehicle pseudocode | Greedy (fractional knapsack) | `Source_Code/Task_1/` |
| 2 | Job Sequencing with Deadlines | Greedy | `Source_Code/Task_2/` |
| 3 | 0/1 Knapsack with item reconstruction | Dynamic Programming | `Source_Code/Task_3/` |
| 4 | WordBreak forensics (find, fail, repair) | Dynamic Programming | `Source_Code/Task_4/` |
| 5 | Dijkstra, Bellman-Ford, Floyd | Greedy / DP | `Source_Code/Task_5/` |
| 6 | Energy-aware job scheduling (Design Challenge) | DP (weighted interval scheduling) | `Source_Code/Task_6/` |

## Structure

```
CO4_Assignment_4A/
├── Source_Code/
│   ├── Task_1/ ... Task_6/     pseudocode (.txt)
├── Report/
│   ├── CO4_Assignment_4A_Report.pdf
│   └── CO4_Assignment_4A_Report.docx
└── README.md
```

## Key results

- Task 1: sample check (capacity 50) gives total value 240.
- Task 2: schedule C, A, D with total profit 180; after changing B's profit to 90: B, A, D = 210.
- Task 3: capacity 7 selects items Q and R, maximum value 45.
- Task 4: "abxcd" with {ab, cd} breaks the original (first wrong state DP[5]); fixed by adding `DP[j] = TRUE`.
- Task 5: shortest path A→B→C→D→E, distance 10.
- Task 6: jobs J2, J5, J7, J8 give maximum energy saving 200; adversarial test gives 120.

## Notes

Pseudocode follows the structure used in the assignment sheet (INPUT/OUTPUT, BEGIN/END, `←` assignment).
