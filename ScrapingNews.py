import requests
import csv
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


start=1
end=501

headlines=[]
news=[]
target=[]
user_agent = UserAgent()

for i in range(start,end):                               #iterating through web pages


	r=requests.get(f'https://www.politifact.com/factchecks/list/?page={i}',headers={"user-agent": user_agent.chrome})
	soup=BeautifulSoup(r.content,'lxml')
	headlines=soup.find_all('li',{ "class" : "o-listicle__item"})         

	
	for j in range(len(headlines)):					    #iterating through different news headlines in a single webpage
		info=headlines[j].find('div',{"class":"m-statement__quote"})
		news.append(info.find('a').text)                #extracting actual news headline text
		news[j]=news[j].strip('\n')
		news[j]=news[j].strip('"')
		
		pic=headlines[j].find('div',{"class":"m-statement__meter"})
		tar=pic.find('img',{"class":"c-image__thumb"})         #extracting whether news is real or fake
		target.append((tar.get('alt')))                

	print(f'page {i} scraped')
		

for i in range(len(target)):                              #converting real to 1 and fake to 0
	if target[i]=="true":
		target[i]=1
	else:
		target[i]=0
 

with open('Fake News Data.csv','a',encoding='utf-8') as csv_file:       #saving the scraped data to a csv file
	writer=csv.writer(csv_file)
	for i in range(len(target)):
		writer.writerow([news[i],target[i]])

print("Saved to the file")
print(len(news))
print(len(target))
