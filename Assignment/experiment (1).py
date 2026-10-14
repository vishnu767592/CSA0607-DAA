import random, time, json, sys
sys.setrecursionlimit(10000)
random.seed(42)

# ---------------- Algorithm 1: linear search (iterative, brute force) ----------------
def linear_count(a, key):
    c = 0
    for i in range(len(a)):
        c += 1
        if a[i] == key:
            return i, c
    return -1, c

def linear_plain(a, key):
    for i in range(len(a)):
        if a[i] == key:
            return i
    return -1

# ---------------- Preprocessing: merge sort (divide and conquer) ----------------
def merge_sort(a, c):
    n = len(a)
    if n <= 1:
        return a
    mid = n // 2
    L = merge_sort(a[:mid], c)
    R = merge_sort(a[mid:], c)
    out = []
    i = j = 0
    while i < len(L) and j < len(R):
        c[0] += 1
        if L[i] <= R[j]:
            out.append(L[i]); i += 1
        else:
            out.append(R[j]); j += 1
    out.extend(L[i:]); out.extend(R[j:])
    return out

# ---------------- Algorithm 2: recursive binary search (decrease and conquer) ----------------
def bs_count(a, key, lo, hi, c):
    if lo > hi:
        return -1
    mid = (lo + hi) // 2
    c[0] += 1
    if a[mid] == key:
        return mid
    if key < a[mid]:
        return bs_count(a, key, lo, mid - 1, c)
    return bs_count(a, key, mid + 1, hi, c)

def bs_plain(a, key, lo, hi):
    if lo > hi:
        return -1
    mid = (lo + hi) // 2
    v = a[mid]
    if v == key:
        return mid
    if key < v:
        return bs_plain(a, key, lo, mid - 1)
    return bs_plain(a, key, mid + 1, hi)

# ---------------- Algorithm 3: hash table with chaining (time-space trade-off) ----------------
def next_prime(x):
    def is_p(v):
        if v < 2: return False
        i = 2
        while i * i <= v:
            if v % i == 0: return False
            i += 1
        return True
    while not is_p(x):
        x += 1
    return x

def ht_build(keys):
    m = next_prime(len(keys))
    t = [None] * m
    for k in keys:
        h = k % m
        if t[h] is None:
            t[h] = [k]
        else:
            t[h].append(k)
    return t, m

def ht_count(t, m, key):
    b = t[key % m]
    c = 0
    if b is None:
        return -1, 0
    for x in b:
        c += 1
        if x == key:
            return 1, c
    return -1, c

def ht_plain(t, m, key):
    b = t[key % m]
    if b is None:
        return -1
    for x in b:
        if x == key:
            return 1
    return -1

SIZES = [1000, 10000, 100000, 1000000]
res = {}
for n in SIZES:
    keys = random.sample(range(10**8, 10**9), n)       # unsorted registration numbers
    kset = set(keys)
    Qf = 3000 if n <= 10000 else 20                      # fewer queries for slow linear search
    Qf = max(20, 2_000_000 // n) if n >= 1000 else 3000
    Qf = min(Qf, 2000)
    Qfast = 20000
    hits_all = [random.choice(keys) for _ in range(Qfast)]
    miss_all = []
    while len(miss_all) < Qfast:
        k = random.randrange(10**8, 10**9)
        if k not in kset:
            miss_all.append(k)
    hits_slow = hits_all[:Qf]; miss_slow = miss_all[:Qf]
    r = {"n": n, "Q_linear": Qf, "Q_fast": Qfast}

    # ---- preprocessing ----
    t0 = time.perf_counter(); c = [0]; sorted_keys = merge_sort(keys, c); r["sort_time_s"] = time.perf_counter() - t0
    r["sort_comparisons"] = c[0]
    t0 = time.perf_counter(); sorted(keys); r["builtin_sort_time_s"] = time.perf_counter() - t0
    t0 = time.perf_counter(); table, m = ht_build(keys); r["hash_build_time_s"] = time.perf_counter() - t0
    chain_lens = [len(b) for b in table if b]
    r["hash_m"] = m; r["hash_max_chain"] = max(chain_lens)
    r["hash_load"] = n / m

    # ---- correctness checks ----
    for k in hits_all[:500]:
        assert keys[linear_plain(keys, k)] == k
        assert sorted_keys[bs_plain(sorted_keys, k, 0, n - 1)] == k
        assert ht_plain(table, m, k) == 1
    for k in miss_all[:500]:
        assert linear_plain(keys, k) == -1 and bs_plain(sorted_keys, k, 0, n - 1) == -1 and ht_plain(table, m, k) == -1

    # ---- comparisons ----
    r["lin_cmp_hit"] = sum(linear_count(keys, k)[1] for k in hits_slow) / Qf
    r["lin_cmp_miss"] = sum(linear_count(keys, k)[1] for k in miss_slow) / Qf
    cc = []
    for k in hits_all:
        c = [0]; bs_count(sorted_keys, k, 0, n - 1, c); cc.append(c[0])
    r["bin_cmp_hit"] = sum(cc) / len(cc); r["bin_cmp_hit_max"] = max(cc)
    cc = []
    for k in miss_all:
        c = [0]; bs_count(sorted_keys, k, 0, n - 1, c); cc.append(c[0])
    r["bin_cmp_miss"] = sum(cc) / len(cc); r["bin_cmp_miss_max"] = max(cc)
    r["hash_cmp_hit"] = sum(ht_count(table, m, k)[1] for k in hits_all) / Qfast
    r["hash_cmp_miss"] = sum(ht_count(table, m, k)[1] for k in miss_all) / Qfast
    # best / worst
    r["lin_best"] = linear_count(keys, keys[0])[1]; r["lin_worst"] = linear_count(keys, keys[-1])[1]
    c = [0]; bs_count(sorted_keys, sorted_keys[(n - 1) // 2], 0, n - 1, c); r["bin_best"] = c[0]
    longest = max((b for b in table if b), key=len)
    r["hash_best"] = ht_count(table, m, table[keys[0] % m][0])[1]; r["hash_worst"] = ht_count(table, m, longest[-1])[1]

    # ---- timing (plain implementations, microseconds per query) ----
    t0 = time.perf_counter()
    for k in hits_slow: linear_plain(keys, k)
    r["lin_us_hit"] = (time.perf_counter() - t0) / Qf * 1e6
    t0 = time.perf_counter()
    for k in miss_slow: linear_plain(keys, k)
    r["lin_us_miss"] = (time.perf_counter() - t0) / Qf * 1e6
    t0 = time.perf_counter()
    for k in hits_all: bs_plain(sorted_keys, k, 0, n - 1)
    r["bin_us_hit"] = (time.perf_counter() - t0) / Qfast * 1e6
    t0 = time.perf_counter()
    for k in miss_all: bs_plain(sorted_keys, k, 0, n - 1)
    r["bin_us_miss"] = (time.perf_counter() - t0) / Qfast * 1e6
    t0 = time.perf_counter()
    for k in hits_all: ht_plain(table, m, k)
    r["hash_us_hit"] = (time.perf_counter() - t0) / Qfast * 1e6
    t0 = time.perf_counter()
    for k in miss_all: ht_plain(table, m, k)
    r["hash_us_miss"] = (time.perf_counter() - t0) / Qfast * 1e6

    # ---- daily update of 1000 new records ----
    if n == 1000000:
        batch = random.sample([x for x in range(10**8, 10**9) if x not in kset][:5000], 1000) if False else [10**9 + i * 7 for i in range(1000)]
        t0 = time.perf_counter()
        bs = sorted(batch)
        out = []; i = j = 0
        while i < len(sorted_keys) and j < len(bs):
            if sorted_keys[i] <= bs[j]: out.append(sorted_keys[i]); i += 1
            else: out.append(bs[j]); j += 1
        out.extend(sorted_keys[i:]); out.extend(bs[j:])
        r["daily_merge_time_s"] = time.perf_counter() - t0
        t0 = time.perf_counter()
        for k in batch:
            h = k % m
            if table[h] is None: table[h] = [k]
            else: table[h].append(k)
        r["daily_hash_insert_time_s"] = time.perf_counter() - t0
    res[n] = r
    print(n, "done", flush=True)

json.dump(res, open("/tmp/work/results.json", "w"), indent=1)

# ---------------- charts ----------------
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
ns = SIZES
def S(key): return [res[n][key] for n in ns]

plt.figure(figsize=(6.5, 4))
plt.loglog(ns, S("lin_cmp_hit"), "o-", label="Linear search")
plt.loglog(ns, S("bin_cmp_hit"), "s-", label="Binary search (recursive)")
plt.loglog(ns, S("hash_cmp_hit"), "^-", label="Hash table (chaining)")
plt.xlabel("Number of records n"); plt.ylabel("Avg comparisons per successful search")
plt.title("Comparisons vs n (log-log)"); plt.grid(True, which="both", alpha=.3); plt.legend(); plt.tight_layout()
plt.savefig("/tmp/work/chart_comparisons.png", dpi=170); plt.close()

plt.figure(figsize=(6.5, 4))
plt.loglog(ns, S("lin_us_hit"), "o-", label="Linear search")
plt.loglog(ns, S("bin_us_hit"), "s-", label="Binary search (recursive)")
plt.loglog(ns, S("hash_us_hit"), "^-", label="Hash table (chaining)")
plt.xlabel("Number of records n"); plt.ylabel("Avg time per successful search (microseconds)")
plt.title("Search time vs n (log-log)"); plt.grid(True, which="both", alpha=.3); plt.legend(); plt.tight_layout()
plt.savefig("/tmp/work/chart_time.png", dpi=170); plt.close()

plt.figure(figsize=(6.5, 4))
plt.loglog(ns, S("sort_time_s"), "s-", label="Merge sort (for binary search)")
plt.loglog(ns, S("hash_build_time_s"), "^-", label="Build hash table")
plt.xlabel("Number of records n"); plt.ylabel("Preprocessing time (seconds)")
plt.title("Preprocessing cost vs n"); plt.grid(True, which="both", alpha=.3); plt.legend(); plt.tight_layout()
plt.savefig("/tmp/work/chart_preprocessing.png", dpi=170); plt.close()

big = res[1000000]
qs = [10 ** (i / 4) for i in range(0, 4 * 8 + 1)]
lin = [q * big["lin_us_hit"] / 1e6 for q in qs]
binr = [big["sort_time_s"] + q * big["bin_us_hit"] / 1e6 for q in qs]
hsh = [big["hash_build_time_s"] + q * big["hash_us_hit"] / 1e6 for q in qs]
plt.figure(figsize=(6.5, 4))
plt.loglog(qs, lin, label="Linear (no preprocessing)")
plt.loglog(qs, binr, label="Sort once + binary search")
plt.loglog(qs, hsh, label="Build hash once + hash search")
plt.axvline(50000, color="gray", ls="--"); plt.text(52000, min(lin) * 3, "50,000 queries/hour", rotation=90, fontsize=8)
plt.xlabel("Number of queries q"); plt.ylabel("Total time = preprocessing + q x search (seconds)")
plt.title("Total cost at n = 1,000,000"); plt.grid(True, which="both", alpha=.3); plt.legend(); plt.tight_layout()
plt.savefig("/tmp/work/chart_total.png", dpi=170); plt.close()

# break-even
be_bin = big["sort_time_s"] / ((big["lin_us_hit"] - big["bin_us_hit"]) / 1e6)
be_hash = big["hash_build_time_s"] / ((big["lin_us_hit"] - big["hash_us_hit"]) / 1e6)
print("break-even queries vs linear: binary", be_bin, "hash", be_hash)
json.dump({"be_bin": be_bin, "be_hash": be_hash}, open("/tmp/work/breakeven.json", "w"))
