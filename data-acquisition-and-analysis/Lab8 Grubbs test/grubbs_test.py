import pandas as pd
import numpy as np
import json
import itertools
import matplotlib.pyplot as plt
import scipy.stats as stats

def read_data(d, temp, filename):
    with open(f'{filename}.json') as f:
        data = json.load(f)
    d = pd.Series(list((itertools.chain.from_iterable([v for k, v in data.items() if f'{d}' in k]))))
    temp = pd.Series(list((itertools.chain.from_iterable([v for k, v in data.items() if f'{temp}' in k]))))
    return d, temp

def calculate_gcritical_g(n, alpha):
    t_dist = stats.t.ppf(1 - alpha / (2 * n), n-2)
    numerator =  (n - 1) * np.sqrt(np.square(t_dist))
    denominator = np.sqrt(n) * np.sqrt(n - 2 + np.square(t_dist))
    critical_g = numerator / denominator
    return critical_g

def plot(d, temp, i, stage):
    plt.scatter(d, temp)
    plt.xlabel("Date")
    plt.ylabel("Temp [C]")
    plt.title(f"DATASET{i} {stage}")
    plt.show()

def grubb_test(d, temp, alpha, i):
    print("\n-------------------")
    print(f"TEST FOR DATASET{i}")
    n_temp = temp.size
    n_d = d.size

    if n_d == n_temp:
        temp_to_std = pow((temp - temp.mean()), 2)

        temp_std = pow(temp_to_std.sum() / n_temp, 0.5)

        g_n = float((temp.max() - temp.mean()) / temp_std)
        print("Gn:", round(g_n, 2))

        g_1 = float((temp.mean() - temp.min()) / temp_std)
        print("G1:", round(g_1, 2))

        critical_value = float(calculate_gcritical_g(n_temp, alpha))
        print("Gcritical:", round(critical_value, 2))

        if g_1 > critical_value or g_n > critical_value:
            if g_1 > critical_value:
                idx_to_del = temp[temp == temp.min()].index[0]
            elif g_n > critical_value:
                idx_to_del = temp[temp == temp.max()].index[0]
            print("HYPOTHESIS H1:")
            print("DELETE VALUE - Date:", d[idx_to_del], " - Temperature:", temp[idx_to_del])
            new_d = d.drop(idx_to_del)
            new_temp = temp.drop(idx_to_del)
            grubb_test(new_d, new_temp, alpha, i)
        else:
            print("HYPOTHESIS H0")
            plot(d, temp, i, "after Grubb test")
            return

if __name__ == "__main__":
    print("Input desired alpha (0.05 is a standard value):")
    alpha = float(input())

    for i in range(1,4):
        d, temp = read_data(f'd{i}', f'temp{i}', 'temp')
        plot(d, temp, i, "entrance data")
        grubb_test(d, temp, alpha, i)