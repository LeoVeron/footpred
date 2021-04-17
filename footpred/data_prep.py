from os import path
import pandas as pd

def win_lose_draw(ser):
    sc = ser.split(' - ')
    pt1 = int(sc[0])
    pt2 = int(sc[1])
    if pt1 == pt2:
        return pd.Series([0,0,1])
    elif pt1 > pt2:
        return pd.Series([1,0,0])
    return pd.Series([0,1,0])

