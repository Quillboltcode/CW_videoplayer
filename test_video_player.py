import polars as pl

df = pl.DataFrame._read_csv("library.csv", )
df.transpose().to_dict(as_series=False)
print(df.transpose(include_header=True).to_dict(as_series=False))