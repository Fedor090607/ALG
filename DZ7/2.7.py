import sys

def main():
    with open("input2.txt", "r") as f:
        data = f.read().split()
    
    if not data:
        return

    n = int(data[0])
    m = int(data[1])
    
    field = data[2:2+n]

    dp = [[0] * m for _ in range(n)]

    dp[n - 1][0] = int(field[n - 1][0])

    for j in range(1, m):
        dp[n - 1][j] = dp[n - 1][j - 1] + int(field[n - 1][j])

    for i in range(n - 2, -1, -1):
        dp[i][0] = dp[i + 1][0] + int(field[i][0])

    for i in range(n - 2, -1, -1):
        for j in range(1, m):
            dp[i][j] = max(dp[i + 1][j], dp[i][j - 1]) + int(field[i][j])

    print(dp[0][m - 1])

if __name__ == '__main__':
    main()