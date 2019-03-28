import pandas as pd
df = pd.read_csv("./point.csv", header=None)
print(sum([int(''.join(filter(str.isdigit, s))) for s in df[2].tolist()]))