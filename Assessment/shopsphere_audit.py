"""
CSA06 - Design and Analysis of Algorithms
CO1 - Assessment Tool 1: Scalability Audit of "ShopSphere"

Implements instrumented versions of modules M1-M5 and S1/S2, counts the basic
operation, checks every closed form derived in the report against the counts,
and produces the scalability table for n = 100,000 and n = 1,000,000.

Run:  python3 shopsphere_audit.py
"""
import math
import random

# ---------------------------------------------------------------------------
# Assumption: the question paper prints "10 basic operations per second" with
# the exponent lost in the PDF. We assume 10^8 ops/s (typical for one server
# core) and also print a sensitivity table for 10^7 and 10^9.
# ---------------------------------------------------------------------------
OPS_PER_SEC = 10 ** 8
WINDOW_SEC = 10 * 60          # nightly window: 10 minutes


# ============================ (b) M1 ========================================
def m1_count(n):
    """Run the M1 double loop, counting the title/seller comparisons."""
    count = 0
    for i in range(0, n - 1):            # i = 0 .. n-2
        for j in range(i + 1, n):        # j = i+1 .. n-1
            count += 1                   # one comparison (basic operation)
    return count


def m1_formula(n):
    return n * (n - 1) // 2


# ============================ (b) M2 ========================================
def m2_count(n):
    """Run the M2 loop, counting Audit() calls."""
    count = 0
    i = 1
    while i < n:
        for _ in range(0, i):
            count += 1                   # Audit(Request[j])
        i *= 2
    return count


def m2_formula(n):
    """Exact count = 2^ceil(log2 n) - 1 (n >= 2)."""
    return 2 ** math.ceil(math.log2(n)) - 1


# ============================ (c)/(e) M3 ====================================
def s1_search(arr, key):
    """Sequential search; returns (index or -1, comparisons)."""
    comps = 0
    for idx, v in enumerate(arr):
        comps += 1
        if v == key:
            return idx, comps
    return -1, comps


def s2_iterative(arr, key):
    """Binary search (iterative); returns (index or -1, comparisons)."""
    lo, hi, comps = 0, len(arr) - 1, 0
    while lo <= hi:
        mid = (lo + hi) // 2
        comps += 1
        if arr[mid] == key:
            return mid, comps
        elif arr[mid] < key:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1, comps


def s2_recursive(arr, key, lo=0, hi=None, depth=1):
    """Binary search (recursive); returns (index, comparisons, max_depth)."""
    if hi is None:
        hi = len(arr) - 1
    if lo > hi:
        return -1, 0, depth
    mid = (lo + hi) // 2
    if arr[mid] == key:
        return mid, 1, depth
    if arr[mid] < key:
        idx, c, d = s2_recursive(arr, key, mid + 1, hi, depth + 1)
    else:
        idx, c, d = s2_recursive(arr, key, lo, mid - 1, depth + 1)
    return idx, c + 1, d


def t_s2(n):
    """T(n) = T(n/2) + 1, T(1) = 1, evaluated directly (n a power of 2)."""
    return 1 if n == 1 else t_s2(n // 2) + 1


def s1_average(n, p):
    """E[comparisons] = p(n+1)/2 + (1-p)n."""
    return p * (n + 1) / 2 + (1 - p) * n


# ============================ (d) M4 / M5 ===================================
def t_m4_current(n):
    return 1 if n == 1 else 4 * t_m4_current(n // 2) + n


def t_m4_redesign(n):
    return 1 if n == 1 else 2 * t_m4_redesign(n // 2) + n


def t_m5(n):
    return 1 if n == 1 else 2 * t_m5(n // 2) + n * int(math.log2(n))


def m4_current_closed(n):          # 2n^2 - n
    return 2 * n * n - n


def m4_redesign_closed(n):         # n log n + n
    return n * int(math.log2(n)) + n


def m5_closed(n):                  # n*k(k+1)/2 + n, k = log2 n
    k = int(math.log2(n))
    return n * k * (k + 1) // 2 + n


# ============================ (f) =========================================
def f(n):
    return 3 * n * n + 10 * n * math.log2(n) + 50


def check_theta_n2():
    """Verify 3n^2 <= f(n) <= 4n^2 for all n >= 64 (checked up to 10^6),
    and also f(n) <= 63 n^2 for all n >= 1."""
    ok_tight = all(3 * n * n <= f(n) <= 4 * n * n for n in range(64, 10 ** 6 + 1, 7))
    ok_loose = all(f(n) <= 63 * n * n for n in range(2, 10 ** 5 + 1, 3))
    return ok_tight, ok_loose


# ============================ main ========================================
def fmt_time(sec):
    if sec < 1:
        return f"{sec * 1000:.3f} ms"
    if sec < 120:
        return f"{sec:.2f} s"
    if sec < 7200:
        return f"{sec / 60:.2f} min"
    if sec < 172800:
        return f"{sec / 3600:.2f} h"
    return f"{sec / 86400:.2f} days"


def main():
    print("=" * 72)
    print(" ShopSphere Scalability Audit  -  CSA06 CO1-AT1")
    print("=" * 72)
    print(f"Assumed server speed : {OPS_PER_SEC:.0e} basic operations / second")
    print(f"Nightly window       : {WINDOW_SEC} s (10 minutes)\n")

    # ---- (b) M1 verification
    print("-- (b) M1: comparisons = n(n-1)/2 ------------------------------------")
    for n in (2, 5, 10, 100, 1000):
        c, fm = m1_count(n), m1_formula(n)
        print(f"n={n:>5}  counted={c:>8}  formula={fm:>8}  match={c == fm}")
        assert c == fm

    # ---- (b) M2 verification
    print("\n-- (b) M2: Audit calls = 2^ceil(log2 n) - 1 --------------------------")
    for n in (2, 3, 5, 8, 100, 1000, 1024, 1025):
        c, fm = m2_count(n), m2_formula(n)
        print(f"n={n:>5}  counted={c:>6}  formula={fm:>6}  "
              f"claim n*log2(n)={n * math.log2(n):>8.0f}  match={c == fm}")
        assert c == fm
    n = 1024
    print(f"\nVerification n=1024: i takes 1,2,4,...,512 (10 values); "
          f"sum = {m2_count(n)} = 2^10 - 1 = {2**10 - 1}")
    print(f"Team-member claim n*log2(n) = {n * int(math.log2(n))}  "
          f"(10x too large)   ratio count/n = {m2_count(n) / n:.4f}")

    # ---- (c) S2 recurrence
    print("\n-- (c) S2: T(n) = T(n/2)+1, T(1)=1  ->  T(n) = log2 n + 1 -----------")
    for k in range(0, 21, 4):
        n = 2 ** k
        print(f"n=2^{k:<2} = {n:>8}  T(n)={t_s2(n):>3}  log2 n + 1 = {k + 1:>3}")
        assert t_s2(n) == k + 1

    # ---- (c)/(e) search measurements
    print("\n-- (e) Search cases (n = 1,000,000 sorted keys 0..n-1) --------------")
    N = 1_000_000
    arr = list(range(N))
    _, s1_best = s1_search(arr, 0)
    _, s1_worst = s1_search(arr, N - 1)
    _, s1_miss = s1_search(arr, -5)
    print(f"S1 best  (key at position 1)    : {s1_best} comparison")
    print(f"S1 worst (last / absent)        : {s1_worst} / {s1_miss} comparisons")
    # key at 0-based position idx costs idx+1 comparisons; average over all N keys
    avg_present = sum(idx + 1 for idx in range(N)) / N
    print(f"S1 avg, successful (all keys)   : {avg_present:.1f}  (theory (n+1)/2 = {(N + 1) / 2:.1f})")
    print(f"S1 avg, p=0.5 (formula)         : {s1_average(N, 0.5):.2f}")
    _, b_best = s2_iterative(arr, (N - 1) // 2)
    worst_b = max(s2_iterative(arr, k)[1] for k in random.sample(range(N), 20000))
    _, miss_b = s2_iterative(arr, -5)
    _, _, depth = s2_recursive(arr, -5)
    print(f"S2 best (key = middle)          : {b_best} comparison")
    print(f"S2 worst (sampled / absent)     : {worst_b} / {miss_b}  "
          f"(floor(log2 n)+1 = {int(math.log2(N)) + 1})")
    print(f"S2 recursion depth (absent key) : {depth}  -> recursive stack O(log n)")
    # exact S2 average for successful search, n = 2^k - 1
    k = 10
    m = 2 ** k - 1
    a = list(range(m))
    tot = sum(s2_iterative(a, x)[1] for x in a)
    print(f"S2 avg successful, n={m}: {tot / m:.4f}  "
          f"(formula ((k-1)2^k+1)/(2^k-1) = {((k - 1) * 2 ** k + 1) / m:.4f})")
    print("S1 avg for p in {0, 0.5, 1} at n = 10^6: "
          + ", ".join(f"{s1_average(N, p):,.2f}" for p in (0, 0.5, 1)))

    # ---- (d) recurrences
    print("\n-- (d) M4 / M5 recurrences vs closed forms ---------------------------")
    for k in (1, 4, 8, 12, 16):
        n = 2 ** k
        a, b, c = t_m4_current(n), t_m4_redesign(n), t_m5(n)
        assert a == m4_current_closed(n) and b == m4_redesign_closed(n) and c == m5_closed(n)
        print(f"n=2^{k:<2}  M4cur={a:>12,}  (2n^2-n)  M4new={b:>10,}  (n log n + n)  "
              f"M5={c:>12,}  (n k(k+1)/2 + n)")
    print("\nDoubling the data (n -> 2n):")
    for k in (10, 14, 18):
        n = 2 ** k
        print(f"n=2^{k}: M4 current x{m4_current_closed(2 * n) / m4_current_closed(n):.3f}   "
              f"M4 redesign x{m4_redesign_closed(2 * n) / m4_redesign_closed(n):.3f}   "
              f"M5 x{m5_closed(2 * n) / m5_closed(n):.3f}")

    # ---- (f) asymptotic proof check
    print("\n-- (f) f(n) = 3n^2 + 10 n log2 n + 50  is  Theta(n^2) ----------------")
    t, l = check_theta_n2()
    print(f"3n^2 <= f(n) <= 4n^2 for all tested n >= 64  : {t}")
    print(f"f(n) <= 63 n^2 for all tested n >= 2         : {l}")
    for n in (8, 16, 32, 63, 64, 128):
        print(f"n={n:>4}  f(n)={f(n):>10.0f}  4n^2={4 * n * n:>8}  f<=4n^2 : {f(n) <= 4 * n * n}")
    print("f(n)/n  grows without bound (not O(n)):",
          ", ".join(f"n={n}: {f(n) / n:,.0f}" for n in (10, 1000, 100000)))

    # ---- (g) scalability table
    print("\n-- (g) Scalability decision -------------------------------------------")
    rows = []
    for N in (100_000, 1_000_000):
        lg = math.log2(N)
        ops = {
            "M1  n(n-1)/2": m1_formula(N),
            "M2  2^ceil(lg n)-1": m2_formula(N),
            "S2  floor(lg n)+1 (one query)": int(lg) + 1,
            "M4 current 2n^2-n": 2 * N * N - N,
            "M4 redesign n lg n + n": int(N * lg + N),
            "M5  n lg^2 n / 2": int(N * int(lg) * (int(lg) + 1) / 2 + N),
        }
        print(f"\nn = {N:,}   (log2 n = {lg:.3f})")
        print(f"{'Module':<32}{'basic ops':>20}{'time @1e8/s':>16}{'<=10 min?':>11}")
        for name, o in ops.items():
            sec = o / OPS_PER_SEC
            print(f"{name:<32}{o:>20,}{fmt_time(sec):>16}{'YES' if sec <= WINDOW_SEC else 'NO':>11}")
            rows.append((N, name, o, sec))

    print("\nSensitivity of the 10-minute verdict to the assumed server speed (n = 10^6):")
    N = 1_000_000
    lg = int(math.log2(N))
    base = {"M1": m1_formula(N), "M2": m2_formula(N), "M4 current": 2 * N * N - N,
            "M4 redesign": int(N * math.log2(N) + N),
            "M5": N * lg * (lg + 1) // 2 + N}
    print(f"{'Module':<14}" + "".join(f"{'@' + format(r, '.0e') + '/s':>18}" for r in (1e7, 1e8, 1e9)))
    for name, o in base.items():
        print(f"{name:<14}" + "".join(
            f"{fmt_time(o / r) + (' OK' if o / r <= WINDOW_SEC else ' FAIL'):>18}" for r in (1e7, 1e8, 1e9)))

    print("\nGrowth when n goes 10^5 -> 10^6 (x10):")
    print(f"  M1 x{m1_formula(10**6) / m1_formula(10**5):.1f}   "
          f"M2 x{m2_formula(10**6) / m2_formula(10**5):.1f}   "
          f"M4 current x{(2e12 - 1e6) / (2e10 - 1e5):.1f}   "
          f"M4 redesign x{base['M4 redesign'] / (1e5 * math.log2(1e5) + 1e5):.1f}")
    print("\nAll assertions passed.")


if __name__ == "__main__":
    main()
