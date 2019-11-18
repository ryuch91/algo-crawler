import urllib.request
import configparser
from github import Github

# config를 담을 객체(user id 목록, github login 아이디, github api 연결 토큰)
class Config:
	def __init__(self, file_path):
		self.config_path = file_path
		parser = configparser.ConfigParser()
		parser.read(file_path)

		self.user_ids = parser.get('MAIN', 'user_ids')
		self.github_id = parser.get('MAIN', 'github_id')
		self.github_token = parser.get('MAIN', 'github_token')

	# user_ids를 list 형태로 변환하여 반환
	def getUserIds(self):
		user_ids = [i.strip() for i in (self.user_ids).split(',')]
		return user_ids

	def getGitId(self):
		return self.github_id

	def getGitToken(self):
		return self.github_token

if __name__ == '__main__':
	config = Config('./secure.conf')

	user_ids = config.getUserIds()
	github_id = config.getGitId()

	print(user_ids)
	print(github_id)
