import urllib.request
import configparser
from github import Github

# secure.conf 파일을 읽어서 설정값들을 반환(user id목록, github login아이디, github token) 
def readConfig():
	parser = configparser.ConfigParser()
	parser.read('./secure.conf')

	user_ids = parser.get('MAIN', 'user_ids')
	github_id = parser.get('MAIN', 'github_id')
	github_token = parser.get('MAIN', 'github_token')

	return (user_ids, github_id, github_token)

# secure.conf 파일을 읽어서 user id들을 list 형태로 반환
def readIDs():
	parser = configparser.ConfigParser()
	parser.read('./secure.conf')

	user_ids = [i.strip() for i in parser.get('MAIN','user_ids').split(',')]
	return user_ids

def readGitID():
	parser = configparser.ConfigParser()
	parser.read('./secure.conf')
	github_id = parser.get('MAIN', 'github_id')
	return github_id

def readGitToken():
	parser = configparser.ConfigParser()
	parser.read('./secure.conf')
	github_token = parser.get('MAIN', 'github_token')
	return github_token

if __name__ == '__main__':
	config = readConfig()
	user_ids = readIDs()
	github_id = readGitID()
	github_token = readGitToken()

	print(config[0], config[1], config[2])
	print(user_ids)
	print(github_id)
	print(github_token)
