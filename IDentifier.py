import requests
from bs4 import BeautifulSoup
from thefuzz import process
from time import sleep as s
import os
import pyperclip

# - shared variables and functions
def cls(): os.system('cls' if os.name == 'nt' else 'clear')
textlist, urllist = None, None
    
# - main "page" function
def main(textlist, urllist):
    cls()
    print("App IDentifier     -  prezzah  -  Enter to return / exit\n\n\n\n\n")


    searchterm = input("Search Titles:")
    if searchterm == "": 
        cls()
        exit()
    searchamt = input("Title Selection Amount (max 5, default 3): ")
    
    # - turns searchamt into int and defaults searchamt to either 3 or 5 depending on incorrect inputs
    try:
        searchamt = int(searchamt)
        if searchamt < 1:
            searchamt = 3
        elif searchamt > 5:
            searchamt = 5
    except ValueError:
        searchamt = 3
    
    searchurl = f"https://store.steampowered.com/search?term={(searchterm.replace(" ", "+")).lower()}"

    # - scrape data from Steam, if unable to, returns error
    try:
        response = requests.get(searchurl, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, features="html.parser")
    except requests.RequestException:
        cls()
        print("App IDentifier     -  prezzah\n\n\n")
        print(f"Error connecting to Steam. Please check your internet connection.")
        s(3)
        return main, textlist, urllist
    
    # - scrape title and url elements from Steam search results
    titles = soup.find_all('span', {'class': 'title'})
    urls = soup.find_all('a', {'class': 'search_result_row ds_collapse_flag'})

    # - filter results using fuzzy matching and limit to searchamt
    titlematch = (process.extract(searchterm, titles))[:searchamt]
    urlmatch = (process.extract(searchterm, urls))[:searchamt]

    # - lists to store parsed titles and app IDs
    textlist = []
    urllist = []

    # - appending "for" loops  -  neat-ifies the "..match" variables (html jumbo) into the two lists above ^
    for i in titlematch:
        i=str(i)
        start = i.find('">')
        end = i.find('</span')
        textlist.append(i[start+2:end])
    for i in urlmatch:
        i=str(i)
        start = i.find('data-ds-appid=')
        i=i[start+15:start+30]
        end = i.rfind('"')
        urllist.append(i[:end])
    
    # - transitioning text  -  if titles found, continue, if not, restarts page
    if len(textlist) > 0:
        cls()
        print("App IDentifier     -  prezzah\n\n\n")
        print(f"Titles found!  ({len(textlist)})")
        s(1)
        cls()
        return titlespg, textlist, urllist
    else:
        cls()
        print("App IDentifier     -  prezzah\n\n\n")
        print(f"No titles found. Try another search  ({len(textlist)})")
        s(3)
        return main, textlist, urllist
        

    
    

# - titles "page"  -  called by / ran after main, neat-ifies and displays data to user, etc.
def titlespg(textlist, urllist):
    cls()
    print("App IDentifier     -  prezzah  -  Enter to return / exit\n\n")
    
    
    # - displays title and corresponding app ID
    for i in textlist:
        idx = textlist.index(i)
        print(f'{idx+1}. {i} - {urllist[idx]}')
    
    copyel = input(f"\n\nCopy to clipboard (1-{len(urllist)}) or press Enter to search again: ")
    if copyel == "": return main, textlist, urllist
    
    # - verifies correct integer input, and copies app ID to user clipboard
    try:
        copyel = int(copyel)
        if 1 <= copyel <= len(urllist):
            pyperclip.copy(urllist[copyel-1])
            print(f"Copied '{urllist[copyel-1]}' to clipboard!")
            s(1)
        else:
            print("Invalid selection!")
            s(1)
    except ValueError:
        print("Invalid input! Please enter a number.")
        s(1)
        
    return titlespg, textlist, urllist
    
    
# - "page" navigation loop
current_page = main

while current_page is not None:
    current_page, textlist, urllist = current_page(textlist, urllist)