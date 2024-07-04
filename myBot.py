from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from bale import Bot, Message
import os 

# Token for your Bale bot
# TOKEN = '1244544145:mqHNLLxL2kFbP9qiCz6AcRp4ikxe9GQzMCMVvNLI'
load_dotenv()
myToken = os.environ.get('TOKEN')
# myToken = "2070467203:jaK15Gxse6kJ7FsEgb3AC9dfJ6hl5CIlM4wymjfQ"
bot = Bot(token=myToken)

# Fixed base URL and keyword
base_url_template = 'https://jobinja.ir/jobs?&filters%5Bjob_categories%5D%5B0%5D=IT%20%2F%20DevOps%20%2F%20Server&filters%5Bkeywords%5D%5B0%5D=&filters%5Blocations%5D%5B0%5D=%D8%AA%D9%87%D8%B1%D8%A7%D9%86&page={}&preferred_before=1718817613&sort_by=published_at_desc'
keyword = 'امریه'

# Function to search for the keyword in a given page
def search_keyword_in_page(url, keyword):
    matching_links = []
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            page_text = soup.get_text()

            if keyword in page_text:
                matching_links.append(url)
    except Exception as e:
        print(f"Error loading {url}: {e}")
    return matching_links

# Function to find links in the specified section
def find_links_in_section(url):
    matching_links = []
    visited_links = set()
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            target_section = soup.find('ul', class_='o-listView__list c-jobListView__list')
            if target_section:
                links = target_section.find_all('a', href=True)
                for link in links:
                    href = link['href']
                    full_url = urljoin(url, href)
                    if full_url not in visited_links:
                        visited_links.add(full_url)
                        matching_links += search_keyword_in_page(full_url, keyword)
            else:
                print("Target section not found.")
        else:
            print(f"Error loading base page! (Status code: {response.status_code})")
    except Exception as e:
        print(f"Error loading {url}: {e}")
    return matching_links

# Bale bot event handler
@bot.event
async def on_message(pm: Message):
    matching_links = []
    for page in range(1, 8):
        base_url = base_url_template.format(page)
        print(f"Searching in: {base_url}")
        matching_links += find_links_in_section(base_url)
    if matching_links:
        response = "\n".join(matching_links)
    else:
        response = f"No links containing the keyword '{keyword}' were found."
    await pm.reply(response)


def run_by():
    bot.run()
    
# Start the bot
# if __name__ == "__main__":
#     bot.run()