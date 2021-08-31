import pandas as pd
import re

df_demo = pd.read_excel("AgeStructure.xlsx", index_col = 0)

show_county = pd.read_excel("AgeStructure.xlsx", converters={'COUNTRY': str.strip})
show_countyw = show_county['COUNTRY']

# reset index without removing default index 
df_demo = df_demo.reset_index(drop = True) 
df_demo = df_demo.join(show_countyw)

cols = list(df_demo)
cols.insert(0, cols.pop(cols.index('COUNTRY')))

df_mix = df_demo.loc[:, cols]
df_mix

df_combinedN = df_mix.sort_values(by='0-14 years old %', ascending=False) # sorted float

# Sort Data
df_combinedN['Rank'] = df_combinedN['0-14 years old %'].rank(ascending=False) # create serial number by sorted

#move column Number
move_number = df_combinedN['Rank']
df_combinedN.drop(labels=['Rank'], axis=1, inplace = True)
df_combinedN.insert(0, 'Rank', move_number)

df_combinedN.iloc[0:50]