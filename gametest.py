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
import re
from xml.dom.minidom import parseString
from operator import itemgetter, attrgetter

def bggarray(user):
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
    try:
        i = 1
        numlist = []
        for node in xmlList:
            name = node.firstChild.data
            numlist.append([i,str(name),0])
            i += 1
    
        return numlist

    except TypeError:
        return []

def showlist(list):
     #display list of games
    for item in list:
        print(str(item[0]) + " " + item[1])

def validate(choice,choicelist,most):
    if choice >= 1 and choice <= most and choice not in choicelist:
        return True
    else:
        return False

def cullList(numCull,numlist):
    #build culled list of games from initiator
    error = 'Please enter a valid number from the list which has not been previously chosen.'    
    voteList = []
    choicelist = []
    i = 1
    while i <= numCull:
        try:
            j = int(raw_input('Enter choice ' + str(i) + ': '))
            if validate(j,choicelist,len(numlist)):
                for k in numlist:
                    if k[0] == j:
                        voteList.append([i, k[1], 0])
                        choicelist.append(j)
                i += 1
            else:
                print(error)
        except ValueError:
            print(error)
    return voteList


def userVoting(numVoters,voteList,numCull):

    i = 1
    while i <= numVoters:
        print('\n' * 100)
        for item in voteList:
            print(str(item[0]) + ' ' + str(item[1]))
        print
        print('Voter ' + str(i))
        print('Starting at your top choice, enter the game numbers in order of preference.')
        
        #loop through voter choices        
        choicelist = []        
        j = 1        
        while j <= numCull:
            
            try:
                k = int(raw_input("Enter choice " + str(j) + ": "))
                if validate(k,choicelist,numCull):
                    #score choice
                    for l in voteList:
                        if l[0] == k:
                            l[2] += numCull + 1 - int(j)
                            #print(str(k) + " " + l[1])      
                    #add choice to temp choice list
                    choicelist.append(k)
                    #increase counter
                    j += 1
                else:
                    print("Please enter a valid number from the list which has not been previously chosen.")
            except ValueError:
                print("Please enter a valid number from the list which has not been previously chosen.")                    
        print
        i += 1
    return voteList

def results(voteList):
	top = sorted(voteList, key=itemgetter(2), reverse=True)
	for item in top:
		if item[2] != 0:
			print(str(item[2]) + ' ' + str(item[1]))

def validatequan(choice,most):
     if choice >= 1 and choice <= most:
        return True
     else:
        return False

def main():

    done = False
    
    while not done:
        #bgg username    
        print
        user = raw_input('Enter username: ')
        numlist = bggarray(user)

        if len(numlist) > 0:
        
            #display bgg user's owned games
            print
            showlist(numlist)
    
            #number of games to build new list
            print

            quan = False
            while not quan:
                numCull = int(raw_input('Enter the quantity of games for the voting pool: '))
                quan = validatequan(numCull,len(numlist))
        
            #build the new culled list
            print
            print('Choose the games for the vote list.')
            voteList = cullList(numCull, numlist)
        
            #get number of voters    
            print
            numVoters = int(raw_input('Enter the number of voters: '))
    
            #user voting
            finallist = userVoting(numVoters,voteList,numCull)
    
            #sort and display results of user voting
            print
            results(finallist)
    
            done = True
        else:
            print('Enter a valid username.\n')
	
if __name__ == "__main__":
    main()	
	
