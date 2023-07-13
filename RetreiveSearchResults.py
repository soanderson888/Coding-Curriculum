import requests
import bs4


text= input("Please type a search prompt")
url = 'https://google.com/search?q=' + text


request_result=requests.get(url)

soup = bs4.BeautifulSoup(request_result.text,
						"html.parser")

heading_object=soup.find_all('h3')

spacer = "___________________"
spacer_count = 0
max_headings = 9

while spacer_count < max_headings:
    for info in heading_object:
        print(spacer)
        spacer_count += 1
        print(info.getText())
