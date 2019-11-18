from github import Github
import util

class GitConnector:
	def __init__(self, token):
		self.access_token = token
		self.git_client = Github(self.access_token)

	def getContents(self, repo_name, file_name):
		repo = (self.git_client).get_repo(repo_name)
		contents = repo.get_contents(file_name)
		return contents

	# utf-8로 디코딩 된 string 형태의 데이터를 얻기 위해 사용
	def getDecodedContents(self, repo_name, file_name):
		repo = (self.git_client).get_repo(repo_name)
		contents = repo.get_contents(file_name)
		#contents = branch.get_contents(file_name)
		return contents.decoded_content.decode('utf-8')

	# 만들어진 github연결체를 통해 지정된 repo의 branch의 contents를 새로운 input으로 업데이트
	def updateFile(self, repo_name, file_name, commit_msg, input_text, branch_name):
		repo = (self.git_client).get_repo(repo_name)
		contents = repo.get_contents(file_name)
		repo.update_file(contents.path, commit_msg, input_text, contents.sha, branch=branch_name)
		

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
	config = util.Config('./secure.conf')
	git_connector = GitConnector(config.getGitToken())
	git_decoded_contents = git_connector.getDecodedContents('yhchoi0225/AlgoBoard', 'README.md')
	print(git_decoded_contents)
