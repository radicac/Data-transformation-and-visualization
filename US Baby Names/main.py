import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


names1880 = pd.read_csv('C:/Users/radica/Desktop/pydata-book/datasets/babynames/yob1880.txt', names=['name', 'sex', 'births'])
#print(names1880)

n_female = names1880.groupby('sex').births.sum()['F']
#print(n_female)

years = range(1880, 2011)
pieces = []
columns = ['name', 'sex', 'births']

for year in years:
    path = 'C:/Users/radica/Desktop/pydata-book/datasets/babynames/yob%d.txt' % year
    piece = pd.read_csv(path, names=columns)
    piece['year'] = year
    pieces.append(piece)

names = pd.concat(pieces, ignore_index=True)
#print(names[:20])

total_births = names.pivot_table('births', columns='sex', index='year', aggfunc=sum)
#print(total_births)


fig = total_births.plot(title='Total births by sex and year')
plt.savefig('Total births by sex and year.pdf')


def add_prop(group):
    group['prop'] = group.births / group.births.sum()
    return group


names = names.groupby(['year', 'sex']).apply(add_prop)
#print(names)


def get_top1000(group):
    return group.sort_values(by='births', ascending=False)[:1000]


grouped = names.groupby(['year', 'sex'])

top1000 = grouped.apply(get_top1000)
top1000.reset_index(inplace=True, drop=True)
#print(top1000)

boys = top1000[top1000.sex == 'M']
girls = top1000[top1000.sex == 'F']

total_births = top1000.pivot_table('births', index='year', columns='name', aggfunc=sum)

subset = total_births[['John', 'Harry', 'Mary', 'Marilyn']]
fig = subset.plot(subplots=True, figsize=(12, 20), grid=False, title='Number of births per year')
plt.savefig('Number of births per year for special names.pdf')


table = top1000.pivot_table('prop', index='year', columns='sex', aggfunc=sum)
fig = table.plot(title='Sum of table1000.prop by year and sex', yticks=np.linspace(0, 1.2, 13), xticks=range(1880, 2020, 10))
plt.savefig('Sum of table1000.prop by year and sex.pdf')


df = boys[boys.year == 2010]
#print(df)
prop_cumsum = df.sort_values(by='prop', ascending=False).prop.cumsum()
#print(prop_cumsum[:10])
#print(prop_cumsum.values.searchsorted(0.5))

df = boys[boys.year == 1900]
#print(df)
prop_cumsum = df.sort_values(by='prop', ascending=False).prop.cumsum()
#print(prop_cumsum.values.searchsorted(0.5))


def get_quantile_count(group, q=0.5):
    group = group.sort_values(by='prop', ascending=False)
    return group.prop.cumsum().values.searchsorted(q) + 1


diversity = top1000.groupby(['year', 'sex']).apply(get_quantile_count)
diversity = diversity.unstack('sex')
print(diversity.head())
fig = diversity.plot(title='Number of popular names in top 50%')
plt.savefig('Number of popular names in top 50%.pdf')

