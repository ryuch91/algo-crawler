from urllib.request import urlopen
from bs4 import BeautifulSoup as BS
import util
import git
import re
import time

ALGO_RESULT_URL = "https://algospot.com/judge/submission/recent/"
CONFIG_PATH = "./secure.conf"
REPO_NAME = "yhchoi0225/AlgoBoard"
FILE_NAME = "README.md"
COMMIT_MSG = "README update by auto-crawler"
BRANCH_NAME = "updateStatus"
#BRANCH_NAME = "master"

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


#MAIN 파트 시작
if __name__ == "__main__":
	config = util.Config(CONFIG_PATH) #config 객체 생성
	userIds = config.getUserIds() # config 객체에서 user id를 읽어옴
	token = config.getGitToken() # git api에 연결할 토큰 가져옴
	userResultDicts = [dict() for i in range(len(userIds))] # 각 유저의 문제별 시간을 dict으로 저장할 자료구조 생성

	# 토큰을 통해서 git api 연결
	gitCli = git.GitConnector(token)
	# 해당 REPO의 file 컨텐츠 다운
	gitContentStr = gitCli.getDecodedContents(REPO_NAME, FILE_NAME)
	
	# 각 유저에 대해 결과 dictionary 채움
	for idx, user in enumerate(userIds):
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

	# 유저별 결과 dict을 문제별로 순차적으로 서치하여 새로운 컨텐츠 작성
	newGitContentStr = str()
	splitedStr = gitContentStr.split('\n')
	for line in splitedStr:
		if len(line) > 1 and line[0] is '|' and line[1].isdigit():
			lineArr = line.split('|')
			probName = lineArr[2]
			for idx in range(len(userIds)):
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

	print(newGitContentStr.encode('utf-8'))
	while( newGitContentStr[-1] == '\n'):
		newGitContentStr = newGitContentStr[:-1]
	newGitContentStr = newGitContentStr[:newGitContentStr.rfind('\n')]
	dateLine = "# Last update : " + time.strftime('%c', time.localtime(time.time()))
	newGitContentStr += ('\n'+ dateLine)
	print(newGitContentStr.encode('utf-8'))

	# 최종적으로 만들어진 컨텐츠(str)를 해당 file로 다시 커밋하여 업데이트
	gitCli.updateFile(REPO_NAME, FILE_NAME, COMMIT_MSG, newGitContentStr, BRANCH_NAME)
