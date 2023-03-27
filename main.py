import requests
import pandas
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as BSHTML
request=requests.get("https://www.ariamarz.com/buy-apartment/isfahan?in=&sub_categories[]=sale&sub_categories[]=owner&sub_categories[]=foreclosures&potential_categories[]=coming-soon&potential_categories[]=participation&potential_categories[]=auction&home_types[]=10&add_id=52&add_type=city&q=%D8%A7%D8%B5%D9%81%D9%87%D8%A7%D9%86%20&sorting_order=featured&lat0=32.77980759773184&lat1=32.5251270603347&lng0=51.872458317195985&lng1=51.51316486301032")
content=request.content
soup=BeautifulSoup(content)
all=soup.find_all("a",{"class":"product-plate-detail"})
list_di=[] #for saving dictionaries 
for item in range(len(all)):
    d={}    # a dictionary for saving the properties of house like price and ...
    price_text=str(all[item].find("strong"))
    BS=BSHTML(
        price_text
    )
    d["price"]=BS.strong.contents[0].strip()
    # find desciption of house
    des=str(all[item].find("li",{"class":"medium-sm-text"}))
    des=des.replace(r'<br/>',"@")
    BS_des=BSHTML(
        des
    )
    details=BS_des.li.contents[0].strip()
    details=details.split('@')
    d["title"]=details[0]
    d["address"]=details[1]

    #find the Features of the house
    Features=all[item].find_all("span",{"class":"medium-sm-text"})
    list=[]
    list_of_features=["bed","Foundation","year of buld","land area","floor","elevator"]
    for x in range(len(Features)):
         BS_Features=BSHTML(
                str(Features[x])
            )
         list.append(BS_Features.span.contents[0].strip())
         d[list_of_features[x]]=BS_Features.span.contents[0].strip()

    list_di.append(d)

#create a data frame by pandas and save it to a csv file
df=pandas.DataFrame(list_di)
df.to_csv("output.csv")