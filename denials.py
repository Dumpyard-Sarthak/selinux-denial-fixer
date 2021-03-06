# Copyright (C) 2019 baalajimaestro
# Copyright (C) 2020-2021 Giovix92

import re
import os
import sys, getopt
import shutil

version = "v1.1"
wfixes = []
namefile = ""
inputfile = "denials.txt"

print("Giovix92's SELinux denial fixer,", version)

if not os.path.exists("sepolicy"):
    os.makedirs("sepolicy")
else:
    shutil.rmtree("sepolicy")
    os.makedirs("sepolicy")

if os.path.exists("denials.txt"):
    os.remove("denials.txt")

for i in range(1, len(sys.argv)):
    # Verbose
    if sys.argv[i] == "-v" or sys.argv[i] == "--verbose":
        write = True
        namefile = "verbose"
        print("Verbose mode enabled!")
        print("Outputting every denial into its respective file.")
    # Logcat
    elif sys.argv[i] == "-l" or sys.argv[i] == "--logcat":
        print("Parsing denials from logcat!")
        try:
            if not "-" in sys.argv[i+1]:
    	        logname = sys.argv[i+1]
    	        print("Using custom logcat!")
            else:
                sys.exit()
        except:
    	    logname = "logcat.txt"
        if not os.path.isfile(logname):
            print("logcat is missing! Exiting.")
            sys.exit()
        os.system('cat %s | grep "avc: denied" > denials.txt' % logname)
    # Help part
    elif sys.argv[i] == "-h" or sys.argv[i] == "--help":
    	print("Usage: denials.py [-v] [-l logcat_name]")
    	sys.exit()

if namefile == "":
    namefile = "sepolicy/fixes.txt"
    write = False

if not os.path.isfile(inputfile):
	print("denials file is missing! Exiting.")
	sys.exit()

with open(inputfile) as denfile:
    data=denfile.read()
data=data.split("\n")
data.remove(data[-1])

# Parsin' 'n yeetin' the data
for i in data:
    test=re.search("{",i)
    test2=re.search("}",i)
    se_context=i[test.span()[0]:test2.span()[0]+1]
    test=re.search("scontext",i)
    scontext=i[(test.span()[0]):].split(":")[2]
    test=re.search("tcontext",i)
    tcontext=i[(test.span()[0]):].split(":")[2]
    test=re.search("tclass",i)
    tclass=i[(test.span()[0]):].split("=")[1].split(" ")[0]
    fix="allow "
    fix+=scontext
    fix+=" "
    if scontext == tcontext:
        tcontext="self"
    fix+=tcontext
    fix+=":"
    fix+=tclass
    fix+=" "
    fix+=se_context
    fix+=";"
    fix+="\n"
    wfixes.append(fix)
    if write:
        namefile="sepolicy/" + scontext + ".te"
    if not os.path.exists(namefile):
        os.mknod(namefile)
    with open (namefile, "a+") as ffnew:
        for line in wfixes:
            if line.strip("\n") == fix.strip("\n"):
                pass
        else:
            ffnew.write(fix)
