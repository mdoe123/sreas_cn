import numpy as np

# 给定的 x 和 y 值
x = np.array([121.14, 120.04, 135.07, 122.64, 74.61, 101.75, 124.50])
y = np.array([134, 125, 244, 146, -236, -20, 160])

# 进行二次函数拟合
coefficients = np.polyfit(x, y, 2)

# 提取系数
a, b, c = coefficients

# 输出二次函数的表达式
print(f"拟合的二次函数为: y = {a:.6f}x^2 + {b:.6f}x + {c:.6f}")
    