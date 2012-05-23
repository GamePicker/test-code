#!/usr/bin/python
# grab list of owned games from a user on BGG
# 2.7

import urllib
from operator import itemgetter, attrgetter
import re
 
#import easy to use xml parser called minidom:
from xml.dom.minidom import parseString

user = raw_input('Enter username: ')
url =  'http://boardgamegeek.com/xmlapi2/collection?username=' + user + '&own=1'

#download the file:
file = urllib.urlopen(url)
data = file.read()
file.close()

#parse the xml
dom = parseString(data)

#get list of game names
xmlList = dom.getElementsByTagName('name')

#step through games
i = 1
numlist = []
for node in xmlList:
    name = node.firstChild.data
    #print(name)
    numlist.append([i,str(name),0])
    print(str(i) + " " + numlist[i-1][1])
    #print(numlist)
    i += 1

z = int(raw_input('Enter the number of voters: '))
y = 1
while y <= z:
    for item in numlist:
        print(str(item[0]) + ' ' + str(item[1]))
    print
    print('Voter ' + str(y))
    print('Enter the numbers of your top five choices, starting at your top choice.')

    # choose top 5
    for j in range(1,6):
        k = raw_input("Enter choice " + str(j) + ": ")
        for l in numlist:
            if l[0] == int(k):
                l[2] += int(j)
            #print l

    print
    y += 1
    
#show list with scores
#for item in numlist:
#    print(str(item[0]) + ' ' + str(item[1]) + ' ' + str(item[2]))

print

#show final sorted list
top = sorted(numlist, key=itemgetter(2))
for item in top:
    if item[2] != 0:
        print(str(item[1]) + ' ' + str(item[2]))

print
