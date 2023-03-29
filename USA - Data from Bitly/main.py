import json
import numpy as np
import pandas as pd
import matplotlib as plt

path = './example.txt'
records = [json.loads(line) for line in open(path)]
frame = pd.DataFrame(records)
#print(frame.info)

tz_counts = frame['tz'].value_counts()

clean_tz = frame['tz'].fillna('Missing')
clean_tz[clean_tz == ''] = 'Unknown'
tz_counts = clean_tz.value_counts()
#print(tz_counts)

import seaborn as sns

subset = tz_counts[:10]
#sns.barplot(y=subset.index, x=subset.values)
#plt.pyplot.show()

results = pd.Series([x.split()[0] for x in frame.a.dropna()])
#print(results[:10])
#print(results.value_counts()[:10])

cframe = frame[frame.a.notnull()]
cframe['os'] = np.where(cframe['a'].str.contains('Windows'), 'Windows', 'Not Windows')
#print(cframe['os'][:5])

by_tz_os = cframe.groupby(['tz', 'os'])
agg_counts = by_tz_os.size().unstack().fillna(0)
#print(agg_counts[:5])

indexer = agg_counts.sum(1).argsort()
#print(indexer[:5])

count_subset = agg_counts.take(indexer[-10:])
#print(count_subset)

#print(agg_counts.sum(1).nlargest(13))

count_subset = count_subset.stack()
count_subset.name = 'total'
count_subset = count_subset.reset_index()
print(count_subset[:10])

#sns.barplot(x='total', y='tz', hue='os', data=count_subset)
#plt.pyplot.show()

def norm_total(group):
    group['normed_total'] = group.total / group.total.sum()
    return group


results = count_subset.groupby('tz').apply(norm_total)

sns.barplot(x='normed_total', y='tz', hue='os', data=results)
plt.pyplot.show()
