import time
import matplotlib.pyplot as plt

def test(n):
    d = {i: i for i in range(n)}
    key = n // 2
    start = time.perf_counter_ns()
    del d[key]
    end = time.perf_counter_ns()
    return end - start

sizes = [10, 100,1000,10000,100000, 200000, 500000,700000, 1000000, 2000000]
times = []

for n in sizes:
    t = test(n)
    times.append(t)
    print(n, t, "ns")

plt.plot(sizes, times, marker='o')
plt.title("Удаление элемента из словаря (ns)")
plt.xlabel("Размер словаря")
plt.ylabel("Время")
plt.grid()
plt.show()
