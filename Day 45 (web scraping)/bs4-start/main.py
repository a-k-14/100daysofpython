from bs4 import BeautifulSoup

with open("website.html") as f:
    contents = f.read()
    # print(contents)

soup = BeautifulSoup(contents, "html.parser")
# print HTML with indentation for readability
# print(soup.prettify())

# print the first h3 tag's name
# print(soup.h3.name) # h3

# print the id value of the first h1 tag
# print(soup.h1.get("id"))

# find all the anchor tags in the HTML
all_anchor_tags: list =  soup.find_all(name="a")
# print(all_anchor_tags)
for tag in all_anchor_tags:
    # print the content in the tag
    # print(tag.string)
    # print(tag.getText())
    # print(tag.get("href"))
    ...

# get a tag that has a specific attribute
heading = soup.find(name="h3", class_="heading")
# print(heading)

# get the anchor tag that has the company url
company_url = soup.select_one(selector="p em strong a").get("href")
print(company_url)

# get the tag that has id=name
name_tag = soup.select_one(selector="#name")
# print(name_tag)
# print(soup.find(id="name"))

# get all the headings
headings = soup.select(selector=".heading")
print(headings)