#!/usr/bin/python
#
# grab list of owned games from a user on BGG
# initiator sets number of games to be in vote list
# initiator chooses games to appear in vote list
# intiator chooses number of voters
# voters vote
# app returns list of games ordered by score
#
# TODO:
# - functionize chunks > limit variable scope > reclaim variables

import urllib
from operator import itemgetter, attrgetter
import re
 
#import easy to use xml parser called minidom:
from xml.dom.minidom import parseString

user = raw_input('Enter username: ')
url = 'http://boardgamegeek.com/xmlapi2/collection?username=' + user + '&own=1'

#download the file:
file = urllib.urlopen(url)
data = file.read()
file.close()

#parse the xml
dom = parseString(data)

#get list of game names
xmlList = dom.getElementsByTagName('name')

#build game array
i = 1
numlist = []
for node in xmlList:
    name = node.firstChild.data
    numlist.append([i,str(name),0])
    print(str(i) + " " + numlist[i-1][1])
    i += 1

#have initiator create a culled list to present to voters
numCull = int(raw_input('Enter the number of games from which to choose: '))

voteList = []
i = 1

while i <= numCull:
	j = int(raw_input('Enter choice ' + str(i) + ': '))
	for k in numlist:
		if k[0] == j:
			voteList.append([i, k[1], 0])
	i += 1
	

# voting
numVoters = int(raw_input('Enter the number of voters: '))

# each voter votes
y = 1
while y <= numVoters:
    for item in voteList:
        print(str(item[0]) + ' ' + str(item[1]))
    print
    print('Voter ' + str(y))
    print('Starting at your top choice, enter the game numbers in order of preference.')

    # choose top 5
    for j in range(1,numCull+1):
        k = raw_input("Enter choice " + str(j) + ": ")
        for l in voteList:
            if l[0] == int(k):
                l[2] += numCull + 1 - int(j)
            #print l

    print
    y += 1

print

#show final sorted list
top = sorted(voteList, key=itemgetter(2), reverse=True)
for item in top:
    if item[2] != 0:
        print(str(item[2]) + ' ' + str(item[1]))

print
