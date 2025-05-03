# read the weather data from the csv file
# store that data as a list
with open("weather_data.csv") as weather_data_file:
    data = []
    for line in weather_data_file:
        data.append(line.strip())

    print(data)

print("\n")

import csv

# with csv module
with open("weather_data.csv") as weather_data_file:
    # returns each row as a list
    raw_data = csv.reader(weather_data_file)
    print(raw_data)

    # data would be list of lists - each row is a list
    data = []
    for row in raw_data:
        data.append(row)
    print(data)

    # get the temperatures as a list of ints
    temperatures = []
    for i in range(1, len(data)):
        temperature = int(data[i][1])
        temperatures.append(temperature)
    print("\nList of temperatures with inbuilt csv module:")
    print(temperatures)

# with csv module
with open("weather_data.csv") as data_file:
    data = csv.reader(data_file)

    temps = []
    for row in data:
        temp = row[1]
        if temp != "temp":
            temps.append(int(temp))
    print("\nList of temperatures with inbuilt csv module:")
    print(temps)


# with pandas package
import pandas

print("\nUsing pandas package:\n")

# no need to open file separately
# read the csv file
csv_data = pandas.read_csv("weather_data.csv")

# type of output
print(type(csv_data))

# print(csv_data)

# convert the temp_data DataFrame to dict
# print(csv_data.to_dict())

# print(type(csv_data.temp))
print(type(csv_data["temp"]))

# print(csv_data["temp"])
# as csv_data["temp"] prints key value (0 12), we loop and print only values
# 0    12
# 1    14
# 2    15
# 3    14
# 4    21
# 5    22
# 6    24
temp_series = csv_data["temp"]
print(temp_series)
# for key in temp_series.keys():
#     print(temp_dict[key])

for item in temp_series:
    print(item)

# converting series to dict
print("\nConverting the series to dict using pandas inbuilt methods:")
print(csv_data["temp"].to_dict())
print(csv_data.day.to_dict())

# convert the temp series to list (To get the data in a column, we can use this)
temp_list = csv_data["temp"].to_list()
print("\nList of temps after converting the csv_data[\"temp\"] series to list: ")
print(temp_list)

# print(f"Average Temperature: {average(temp_list)}")
average_temp = sum(temp_list) / len(temp_list)
# print(f"Average Temperature: {average_temp}")

print(f'Average Temperature: {csv_data["temp"].mean()}')
max_temp = csv_data["temp"].max()
print(f'Max Temperature: {max_temp}')

# get the row in the data with max temp
print("\nDay with max temperature: ")
max_temp_day = csv_data[csv_data.temp == max_temp]
print(max_temp_day)

print(type(max_temp_day))

print("\nClimate condition on day with max temperature: ")
print(max_temp_day.condition)
print(max_temp_day.condition.to_list()[0])
# print(max_temp_day.condition[6])

# convert monday's temp from c to f
# get the monday row
monday = csv_data[csv_data.day == "Monday"]
print(monday)
# we need not convert to list by using [0] directly - but not a good way
monday_temp_c = monday.temp[0]
monday_temp_f = monday_temp_c * 9 / 5 + 32
print(f"\nMonday temperature: {monday_temp_c}℃ {monday_temp_f}℉")

print("\n")

# create a DataFrame from scratch and write it to a csv
scores_dict = {
    "player": ["a", "b", "c", "d"],
    "score": [120, 209, 110, 98],
    "level": [3, 5, 3, 2]
}
scores_dataframe = pandas.DataFrame(scores_dict)
print(scores_dataframe)
scores_dataframe.to_csv("scores.csv")

player_coins = {
    "coins": {0: 20, 1: 41, 2: 18, 3: 15}
}
player_coins_dataframe = pandas.DataFrame(player_coins)
print(player_coins_dataframe)
player_coins_dataframe.to_csv("player_coins.csv")

# output of csv_data.to_dict()
x = {
    'day':
        {
            0: 'Monday',
            1: 'Tuesday',
            2: 'Wednesday',
            3: 'Thursday',
            4: 'Friday',
            5: 'Saturday',
            6: 'Sunday'
        },
     'temp':
         {
             0: 12,
             1: 14,
             2: 15,
             3: 14,
             4: 21,
             5: 22,
             6: 24
         },
     'condition':
         {
             0: 'Sunny',
             1: 'Rain',
             2: 'Rain',
             3: 'Cloudy',
             4: 'Sunny',
             5: 'Sunny',
             6: 'Sunny'
         }
    }
