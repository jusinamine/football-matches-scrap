import httplib2
from bs4 import BeautifulSoup
import json


## script to get all matches available from footballontv.com
## using web scraping

http = httplib2.Http()
status, response = http.request('https://www.live-footballontv.com/')
soup = BeautifulSoup(response)
elements = soup.select("#listings .row-fluid")
result = [] #lis of dict we will save all days of matches
index = 0 
next_element = True

for e in elements:#map all the rows of matches table
    sub_elements = list(e.children) #sub elements is the row of the table contain date or match info
    if(len(sub_elements) ==1): #when the sub element length is 1 so this element contain date of matches
        if(len(list(sub_elements[0].children)) == 1):
            next_element = True
            result.append({"date":sub_elements[0].getText(),"matches":[]})
            index +=1
        else:
            next_element = False
    else:#if the length is not equal to 1 so the element contain match information like time and teams ...
        if(next_element): #when the element before is date so after the date we will see all matches in this date
            teams = sub_elements[0].getText().split()
            #check if element containt "v" for exemple "barcelona v real madrid"
            if("v" in teams):
                result[index - 1]["matches"].append({
                    "first_team":' '.join(teams[0:teams.index("v")]), #first team is the team before the "v" 
                    "second_team":' '.join(teams[teams.index("v")+1:len(teams)]), #second team after "v"
                    "compitition":sub_elements[1].getText(),
                    "time":sub_elements[2].getText(),
                    "channels":sub_elements[3].getText().split("/") #the separation between channels is "/" so we split after each "/"
                })

print(result)
with open('football_matches.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)

    