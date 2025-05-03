import pandas as pd

# to get the count of squirrels by the Primary Fur Color
# 1. read the csv data file with pd
# 2. get the unique values of the column Primary Fur Color
# 3. count the rows matching for each Primary Fur Color

df = pd.read_csv("squirrel_data.csv")
# get the unique values in the Primary Fur Color column
unique_fur_colors = df["Primary Fur Color"].dropna().unique()

# to remove nan
# unique_fur_colors = [item for item in unique_fur_colors if str(item) != "nan"]
# print(unique_fur_colors)

# dict to hold the fur colors and respective count
count_by_fur_color = {"Fur Color": unique_fur_colors, "Count": []}

# get the count for each color in unique_fur_colors
for value in unique_fur_colors:
    matching_rows = df[df["Primary Fur Color"] == value]
    count_of_matching_rows = len(matching_rows)
    # update the dict
    # count_by_fur_color["Fur Color"].append(value)
    count_by_fur_color["Count"].append(count_of_matching_rows)

print(count_by_fur_color)

summary = pd.DataFrame(count_by_fur_color)
# print(summary)
summary.to_csv("analysis.csv")

# simple 1 line
new_summary= df.groupby(["Primary Fur Color"]).size().reset_index(name="count")
# new_summary= df.groupby(["Primary Fur Color", "Highlight Fur Color"]).size().reset_index(name="count")
print(new_summary)
print(type(new_summary))

print(df["Primary Fur Color"].value_counts().reset_index(name="count"))