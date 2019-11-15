# algo-crawler
crawl algoboard state for algorithm study


# secure.conf 작성법  

[MAIN] 아래에 다음 항목들을 작성한다

user_ids = "id1", "id2", "id3", "id4"  

github_id = "github login에 사용할 id"  
github_token = "github > developer settings > personal access token -> 토큰 제작"으로 생성한 토큰  


# 실행 환경

python 3.6 버전  

공식 모듈 : requests, beautifulsoup4  
비공식(3rd party) 모듈 : PyGithub  
사용 모듈 :  
	import util  
	import re  
	import time  
	import urllib.request  
	from urllib.request import urlopen  
	import configparser  
	from github import Github  
	
