

class CFG:
    seed = 29
    target_col = 'pm25_mid'
    n_fold = 4

# print(df_train[cv_col].value_counts())

"""
KFold
"""
from sklearn.model_selection import KFold
def get_KFold(df, cfg, seed):
    Fold = KFold(n_splits=cfg.n_fold, shuffle=True, random_state=seed)
    for n, (train_index, val_index) in enumerate(Fold.split(df, df[cfg.target_col])):
        df.loc[val_index, 'fold'] = int(n)
    return df

"""
StratifiedKFold
"""
from sklearn.model_selection import StratifiedKFold
def get_StratifiedKFold(df, cfg, seed):
    Fold = StratifiedKFold(n_splits=cfg.n_fold, shuffle=True, random_state=seed)
    for n, (train_index, val_index) in enumerate(Fold.split(df, df[cfg.target_col])):
        df.loc[val_index, 'fold'] = int(n)
    return df
    
"""
GroupKFold
"""
from sklearn.model_selection import GroupKFold
def get_GroupKFold(df, cfg, group_col):
    Fold = GroupKFold(n_splits=cfg.n_fold)
    for n, (train_index, val_index) in enumerate(Fold.split(df, df[cfg.target_col], df_train[group_col].values)):
        df.loc[val_index, 'fold'] = int(n)
    return df
"""
SeedつきGroupKFold
"""
from sklearn.model_selection import KFold
def get_GroupKFold_with_seed(df, cfg, seed, group_col):
    unique_groups = df[group_col].unique()
    Fold = KFold(n_splits=cfg.n_fold, shuffle=True, random_state=seed)
    for n, (train_index, val_index) in enumerate(Fold.split(unique_groups)):
        df.loc[df[group_col].isin(unique_groups[val_index]), 'fold'] = int(n)
    df['fold'] = df['fold'].astype(int)
    return df

if __name__ == '__main__':
    df_train["fold"] = -1
    df_train = get_KFold(df_train, cfg, 29)
    df_oof['fold'] = df_train['fold']
    # print(df.groupby(['fold', group_col]).size())
    print(df.fold.value_counts())