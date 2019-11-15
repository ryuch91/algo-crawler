from github import Github
import util

# token을 통해 github 연결체를 만들고 해당 repo에서 특정 content를 읽어옴
def updateMDFile(inputText):
	ACCESS_TOKEN = util.readGitToken()
	gitCli = Github(ACCESS_TOKEN)

	algoRepo = gitCli.get_repo("yhchoi0225/AlgoBoard")
	algoContents = algoRepo.get_contents("README.md")
	
	# 처음 텍스트가 commit message, 두번째 텍스트가 실제로 삽입되는 텍스트
	algoRepo.update_file(algoContents.path, "README update by auto crawler",inputText, algoContents.sha,branch="updateStatus")

	return algoContents

def readMDFile():
	ACCESS_TOKEN = util.readGitToken()
	gitCli = Github(ACCESS_TOKEN)
	algoRepo = gitCli.get_repo("yhchoi0225/AlgoBoard")
	algoContents = algoRepo.get_contents("README.md")

	return algoContents

if __name__=='__main__':
	gitContents = readMDFile()
	print(gitContents.decoded_content.decode('utf-8'))
	contentLines = gitContents.decoded_content.split('\n')
	for line in contentLines:
		print(line)
