# Third party
import numpy as np
import pandas as pd

from sklearn.model_selection import KFold

import category_encoders as ce
from xfeat import *

# Category Encodeing
def category_encoding(oe_columns: list, train: pd.DataFrame, test: pd.DataFrame = None):
    """trainのみでも使える"""
    OE_COLS = ['OE_' + col for col in oe_columns]
    ce_oe = ce.OrdinalEncoder(cols=oe_columns, handle_missing='return_nan')
    train[OE_COLS] = ce_oe.fit_transform(train[oe_columns])
    if test is not None:
        test[OE_COLS] = ce_oe.transform(test[oe_columns])
    return OE_COLS, train, test


# Count Encoding
def count_encoding(ce_columns: list, train: pd.DataFrame, test: pd.DataFrame = None):
    """trainのみでも使える"""
    CE_COLS = ['CE_' + col for col in ce_columns]
    for col in ce_columns:
        encoder = train[col].value_counts()
        train[f'CE_{col}'] = train[col].map(encoder)
        if test is not None:
            test[f'CE_{col}'] = test[col].map(encoder)
    return CE_COLS, train, test  # ,encoder


# target encoding
def target_encoding(re_columns: list, target: str, train: pd.DataFrame, test: pd.DataFrame = None):
    """trainのみでも使える"""
    RE_COLS = [col + '_re' for col in re_columns]
    target_encoder = TargetEncoder(input_cols=re_columns,
                                   target_col=[target],
                                   fold=KFold(n_splits=5, shuffle=True, random_state=29),
                                   output_suffix="_re")
    train = target_encoder.fit_transform(train)
    if test is not None:
        test = target_encoder.transform(test)

    return RE_COLS, train, test


"""
category encoding
"""
OE_COLS, df_books, _ = category_encoding(['year'], df_books)
CFG.feature_cols += OE_COLS
display(df_books.head())

OE_COLS, df_train, df_test = category_encoding(['user_id'], df_train, df_test)
CFG.feature_cols += OE_COLS
display(df_train.head())

OE_COLS, df_users, _ = category_encoding(['city', 'province', 'country'], df_users)
CFG.feature_cols += OE_COLS
display(df_users.head())

"""
countencoding
"""
CE_COLS, df_users, _ = count_encoding(['city', 'country'], df_users)
CFG.feature_cols += CE_COLS

CFG.feature_cols = list(set(CFG.feature_cols))