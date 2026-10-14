# CSA06 – Design and Analysis of Algorithms
## CO1 – Assessment Tool 1: Scalability Audit of an E-Commerce Platform (ShopSphere)

Student Name: ____________________  Reg. No.: ____________________

### Repository structure

```
CO1_AT1/
├── Question_1/
│   ├── Source_Code/
│   │   └── shopsphere_audit.py     # instrumented M1–M5, S1/S2, scalability table
│   └── Report/
│       ├── Report.pdf              # full report (derivations, analysis, screenshots)
│       ├── Report.docx             # editable Word version
│       ├── Report.md               # Markdown source of the report
│       ├── output.txt              # captured program output
│       └── screenshots/            # source-code and output screenshots
└── README.md
```

### How to run

Requires Python 3.8+ (standard library only).

```bash
cd Question_1/Source_Code
python3 shopsphere_audit.py
```

The program counts the basic operation of each module, asserts every closed form
derived in the report against the counted value, and prints the scalability
table for n = 100,000 and n = 1,000,000.

### Summary of results

| Part | Result |
|---|---|
| (b) M1 | n(n−1)/2 comparisons → Θ(n²), space Θ(1) |
| (b) M2 | 2^⌈log₂n⌉ − 1 Audit calls → **Θ(n)** (the Θ(n log n) claim is wrong; n = 1024 gives 1023) |
| (c) S2 | T(n) = log₂n + 1 → Θ(log n); iterative space Θ(1), recursive Θ(log n) |
| (d) M4 | Current Θ(n²) (Case 1); redesign Θ(n log n) (Case 2) |
| (d) M5 | No standard case applies; extended theorem / recursion tree → Θ(n log² n) |
| (e) S1 average | p(n+1)/2 + (1−p)n = 750,000.25 for n = 10⁶, p = 0.5 |
| (f) | 3n² ≤ f(n) ≤ 4n² for n ≥ 64 → Θ(n²); f(n) is not O(n) |
| (g) | M1 and M4 (current) miss the 10-minute window at n = 10⁶; redesign both |

### Assumption

The question paper prints "10 basic operations per second" with the exponent
missing. The report assumes 10⁸ operations/second and also shows 10⁷ and 10⁹ in
a sensitivity table (the verdicts are the same except M1 at 10⁹).
