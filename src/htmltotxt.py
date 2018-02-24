from math import floor
import sys
import os
from shutil import rmtree

# https://github.com/LuminosoInsight/python-ftfy
import ftfy

# https://www.crummy.com/software/BeautifulSoup/bs4/doc/
from bs4 import BeautifulSoup

PROCESSED_PATH = "htmltotxt_converted/"

htmlDirectory = ""

if len(sys.argv) < 2:
	htmlDirectory = input("Please name the folder where your HTML files are. : ")
else:
	htmlDirectory = sys.argv[1]

if not htmlDirectory.endswith("/"):
	htmlDirectory +="/"

if os.path.exists(PROCESSED_PATH):
	userInput = ""
	while userInput != "Y" and userInput != "N":
		userInput = input("WARNING: need to replace directory '{}'. ALL EXISTING CONTENTS WILL BE DELETED. Enter 'Y' to confirm. Otherwise 'N'. : ".format(PROCESSED_PATH.lower())).upper()
	
	if userInput == "Y":
		rmtree(PROCESSED_PATH)
		print("Deleted. Continuing...")
	else:
		print("Cannot continue.")
		exit()
os.makedirs(PROCESSED_PATH)

def listHtmlFiles(sourcePath):
	return [name for name in os.listdir(sourcePath) if os.path.isfile(sourcePath + name) and name.lower().endswith((".html", ".htm"))]

def listDirectories(sourcePath):
	return [name for name in os.listdir(sourcePath) if os.path.isdir(sourcePath + name)]

nFilesToProcess = 0
nFilesProcessed = 0

def countHtmlFilesWithin(sourcePath):
	global nFilesToProcess
	nFilesToProcess += len(listHtmlFiles(sourcePath))
	for name in listDirectories(sourcePath):
		countHtmlFilesWithin(f"{sourcePath}{name}"+ "/")

countHtmlFilesWithin(htmlDirectory)

# from https://github.com/DanielJohnBenton/TownsAndVillages/blob/master/src/discover.py
def progressBar(completed, all, n):
	bars = floor((n / all) * completed)
	out = "\r["
	for i in range(bars):
		out +="|"
	for i in range(bars + 1, n):
		out +="-"
	out += "] "+ str(completed)
	sys.stdout.write(out)

newlineTags = ("br", "p", "div", "hr", "ol", "ul", "li", "table", "tr", "h1", "h2", "h3", "h4", "h5", "h6")

def convertFiles(sourcePath, targetPath):
	global nFilesProcessed
	files = listHtmlFiles(sourcePath)
	directories = listDirectories(sourcePath)
	for name in files:
		contents = ""
		with open(sourcePath + name, "r", encoding="latin-1") as sourceFile:
			contents = ftfy.fix_text(sourceFile.read())
		
		contents = contents.replace("\r\n", " ").replace("\n", " ").replace("\r", " ")
		for tag in newlineTags:
			contents = contents.replace(f"<{tag}", f"\n<{tag}").replace(f"<{tag.upper()}", f"\n<{tag.upper()}")
			contents = contents.replace(f"</{tag}>", f"</{tag}> ").replace(f"</{tag.upper()}>", f"</{tag.upper()}> ")
		
		with open(targetPath + name +".txt", "w", encoding="utf-8") as targetFile:
			soup = BeautifulSoup(contents, "html5lib")
			[scriptTag.extract() for scriptTag in soup("script")]
			text = ftfy.fix_text(soup.body.get_text())
			targetFile.write(text)
		
		nFilesProcessed += 1
		progressBar(nFilesProcessed, nFilesToProcess, 100)
	
	for name in directories:
		os.makedirs(targetPath + name)
		convertFiles(sourcePath + name +"/", targetPath + name +"/")

print("Converting files...")
convertFiles(htmlDirectory, PROCESSED_PATH)

print("")
print("Done.")