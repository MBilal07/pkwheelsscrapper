# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 10:08:08 2022

@author: Bilal
"""

from bs4 import BeautifulSoup
from selenium import webdriver
from csv import DictWriter



def getSoupDataFromUrl(url):
    try:
        driver = webdriver.Firefox(executable_path="C:/Users/Bilal/Documents/geckodriver.exe") # You can replace this with other web drivers
        driver.get(url)
        source = driver.page_source # Here is your populated data.
        driver.quit() # don't forget to quit the driver!
        return BeautifulSoup(source, 'lxml')
    except:
        return None;

def getLinksByKeyWord(soup,keyWord):
    return  [i.get("href") for i in soup.find_all('a') if i.get("href").find(keyWord) != -1]           

def getTagsByKeyWords(soup, tagName, propertyName, keyword):
   return soup.find_all(tagName,{propertyName: keyword})  

def getSingleTagByKeyWord(soup, tagName, propertyName, keyword):
    return soup.find(tagName,{propertyName: keyword})
     
    

           
def extractSingleCarInfo(soup):
    carProperties = ['year','millage','type','transmission']
    propertiesDictionary={}
    carName = getSingleTagByKeyWord(soup,'div','id','scroll_car_info').find('h1').find(text=True)
    propertiesDictionary['name'] = carName
    for carProperty in carProperties:
        propertyTag = getSingleTagByKeyWord(soup,'span','class',carProperty) 
        if propertyTag:
            propertiesDictionary[carProperty]=propertyTag.parent.find('p').find(text = True)
        print('parent',propertyTag.parent.find('p').find(text = True))
    
    # extracting more manual properties list
    otherPropertytags = getTagsByKeyWords(soup,'li','class','ad-data')  
    for i in otherPropertytags:
        propertiesDictionary[i.find(text = True)] = i.find_next_sibling('li').find(text=True)
    print('other Properties',otherPropertytags)

    # extracting car features  
    featureTags = getSingleTagByKeyWord(soup,'ul','class','car-feature-list').find_all('li')
    carFeaturesList = [featureTag.find(text = True) for featureTag in featureTags ]
    propertiesDictionary['features'] =carFeaturesList 
    
    # get seller comments
    
    sellerComments = getSingleTagByKeyWord(soup, 'h2', 'id', 'scroll_seller_comments').find_next_sibling('div').findAll(text=True)
    propertiesDictionary['sellerComments'] = ''.join(sellerComments)
    
    # get price
    price = getSingleTagByKeyWord(soup, 'div', 'class', 'price-box').find_all(text = True)
    propertiesDictionary['price'] =''.join( price)
    
    return propertiesDictionary    
        
# def getUniqueLinks(links):
#     allAppLinks = reduce(operator.concat, links)
#     allAppLinks = list(set(allAppLinks))
#     allAppLinks = [i for i in allAppLinks if i.count("/")>3]
    
def saveDataInFile(carsData, keys):
    with open('spreadsheet.csv','w') as outfile:
        writer = DictWriter(outfile, keys)
        writer.writeheader()
        writer.writerows(carsData)

baseUrl="https://www.pakwheels.com";
carsInfoList = []
# getting data from pages
for i in range(1,2634):
    soup = getSoupDataFromUrl(baseUrl+"/used-cars/search/-/"+'?page='+i)
    carsOnSinglePage = getTagsByKeyWords(soup,'li','class','managed-pw')
    
    for carInfo in carsOnSinglePage:
        carDetailLinkTags = getTagsByKeyWords(carInfo,'a','class','ad-detail-path')
        if(len(carDetailLinkTags)>0):
            individualCarLink = carDetailLinkTags[0].get('href')
            carDetailedSoup = getSoupDataFromUrl(baseUrl+individualCarLink)
            singleCarProperties = extractSingleCarInfo(carDetailedSoup)
            carsInfoList.append(singleCarProperties)
            print('props',singleCarProperties)
    saveDataInFile(carsInfoList,list(carsInfoList[0].keys()))
            
            


















