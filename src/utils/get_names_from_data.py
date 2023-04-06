import pandas as pd

old_df = pd.read_table('../../data/0163061-220831081235567.csv', chunksize=10)
print(next(old_df))
print(next(old_df).info(verbose=True))

new_df = pd.read_parquet('../data/realtime/1680459529.542282.parquet')
print(new_df)
print(new_df.info(verbose=True))
