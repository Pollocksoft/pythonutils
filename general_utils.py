#!/usr/bin/env python

import os

newdir = "."

def addSub(newdir = "."):
    for root, dirs, files in os.walk(newdir):
        print "Root: " + root
        for file in files:
            print "Processing: " + file + ", ext:" + os.path.splitext(file)[1]
            if os.path.splitext(file)[1] == '.mkv' or os.path.splitext(file)[1] == '.mp4':
                print 'Current file: ' + file
                subfile = os.path.splitext(file)[0] + '.srt'
                print 'Sub: ' + subfile
                subas = os.path.splitext(file)[0] + '.ass'
                outfile = os.path.splitext(file)[0] + '.m4v'
                if os.path.isfile(subfile):
                    print "Subtitle exists"
                    if os.path.isfile(subas):
                        print ".ass exists"
                    else:
                        print "Createing .ass file"
                        os.system("ffmpeg -i '" + subfile + "' '" + subas + "'")
                    print "######################################################"
                    print "######### FFMPEG ENCODING ############################"
                    print "######################################################"
                    command = "ffmpeg -i '" + file + "' -i '" + subas + "' "
                    command = command + " -y -map 0:0 -map 0:1 -map 1:0 -c:v copy "
                    command = command + "-c:a:0 aac -metadata:s:a:0 language=eng -b:a:0 160k -ac:a:0 2 -strict -2 "
                    command = command + "-c:s mov_text "
                    command = command + "-metadata:s:s:0 language=kor "
                    command = command + "-pix_fmt yuv420p '" + outfile + "' "
                    print command
                    os.system(command)
                else:
                    print "No subtitle - exit"
            else:
                print "Not mkv or mp4"
