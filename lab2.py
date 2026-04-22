import random
import math
import statistics


def gen_normal(n):
    result = []
    for _ in range(n // 2):
        u1 = random.random()
        u2 = random.random()
        z1 = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
        z2 = math.sqrt(-2 * math.log(u1)) * math.sin(2 * math.pi * u2)
        result.append(z1)
        result.append(z2)
    if n % 2 == 1:
        u1 = random.random()
        u2 = random.random()
        result.append(math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2))
    return result[:n]


def gen_cauchy(n):
    return [math.tan(math.pi * (random.random() - 0.5)) for _ in range(n)]


def gen_laplace(n, b=1 / math.sqrt(2)):
    result = []
    for _ in range(n):
        u = random.random()
        if u < 0.5:
            result.append(b * math.log(random.random()))
        else:
            result.append(-b * math.log(random.random()))
    return result


def gen_poisson(n, lam=10):
    result = []
    for _ in range(n):
        L = math.exp(-lam)
        k = 0
        p = 1.0
        while p > L:
            k += 1
            p *= random.random()
        result.append(k - 1)
    return result


def gen_uniform(n, a=-math.sqrt(3), b=math.sqrt(3)):
    return [random.uniform(a, b) for _ in range(n)]


def z_R(sample):
    return (min(sample) + max(sample)) / 2


def z_Q(sample):
    s = sorted(sample)
    n = len(s)
    q1 = s[int(0.25 * n)]
    q3 = s[int(0.75 * n)]
    return (q1 + q3) / 2


def z_tr(sample, trim=0.1):
    s = sorted(sample)
    n = len(s)
    k = int(trim * n)
    if k == 0:
        return sum(s) / n
    trimmed = s[k:-k]
    return sum(trimmed) / len(trimmed)


n_values = [10, 100, 1000]
n_reps = 1000
random.seed(42)

distributions = {
    "Normal": gen_normal,
    "Cauchy": gen_cauchy,
    "Laplace": gen_laplace,
    "Poisson": lambda n: gen_poisson(n, 10),
    "Uniform": gen_uniform
}

# Заголовки
print(f"{'Distribution':<12} {'n':>4} {'Characteristic':<15} {'E(z)':>12} {'D(z)':>14}")
print("-" * 62)

for dist_name, generator in distributions.items():
    for n in n_values:
        stats_names = ["value", "median", "zR", "zQ", "ztr"]
        all_vals = {name: [] for name in stats_names}

        for _ in range(n_reps):
            sample = generator(n)
            all_vals["value"].append(statistics.mean(sample))
            all_vals["median"].append(statistics.median(sample))
            all_vals["zR"].append(z_R(sample))
            all_vals["zQ"].append(z_Q(sample))
            all_vals["ztr"].append(z_tr(sample))

        for name in stats_names:
            mean_val = statistics.mean(all_vals[name])
            var_sample = statistics.variance(all_vals[name])
            var_pop = var_sample * (n_reps - 1) / n_reps
            print(f"{dist_name:<12} {n:>4} {name:<15} {mean_val:>12.4f} {var_pop:>14.4f}")