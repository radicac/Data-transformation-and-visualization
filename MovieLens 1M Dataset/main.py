import pandas as pd

unames = ['user_id', 'gender', 'age', 'occupation', 'zip']
users = pd.read_table('./users.dat', engine='python', sep='::', header=None, names=unames)

mnames = ['movie_id', 'title', 'genres']
movies = pd.read_table('./movies.dat', engine='python', sep='::', header=None, names=mnames)

rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_table('./ratings.dat', engine='python', sep='::', header=None, names=rnames)


#print(users[:5])
#print(movies[:5])
#print(ratings[:5])

data = pd.merge(pd.merge(ratings, users), movies)

#print(data[:10])
#print(data.iloc[2])

mean_ratings = data.pivot_table('rating', index='title', columns='gender', aggfunc='mean')
#print(mean_ratings[:30]

ratings_by_titles = data.groupby('title').size()
#print(ratings_by_titles[:10])

active_movies = ratings_by_titles.index[ratings_by_titles >= 250]
#print(active_movies)

mean_ratings = mean_ratings.loc[active_movies]
#print(mean_ratings)

top_female_movies = mean_ratings.sort_values(by='F', ascending=False)
#print(top_female_movies)

female = top_female_movies.loc[:, 'F']
#print(female)

mean_ratings['diff'] = mean_ratings['M'] - mean_ratings['F']
sorted_by_diff = mean_ratings.sort_values(by='diff')

rating_std_by_title = data.groupby('title')['rating'].std()
rating_std_by_title = rating_std_by_title.loc[active_movies]
print(rating_std_by_title.sort_values(ascending=False)[:10])

