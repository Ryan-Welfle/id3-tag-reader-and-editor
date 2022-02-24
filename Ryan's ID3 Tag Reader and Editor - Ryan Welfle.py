#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 17:26:18 2019
@author: ryanwelfle

This was created via Spyder 3.3.2, and would best be run via that environment.
 
Description: This is a program that allows the user to read the ID3 tags from mp3 files
contained in a chosen pathway. It also allows for the changing and editing of certain
ID3 tags. Finally, it allows to view only certain files in a pathway based on specific
ID3 criteria.

ID3 tags on mp3s simply show the artist name, song title, file size, bitrate, etc. of
mp3 files.

This program is based somewhat on a YouTube video by "Tutorial Spot",
called "Python Programming - Extracting ID3 Tags from MP3 Files", which can
be found here: https://www.youtube.com/watch?v=rnW2ibT89Hw

Additional libraries that this program requires in order to works are:
• tinytag
• mutagen

I installed both of these using Terminal, with these commands:

• pip install tinytag
• pip install mutagen   

How to use this program itself:

An example of a pathway to a folder is:
"/Users/ryanwelfle/Desktop/musicfiles/"

In the above example, the folder holding the mp3s is called "musicfiles"

You can find the pathway to your mp3 folder by dragging and dropping
your folder into Command Prompt (for Windows users), or Terminal (for Mac
users, like myself). Whatever pops up on the command line is your pathway.

An example of an individual file name to enter is:
"02 Falling.mp3"

Basically, just type in the file name as it appears in your folder, with the
".mp3" extension as well.

"""

import sys      ###used to exit the program
import os
from tinytag import TinyTag, TinyTagException # used to read the mp3 ID3 tags
from mutagen.id3 import ID3, TIT2, TALB, TRCK, TPE1, TCON, TYER, TLEN # used to edit the mp3 ID3 tags
        
def main():    #entire program is in this function
    print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('\nWelcome to Ryan\'s ID3 Tag Reader & Editor!\n')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    pathway = input('Please type in the pathway to your music folder ...\n(or type "exit" to leave the program):\n')
    if pathway.lower().strip() == 'exit':
        print('\n~~~~~~~~~~~~~~~')
        print('\nCome back soon!\n')
        print('~~~~~~~~~~~~~~~\n')
        sys.exit()
    if not(pathway.endswith('/')):  #adds forward-slash to end of pathway name if pathway name is not written with one
        pathway += '/'
    if not(pathway.startswith('/')): #adds forward-slash to beginning pathway name if pathway name is not written with one
        pathway = '/' + pathway
    if True:
        amountoffiles = input('\nWould you like to look at: \n(A) all of the files in this folder, or ... \n(B) just one file ... \n\nMake a selection: (A/B) ').lower().strip()    # using lower() and strip() to take away whitespace and put input in lower case to avoid answers that lead no-where        
        if amountoffiles == 'b':
            whichfile = input('\nType in the exact name of the file that you want to view: ')
            if whichfile.startswith('/'):                   # removes forward-slash from beginning of filename if user writes it with one
                whichfile = whichfile.replace('/', '')
            tracks = []
            for root, dirs, files, in os.walk(pathway):     # a "for" loop to check the pathway location itself, the files in the root directory, and the folders in the directory
                for name in files:                          #a "for" loop that's purpose is to look at each file in the pathway, to then search for the file name inputted by the user
                    if name.endswith((whichfile)):
                        tracks.append(name)                 #if the inputted file name is found, then it gets appended to a list
                        try:
                            temp_track = TinyTag.get(root + "/" + name)     #"tinytag" library is used to retrieve the mp3 file (if it is found) so that ID3 tags may be read
                            print("\nArtist Name: " + temp_track.artist)    #using 'tinytag' method to display mp3 file artist name
                            print("Song Title: " + temp_track.title)     #using 'tinytag' method to display mp3 file song title 
                            print("Album Title: " + temp_track.album)    #using 'tinytag' method to display mp3 file album name
                            print("Track Number: " + str(temp_track.track))  #using 'tinytag' method to display mp3 file track number
                            print("Year Released: " + str(temp_track.year))      #using 'tinytag' method to display mp3 file year released
                            print("Song Length: " + str(int((temp_track.duration)//60)) + ':' + str(int(temp_track.duration)%60))    #'tinytag' displays song length in seconds, so I used integer divide and modulus to convert length into minutes:seconds
                            print("Bitrate: " + str(int(temp_track.bitrate)) + " kBits/s")  #using 'tinytag' method to display mp3 file bitrate, and conatenated bitrate unit
                            print("Sample Rate: " + str((temp_track.samplerate)/1000) + " kHz")  #using 'tinytag' method to display mp3 file sample rate; I converted sample rate from Hz to kHz, and concatenated the 'kHz' unit
                            print("File Size: " + str(round((temp_track.filesize/1000000), 2)) + ' MB')  #using 'tinytag' method to display mp3 file size; I converted the file size from bytes to MB with division and rounded the answer to two decimal places with the round() function 
                            print("Genre: " + temp_track.genre)  #using 'tinytag' method to display mp3 file genre name
                            print(' ')
                            if tracks == []:        # 'if' statement for a circumstance where file is not found, thus nothing is appended to the "tracks" list
                                print('\nERROR!')
                                print('\nThere are either:\n\n• no files in the selected pathway, or \n• your pathway entry was invalid')
                                print('\nReturning to start of program ... \n')
                                main()   #returns to the beginning of the program by calling the main() function
                            else:
                                wanttochange = input('Would you like to change a specific tag? (yes/no) ').lower().strip()
                                if wanttochange == 'no':
                                    print('\nReturning to start of program ... \n')
                                    main()
                                if wanttochange == 'yes':
                                    print('\nWhat would you like to change?')
                                    print('\n(A) Artist Name \n(B) Song Title \n(C) Album Title')
                                    print('(D) Track Number \n(E) Year Released \n(F) Genre Name')
                                    edittag = input('\nEnter a selection: (A/B/C/D/E/F) ').lower().strip()
                                    if edittag == 'f':      #editing genre name
                                        while True:
                                            print('\nType in the new genre name ...')
                                            genrename = input('Note: user input will convert to all lower-case \nto bypass pre-set ID3 genre tags and retain \nuser input: ').lower().strip() #input genre name here
                                            audio = ID3(str(pathway) + str(whichfile))   #creating 'audio' variable for mutagen library to hold the file pathway name, and the file name itself, that that ID3 tag may be edited
                                            audio.add(TCON(encoding=3, text=genrename))  #the mutagen .add method is used to change a specified ID3 tag; within this method the TCON function is used to change genre name, inputted text is to the right of "text="
                                            audio.save()                                    #mutagen saves changes to tag
                                            temp_track = TinyTag.get(root + "/" + name)
                                            print("\nArtist Name: " + temp_track.artist)        #@@@@@@@@@@@@@@@@@@@
                                            print("Song Title: " + temp_track.title)            #displaying all tags to show what exactly has changed
                                            print("Album Title: " + temp_track.album)
                                            print("Track Number: " + str(temp_track.track))
                                            print("Year Released: " + str(temp_track.year))
                                            print("Song Length: " + str(int((temp_track.duration)//60)) + ':' + str(int(temp_track.duration)%60))
                                            print("Bitrate: " + str(int(temp_track.bitrate)) + " kBits/s")
                                            print("Sample Rate: " + str((temp_track.samplerate)/1000) + " kHz")
                                            print("File Size: " + str(round((temp_track.filesize/1000000), 2)) + ' MB')
                                            print("Genre: " + temp_track.genre)
                                            lookokay = input('\nDoes this look correct to you? (yes/no) ').lower().strip()
                                            if lookokay == 'yes':
                                                main()              #program returns to start if no changes need to be made
                                            if lookokay == 'no':
                                                continue             #while loop returns to beginning if you still need to make a change
                                    if edittag == 'e':
                                        while True:
                                            year = input('\nType in the new year of release: ')
                                            audio = ID3(str(pathway) + str(whichfile))
                                            audio.add(TYER(encoding=3, text=year))  #the mutagen .add method is used to change a specified ID3 tag; within this method the TYER function is used to change year of release, inputted text is to the right of "text="
                                            audio.save()
                                            temp_track = TinyTag.get(root + "/" + name)
                                            print("\nArtist Name: " + temp_track.artist)
                                            print("Song Title: " + temp_track.title)
                                            print("Album Title: " + temp_track.album)
                                            print("Track Number: " + str(temp_track.track))
                                            print("Year Released: " + str(temp_track.year))
                                            print("Song Length: " + str(int((temp_track.duration)//60)) + ':' + str(int(temp_track.duration)%60))
                                            print("Bitrate: " + str(int(temp_track.bitrate)) + " kBits/s")
                                            print("Sample Rate: " + str((temp_track.samplerate)/1000) + " kHz")
                                            print("File Size: " + str(round((temp_track.filesize/1000000), 2)) + ' MB')
                                            print("Genre: " + temp_track.genre)
                                            lookokay = input('\nDoes this look correct to you? (yes/no) ').lower().strip()
                                            if lookokay == 'yes':
                                                main()
                                            if lookokay == 'no':
                                                continue
                                    if edittag == 'd':
                                        while True: 
                                            tracknumber = input('\nType in the new track number: ')    
                                            audio = ID3(str(pathway) + str(whichfile))
                                            audio.add(TRCK(encoding=3, text=tracknumber)) #the mutagen .add method is used to change a specified ID3 tag; within this method the TRCK function is used to change track number, inputted text is to the right of "text="
                                            audio.save()
                                            temp_track = TinyTag.get(root + "/" + name)
                                            print("\nArtist Name: " + temp_track.artist)
                                            print("Song Title: " + temp_track.title)
                                            print("Album Title: " + temp_track.album)
                                            print("Track Number: " + str(temp_track.track))
                                            print("Year Released: " + str(temp_track.year))
                                            print("Song Length: " + str(int((temp_track.duration)//60)) + ':' + str(int(temp_track.duration)%60))
                                            print("Bitrate: " + str(int(temp_track.bitrate)) + " kBits/s")
                                            print("Sample Rate: " + str((temp_track.samplerate)/1000) + " kHz")
                                            print("File Size: " + str(round((temp_track.filesize/1000000), 2)) + ' MB')
                                            print("Genre: " + temp_track.genre)
                                            lookokay = input('\nDoes this look correct to you? (yes/no) ').lower().strip()
                                            if lookokay == 'yes':
                                                main()
                                            if lookokay == 'no':
                                                continue
                                    if edittag == 'c':
                                        while True:
                                            albumname = input('\nType in the new album title: ')
                                            audio = ID3(str(pathway) + str(whichfile))
                                            audio.add(TALB(encoding=3, text=albumname)) #the mutagen .add method is used to change a specified ID3 tag; within this method the TALB function is used to change album name, inputted text is to the right of "text="
                                            audio.save()
                                            temp_track = TinyTag.get(root + "/" + name)
                                            print("\nArtist Name: " + temp_track.artist)
                                            print("Song Title: " + temp_track.title)
                                            print("Album Title: " + temp_track.album)
                                            print("Track Number: " + str(temp_track.track))
                                            print("Year Released: " + str(temp_track.year))
                                            print("Song Length: " + str(int((temp_track.duration)//60)) + ':' + str(int(temp_track.duration)%60))
                                            print("Bitrate: " + str(int(temp_track.bitrate)) + " kBits/s")
                                            print("Sample Rate: " + str((temp_track.samplerate)/1000) + " kHz")
                                            print("File Size: " + str(round((temp_track.filesize/1000000), 2)) + ' MB')
                                            print("Genre: " + temp_track.genre)
                                            lookokay = input('\nDoes this look correct to you? (yes/no) ').lower().strip()
                                            if lookokay == 'yes':
                                                main()
                                            if lookokay == 'no':
                                                continue
                                    if edittag == 'b':
                                        while True:
                                            titlename = input('\nType in the new song title: ')
                                            audio = ID3(str(pathway) + str(whichfile))
                                            audio.add(TIT2(encoding=3, text=titlename)) #the mutagen .add method is used to change a specified ID3 tag; within this method the TIT2 function is used to change song title, inputted text is to the right of "text="
                                            audio.save()
                                            temp_track = TinyTag.get(root + "/" + name)
                                            print("\nArtist Name: " + temp_track.artist)
                                            print("Song Title: " + temp_track.title)
                                            print("Album Title: " + temp_track.album)
                                            print("Track Number: " + str(temp_track.track))
                                            print("Year Released: " + str(temp_track.year))
                                            print("Song Length: " + str(int((temp_track.duration)//60)) + ':' + str(int(temp_track.duration)%60))
                                            print("Bitrate: " + str(int(temp_track.bitrate)) + " kBits/s")
                                            print("Sample Rate: " + str((temp_track.samplerate)/1000) + " kHz")
                                            print("File Size: " + str(round((temp_track.filesize/1000000), 2)) + ' MB')
                                            print("Genre: " + temp_track.genre)
                                            lookokay = input('\nDoes this look correct to you? (yes/no) ').lower().strip()
                                            if lookokay == 'yes':
                                                print('\nReturning to start of program ... \n')
                                                main()
                                            if lookokay == 'no':
                                                continue
                                    if edittag == 'a':
                                        while True:
                                            artistname = input('\nType in the new artist name: ').strip()
                                            audio = ID3(str(pathway) + str(whichfile))
                                            audio.add(TPE1(encoding=3, text=artistname)) #the mutagen .add method is used to change a specified ID3 tag; within this method the TPE1 function is used to change artist name, inputted text is to the right of "text="
                                            audio.save()
                                            temp_track = TinyTag.get(root + "/" + name)
                                            print("\nArtist Name: " + temp_track.artist)
                                            print("Song Title: " + temp_track.title)
                                            print("Album Title: " + temp_track.album)
                                            print("Track Number: " + str(temp_track.track))
                                            print("Year Released: " + str(temp_track.year))
                                            print("Song Length: " + str(int((temp_track.duration)//60)) + ':' + str(int(temp_track.duration)%60))
                                            print("Bitrate: " + str(int(temp_track.bitrate)) + " kBits/s")
                                            print("Sample Rate: " + str((temp_track.samplerate)/1000) + " kHz")
                                            print("File Size: " + str(round((temp_track.filesize/1000000), 2)) + ' MB')
                                            print("Genre: " + temp_track.genre)
                                            lookokay = input('\nDoes this look correct to you? (yes/no) ').lower().strip()
                                            if lookokay == 'yes':
                                                main()
                                            if lookokay == 'no':
                                                continue
                        except TypeError:
                            print('\nERROR!')
                            print('Returning to start of program ...')
                            main()
                        except TinyTagException:
                            print('Invalid entry!')
                            main()
                else:
                    print('\nERROR!')
                    print('\nThere are either:\n\n• no files in the selected pathway, or \n• your pathway or filename entry was invalid or typed incorrectly, or \n• you\'ve entered an invalid option')
                    print('\nReturning to start of program ... \n')
                    main()
        if amountoffiles == 'a':                      #this is the 'if' statement that triggers if you want to look at all files at the end of the pathway
            tracks = []
            for root, dirs, files, in os.walk(pathway):
                for name in files:
                    if name.endswith(('.mp3')):
                        tracks.append(name)
                        try:
                            temp_track = TinyTag.get(root + "/" + name)
                            print("\nArtist Name: " + temp_track.artist)
                            print("Song Title: " + temp_track.title)
                            print("Album Title: " + temp_track.album)
                            print("Track Number: " + str(temp_track.track))
                            print("Year Released: " + str(temp_track.year))
                            print("Song Length: " + str(int((temp_track.duration)//60)) + ':' + str(int(temp_track.duration)%60))
                            print("Bitrate: " + str(int(temp_track.bitrate)) + " kBits/s")
                            print("Sample Rate: " + str((temp_track.samplerate)/1000) + " kHz")
                            print("File Size: " + str(round((temp_track.filesize/1000000), 2)) + ' MB')
                            print("Genre: " + temp_track.genre)
                            print(' ')
                        except TinyTagException:  # this is a TinyTag-related exception that occurs if there's a corrpution in one of the ID3 tags
                            print('Error!\n')
                            main()
                        except TypeError:       # this exception prevents the program from shutting down if there is a 'None' value in one of the tags
                            print('Error!\n')
                            main()
            if tracks == []:            # this statements checks if the "tracks" list is empty; if it is, then the pathway likely leads to no mp3 files
                print('\nERROR!')
                print('\nThere are either:\n\n• no files in the selected pathway, or \n• your pathway entry was invalid')
                print('\nReturning to start of program ... \n')
                main()
            else:
                print('Would you like to: \n(A) choose a specific song to change the tags of? ... or ... ')
                print('(B) view songs based on particular criteria? ... or ...  ')
                print('(C) neither?')
                sortorchange = input('Make a selection: (A/B/C) ').lower().strip()
                if sortorchange == 'b':             #filtering the list of mp3s by a certain criteria
                    print('\nWould you like to choose based on:')
                    print('(A) artist name \n(B) album title \n(C) year released \n(D) song length \n(E) bitrate \n(F) file size \n(G) genre')
                    criteria = input('Make a selection: (A/B/C/D/E/F/G) ').lower().strip()
                    if criteria == 'e': #filtering list based on bitrate
                        try:
                            print('\nWould you like to choose: \n(A) a bitrate range, or ... \n(B) a specific bitrate ...')
                            choosebitrate = input('Make a selection: (A/B) ') 
                            if choosebitrate == 'b': #choosing a specific bitrate to filter to
                                specificbitrate = int(input('Enter a specific bitrate (in kBits/s): '))
                                tracks = []
                                for root, dirs, files, in os.walk(pathway):
                                    for name in files:
                                        if name.endswith(('.mp3')): #searching for file names that only end in .mp3
                                            tracks.append(name)
                                            try:
                                                temp_track = TinyTag.get(root + "/" + name)
                                                if temp_track.bitrate == specificbitrate:    #if statment checks to see if user input bitrate (specificbitrate) matches an ID3 bitrate tag (temp_track.bitrate)
                                                    print("\nArtist Name: " + temp_track.artist)
                                                    print("Song Title: " + temp_track.title)
                                                    print("Album Title: " + temp_track.album)           ##@@@@@@@@@@@@@@@@@@@@
                                                    print("Track Number: " + str(temp_track.track))     #printing out all of the ID3 tags of each file that meets the criteria
                                                    print("Year Released: " + str(temp_track.year))
                                                    print("Song Length: " + str(int((temp_track.duration)//60)) + ':' + str(int(temp_track.duration)%60))
                                                    print("Bitrate: " + str(int(temp_track.bitrate)) + " kBits/s")
                                                    print("Sample Rate: " + str((temp_track.samplerate)/1000) + " kHz")
                                                    print("File Size: " + str(round((temp_track.filesize/1000000), 2)) + ' MB')
                                                    print("Genre: " + temp_track.genre)
                                                    print(' ')
                                            except TinyTagException:
                                                print('Error!\n')
                                                main()
                                            except TypeError:
                                                print('Error!\n')
                                                main()
                        except ValueError:
                            print('\nERROR!')
                            print('\nInvalid entry!')
                            print('\nReturning to start of program ... \n')
                            main()
                        if choosebitrate == 'a':  # if choosing to search between one bitrate and another
                            print('For a bitrate range ... \nenter the lowest and highest bitrate of the range')
                            bitrateone = int(input('Enter lowest bitrate (in kBits/s): '))    #entering lowest bitrate in the range
                            bitratetwo = int(input('Enter highest bitrate (in kBits/s): '))     #entering highest bitrate in the range
                            tracks = []
                            for root, dirs, files, in os.walk(pathway):
                                for name in files:
                                    if name.endswith(('.mp3')):
                                        tracks.append(name)
                                        try:
                                            temp_track = TinyTag.get(root + "/" + name)
                                            if bitrateone <= temp_track.bitrate <= bitratetwo: #using comparison operators to find the range of directory bitrates (temp_track.bitrate) between the inputted bitrates
                                                print("\nArtist Name: " + temp_track.artist)
                                                print("Song Title: " + temp_track.title)
                                                print("Album Title: " + temp_track.album)
                                                print("Track Number: " + str(temp_track.track))
                                                print("Year Released: " + str(temp_track.year))
                                                print("Song Length: " + str(int((temp_track.duration)//60)) + ':' + str(int(temp_track.duration)%60))
                                                print("Bitrate: " + str(int(temp_track.bitrate)) + " kBits/s")
                                                print("Sample Rate: " + str((temp_track.samplerate)/1000) + " kHz")
                                                print("File Size: " + str(round((temp_track.filesize/1000000), 2)) + ' MB')
                                                print("Genre: " + temp_track.genre)
                                                print(' ')
                                        except TinyTagException:
                                            print('Error!\n')
                                            main()
                                        except TypeError:
                                            print('Error!\n')
                                            main()
                            dothings = input('These are all the results that could be found ... \nPress enter to return to the main menu: ').lower().strip()
                            while True:
                                main()
                    if criteria == 'g':     #if choosing to filter directory by genre name
                        typeinagenre = input('\nWhich genre type do you want to display? \n(note: capitalizations matter):').strip()
                        tracks = []
                        for root, dirs, files, in os.walk(pathway):
                            for name in files:
                                if name.endswith(('.mp3')):
                                    tracks.append(name)
                                    try:
                                        temp_track = TinyTag.get(root + "/" + name)
                                        if temp_track.genre == typeinagenre:    #if statement that makes it so directory files are only printed if user input (typeinagenre) matches genre ID3 tag (temp_track.genre)
                                            print("\nArtist Name: " + temp_track.artist)
                                            print("Song Title: " + temp_track.title)
                                            print("Album Title: " + temp_track.album)
                                            print("Track Number: " + str(temp_track.track))
                                            print("Year Released: " + str(temp_track.year))
                                            print("Song Length: " + str(int((temp_track.duration)//60)) + ':' + str(int(temp_track.duration)%60))
                                            print("Bitrate: " + str(int(temp_track.bitrate)) + " kBits/s")
                                            print("Sample Rate: " + str((temp_track.samplerate)/1000) + " kHz")
                                            print("File Size: " + str(round((temp_track.filesize/1000000), 2)) + ' MB')
                                            print("Genre: " + temp_track.genre)
                                            print(' ')
                                    except TinyTagException:
                                        print('Error!\n')
                                        main()
                                    except TypeError:
                                        print('Error!\n')
                                        main()
                        dothings = input('These are all the results that could be found ... \nPress enter to return to the main menu: ').lower().strip()
                        while True:
                            main()
                    if criteria == 'd': #if choosing to filter directory by song length
                        print('\nWould you like to choose: \n(A) a song length range, or ... \n(B) a song length threshold ...') #user prompt to choose a song range, or song length threshold
                        howlength = input('Make a selection: (A/B) ')
                        if howlength == 'b': #if the user wants to choose a song length threshold
                            try:
                                print('For a song length range threshold ... \nenter a song length in terms of minutes, and additional seconds')
                                lengthmin = int(input('Enter minutes: ')) #user inputs minutes of song length
                                lengthmin *= 60                             #multiplying the "minutes" value by 60 because mutagen itself only reads/conveys song length in seconds
                                lengthsec = int(input('Enter seconds: ')) #user inputs additonal seconds of song lengt
                                lengththreshold = lengthmin + lengthsec   #adding "lengthmin" and "lengthsec" variables together to get a song length in seconds, so that mutagen can read inputted song-length accurately
                                print('\nWould you like to only show folder tracks ... \n(A) above the threshold, or ... \n(B) below the threshold ...')
                                abovebelow = input('Make a selection: (A/B) ') #selection whether user wants to filter song lengths longer inputted song length, or shorter
                                if abovebelow == 'b':   #if user wants to see song lengths below inputted song length
                                    tracks = []
                                    for root, dirs, files, in os.walk(pathway):
                                        for name in files:
                                            if name.endswith(('.mp3')):
                                                tracks.append(name)
                                                try:
                                                    temp_track = TinyTag.get(root + "/" + name)
                                                    if temp_track.duration <= lengththreshold:  #if statment that uses equal-to-or-less-than operator to filter mp3 files with song lengths under threshold
                                                        print("\nArtist Name: " + temp_track.artist)
                                                        print("Song Title: " + temp_track.title)
                                                        print("Album Title: " + temp_track.album)
                                                        print("Track Number: " + str(temp_track.track))
                                                        print("Year Released: " + str(temp_track.year))
                                                        print("Song Length: " + str(int((temp_track.duration)//60)) + ':' + str(int(temp_track.duration)%60))
                                                        print("Bitrate: " + str(int(temp_track.bitrate)) + " kBits/s")
                                                        print("Sample Rate: " + str((temp_track.samplerate)/1000) + " kHz")
                                                        print("File Size: " + str(round((temp_track.filesize/1000000), 2)) + ' MB')
                                                        print("Genre: " + temp_track.genre)
                                                        print(' ')
                                                except TinyTagException:
                                                    print('Error!\n')
                                                    main()
                                                except TypeError:
                                                    print('Error!\n')
                                                    dothings = input('These are all the results that could be found ... \nPress enter to return to the main menu: ').lower().strip()
                                                    while True:
                                                        main()
                            except ValueError:
                                print('\nERROR!')
                                print('\nInvalid entry!')
                                print('\nReturning to start of program ... \n')
                                main()
                            if abovebelow == 'a':  #if user wants to see song lengths above inputted song length
                                tracks = []
                                for root, dirs, files, in os.walk(pathway):
                                    for name in files:
                                        if name.endswith(('.mp3')):
                                            tracks.append(name)
                                            try:
                                                temp_track = TinyTag.get(root + "/" + name)
                                                if lengththreshold <= temp_track.duration: #if statement that uses equal-to-or-less-than operator to filter mp3 files with song lengths above threshold
                                                    print("\nArtist Name: " + temp_track.artist)
                                                    print("Song Title: " + temp_track.title)
                                                    print("Album Title: " + temp_track.album)
                                                    print("Track Number: " + str(temp_track.track))
                                                    print("Year Released: " + str(temp_track.year))
                                                    print("Song Length: " + str(int((temp_track.duration)//60)) + ':' + str(int(temp_track.duration)%60))
                                                    print("Bitrate: " + str(int(temp_track.bitrate)) + " kBits/s")
                                                    print("Sample Rate: " + str((temp_track.samplerate)/1000) + " kHz")
                                                    print("File Size: " + str(round((temp_track.filesize/1000000), 2)) + ' MB')
                                                    print("Genre: " + temp_track.genre)
                                                    print(' ')
                                            except TinyTagException:
                                                print('Error!\n')
                                                main()
                                            except TypeError:
                                                print('Error!\n')
                                                main()
                            dothings = input('These are all the results that could be found ... \nPress enter to return to the main menu: ').lower().strip()
                            while True:
                                main() 
                        if howlength == 'a': #if user wants to create a song length range to filter songs by
                            try:
                                print('For song length range, enter shortest song length in terms \nof how many minutes, and additional seconds, it is:')
                                lengthonemin = int(input('Enter minutes: '))    #creating shortest song length
                                lengthonemin *= 60
                                lengthonesec = int(input('Enter seconds: '))
                                lengthone = lengthonemin + lengthonesec
                                print('For song length range, enter longest song length in terms \nof how many minutes, and additional seconds, it is:')
                                lengthtwomin = int(input('Enter minutes: '))    #creating longest song length
                                lengthtwomin *= 60
                                lengthtwosec = int(input('Enter seconds: '))
                                lengthtwo = lengthtwomin + lengthtwosec
                                tracks = []
                                for root, dirs, files, in os.walk(pathway):
                                    for name in files:
                                        if name.endswith(('.mp3')):
                                            tracks.append(name)
                                            try:
                                                temp_track = TinyTag.get(root + "/" + name)
                                                if lengthone <= temp_track.duration <= lengthtwo: #using comparisons operators in an "if" statement to only show song lengths in between the two inputted song lengths
                                                    print("\nArtist Name: " + temp_track.artist)
                                                    print("Song Title: " + temp_track.title)
                                                    print("Album Title: " + temp_track.album)
                                                    print("Track Number: " + str(temp_track.track))
                                                    print("Year Released: " + str(temp_track.year))
                                                    print("Song Length: " + str(int((temp_track.duration)//60)) + ':' + str(int(temp_track.duration)%60))
                                                    print("Bitrate: " + str(int(temp_track.bitrate)) + " kBits/s")
                                                    print("Sample Rate: " + str((temp_track.samplerate)/1000) + " kHz")
                                                    print("File Size: " + str(round((temp_track.filesize/1000000), 2)) + ' MB')
                                                    print("Genre: " + temp_track.genre)
                                                    print(' ')
                                            except TinyTagException:
                                                print('Error!\n')
                                                main()
                                            except TypeError:
                                                print('Error!\n')
                                                main()
                            except ValueError:
                                print('\nERROR!')
                                print('\nInvalid entry!')
                                print('\nReturning to start of program ... \n')
                                main()                 
                            dothings = input('These are all the results that could be found ... \nPress enter to return to the main menu: ').lower().strip()
                            while True:
                                main()
                    if criteria == 'c': #if user wants to filter mp3s in directory by year
                        print('\nWould you like to choose: \n(A) a specific year, or ... \n(B) a range of years ... ')
                        howyear = input('Make a selection: (A/B) ') #choosing to filter by a specific year, or range of years
                        if howyear == 'b': #choosing to filter mp3 directory by range of years
                            yearone = input('\nType in the first year of the range: ').strip()    #inputting range of years here, and in line below
                            yeartwo = input('\nType in the second year of the range: ').strip()
                            tracks = []
                            for root, dirs, files, in os.walk(pathway):
                                for name in files:
                                    if name.endswith(('.mp3')):
                                        tracks.append(name)
                                        try:
                                            temp_track = TinyTag.get(root + "/" + name)
                                            if yearone <= temp_track.year <= yeartwo:   #using comparisons operators in an "if" statement to only show release years in between the two inputted years
                                                print("\nArtist Name: " + temp_track.artist)
                                                print("Song Title: " + temp_track.title)
                                                print("Album Title: " + temp_track.album)
                                                print("Track Number: " + str(temp_track.track))
                                                print("Year Released: " + str(temp_track.year))
                                                print("Song Length: " + str(int((temp_track.duration)//60)) + ':' + str(int(temp_track.duration)%60))
                                                print("Bitrate: " + str(int(temp_track.bitrate)) + " kBits/s")
                                                print("Sample Rate: " + str((temp_track.samplerate)/1000) + " kHz")
                                                print("File Size: " + str(round((temp_track.filesize/1000000), 2)) + ' MB')
                                                print("Genre: " + temp_track.genre)
                                                print(' ')
                                        except TinyTagException:
                                            print('Error!\n')
                                            main()
                                        except TypeError:
                                            print('Error!\n')
                                            main()
                            dothings = input('These are all the results that could be found ... \nPress enter to return to the main menu: ').lower().strip()
                            while True:
                                main()
                        if howyear == 'a': #choosing to filter mp3 directory by a specific release year 
                            exactyear = input('\nWhich release year do you want appearing? ').strip() #typing in exact year that user wants the filter by
                            tracks = []
                            for root, dirs, files, in os.walk(pathway):
                                for name in files:
                                    if name.endswith(('.mp3')):
                                        tracks.append(name)
                                        try:
                                            temp_track = TinyTag.get(root + "/" + name)
                                            if temp_track.year == exactyear: #only prints out complete tags for release year ID3 tags (temp_track.year) that matches user input (exactyear)
                                                print("\nArtist Name: " + temp_track.artist)
                                                print("Song Title: " + temp_track.title)
                                                print("Album Title: " + temp_track.album)
                                                print("Track Number: " + str(temp_track.track))
                                                print("Year Released: " + str(temp_track.year))
                                                print("Song Length: " + str(int((temp_track.duration)//60)) + ':' + str(int(temp_track.duration)%60))
                                                print("Bitrate: " + str(int(temp_track.bitrate)) + " kBits/s")
                                                print("Sample Rate: " + str((temp_track.samplerate)/1000) + " kHz")
                                                print("File Size: " + str(round((temp_track.filesize/1000000), 2)) + ' MB')
                                                print("Genre: " + temp_track.genre)
                                                print(' ')
                                        except TinyTagException:
                                            print('Error!\n')
                                            main()
                                        except TypeError:
                                            print('Error!\n')
                                            main()
                            dothings = input('These are all the results that could be found ... \nPress enter to return to the main menu: ').lower().strip()
                            while True:
                                main()
                    if criteria == 'b': #choosing to filter mp3 directory by album title 
                        whichalbum = input('\nWhich album title do you want appearing? \n(note: capitalizations matter): ').strip()
                        tracks = []
                        for root, dirs, files, in os.walk(pathway):
                            for name in files:
                                if name.endswith(('.mp3')):
                                    tracks.append(name)
                                    try:
                                        temp_track = TinyTag.get(root + "/" + name)
                                        if temp_track.album == whichalbum: #only prints out complete tags for album title ID3 tags (temp_track.album) that matches user input (whichalbum)
                                            print("\nArtist Name: " + temp_track.artist)
                                            print("Song Title: " + temp_track.title)
                                            print("Album Title: " + temp_track.album)
                                            print("Track Number: " + str(temp_track.track))
                                            print("Year Released: " + str(temp_track.year))
                                            print("Song Length: " + str(int((temp_track.duration)//60)) + ':' + str(int(temp_track.duration)%60))
                                            print("Bitrate: " + str(int(temp_track.bitrate)) + " kBits/s")
                                            print("Sample Rate: " + str((temp_track.samplerate)/1000) + " kHz")
                                            print("File Size: " + str(round((temp_track.filesize/1000000), 2)) + ' MB')
                                            print("Genre: " + temp_track.genre)
                                            print(' ')
                                    except TinyTagException:
                                        print('Error!\n')
                                        main()
                                    except TypeError:
                                        print('Error!\n')
                                        main()
                        dothings = input('These are all the results that could be found ... \nPress enter to return to the main menu: ').lower().strip()
                        while True:
                            main()
                    if criteria == 'a': #if user wants to filter mp3 directory based on artist name
                        whichartist = input('\nWhich artist name do you want appearing? \n(note: capitalizations matter): ').strip()
                        tracks = []
                        for root, dirs, files, in os.walk(pathway):
                            for name in files:
                                if name.endswith(('.mp3')):
                                    tracks.append(name)
                                    try:
                                        temp_track = TinyTag.get(root + "/" + name)
                                        if temp_track.artist == whichartist:  #prints out entire ID3 tags of the mp3 files that have artist names (temp_track.artist) that equal their input (whichartist)
                                            print("\nArtist Name: " + temp_track.artist)
                                            print("Song Title: " + temp_track.title)
                                            print("Album Title: " + temp_track.album)
                                            print("Track Number: " + str(temp_track.track))
                                            print("Year Released: " + str(temp_track.year))
                                            print("Song Length: " + str(int((temp_track.duration)//60)) + ':' + str(int(temp_track.duration)%60))
                                            print("Bitrate: " + str(int(temp_track.bitrate)) + " kBits/s")
                                            print("Sample Rate: " + str((temp_track.samplerate)/1000) + " kHz")
                                            print("File Size: " + str(round((temp_track.filesize/1000000), 2)) + ' MB')
                                            print("Genre: " + temp_track.genre)
                                            print(' ')
                                    except TinyTagException:
                                        print('Error!\n')
                                        main()
                                    except TypeError:
                                        print('Error!\n')
                                        main()
                        dothings = input('These are all the results that could be found ... \nPress enter to return to the main menu: ').lower().strip()
                        while True:
                            main()
                    if criteria == 'f': # if user wants to filter mp3 directory based on  file size, in megabytes
                        try:
                            print('\nWould you like a choose ... \n(A) a file size as a threshold, or ... \n(B) a file size range ...')
                            filechoose = input('Make a selection: (A/B) ').lower().strip() #user chooses whether to filter with a file size threshold, or a file size range
                            if filechoose == 'a':
                                thesize = input('\nWhat is the file size threshold that you want appearing, in MB? (note: decimal places are okay!) ') 
                                filesizer = float(thesize)*1000000 #multipling user input by "1000000" because mutagen only reads/edits file size tags in bytes; thus need to convert MB to bytes
                                aboveorbelow = input('Would you like to display files that are ... \n(A) above the threshold, or ... \n(B) below the threshold ...\n')
                                if aboveorbelow == 'a': #if user chooses to view only file sizes above the inputted threshold
                                    tracks = []
                                    for root, dirs, files, in os.walk(pathway):
                                        for name in files:
                                            if name.endswith(('.mp3')):
                                                tracks.append(name)
                                                try:
                                                    temp_track = TinyTag.get(root + "/" + name)
                                                    if temp_track.filesize >= float(filesizer): #if statement makes it so that we only see files sizes that are greater-than-or-equal to the inputted file size
                                                        print("\nArtist Name: " + temp_track.artist)
                                                        print("Song Title: " + temp_track.title)
                                                        print("Album Title: " + temp_track.album)
                                                        print("Track Number: " + str(temp_track.track))
                                                        print("Year Released: " + str(temp_track.year))
                                                        print("Song Length: " + str(int((temp_track.duration)//60)) + ':' + str(int(temp_track.duration)%60))
                                                        print("Bitrate: " + str(int(temp_track.bitrate)) + " kBits/s")
                                                        print("Sample Rate: " + str((temp_track.samplerate)/1000) + " kHz")
                                                        print("File Size: " + str(round((temp_track.filesize/1000000), 2)) + ' MB')
                                                        print("Genre: " + temp_track.genre)
                                                        print(' ')
                                                except TinyTagException:
                                                    print('Error!\n')
                                                    main()
                                                except TypeError:
                                                    print('Error!\n')
                                                    main()
                                    dothings = input('These are all the results that could be found ... \nPress enter to return to the main menu: ').lower().strip()
                                    while True:
                                        main()                        
                                if aboveorbelow == 'b': #if user chooses to view only file sizes below the inputted threshold
                                    tracks = []
                                    for root, dirs, files, in os.walk(pathway):
                                        for name in files:
                                            if name.endswith(('.mp3')):
                                                tracks.append(name)
                                                try:
                                                    temp_track = TinyTag.get(root + "/" + name)
                                                    if temp_track.filesize <= float(filesizer): #if statement makes it so that we only see files sizes that are less-than-or-equal to the inputted file size
                                                        print("\nArtist Name: " + temp_track.artist)
                                                        print("Song Title: " + temp_track.title)
                                                        print("Album Title: " + temp_track.album)
                                                        print("Track Number: " + str(temp_track.track))
                                                        print("Year Released: " + str(temp_track.year))
                                                        print("Song Length: " + str(int((temp_track.duration)//60)) + ':' + str(int(temp_track.duration)%60))
                                                        print("Bitrate: " + str(int(temp_track.bitrate)) + " kBits/s")
                                                        print("Sample Rate: " + str((temp_track.samplerate)/1000) + " kHz")
                                                        print("File Size: " + str(round((temp_track.filesize/1000000), 2)) + ' MB')
                                                        print("Genre: " + temp_track.genre)
                                                        print(' ')
                                                except TinyTagException:
                                                    print('Error!\n')
                                                    main()
                                                except TypeError:
                                                    print('Error!\n')
                                                    main()
                                    dothings = input('These are all the results that could be found ... \nPress enter to return to the main menu: ').lower().strip()
                                    while True:
                                        main()  
                                else:
                                    print('\nERROR!')
                                    print('\nInvalid entry!')
                                    print('\nReturning to start of program ... \n')
                                    main()
                            if filechoose == 'b': #if user wants to filter mp3 directory to show a particular range of file sizes
                                print('For a file size range ... \nenter the lowest and highest filesize of the range (in MB)')
                                filesizeone = int(input('Enter lowest file size (in MB): ')) #entering lowest file size in range
                                megabyteone = float(filesizeone)*1000000        #converting MB to bytes
                                filesizetwo = int(input('Enter highest file size (in MB): ')) #entering highest file size in range
                                megabytetwo = float(filesizetwo)*1000000        #converting MB to bytes
                                tracks = []
                                for root, dirs, files, in os.walk(pathway):
                                    for name in files:
                                        if name.endswith(('.mp3')):
                                            tracks.append(name)
                                            try:
                                                temp_track = TinyTag.get(root + "/" + name)
                                                if megabyteone <= temp_track.filesize <= megabytetwo: #using comparison operators in "if" statement to only show file sizes in the inputted range
                                                    print("\nArtist Name: " + temp_track.artist)
                                                    print("Song Title: " + temp_track.title)
                                                    print("Album Title: " + temp_track.album)
                                                    print("Track Number: " + str(temp_track.track))
                                                    print("Year Released: " + str(temp_track.year))
                                                    print("Song Length: " + str(int((temp_track.duration)//60)) + ':' + str(int(temp_track.duration)%60))
                                                    print("Bitrate: " + str(int(temp_track.bitrate)) + " kBits/s")
                                                    print("Sample Rate: " + str((temp_track.samplerate)/1000) + " kHz")
                                                    print("File Size: " + str(round((temp_track.filesize/1000000), 2)) + ' MB')
                                                    print("Genre: " + temp_track.genre)
                                                    print(' ')
                                            except TinyTagException:
                                                print('Error!\n')
                                                main()
                                            except TypeError:
                                                print('Error!\n')
                                                main()
                                dothings = input('These are all the results that could be found ... \nPress enter to return to the main menu: ').lower().strip()
                                while True:
                                    main()
                            else:
                                print('\nReturning to start of program ... \n')
                                main()
                        except ValueError:
                            print('\nERROR!')
                            print('\nInvalid entry!')
                            print('\nReturning to start of program ... \n')
                            main()
                if sortorchange == 'a': #if user wants to look at an exact file after looking through all of them in the directory
                    exactfile = input('\nType in the exact name of the file that you want to view: ').strip()
                    if exactfile.startswith('/'):               #removes forward slash from file name if user inputs it, because there is already a forward slash in the pathway to the directory
                        exactfile = exactfile.replace('/', '')   #removing with .replace() method
                    tracks = []
                    for root, dirs, files, in os.walk(pathway):
                        for name in files:
                            if name.endswith((exactfile)): #only finds the file pathway that ends with what the user has typed in
                                tracks.append(name)
                                try:
                                    temp_track = TinyTag.get(root + "/" + name)
                                    print("\nArtist Name: " + temp_track.artist)
                                    print("Song Title: " + temp_track.title)
                                    print("Album Title: " + temp_track.album)
                                    print("Track Number: " + str(temp_track.track))
                                    print("Year Released: " + str(temp_track.year))
                                    print("Song Length: " + str(int((temp_track.duration)//60)) + ':' + str(int(temp_track.duration)%60))
                                    print("Bitrate: " + str(int(temp_track.bitrate)) + " kBits/s")
                                    print("Sample Rate: " + str((temp_track.samplerate)/1000) + " kHz")
                                    print("File Size: " + str(round((temp_track.filesize/1000000), 2)) + ' MB')
                                    print("Genre: " + temp_track.genre)
                                    print(' ')
                                    print('\nWhat would you like to change?')
                                    print('\n(A) Artist Name \n(B) Song Title \n(C) Album Title')
                                    print('(D) Track Number \n(E) Year Released \n(F) Genre Name')
                                    print(' ')
                                    edittag = input('\nEnter a selection: (A/B/C/D/E/F) ').lower().strip()
                                    if edittag == 'f':  #if user wants to change the genre name for a specific file
                                        while True:
                                            print('\nType in the new genre name ...')
                                            genrename = input('Note: user input will convert to all lower-case \nto bypass pre-set ID3 genre tags and retain \nuser input: ').lower().strip() #genre name is put to lower-case because if genre name is capitalized then it conforms to ID3 naming protocol; lower case makes it so you can have any genre name you want
                                            audio = ID3(str(pathway) + str(exactfile))
                                            audio.add(TCON(encoding=3, text=genrename))
                                            audio.save()
                                            temp_track = TinyTag.get(root + "/" + name)
                                            print("\nArtist Name: " + temp_track.artist)
                                            print("Song Title: " + temp_track.title)
                                            print("Album Title: " + temp_track.album)
                                            print("Track Number: " + str(temp_track.track))
                                            print("Year Released: " + str(temp_track.year))
                                            print("Song Length: " + str(int((temp_track.duration)//60)) + ':' + str(int(temp_track.duration)%60))
                                            print("Bitrate: " + str(int(temp_track.bitrate)) + " kBits/s")
                                            print("Sample Rate: " + str((temp_track.samplerate)/1000) + " kHz")
                                            print("File Size: " + str(round((temp_track.filesize/1000000), 2)) + ' MB')
                                            print("Genre: " + temp_track.genre)
                                            lookokay = input('\nDoes this look correct to you? (yes/no) ').lower().strip()
                                            if lookokay == 'yes':
                                                exactfile = ''
                                                main()
                                            if lookokay == 'no':
                                                continue
                                    if edittag == 'e': #if user wants to change the release year for a specific file
                                        while True:
                                            year = input('\nType in the new year of release: ')
                                            audio = ID3(str(pathway) + str(exactfile))
                                            audio.add(TYER(encoding=3, text=year))
                                            audio.save()
                                            temp_track = TinyTag.get(root + "/" + name)
                                            print("\nArtist Name: " + temp_track.artist)
                                            print("Song Title: " + temp_track.title)
                                            print("Album Title: " + temp_track.album)
                                            print("Track Number: " + str(temp_track.track))
                                            print("Year Released: " + str(temp_track.year))
                                            print("Song Length: " + str(int((temp_track.duration)//60)) + ':' + str(int(temp_track.duration)%60))
                                            print("Bitrate: " + str(int(temp_track.bitrate)) + " kBits/s")
                                            print("Sample Rate: " + str((temp_track.samplerate)/1000) + " kHz")
                                            print("File Size: " + str(round((temp_track.filesize/1000000), 2)) + ' MB')
                                            print("Genre: " + temp_track.genre)
                                            lookokay = input('\nDoes this look correct to you? (yes/no) ').lower().strip()
                                            if lookokay == 'yes':
                                                main()
                                            if lookokay == 'no':
                                                continue
                                    if edittag == 'd': #if user wants to change the track number for a specific file
                                        while True:
                                            tracknumber = input('\nType in the new track number: ')
                                            audio = ID3(str(pathway) + str(exactfile))
                                            audio.add(TRCK(encoding=3, text=tracknumber))
                                            audio.save()
                                            temp_track = TinyTag.get(root + "/" + name)
                                            print("\nArtist Name: " + temp_track.artist)
                                            print("Song Title: " + temp_track.title)
                                            print("Album Title: " + temp_track.album)
                                            print("Track Number: " + str(temp_track.track))
                                            print("Year Released: " + str(temp_track.year))
                                            print("Song Length: " + str(int((temp_track.duration)//60)) + ':' + str(int(temp_track.duration)%60))
                                            print("Bitrate: " + str(int(temp_track.bitrate)) + " kBits/s")
                                            print("Sample Rate: " + str((temp_track.samplerate)/1000) + " kHz")
                                            print("File Size: " + str(round((temp_track.filesize/1000000), 2)) + ' MB')
                                            print("Genre: " + temp_track.genre)
                                            lookokay = input('\nDoes this look correct to you? (yes/no) ').lower().strip()
                                            if lookokay == 'yes':
                                                main()
                                            if lookokay == 'no':
                                                continue
                                    if edittag == 'c': #if user wants to change the album name for a specific file
                                        while True:
                                            albumname = input('\nType in the new album title: ')
                                            audio = ID3(str(pathway) + str(exactfile))
                                            audio.add(TALB(encoding=3, text=albumname))
                                            audio.save()
                                            temp_track = TinyTag.get(root + "/" + name)
                                            print("\nArtist Name: " + temp_track.artist)
                                            print("Song Title: " + temp_track.title)
                                            print("Album Title: " + temp_track.album)
                                            print("Track Number: " + str(temp_track.track))
                                            print("Year Released: " + str(temp_track.year))
                                            print("Song Length: " + str(int((temp_track.duration)//60)) + ':' + str(int(temp_track.duration)%60))
                                            print("Bitrate: " + str(int(temp_track.bitrate)) + " kBits/s")
                                            print("Sample Rate: " + str((temp_track.samplerate)/1000) + " kHz")
                                            print("File Size: " + str(round((temp_track.filesize/1000000), 2)) + ' MB')
                                            print("Genre: " + temp_track.genre)
                                            lookokay = input('\nDoes this look correct to you? (yes/no) ').lower().strip()
                                            if lookokay == 'yes':
                                                main()
                                            if lookokay == 'no':
                                                continue
                                    if edittag == 'b': #if user wants to change the song title for a specific file
                                        while True:
                                            titlename = input('\nType in the new song title: ')
                                            audio = ID3(str(pathway) + str(exactfile))
                                            audio.add(TIT2(encoding=3, text=titlename))
                                            audio.save()
                                            temp_track = TinyTag.get(root + "/" + name)
                                            print("\nArtist Name: " + temp_track.artist)
                                            print("Song Title: " + temp_track.title)
                                            print("Album Title: " + temp_track.album)
                                            print("Track Number: " + str(temp_track.track))
                                            print("Year Released: " + str(temp_track.year))
                                            print("Song Length: " + str(int((temp_track.duration)//60)) + ':' + str(int(temp_track.duration)%60))
                                            print("Bitrate: " + str(int(temp_track.bitrate)) + " kBits/s")
                                            print("Sample Rate: " + str((temp_track.samplerate)/1000) + " kHz")
                                            print("File Size: " + str(round((temp_track.filesize/1000000), 2)) + ' MB')
                                            print("Genre: " + temp_track.genre)
                                            lookokay = input('\nDoes this look correct to you? (yes/no) ').lower().strip()
                                            if lookokay == 'yes':
                                                print('\nReturning to start of program ... \n')
                                                main()
                                            if lookokay == 'no':
                                                continue
                                    if edittag == 'a': #if user wants to change the artist name for a specific file
                                        while True:
                                            artistname = input('\nType in the new artist name: ')
                                            audio = ID3(str(pathway) + str(exactfile))
                                            audio.add(TPE1(encoding=3, text=artistname))
                                            audio.save()
                                            temp_track = TinyTag.get(root + "/" + name)
                                            print("\nArtist Name: " + temp_track.artist)
                                            print("Song Title: " + temp_track.title)
                                            print("Album Title: " + temp_track.album)
                                            print("Track Number: " + str(temp_track.track))
                                            print("Year Released: " + str(temp_track.year))
                                            print("Song Length: " + str(int((temp_track.duration)//60)) + ':' + str(int(temp_track.duration)%60))
                                            print("Bitrate: " + str(int(temp_track.bitrate)) + " kBits/s")
                                            print("Sample Rate: " + str((temp_track.samplerate)/1000) + " kHz")
                                            print("File Size: " + str(round((temp_track.filesize/1000000), 2)) + ' MB')
                                            print("Genre: " + temp_track.genre)
                                            lookokay = input('\nDoes this look correct to you? (yes/no) ').lower().strip()
                                            if lookokay == 'yes':
                                                main()
                                            if lookokay == 'no':
                                                continue
                                    else:
                                        print('\nReturning to start of program ... \n')
                                        main()
                                except TinyTagException:
                                    print('Error!\n')
                                    main()
                                except TypeError:
                                    print('Error!\n')
                                    main()
                        else:
                            print('\nERROR!')
                            print('\nThere are either:\n\n• no files in the selected pathway, or \n• your pathway or filename entry was invalid or typed incorrectly')
                            print('\nReturning to start of program ... \n')
                            main()
                else:
                    print('\nReturning to start of program ... \n')
                    main()
        else:
            print('\nReturning to start of program ... \n')
            main() 
                                                                                 
main()                                       
