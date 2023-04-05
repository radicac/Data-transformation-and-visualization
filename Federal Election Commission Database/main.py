import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


fec = pd.read_csv('P00000001-ALL.csv')
#print(fec.info())
#print(fec.iloc[123456])


unique_cands = fec.cand_nm.unique()
print(unique_cands)

parties = {'Bachmann, Michelle': 'Republican',
           'Cain, Herman': 'Republican',
           'Gingrich, Newt': 'Republican',
           'Hutsman, Jon': 'Republican',
           'McCotter, Thaddeus G': 'Republican',
           'Obama, Barack': 'Democrat',
           'Paul, Ron': 'Republican',
           'Pawlenty, Timothy': 'Republican',
           'Perry, Rick': 'Republican',
           "Roemer, Charles E. 'Buddy' III": 'Republican',
           'Romney, Mitt': 'Republican',
           'Santorum, Rick': 'Republican'}


#print(fec.cand_nm[123456:123461])


#adding new column
fec['party'] = fec.cand_nm.map(parties)
#print(fec.party.value_counts())
#print((fec.contb_receipt_amt > 0).value_counts())


fec = fec[fec.contb_receipt_amt > 0]
fec_mrbo = fec[fec.cand_nm.isin(['Obama, Barack', 'Romney, Mitt'])]

#print(fec.contbr_occupation.value_counts()[:10])

occ_maping = {
    'INFROMATION REQUESTED PER BEST EFFORTS': 'NOT PROVIDED',
    'INFROMATION REQUESTED': 'NOT PROVIDED',
    'INFROMATION REQUESTED PER (BEST EFFORTS)': 'NOT PROVIDED',
    'C.E.O': 'CEO'
}


f = lambda x: occ_maping.get(x, x)
fec.contbr_occupation = fec.contbr_occupation.map(f)


emp_mapping = {
    'INFROMATION REQUESTED PER BEST EFFORTS': 'NOT PROVIDED',
    'INFROMATION REQUESTED': 'NOT PROVIDED',
    'SELF': 'SELF-EMPLOYED',
    'SELF EMPLOYED': 'SELF-EMPLOYED'
}

f = lambda x: emp_mapping.get(x, x)
fec.contbr_employer = fec.contbr_employer.map(f)


#print(fec.contbr_occupation.value_counts()[:10])
#print(fec.contbr_employer.value_counts()[:10])

by_occupation = fec.pivot_table('contb_receipt_amt', index='contbr_occupation', columns='party', aggfunc='sum')

over_2mm = by_occupation[by_occupation.sum(1) > 2000000]
#print(over_2mm)

over_2mm.plot(kind='barh')
#plt.show()

def get_top_amounts(group, key, n=5):
    totals = group.groupby(key)['contb_receipt_amt'].sum()
    return totals.nlargest(n)


grouped = fec_mrbo.groupby('cand_nm')
#print(grouped.apply(get_top_amounts, 'contbr_occupation', n=7))
#print(grouped.apply(get_top_amounts, 'contbr_employer', n=10))

bins = np.array([0, 1, 10, 100, 1000, 10000, 100000, 1000000, 10000000])
labels = pd.cut(fec_mrbo.contb_receipt_amt, bins)
#print(labels)

grouped = fec_mrbo.groupby(['cand_nm', labels])
#print(grouped.size().unstack(0))

#normalize to visualize precentage of total donations of each size by candidate
bucket_sums = grouped.contb_receipt_amt.sum().unstack(0)
normed_sums = bucket_sums.div(bucket_sums.sum(axis=1), axis=0)
#print(normed_sums)

normed_sums[:-2].plot(kind = 'barh')
#plt.show()


grouped_state = fec_mrbo.groupby(['cand_nm', 'contbr_st'])
totals_s = grouped_state.contb_receipt_amt.sum().unstack(0).fillna(0)
totals_s = totals_s[totals_s.sum(1) > 10000]
print(totals_s[:10])

percent = totals_s.div(totals_s.sum(1), axis=0)
print(percent[:10])

