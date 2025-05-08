import numpy as np

# 再次给定的 x 和 y 值
x = np.array([16, 24, 40])
y = np.array([5.71, 6.53, 7.97])

# 进行二次函数拟合
coefficients = np.polyfit(x, y, 2)

# 提取系数
a, b, c = coefficients

# 输出二次函数的表达式
print(f"拟合的二次函数为: y = {a:.6f}x^2 + {b:.6f}x + {c:.6f}")
    