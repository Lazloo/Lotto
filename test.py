import pandas as pd
import datetime
import sidetable
import itertools
import functools
from operator import iadd

df = pd.read_csv('lotto_zahlen_hierarchie.csv')
df['Date'] = pd.to_datetime(df['Date'])
bool_valid_date = df['Date'].dt.tz_localize(None) > pd.to_datetime('01Jan2020')
df = df[bool_valid_date].reset_index(drop=True)

df['Zahlen_split'] = df['Zahlen'].apply(lambda x: [int(i) for i in x.split('-')])
df['combinations'] = df['Zahlen_split'].apply(lambda x: list(itertools.combinations(x, 3)))


combination_list = functools.reduce(iadd, df['combinations'].values)
combination_list_str = [str(i) for i in combination_list]
df_combinations = pd.DataFrame(combination_list_str)
df_combinations['count'] = 1
df_combinations = df_combinations.rename(columns={0: 'combo'})
df_combo_group = df_combinations.groupby(by='combo', as_index=False,group_keys=False).agg({'count': 'sum'})
df_combo_group = df_combo_group.sort_values(by='count', ascending=False)
#
# import itertools
#
# list(itertools.combinations([1, 2, 3, 4, 5, 6], 3))
# (1,2,3) == (1,2,4) -> list of tuples to pandas -> groupby (extra column with 1 for each tuple)