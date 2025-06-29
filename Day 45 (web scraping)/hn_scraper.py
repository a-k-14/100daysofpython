# GOAL - to scrap Y Combinator site with BS4
# from PIL.Image import preinit
from bs4 import BeautifulSoup
import requests
import time

appbrewery_hn: str = "https://appbrewery.github.io/news.ycombinator.com/"
live_hn: str = "https://news.ycombinator.com/news"

# to scrape the hn from appbrewery domain
def scrape_hn_old() -> None:
    response = requests.get(appbrewery_hn)
    response.raise_for_status()
    website_html = response.text

    soup = BeautifulSoup(website_html, "html.parser")

    # get the details of the first article
    # first_article = soup.find(name="a", class_="storylink")
    #
    # first_article_title = first_article.string
    # first_article_link = first_article.get("href")
    # first_article_upvotes = soup.find(name="span", class_="score").string
    # print(first_article_title, first_article_upvotes, first_article_link, sep="\n")

    # get the details of all the articles
    article_tags = soup.find_all(name="a", class_="storylink")

    article_titles = []
    article_links = []

    # iterate through the article_tags to extract article title and link for each article
    for article in article_tags:
        title = article.string
        link = article.get("href")
        article_titles.append(title)
        article_links.append(link)

    # get the upvotes for all articles
    # score format - 38 points
    # split the score to get the number .split() -> default split by space -> ['38', 'points']
    # convert the number to int - int()
    article_upvotes = [int(score.string.split()[0]) for score in soup.find_all(name="span", class_="score")]

    #default sep is space " "
    print(article_titles, article_links, article_upvotes, sep="\n")

    # get the article with max upvotes
    index_of_max_upvotes = article_upvotes.index(max(article_upvotes))
    # print(index_of_max_upvotes)

    print(article_titles[index_of_max_upvotes], article_links[index_of_max_upvotes], article_upvotes[index_of_max_upvotes], sep="\n")

# if we scrape hn live version where the structure has changed a little, there are chances that we may have articles with no upvotes at all i.e., 0 upvotes
# in such cases hn does not show 0, the upvote tag is absent
# in such case, the number of articles and the number of upvotes we capture will not match
# i.e. len(article_tage) != len(article_upvotes)
# based on chatgpt convo -> We must not rely on parallel lists (titles[i] and upvotes[i])
# Instead, scrape the articles row-wise — walk over the DOM in the same structure as the Hacker News layout
def scrape_hn_live() -> None:
    response = requests.get(live_hn)
    response.raise_for_status()
    website_html = response.text

    soup = BeautifulSoup(website_html, "html.parser")
    # print(soup.prettify())

    # list that holds the articles in dict format
    articles :list[dict] = []

    # article display format in hn
    # 2. Why We're Moving on from Nix (railway.com)
    # 38 points by mooreds 2 hours ago | hide | 7 comments

    # HTML structure as on date on the hn site:
    #
    # <tr class="athing submission" id="44208968">
    #       <td align="right" valign="top" class="title"><span class="rank">2.</span></td>
    #       <td valign="top" class="votelinks">
    #       <center>
    #           <a id="up_44208968" href="vote?id=44208968&amp;how=up&amp;goto=news">
    #               <div class="votearrow" title="upvote"></div>
    #           </a>
    #       </center>
    #       </td>
    #       <td class="title">
    #           <span class="titleline">
    #               <a href="https://blog.railway.com/p/introducing-railpack">Why We're Moving on from Nix</a>
    #               <span class="sitebit comhead">
    #                   (<a href="from?site=railway.com">
    #                       <span class="sitestr">railway.com</span>
    #                   </a>)
    #               </span>
    #           </span>
    #       </td>
    # </tr>

    # get all the "tr" elements that hold the "a" elements
    article_rows = soup.find_all(name="tr", class_="athing")

    # extract the title and link inside the "a" element that is inside the "tr" element
    for article_row in article_rows:
        article_tag = article_row.find(name="span", class_="titleline").find(name="a")


        # HTML of table row containing upvotes
        # <tr>
        #   <td colspan="2"></td>
        #   <td class="subtext">
        #       <span class="subline">
        #           <span class="score" id="score_44208968">38 points
        #           </span>
        #           by
        #           <a href="user?id=mooreds" class="hnuser">mooreds
        #           </a>
        #           <span class="age" title="2025-06-07T11:36:13 1749296173">
        #               <a href="item?id=44208968">2 hours ago</a>
        #           </span>
        #           <span id="unv_44208968">
        #           </span>
        #           | <a href="hide?id=44208968&amp;goto=news">hide</a> |
        #           <a href="item?id=44208968">7&nbsp;comments</a>
        #       </span>
        #   </td>
        # </tr>

        # get the "tr" containing the upvotes
        # this "tr" is just below the "tr" containing the article "a" element
        sibling_tr = article_row.find_next_sibling(name="tr")
        # some articles can have 0 upvotes, in those cases there will be no upvote_span
        upvotes_span = sibling_tr.find(name="span", class_="score")

        if upvotes_span:
            upvotes = int(upvotes_span.string.split()[0]) # "123 points" → 123
        else:
            upvotes = 0

        article = {
            "title": article_tag.string,
            "link": article_tag.get("href"),
            "upvotes": upvotes
        }
        articles.append(article)

    # print(articles)
    # print the article with the highest upvotes
    highest_upvoted = max(articles, key=lambda a: a["upvotes"])
    print(highest_upvoted)

start_time = time.time()

# scrape_hn_old()
scrape_hn_live()

def humanize_time(seconds: float) -> None:
    intervals = {
        "days": 24*60*60,
        "hours": 60*60,
        "minutes": 60,
    }

    days, remainder = divmod(seconds, intervals["days"])
    hours, remainder = divmod(remainder, intervals["hours"])
    minutes, remainder = divmod(remainder, intervals["minutes"])
    seconds = round(remainder, 2)

    part = []
    if days:
        part.append(f"{int(days)}d")
    if hours:
        part.append(f"{int(hours)}h")
    if minutes:
        part.append(f"{int(minutes)}m")
    if seconds:
        part.append(f"{seconds}s")

    print( "Elapsed: " + " ".join(part))

end_time = time.time()
humanize_time(end_time - start_time)
