import pandas as pd

# list comprehension
cities = ["San Jose", "San Francisco", "Los Angeles", "Sacramento", "Miami", "Denver"]

# make a list of cities starting with 's' using list comprehension
cities_starting_with_s = [city for city in cities if city[0].lower() == "s"]

# print(cities_starting_with_s)

# dictionary comprehension
pops_mil = [8.7, 10.2, 9.1, 1.5, 5.4, 3.2]

cities_pops = {}

# we have 6 cities
for i in range(0, len(cities)):
    cities_pops[cities[i]] = pops_mil[i]

# print(cities_pops)

# make a dict of cities starting with 's' using list comprehension
s_cities_pops = {city:pops for (city, pops) in cities_pops.items() if city[0].lower() == "s"}
# print(s_cities_pops)

# looping through df

# create the df
# df = pd.DataFrame.from_dict(cities_pops, orient="index")
df = pd.DataFrame(cities_pops.items(), columns=["City", "Population"])
# print(df)

# for (key, value) in df.items():
#     print(key)
#     print(value)

for (index, row) in df.iterrows():
    # print(index)
    # print(row)
    if row.City[0].lower() == "s":
        print(row)