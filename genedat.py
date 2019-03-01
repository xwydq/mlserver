import pandas as pd
import json
import numpy as np

x1 = np.linspace(0, 10, 30)
x2 = np.linspace(0, 2, 30) ** 2
nosie = np.random.randn(30)

y = 3 * x1 + 4 * x2 + 2 + nosie
y

df = pd.DataFrame({
    "y":y,
    "x1":x1,
    "x2":x2
})

df.to_csv('lm_test.csv', index=False)
df.to_json('lm_test.json', orient = 'records')