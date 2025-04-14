import pandas as pd
import numpy as np

def replace(df):
    df["Message"] = df["Message"].str.replace(pat=r"[,\n]", repl=" ", regex=True)
    return df

def extract_domain(df, splitted=False):
    if not splitted:
        replace(df)
        df["s_Message"] = df["Message"].str.split(" ")

    df["email"] =  df["s_Message"].apply(lambda x: x[np.argmax(np.char.lower(np.array(x)) == "from") + 1])
    return df

    