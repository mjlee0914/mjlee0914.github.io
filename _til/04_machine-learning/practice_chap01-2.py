# 1장 2강 문제 1
import pandas as pd

df = pd.read_csv("dataset.csv")

print("중복된 행 개수:", df.duplicated().sum())

df = df.drop_duplicates().reset_index(drop=True)

print("=" * 50)
print("수정 전:")
print(df['duration_ms'].describe())

df = df.query('duration_ms >= 0 or duration_ms <= 1e6')
print("=" * 50)
print("수정 후:")
print(df['duration_ms'].describe())