
def simpson_rule(f, a, b, n):
    if n % 2 == 1:
        n += 1  # Делаем n четным
    h = (b - a) / n
    x = np.linspace(a, b, n+1)
    fx = f(x)

    integral = (h / 3) * (fx[0] + 4 * sum(fx[1:-1:2]) + 2 * sum(fx[2:-2:2]) + fx[-1])
    return integral

# Пример использования

y1 = lambda x: np.cos(x) + 2    
y2 = lambda x: np.cos(x) + 1

f = lambda x: y1(x) - y2(x)


result = simpson_rule(f, 2, 4, 10000)
print(f"Приближённое значение интеграла: {result}")
