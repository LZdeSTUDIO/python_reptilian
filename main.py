import requests
import os
import time
from bs4 import BeautifulSoup

TARGET="cmd.md"

def get_modle():
	print("get model")
	target = "http://man.linuxde.net/"
	req=requests.get(url=target)
	html=req.text
	bf=BeautifulSoup(html, 'html.parser')
	div=bf.find("div",class_="clearfix",id="tags-list")
	bf=BeautifulSoup(div.prettify(), 'html.parser')
	groups=bf.find_all("dl",class_="left")
	i=0
	for group in groups:
		i=i+1
		bf=BeautifulSoup(group.prettify(), 'html.parser')
		group_name=bf.find("dt")
		print("handle {0}".format(group_name.text))
		with open(TARGET,"a+") as f:
			f.write("{0}.{1}".format(i,group_name.text.replace("\n","")))
			f.write("\n")
		get_model_cmds(group,i)

def get_model_cmds(group,i):
	j=0
	bf=BeautifulSoup(group.prettify(), 'html.parser')
	cmds=bf.find_all("a")
	for cmd in cmds:
		i=i+1
		with open(TARGET,"a+") as f:
			f.write("{0}.{1}.{2}".format(i,j,cmd.text))
		get_cmds(cmd,i,j)

def get_cmds(cmds,i,j):
	url_str=cmds.get("href")
	req=requests.get(url=url_str)
	html=req.text
	bf=BeautifulSoup(html, 'html.parser')
	divs=bf.find_all("li",class_="left")
	k=0
	for div in divs:
		k=k+1
		bf=BeautifulSoup(div.prettify(), 'html.parser')
		a=bf.find("a")
		p=bf.find("p")
		save_cmd(a.get("href"))
		with open(TARGET,"a+") as f:
			f.write("{0}.{1}.{2}.{3}".format(i,j,k,div.text))
			f.write("\n")
			f.write("{0} 简介 {1}".format(a.text,p.text))

def save_cmd(url_str):
	print("Get from : {0}".format(url_str))
	req=requests.get(url=url_str)
	html=req.text
	bf=BeautifulSoup(html, 'html.parser')
	content=bf.find("div",id="arc-body")
	try:
		with open(TARGET,"a+") as f:
			f.write(content.text)
			f.write("\n")
		time.sleep(1.5)
	except Exception as e:
		print("==========================\n")
		print(e)

os.system("rm -f {0}".format(TARGET))
get_modle()
#save_cmd("http://man.linuxde.net/syslog")