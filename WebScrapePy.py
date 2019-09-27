from bs4 import BeautifulSoup
import requests
import pandas as pd

url = "http://asd.com.tr/ajax/login.php"
headers = {'User-Agent': 'Mozilla/5.0'}
payload = {'email': '...', 'password': '...'}
#response=requests.post(url,headers=headers,data=payload)
session = requests.Session()
r=session.post(url,headers=headers,data=payload)
print(url)
print("hayrialik@ymail.com => Login oldu")
mainpage=session.get("http://asd.com.tr/")
mainpage_soup= BeautifulSoup(mainpage.text,'html.parser')
paginator = mainpage_soup.find("div",{"class":"paginator"})
totalpage_lis=paginator.find_all("a")
print("http://asd.com.tr/")
print("Sayfa sayısı alınıyor...")
pagenums=[]
for li in totalpage_lis:
    pagenums.append(int(li.text)-1)

print(str(len(pagenums)) +" Sayfa yorum bulundu")
print(pagenums)
dict={}
counter=0

for i in pagenums:
    
    print(str(i+1)+ ". Sayfa başlanıyor...")
    print("http://asd.com.tr/ajax/comments.php?p="+str(i))
    com_page=session.get("http://asd.com.tr/ajax/comments.php?p="+str(i))
    suop= BeautifulSoup(com_page.text,'html.parser')
    boxes=suop.find_all("div",{"class":"comment-box"})
    for box in boxes:
        name=box.find("h6", {"class": "comment-name"}).text.strip()
        comment=box.find("div", {"class": "comment-content"}).text.strip()
        date=box.find("span", {"class": "right"}).text.strip()
        counter+=1
        dict[counter]=[date, name, comment]
    print(str(i+1)+ ". Sayfa tamamlandı")
    time.sleep(1)

dict_df=pd.DataFrame.from_dict(dict, orient='index', columns=["isim", "yorum", "tarih"])
dict_df.to_csv('asdyorumlari.csv')
