from urllib.request import urlopen
from bs4 import BeautifulSoup as BS
import util
import git
import re
import time

ALGO_RESULT_URL = "https://algospot.com/judge/submission/recent/"

def getBSObject(userId):
	html = urlopen(ALGO_RESULT_URL+ "?user="+userId+"&state=6")
	bsObject = BS(html, "html.parser")
	
	return bsObject

def getBSObject(userId, page):
	html = urlopen(ALGO_RESULT_URL + str(page) + "?user="+userId+"&state=6")
	bsObject = BS(html, "html.parser")
	return bsObject

def getTable(bsObject):
	table = bsObject.body.find("table",{"class":"submission_list"})

	return table

#최대 페이지 수 계산
def countPage(bsOject):
	pagination = bsObject.body.find("div",{"class":"pagination"})
	return pagination.find_all("a")[-1].get_text()

# return type: int
# string 안에 숫자가 하나 있을 경우 가져옴(/n/t/t/t/t/t10ms/t/t/t/t/t/)
def extractTime(statString):
	statString = statString.strip()
	
	if (statString[0:-2]).isdigit():
		return int(statString[0:-2])
	else:
		return None

if __name__ == "__main__":
	userIDs = util.readIDs() # config 파일에서 user id를 읽어옴
	userResultDicts = [dict() for i in range(len(userIDs))] # 각 유저의 문제별 시간을 dict으로 저장

	gitContents = git.readMDFile()
	gitContentStr = gitContents.decoded_content.decode('utf-8')
	
	for idx, user in enumerate(userIDs):
		tmpDict = dict()
		bsObject = getBSObject(user, 1)
		pageNumber = int(countPage(bsObject))
		for page in range(1, pageNumber+1):
			bsObject = getBSObject(user, page)
			table = getTable(bsObject)
			for row in table.find("tbody").find_all("tr"):
				probName = row.find("td",{"class":"problem"}).find("a").get_text()
				probStat = row.find("td",{"class":"stats"}).get_text()
				probStatInt = extractTime(probStat)
				if probName in tmpDict:
					if tmpDict.get(probName) > probStatInt:
						tmpDict[probName] = probStatInt
				else:
					tmpDict[probName] = probStatInt
		userResultDicts[idx] = tmpDict;	

	newGitContentStr = str()
	for line in gitContentStr.split('\n'):
		if len(line) > 1 and line[0] is '|' and line[1].isdigit():
			lineArr = line.split('|')
			probName = lineArr[2]
			for idx in range(len(userIDs)):
				if probName in userResultDicts[idx]:
					solveTime = userResultDicts[idx].get(probName)
					lineArr[3+idx] = str(solveTime)+"ms"
				else:
					lineArr[3+idx] = "X"
			newLine = "|".join(lineArr)
			newGitContentStr += newLine
			newGitContentStr += '\n'
		else:
			newGitContentStr += line
			newGitContentStr += '\n'

	newGitContentStr += "# Last update : " + time.strftime('%c', time.localtime(time.time())) + "\n"

	git.updateMDFile(newGitContentStr)
