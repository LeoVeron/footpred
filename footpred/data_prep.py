from os import path
import pandas as pd

def win_lose_draw(ser):
    sc = ser.split(' - ')
    pt1 = int(sc[0])
    pt2 = int(sc[1])
    if pt1 == pt2:
        return pd.Series([0,1,0])
    elif pt1 > pt2:
        return pd.Series([1,0,0])
    return pd.Series([0,0,1])

def create_Y(df):
    return df.scores.apply(win_lose_draw)
    
def create_X(df):
    #Init
    percent_feats = ['tm1_points_h', 'tm1_GS_h', 'tm1_GC_h', 'tm0_GS_h', 
                    'tm2_points_a', 'tm2_GS_a', 'tm2_GC_a', 'tm0_GS_a', 
                    'tm1_wins', 'tm2_wins', 'tm0_wins', 'tm1_defeats', 
                    'tm2_defeats', 'tm0_defeats', 'tm1_D', 'tm2_D', 'tm0_D', 
                    'tm1_25', 'tm2_25', 'tm0_25', 'tm1_35', 'tm2_35', 'tm0_35', 
                    'tm1_BTS', 'tm2_BTS', 'tm0_BTS', 'tm1_wins_h', 'tm0_wins_h', 
                    'tm1_defeats_h', 'tm0_defeats_h', 'tm1_D_h', 'tm0_D_h', 
                    'tm1_25_h', 'tm0_25_h', 'tm1_35_h', 'tm0_35_h', 'tm1_BTS_h', 
                    'tm0_BTS_h', 'tm2_wins_a', 'tm0_wins_a', 'tm2_defeats_a', 
                    'tm0_defeats_a', 'tm2_D_a', 'tm0_D_a', 'tm2_25_a', 'tm0_25_a', 
                    'tm2_35_a', 'tm0_35_a', 'tm2_BTS_a', 'tm0_BTS_a', 'tm1_ClS_h', 
                    'tm1_WtN_h', 'tm1_SiBH_h', 'tm1_BoTS_h', 'tm1_FtS_h', 'tm1_LtN_h', 
                    'tm1_CiBH_h', 'tm2_ClS_h', 'tm2_WtN_h', 'tm2_SiBH_h', 'tm2_BoTS_h', 
                    'tm2_FtS_h', 'tm2_LtN_h', 'tm2_CiBH_h']

    score_feats = ['tm1_GSG','tm1_GCG_h','tm0_GCG_a','tm2_PPGA_a',
                    'tm2_GSG_a','tm0_GCG','tm2_TGG','tm1_GSG_h',
                    'tm1_TGG_h','tm0_TGG','tm0_GSG_h','tm0_PPGH_h','tm0_GSG',
                    'tm1_PPGH_h','tm0_PPGH_a','tm0_GSG_a','tm2_GCG','tm0_PPGH',
                    'tm2_TGG_a','tm0_GCG_h','tm0_TGG_h','tm0_TGG_a','tm2_GCG_a',
                    'tm1_TGG','tm2_GSG','tm1_GCG']

    tm1_to_compare = ['tm1_25','tm1_25_h','tm1_35','tm1_35_h','tm1_BTS','tm1_BTS_h',
                    'tm1_D','tm1_D_h','tm1_GS_h','tm1_defeats','tm1_defeats_h',
                    'tm1_wins','tm1_wins_h','tm1_GCG','tm1_GCG_h','tm1_GSG','tm1_GSG_h',
                    'tm1_PPGH_h','tm1_TGG', 'tm1_TGG_h']


    tm2_to_compare = ['tm2_25','tm2_25_a','tm2_35','tm2_35_a','tm2_BTS','tm2_BTS_a','tm2_D',
                    'tm2_D_a','tm2_GS_a','tm2_defeats','tm2_defeats_a','tm2_wins',
                    'tm2_wins_a','tm2_GCG','tm2_GCG_a','tm2_GSG','tm2_GSG_a','tm2_PPGA_a',
                    'tm2_TGG','tm2_TGG_a']

    to_not_compare = ['tm1_BoTS_h','tm1_CiBH_h','tm1_GC_h','tm1_ClS_h','tm1_FtS_h','tm1_LtN_h',
                    'tm1_SiBH_h','tm1_WtN_h','tm1_points_h','tm2_BoTS_h','tm2_CiBH_h','tm2_GC_a',
                    'tm2_ClS_h','tm2_FtS_h','tm2_LtN_h','tm2_SiBH_h','tm2_WtN_h','tm2_points_a']

    #Scale
    df[percent_feats] = df[percent_feats]/100
    df[score_feats] = df[score_feats]/3

    #Create X 
    X = pd.DataFrame()
    for feat in tm1_to_compare:
        X[feat] = df[feat] - df[feat.replace('tm1_','tm0_')]
    for feat in tm2_to_compare:
        X[feat] = df[feat] - df[feat.replace('tm2_','tm0_').replace('PPGA_a','PPGH_a')]
    for feat in to_not_compare:
        X[feat] = df[feat]
        
    return X