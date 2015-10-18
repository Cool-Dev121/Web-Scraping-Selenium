# -*- coding: utf-8 -*-
"""
Created on Tue Oct 06 07:51:50 2015
@author: keyur

### Name: Keyur Doshi
### Student ID: 10405923
### BIA 660B Mid Term Project

Description:

Mid Term project which will perform the following:

Step 1: Select 4 different websites that include reviews on TVs. The reviews should include text, a date of submission, and a star rating.

Step 2: Collect at least 1000 TV reviews from each of the 4 websites. Use a different python script for each website.

Step 3: Store all the reviews from all 4 websites in a single file called "reviews.txt". The file should include the following TAB-separated columns:

: website where the review came from (e.g. amazon.com).
: the FULL review text, exactly as it appears on the website.
: the review's rating 
: the review's date of submission, as it appears on the website.

"""


#Importing the libraries
import time,sys
from selenium import webdriver
from bs4 import BeautifulSoup

#Capturing the start time of this program
start_time = time.clock() 

#Creating a function which will parse Review, Date and Ratings
def parsePage(html,reviewSet):
    bsObj = BeautifulSoup(html)
    del allreviews[:]
    del alldates[:]
    del allratings[:]
    for review in bsObj.findAll("span",{"class":"review-text"}):
        allreviews.append(review.text.replace('\n', ' ').strip())
    for date in bsObj.findAll("div",{"class":"date line fk-font-small"}):
            alldates.append(date.text.strip())
    for rating in bsObj.findAll("div",{"class":"fk-stars"}):
            allratings.append(rating['title'].strip())


#Creating the list to store all the records            
allreviews=list()
alldates=list()
allratings=list()
      
#Opening the file      
fileWriter=open('output.txt','w')
fileReader=open('in.txt')

#Site used for parsing
sitename = 'www.filpkart.com'        

for line in fileReader:
    #Fetch the url from file in.txt    
    reviewlink =line.strip()
    url = reviewlink
    print url
    
    #open the browser and visit the url
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get(url)
    
    #sleep for 2 seconds
    time.sleep(2)
    
    #find the 'View All Top Reviews' button based on its xpath
    #button=driver.find_element_by_css_selector('.lnkViewAll')
    button = driver.find_element_by_xpath("//*[@id='fk-mainbody-id']/div/div[15]/div/div/div[2]/div[2]/a")
    button.click() #click on the button
    time.sleep(2) #sleep
    
    
    #parse the page of reviews
    parsePage(driver.page_source,allreviews)
    lenreview = len(allreviews)
    lendate = len(alldates)
    lenratings=len(allratings)
    
    #Comparing the length of the list
    if lendate == lenratings == lenreview:
            print ' in if :)'
            index = 0
            while (index < lenreview):
                fileWriter.write(sitename + '\t' + allreviews[index].encode('utf8')+ '\t'+ alldates[index].encode('utf8') + '\t' + allratings[index].encode('utf8') + '\n') #Writing the data to file
                index+=1
    else:
        print 'Some issue while writing data to file as records all records are not fetched.'
     
    nextpage=0
    while True:
        #get the css path of the 'next' button
        cssPath='#fk-mainbody-id > div > div.fk-review-page.gd-row.newvd > div.review-left.gd-col.gu12 > div.review-section.helpful-review-container > div.fk-navigation.fk-text-center.tmargin10 > a:nth-child(9)'
    #    cssCustPath = '#fk-mainbody-id > div > div.fk-review-page.gd-row.newvd > div.review-left.gd-col.gu12 > div.review-section.helpful-review-container > div.fk-navigation.fk-text-center.tmargin10 > a:nth-child(8)'
        try:
            button=driver.find_element_by_css_selector(cssPath)
            time.sleep(1)
        except:
            error_type, error_obj, error_info = sys.exc_info()
            print 'STOPPING - COULD NOT FIND THE LINK TO PAGE: ', nextpage
            print error_type, 'Line:', error_info.tb_lineno
            break
   
        #click the button to go the next page, then sleep    
        button.click()
        time.sleep(2)
        
        #parse the page
        parsePage(driver.page_source,allreviews)
    
        #print 'page',nextpage,'done'
        nextpage+=10
        
        #Comparing the length of the list
        lenreview = len(allreviews)
        lendate = len(alldates)
        lenratings=len(allratings)
        
        #           
        if lendate == lenratings == lenreview:
            index = 0
            while (index < lenreview):
                fileWriter.write(sitename + '\t' + allreviews[index].encode('utf8')+ '\t'+ alldates[index].encode('utf8') + '\t' + allratings[index].encode('utf8') + '\n')
                index+=1
        else:
            print 'Some issue while writing data to file as records all records are not fetched.'
            
   
#Printing the running time     
print time.clock() - start_time, "seconds"
#Closing the fileReader
fileReader.close()
#Closing the fileWriter
fileWriter.close()