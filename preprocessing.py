# preprocessing.py

def preprocess_data(df):
    df = df.copy()
    df = df.ffill()
    return df

