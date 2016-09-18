import urllib2
import sys
import sre
import xml.etree.cElementTree as ET
from expletives import flaggedWords
from curses.ascii import isalnum

global foundFlaggedWord # globals are probably not the best syntax; might consider revising
global flaggedDict

def outputString(targetApp, string, color_tag="NORMAL"):
    print string
    targetApp.output(string, color_tag)

def retrieveWebPage(address): 
    # simply retrieves the contents of a url address
    try:
        web_handle = urllib2.urlopen(address)
    except urllib2.HTTPError, e:
        return -1
    except urllib2.URLError, e:
        return -1
    except:
        return -1
    return web_handle

def checkFlaggedWords(string):
    # takes a string of words (lyrics in this targetApplication) and checks for
    # any words from the "flagged words" list in expletives.py
    global foundFlaggedWord
    global flaggedDict

    string = string.split()

    # TODO: check for a more efficient way of determining if a word is contained in
    #       a list. Possibly a string.contains() function?

    for flag in flaggedWords:
        for word in string:
            if flag.lower() == word.lower():
                foundFlaggedWord = True
                flaggedDict[flag] += 1

def removeArrayIndexes(removeArray, stringAsList):
    # removes indexes in the passed removeArray from the passed string

    for i in range(0, len(removeArray)):
        if len(stringAsList) < 1:                  # handles the entire track name being removed
            break
        
        del stringAsList[removeArray[i] - i]        # removes the index from the passed string

def printInfo(targetApp, album, artist):

    ### INITIALIZATIONS ###
    global foundFlaggedWord
    global flaggedDict

    # used while parsing the html of the lyric page
    lyricMatchText = '<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->'
    albumMatchText = "<mbid>"
    lyricSkipArray = ["<p class='verse'>",'</p>','<br>','<br/>','</div>','<i>','</i>']
    tracksXMLIndex = 0

    devMode = False

    ### DETERMINE DEVMODE ###
    if len(sys.argv) > 1:
        if sys.argv[1] == '1':
            devMode = True

    ### CREATE FLAGGEDWORDS DICTIONARY ###
    flaggedDict = {}

    for flag in flaggedWords:                           # setup the flagged words dictionary
        flaggedDict[flag] = 0

    albumArtistRaw = artist
    albumTitleRaw = album

    ### PARSE TITLE AND ARTIST ###

    albumArtist = albumArtistRaw.replace(" ", "+")      # should be a more efficient version of the code below

    #albumArtist = list(albumArtistRaw)
    #for char in albumArtist:
    #    if char == " ":
    #        albumArtist[albumArtist.index(char)] = "+"
    #albumArtist = ''.join(albumArtist)

    albumTitle = albumTitleRaw.replace(" ", "+")

    #albumTitle = list(albumTitleRaw)
    #for char in albumTitle:
    #    if char == " ":
    #        albumTitle[albumTitle.index(char)] = "+"
    #albumTitle = ''.join(albumTitle)

    ### GET ALBUM MBID TO FETCH TRACKS INFO ###

    website_handle = retrieveWebPage("http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key=99b4600df803050c59f71a4d4b506e9e&artist=" + albumArtist.lower() + "&album=" + albumTitle.lower())

    if devMode:
        outputString(targetApp, "http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key=99b4600df803050c59f71a4d4b506e9e&artist=" + albumArtist.lower() + "&album=" + albumTitle.lower())

    if website_handle == -1:
        outputString(targetApp, "\nCould not get data for " + albumTitleRaw)
        return

    outputString(targetApp, "\nSuccessfully retrieved album metadata...\n\n")

    xmlRoot = ET.fromstring(website_handle.read())      # gets the XML root in an array from Scrobbler

    tracksArray = []                                    # should probably move this (and other variable declarations) to a cetnral place

    # get the tracks index from the XML document to prevent fallacious song titles
    for i in range(0, len(xmlRoot[0])):
        if xmlRoot[0][i].tag == "tracks":
            tracksXMLIndex = i
            break

    # handles no valid tag
    if tracksXMLIndex == 0:
        outputString(targetApp, "Could not find any tracks listed for this album on last.fm...\n\n", "ERROR")
        outputString(targetApp, "Feel free to check each track individually with the single lyric checker.\n\n", "ERROR")
        return

    for i in range(0, len(xmlRoot[0][tracksXMLIndex])):
        tracksArray.append(xmlRoot[0][tracksXMLIndex][i][0].text)

    if devMode:
        outputString(targetApp, tracksArray)

    # this is duplicate code from above; should probably consolidate into a function
    if len(tracksArray) == 0:
        outputString(targetApp, "It appears there were no tracks listed for this album on last.fm...\n\n", "ERROR")
        outputString(targetApp, "Feel free to check each track individually with the single lyric checker.\n\n", "ERROR")
        return

    ### PARS TRACK NAMES ###
    cleanTracksArray = list(tracksArray)    # create a clean copy for use later

    for track in tracksArray:
        removeArray = []
        tmpInt = tracksArray.index(track)

        track = track.replace(" ", "")
        
        # remove non-alphanumeric characters from track name
        trackList = list(track)
        for i in range(0, len(trackList)):
            if trackList[i].isalnum() == False:
                removeArray.append(i)
        
    #    track = list(track)
    #    for i in range(0, len(track)):
    #        if track[i] == " ":
    #            track[i] = ""
    #        elif track[i].isalum() == False:
    #            removeArray.append(i)
        
        # remove removeArray items from track name
        removeArrayIndexes(removeArray, trackList)
        removeArray = []    # reset removeArray

        track = ''.join(trackList)      # reset track to the newly parsed value
        tracksArray[tmpInt] = track     # reset the track name in tracksArray to reflect parsed ValueError

    ### PARSE ARTIST NAME ###

    albumArtist = list(albumArtistRaw)

    # remove 'the' from the artist name
    if ''.join(albumArtist[0:4]) == "the ":
        
        if devMode:
            outputString(targetApp, "found 'the'")
        
        del albumArtist[0:4]

    for i in range(0, len(albumArtist)):
        if albumArtist[i] == " ":
            albumArtist[i] = ""
        elif albumArtist[i].isalnum() == False:
            removeArray.append(i)
        else:
            continue

    # remove removeArray items from album artist
    removeArrayIndexes(removeArray, albumArtist)        # is there a reason I'm not waiting until the end?
    removeArray = []

    # handle extra dashes
    if albumArtist[0] == "-":
        del albumArtist[0]

    for i in range(1, len(albumArtist)):
        if albumArtist[i] == "-" and albumArtist[i-1] == "-":
            removeArray.append(i)

    removeArrayIndexes(removeArray, albumArtist)
    removeArray = []

    albumArtist = ''.join(albumArtist)


    ### BEGIN LYRIC PARSING ###

    if devMode:
        outputString(targetApp, cleanTracksArray)      # for easy viewing of original track titles

    for i in range(0, len(tracksArray)):
        lineArray = []
        foundLyrics = False
        foundFlaggedWord = False
        foundSomeLyrics = False

        website_handle = retrieveWebPage("http://www.azlyrics.com/lyrics/" + albumArtist.lower() + "/" + tracksArray[i].lower() + ".html")

        if devMode:
            # outputString(targetApp, website url for easy debugging
            outputString(targetApp, "http://www.azlyrics.com/lyrics/" + albumArtist.lower() + "/" + tracksArray[i].lower() + ".html")
        
        if website_handle == -1:        # url request failed
            outputString(targetApp, "Could not get lyrics for " + cleanTracksArray[i] + ".\n\n", "ERROR")
            continue
        
        outputString(targetApp, "Successfully retrieved lyrics for \"" + cleanTracksArray[i] + "\"\n\n")

        for line in website_handle:
            lineArray.append(line.strip())
        
        # clean up lineArray by narrowing down to only lyrics
        deletedLineCount = 0
        for i in range(0, len(lineArray)):
            if foundLyrics == True:
                if lineArray[i - deletedLineCount].strip() == '</div>':
                    del lineArray[i - deletedLineCount]
                    deletedLineCount += 1
                    foundLyrics = False
                    foundSomeLyrics = True
            else:
                if lineArray[i - deletedLineCount].strip() == lyricMatchText:
                    del lineArray[i - deletedLineCount]
                    deletedLineCount += 1
                    foundLyrics = True
                else:
                    del lineArray[i - deletedLineCount]
                    deletedLineCount += 1
        
        # iterate through each line of lyrics
        for x in range(0, len(lineArray)):
            lineList = list(lineArray[x])
            
            # iterate through each phrase and determine if it is a lyric or an html tag
            for phrase in lyricSkipArray:
                for i in range(0, len(lineList)):
                    if len(lineList) < len(phrase):
                        break
                    else:
                        # remove phrase if it is not a lyric
                        if ''.join(lineList[i:i + len(phrase)]) == phrase:
                            del lineList[i:i + len(phrase)]
                
                lineString = ''.join(lineList)
            
            lineArray[x] = lineString
        
        # now that all lines have been cleaned up, check for flagged words until the end of lyrics
        for line in lineArray:
            if line == "</div>":
                break
            else:
                checkFlaggedWords(line)
        
        # iterate flagged words if there are any
        if foundFlaggedWord == True:

            #sys.stdout.write("\033[31m")                                    # sets text color. Mac only?
            for flag in flaggedDict:
                if flaggedDict[flag] != 0:
                    
                    # create censored word
                    censoredWord = list(flag)
                    for i in range(1,len(censoredWord) - 1):
                        censoredWord[i] = "*"
                    censoredWord = "".join(censoredWord)
                    
                    # outputString(targetApp, plural if multiple
                    if flaggedDict[flag] > 1: 
                        outputString(targetApp, "Found " + str(flaggedDict[flag]) + " instanes of " + censoredWord + "\n\n", "EXPLICIT")
                    else:
                        outputString(targetApp, "Found " + str(flaggedDict[flag]) + " instance of " + censoredWord + "\n\n", "EXPLICIT")
            
            #sys.stdout.write("\033[0m")                                     # sets text color. Mac only?
        
        elif foundSomeLyrics == True:
            outputString(targetApp, "No flagged words found.\n\n", "CLEAN")
        else:
            outputString(targetApp, "No lyrics found.\n\n", "ERROR")
        
        ### RESET FLAGGED WORDS DICT ###
        for item in flaggedDict:
            flaggedDict[item] = 0
        
    return