import re
import requests
import datetime
import pandas as pd
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self):
        self.obj_df = pd.DataFrame()
        self.base_url = 'https://old.reddit.com/r/india/top/'
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; rv:122.0) Gecko/20100101 Firefox/122.0'
        self.headers = {
            "User-Agent": self.user_agent,
            "Accept-Language": "en-US,en;q=0.5"
        }
    
    def make_request(self, url:str) -> requests.models.Response:
        """
            Wrapper for Requests
        """
        return requests.get(url, headers=self.headers)

    def update_obj_list(self, soup:BeautifulSoup) -> None:
        """
            Update main Pandas DF
        """

        ## Remove ADs
        posts = [str(x) for x in soup.select('div#siteTable > div[data-promoted]') if 'alb.reddit.com' not in str(x)]
        posts_html = ''
        for p in posts:
            if '[deleted]' not in p:
                posts_html += p
        soup = BeautifulSoup(posts_html, 'html.parser')

        ## Extract post attributes and create Pandas DF
        titles = [x.contents[0] for x in soup.select('div.entry.unvoted p.title a.title')]
        urls = [x['href'] for x in soup.select('div.entry.unvoted p.title a.title')]
        flairs = [x['title'] for x in soup.select('div.entry.unvoted p.title span.linkflairlabel')]
        domains = [x.contents[0] for x in soup.select('div.entry.unvoted p.title span.domain a:nth-child(1)')]
        timestamps = [x['datetime'] for x in soup.select('div.entry.unvoted p.tagline time:nth-child(1)')]
        users = [x.contents[0] for x in soup.select('div.entry.unvoted p.tagline a.author')]
        user_links = [x['href'] for x in soup.select('div.entry.unvoted p.tagline a.author')]
        comments = [int(re.search('[0-9]+', x.contents[0])[0]) if re.search('[0-9]+', x.contents[0]) else 0 for x in soup.select('a.comments')]
        self_urls = [x['href'] for x in soup.select('a.comments')]
        upvotes = [x.contents[0] for x in soup.select('div.midcol.unvoted > div.score.unvoted')]

        temp_df = pd.DataFrame({
                    'title': titles,
                    'url': urls,
                    'self_url': self_urls,
                    'domain': domains,
                    'flair': flairs,
                    'create_date': timestamps,
                    'user': users,
                    'user_link': user_links,
                    'comments': comments,
                    'upvotes': upvotes
                  })

        ## Append with Main DF
        self.obj_df = pd.concat([self.obj_df, temp_df])

    def scrape(self) -> None:
        """
            Driver function for the scraper
        """
        next_page_flag = True
        next_page_link = self.base_url

        ## Continue scraping till the pages have been exhausted
        while next_page_flag:
            res = self.make_request(next_page_link).text
            res_soup = BeautifulSoup(res, 'html.parser')

            ## Check if 'next' button is available on the page
            next_page_flag = res_soup.select('.next-button > a:nth-child(1)') != []
            next_page_link = None
            if next_page_flag:
                next_page_link = res_soup.select('.next-button > a:nth-child(1)')[0]['href']

            ## Update main Pandas DF for this page
            self.update_obj_list(res_soup)

    def write_to_csv(self) -> None:
        """
            Writes main Pandas DF to CSV 
        """
        self.obj_df.to_csv('/tmp/bronze.csv',index=False)


if __name__ == "__main__":
    s = Scraper()
    s.scrape()
    s.write_to_csv()
