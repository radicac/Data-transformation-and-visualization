import json

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt


path = 'C:/Users/radica/Desktop/pydata-book/datasets/usda_food/database.json'
db = json.load(open(path))
#print(len(db))
#print(db[0]['nutrients'][0])

#nutrients = pd.DataFrame(db[0]['nutrients'])
#print(len(nutrients))
#print(nutrients[:10])

#print(db[0].keys())
info_keys = ['description', 'group', 'id', 'manufacturer']

info = pd.DataFrame(db, columns=info_keys)
#print(info.info)

#print(pd.value_counts(info.group)[:10])

nutrients = []
for rec in db:
    fnuts = pd.DataFrame(rec['nutrients'])
    fnuts['id'] = rec['id']
    nutrients.append(fnuts)

nutrients = pd.concat(nutrients, ignore_index=True)
#print(nutrients)
nutrients = nutrients.drop_duplicates()

#to distinguish col of the two DataFrames
col_mapping = {'description': 'food', 'group': 'fgroup'}
info = info.rename(columns=col_mapping, copy=False)

col_mapping = {'description': 'nutrient', 'group': 'nutgroup'}
nutrients = nutrients.rename(columns=col_mapping, copy=False)
#print(nutrients)

ndata = pd.merge(nutrients, info, on='id', how='outer')
#print(ndata.info())
#print(ndata.iloc[3000])

result = ndata.groupby(['nutrient', 'fgroup'])['value'].quantile()
result['Zinc, Zn'].sort_values().plot(kind='barh')
#plt.show()


by_nutrient = ndata.groupby(['nutgroup', 'nutrient'])

get_maximum = lambda x: x.loc[x.value.idxmax()]
get_minimum = lambda x: x.loc[x.value.idxmin()]

max_foods = by_nutrient.apply(get_maximum)[['value', 'food']]
#print(max_foods)

max_foods.food = max_foods.food.str[:50]

print(max_foods.loc['Amino Acids'])