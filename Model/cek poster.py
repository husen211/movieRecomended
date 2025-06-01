import joblib
df = joblib.load('Model/bert_df.pkl')
print(df.columns)  # Harus ada 'poster_path'
print(df[['title', 'poster_path']].head())
