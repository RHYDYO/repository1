# -*- coding: utf-8 -*- 

################ Server Ver. 18 (2020. 7. 4.) #####################

import os
import sys
import asyncio
import discord
import datetime
import random
import math
import logging
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from gtts import gTTS
from github import Github
import base64
import re #정산
import gspread #정산
from oauth2client.service_account import ServiceAccountCredentials #정산
from io import StringIO
import urllib.request
from math import ceil, floor

##################### 로깅 ###########################
log_stream = StringIO()    
logging.basicConfig(stream=log_stream, level=logging.WARNING)

#ilsanglog = logging.getLogger('discord')
#ilsanglog.setLevel(level = logging.WARNING)
#handler = logging.StreamHandler()
#handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
#ilsanglog.addHandler(handler)
#####################################################

basicSetting = []
bossData = []
fixed_bossData = []

bossNum = 0
fixed_bossNum = 0
chkvoicechannel = 0
chkrelogin = 0
chflg = 0
LoadChk = 0

bossTime = []
tmp_bossTime = []

fixed_bossTime = []

bossTimeString = []
bossDateString = []
tmp_bossTimeString = []
tmp_bossDateString = []

bossFlag = []
bossFlag0 = []
fixed_bossFlag = []
fixed_bossFlag0 = []
bossMungFlag = []
bossMungCnt = []

channel_info = []
channel_name = []
channel_id = []
channel_voice_name = []
channel_voice_id = []
channel_type = []

FixedBossDateData = []
indexFixedBossname = []

client = discord.Client()
client = commands.Bot(command_prefix="", help_command = None, description='일상디코봇')

access_token = os.environ["BOT_TOKEN"]			
git_access_token = os.environ["GIT_TOKEN"]			
git_access_repo = os.environ["GIT_REPO"]			
git_access_repo_restart = os.environ["GIT_REPO_RESTART"]			

g = Github(git_access_token)
repo = g.get_repo(git_access_repo)
repo_restart = g.get_repo(git_access_repo_restart)

def init():
	global basicSetting
	global bossData
	global fixed_bossData

	global bossNum
	global fixed_bossNum
	global chkvoicechannel
	global chkrelogin

	global bossTime
	global tmp_bossTime

	global fixed_bossTime

	global bossTimeString
	global bossDateString
	global tmp_bossTimeString
	global tmp_bossDateString

	global bossFlag
	global bossFlag0
	global fixed_bossFlag
	global fixed_bossFlag0
	global bossMungFlag
	global bossMungCnt
	
	global voice_client1
	
	global channel_info
	global channel_name
	global channel_voice_name
	global channel_voice_id
	global channel_id
	global channel_type
	global LoadChk
	
	global indexFixedBossname
	global FixedBossDateData

	global endTime
	
	global gc #정산
	global credentials #정산
	
	global regenembed
	global command
	global kill_Data
	global kill_Time
	global item_Data

	global tmp_racing_unit

	command = []
	tmp_bossData = []
	tmp_fixed_bossData = []
	FixedBossDateData = []
	indexFixedBossname = []
	kill_Data = {}
	tmp_kill_Data = []
	item_Data = {}
	tmp_item_Data = []
	f = []
	fb = []
	fk = []
	fc = []
	fi = []
	tmp_racing_unit = []
	
	inidata = repo.get_contents("test_setting.ini")
	file_data1 = base64.b64decode(inidata.content)
	file_data1 = file_data1.decode('utf-8')
	inputData = file_data1.split('\n')

	command_inidata = repo.get_contents("command.ini")
	file_data4 = base64.b64decode(command_inidata.content)
	file_data4 = file_data4.decode('utf-8')
	command_inputData = file_data4.split('\n')
	
	boss_inidata = repo.get_contents("boss.ini")
	file_data3 = base64.b64decode(boss_inidata.content)
	file_data3 = file_data3.decode('utf-8')
	boss_inputData = file_data3.split('\n')

	fixed_inidata = repo.get_contents("fixed_boss.ini")
	file_data2 = base64.b64decode(fixed_inidata.content)
	file_data2 = file_data2.decode('utf-8')
	fixed_inputData = file_data2.split('\n')

	kill_inidata = repo.get_contents("kill_list.ini")
	file_data5 = base64.b64decode(kill_inidata.content)
	file_data5 = file_data5.decode('utf-8')
	kill_inputData = file_data5.split('\n')

	item_inidata = repo.get_contents("item_list.ini")
	file_data6 = base64.b64decode(item_inidata.content)
	file_data6 = file_data6.decode('utf-8')
	item_inputData = file_data6.split('\n')

	for i in range(len(fixed_inputData)):
		FixedBossDateData.append(fixed_inputData[i])

	index_fixed = 0

	for value in FixedBossDateData:
		if value.find('bossname') != -1:
			indexFixedBossname.append(index_fixed)
		index_fixed = index_fixed + 1

	for i in range(inputData.count('\r')):
		inputData.remove('\r')

	for i in range(command_inputData.count('\r')):
		command_inputData.remove('\r')
		
	for i in range(boss_inputData.count('\r')):
		boss_inputData.remove('\r')

	for i in range(fixed_inputData.count('\r')):
		fixed_inputData.remove('\r')
	
	for i in range(kill_inputData.count('\r')):
		kill_inputData.remove('\r')

	for i in range(item_inputData.count('\r')):
		item_inputData.remove('\r')

	del(command_inputData[0])
	del(boss_inputData[0])
	del(fixed_inputData[0])
	del(kill_inputData[0])
	del(item_inputData[0])
	
	############## 보탐봇 초기 설정 리스트 #####################
	basicSetting.append(inputData[0][11:])     #basicSetting[0] : timezone
	basicSetting.append(inputData[8][15:])     #basicSetting[1] : before_alert
	basicSetting.append(inputData[10][10:])     #basicSetting[2] : mungChk
	basicSetting.append(inputData[9][16:])     #basicSetting[3] : before_alert1
	basicSetting.append(inputData[13][14:16])  #basicSetting[4] : restarttime 시
	basicSetting.append(inputData[13][17:])    #basicSetting[5] : restarttime 분
	basicSetting.append(inputData[1][15:])     #basicSetting[6] : voice채널 ID
	basicSetting.append(inputData[2][14:])     #basicSetting[7] : text채널 ID
	basicSetting.append(inputData[3][16:])     #basicSetting[8] : 사다리 채널 ID
	basicSetting.append(inputData[12][14:])    #basicSetting[9] : !ㅂ 출력 수
	basicSetting.append(inputData[16][11:])    #basicSetting[10] : json 파일명
	basicSetting.append(inputData[4][17:])     #basicSetting[11] : 정산 채널 ID
	basicSetting.append(inputData[15][12:])    #basicSetting[12] : sheet 이름
	basicSetting.append(inputData[14][16:])    #basicSetting[13] : restart 주기
	basicSetting.append(inputData[17][12:])    #basicSetting[14] : 시트 이름
	basicSetting.append(inputData[18][12:])    #basicSetting[15] : 입력 셀
	basicSetting.append(inputData[19][13:])    #basicSetting[16] : 출력 셀
	basicSetting.append(inputData[11][13:])     #basicSetting[17] : 멍삭제횟수
	basicSetting.append(inputData[5][14:])     #basicSetting[18] : kill채널 ID
	basicSetting.append(inputData[6][16:])     #basicSetting[19] : racing 채널 ID
	basicSetting.append(inputData[7][14:])     #basicSetting[20] : item 채널 ID

	############## 보탐봇 명령어 리스트 #####################
	for i in range(len(command_inputData)):
		tmp_command = command_inputData[i][12:].rstrip('\r')
		fc = tmp_command.split(', ')
		command.append(fc)
		fc = []
		#command.append(command_inputData[i][12:].rstrip('\r'))     #command[0] ~ [24] : 명령어

	################## 척살 명단 ###########################
	for i in range(len(kill_inputData)):
		tmp_kill_Data.append(kill_inputData[i].rstrip('\r'))
		fk.append(tmp_kill_Data[i][:tmp_kill_Data[i].find(' ')])
		fk.append(tmp_kill_Data[i][tmp_kill_Data[i].find(' ')+1:])
		try:
			kill_Data[fk[0]] = int(fk[1])
		except:
			pass
		fk = []

	for i in range(len(item_inputData)):
		tmp_item_Data.append(item_inputData[i].rstrip('\r'))
		fi.append(tmp_item_Data[i][:tmp_item_Data[i].find(' ')])
		fi.append(tmp_item_Data[i][tmp_item_Data[i].find(' ')+1:])
		try:
			item_Data[fi[0]] = int(fi[1])
		except:
			pass
		fi = []


	tmp_killtime = datetime.datetime.now().replace(hour=int(5), minute=int(0), second = int(0))
	kill_Time = datetime.datetime.now()

	if tmp_killtime < kill_Time :
		kill_Time = tmp_killtime + datetime.timedelta(days=int(1))
	else:
		kill_Time = tmp_killtime
	
	for i in range(len(basicSetting)):
		basicSetting[i] = basicSetting[i].strip()
	
	if basicSetting[6] != "":
		basicSetting[6] = int(basicSetting[6])
		
	if basicSetting[7] != "":
		basicSetting[7] = int(basicSetting[7])
	
	if basicSetting[8] != "":
		basicSetting[8] = int(basicSetting[8])
		
	if basicSetting[11] != "":
		basicSetting[11] = int(basicSetting[11])

	if basicSetting[18] != "":
		basicSetting[18] = int(basicSetting[18])

	if basicSetting[19] != "":
		basicSetting[19] = int(basicSetting[19])

	if basicSetting[20] != "":
		basicSetting[20] = int(basicSetting[20])

	tmp_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
	
	if int(basicSetting[13]) == 0 :
		endTime = tmp_now.replace(hour=int(basicSetting[4]), minute=int(basicSetting[5]), second = int(0))
		endTime = endTime + datetime.timedelta(days=int(1000))
	else :
		endTime = tmp_now.replace(hour=int(basicSetting[4]), minute=int(basicSetting[5]), second = int(0))
		if endTime < tmp_now :			
			endTime = endTime + datetime.timedelta(days=int(basicSetting[13]))
	
	bossNum = int(len(boss_inputData)/5)

	fixed_bossNum = int(len(fixed_inputData)/6) 
	
	for i in range(bossNum):
		tmp_bossData.append(boss_inputData[i*5:i*5+5])

	for i in range(fixed_bossNum):
		tmp_fixed_bossData.append(fixed_inputData[i*6:i*6+6]) 
		
	#print (tmp_bossData)
		
	for j in range(bossNum):
		for i in range(len(tmp_bossData[j])):
			tmp_bossData[j][i] = tmp_bossData[j][i].strip()

	for j in range(fixed_bossNum):
		for i in range(len(tmp_fixed_bossData[j])):
			tmp_fixed_bossData[j][i] = tmp_fixed_bossData[j][i].strip()

	############## 일반보스 정보 리스트 #####################
	for j in range(bossNum):
		tmp_len = tmp_bossData[j][1].find(':')
		f.append(tmp_bossData[j][0][11:])         #bossData[0] : 보스명
		f.append(tmp_bossData[j][1][10:tmp_len])  #bossData[1] : 시
		f.append(tmp_bossData[j][2][13:])         #bossData[2] : 멍/미입력
		f.append(tmp_bossData[j][3][20:])         #bossData[3] : 분전 알림멘트
		f.append(tmp_bossData[j][4][13:])         #bossData[4] : 젠 알림멘트
		f.append(tmp_bossData[j][1][tmp_len+1:])  #bossData[5] : 분
		f.append('')                              #bossData[6] : 메세지
		bossData.append(f)
		f = []
		bossTime.append(datetime.datetime.now()+datetime.timedelta(days=365, hours = int(basicSetting[0])))
		tmp_bossTime.append(datetime.datetime.now()+datetime.timedelta(days=365, hours = int(basicSetting[0])))
		bossTimeString.append('99:99:99')
		bossDateString.append('9999-99-99')
		tmp_bossTimeString.append('99:99:99')
		tmp_bossDateString.append('9999-99-99')
		bossFlag.append(False)
		bossFlag0.append(False)
		bossMungFlag.append(False)
		bossMungCnt.append(0)
		
	tmp_fixed_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))

	############## 고정보스 정보 리스트 #####################	
	for j in range(fixed_bossNum):
		tmp_fixed_len = tmp_fixed_bossData[j][1].find(':')
		tmp_fixedGen_len = tmp_fixed_bossData[j][2].find(':')
		fb.append(tmp_fixed_bossData[j][0][11:])                  #fixed_bossData[0] : 보스명
		fb.append(tmp_fixed_bossData[j][1][11:tmp_fixed_len])     #fixed_bossData[1] : 시
		fb.append(tmp_fixed_bossData[j][1][tmp_fixed_len+1:])     #fixed_bossData[2] : 분
		fb.append(tmp_fixed_bossData[j][4][20:])                  #fixed_bossData[3] : 분전 알림멘트
		fb.append(tmp_fixed_bossData[j][5][13:])                  #fixed_bossData[4] : 젠 알림멘트
		fb.append(tmp_fixed_bossData[j][2][12:tmp_fixedGen_len])  #fixed_bossData[5] : 젠주기-시
		fb.append(tmp_fixed_bossData[j][2][tmp_fixedGen_len+1:])  #fixed_bossData[6] : 젠주기-분
		fb.append(tmp_fixed_bossData[j][3][12:16])                #fixed_bossData[7] : 시작일-년	
		fb.append(tmp_fixed_bossData[j][3][17:19])                #fixed_bossData[8] : 시작일-월
		fb.append(tmp_fixed_bossData[j][3][20:22])                #fixed_bossData[9] : 시작일-일
		fixed_bossData.append(fb)
		fb = []
		fixed_bossFlag.append(False)
		fixed_bossFlag0.append(False)
		fixed_bossTime.append(tmp_fixed_now.replace(year = int(fixed_bossData[j][7]), month = int(fixed_bossData[j][8]), day = int(fixed_bossData[j][9]), hour=int(fixed_bossData[j][1]), minute=int(fixed_bossData[j][2]), second = int(0)))
		if fixed_bossTime[j] < tmp_fixed_now :
			while fixed_bossTime[j] < tmp_fixed_now :
				fixed_bossTime[j] = fixed_bossTime[j] + datetime.timedelta(hours=int(fixed_bossData[j][5]), minutes=int(fixed_bossData[j][6]), seconds = int(0))

	################# 이모지 로드 ######################

	emo_inidata = repo.get_contents("emoji.ini")
	emoji_data1 = base64.b64decode(emo_inidata.content)
	emoji_data1 = emoji_data1.decode('utf-8')
	emo_inputData = emoji_data1.split('\n')

	for i in range(len(emo_inputData)):
		tmp_emo = emo_inputData[i][8:].rstrip('\r')
		if tmp_emo != "":
			tmp_racing_unit.append(tmp_emo)
	
	################# 리젠보스 시간 정렬 ######################
	regenData = []
	regenTime = []
	regenbossName = []
	outputTimeHour = []
	outputTimeMin = []

	for i in range(bossNum):
		if bossData[i][2] == "1":
			f.append(bossData[i][0] + "R")
		else:
			f.append(bossData[i][0])
		f.append(bossData[i][1] + bossData[i][5])
		regenData.append(f)
		regenTime.append(bossData[i][1] + bossData[i][5])
		f = []
		
	regenTime = sorted(list(set(regenTime)))
	
	for j in range(len(regenTime)):
		for i in range(len(regenData)):
			if regenTime[j] == regenData[i][1] :
				f.append(regenData[i][0])
		regenbossName.append(f)
		outputTimeHour.append(int(regenTime[j][:2]))
		outputTimeMin.append(int(regenTime[j][2:]))
		f = []

	regenembed = discord.Embed(
			title='----- 보스별 리스폰 시간 -----',
			description= ' ')
	for i in range(len(regenTime)):
		if outputTimeMin[i] == 0 :
			regenembed.add_field(name=str(outputTimeHour[i]) + '시간', value= '```'+ ', '.join(map(str, sorted(regenbossName[i]))) + '```', inline=False)
		else :
			regenembed.add_field(name=str(outputTimeHour[i]) + '시간' + str(outputTimeMin[i]) + '분', value= '```' + ','.join(map(str, sorted(regenbossName[i]))) + '```', inline=False)
	regenembed.set_footer(text = 'R : 멍 보스')

	##########################################################

	if basicSetting[10] !="":
		scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'] #정산
		credentials = ServiceAccountCredentials.from_json_keyfile_name(basicSetting[10], scope) #정산

init()

channel = ''

async def task():
	await client.wait_until_ready()

	global channel
	global endTime
		
	global basicSetting
	global bossData
	global fixed_bossData

	global bossNum
	global fixed_bossNum
	global chkvoicechannel
	global chkrelogin

	global bossTime
	global tmp_bossTime
	
	global fixed_bossTime

	global bossTimeString
	global bossDateString
	global tmp_bossTimeString
	global tmp_bossDateString

	global bossFlag
	global bossFlag0
	global fixed_bossFlag
	global fixed_bossFlag0
	global bossMungFlag
	global bossMungCnt
	
	global voice_client1
	
	global channel_info
	global channel_name
	global channel_id
	global channel_voice_name
	global channel_voice_id
	global channel_type
	
	global endTime
	global kill_Time
	
	if chflg == 1 : 
		if voice_client1.is_connected() == False :
			voice_client1 = await client.get_channel(basicSetting[6]).connect(reconnect=True)
			if voice_client1.is_connected() :
				await dbLoad()
				await client.get_channel(channel).send( '< 다시 왔습니다! >', tts=False)
				print("명치복구완료!")

	while not client.is_closed():
		############ 워닝잡자! ############
		if log_stream.getvalue().find("Awaiting") != -1:
			log_stream.truncate(0)
			log_stream.seek(0)
			await client.get_channel(channel).send( '< 디코접속에러! 잠깐 나갔다 올께요! >', tts=False)
			await dbSave()
			raise SystemExit
		
		log_stream.truncate(0)
		log_stream.seek(0)
		##################################

		now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
		priv0 = now+datetime.timedelta(minutes=int(basicSetting[3]))
		priv = now+datetime.timedelta(minutes=int(basicSetting[1]))
		aftr = now+datetime.timedelta(minutes=int(0-int(basicSetting[2])))

		if channel != '':			
			################ 보탐봇 재시작 ################ 
			if endTime.strftime('%Y-%m-%d ') + endTime.strftime('%H:%M:%S') == now.strftime('%Y-%m-%d ') + now.strftime('%H:%M:%S'):
				await dbSave()
				await FixedBossDateSave()
				await data_list_Save("kill_list.ini", "-----척살명단-----", kill_Data)
				await data_list_Save("item_list.ini", "-----아이템목록-----", item_Data)
				#await client.get_channel(channel).send('<갑자기 인사해도 놀라지마세요!>', tts=False)
				print("보탐봇재시작!")
				endTime = endTime + datetime.timedelta(days = int(basicSetting[13]))
				await voice_client1.disconnect()
				await asyncio.sleep(2)

				inidata_restart = repo_restart.get_contents("restart.txt")
				file_data_restart = base64.b64decode(inidata_restart.content)
				file_data_restart = file_data_restart.decode('utf-8')
				inputData_restart = file_data_restart.split('\n')

				if len(inputData_restart) < 3:	
					contents12 = repo_restart.get_contents("restart.txt")
					repo_restart.update_file(contents12.path, "restart_0", "restart\nrestart\nrestrat\n", contents12.sha)
				else:
					contents12 = repo_restart.get_contents("restart.txt")
					repo_restart.update_file(contents12.path, "restart_1", "", contents12.sha)
			
			################ 킬 목록 초기화 ################ 
			if kill_Time.strftime('%Y-%m-%d ') + kill_Time.strftime('%H:%M') == now.strftime('%Y-%m-%d ') + now.strftime('%H:%M'):
				kill_Time = kill_Time + datetime.timedelta(days=int(1))
				await init_data_list('kill_list.ini', '-----척살명단-----')

			################ 고정 보스 확인 ################ 
			for i in range(fixed_bossNum):
				################ before_alert1 ################ 
				if fixed_bossTime[i] <= priv0 and fixed_bossTime[i] > priv:
					if basicSetting[3] != '0':
						if fixed_bossFlag0[i] == False:
							fixed_bossFlag0[i] = True
							await client.get_channel(channel).send("```" + fixed_bossData[i][0] + ' ' + basicSetting[3] + '분 전 ' + fixed_bossData[i][3] +' [' +  fixed_bossTime[i].strftime('%H:%M:%S') + ']```', tts=False)
							await PlaySound(voice_client1, './sound/' + fixed_bossData[i][0] + '알림1.mp3')

				################ before_alert ################ 
				if fixed_bossTime[i] <= priv and fixed_bossTime[i] > now:
					if basicSetting[1] != '0' :
						if fixed_bossFlag[i] == False:
							fixed_bossFlag[i] = True
							await client.get_channel(channel).send("```" + fixed_bossData[i][0] + ' ' + basicSetting[1] + '분 전 ' + fixed_bossData[i][3] +' [' +  fixed_bossTime[i].strftime('%H:%M:%S') + ']```', tts=False)
							await PlaySound(voice_client1, './sound/' + fixed_bossData[i][0] + '알림.mp3')
				
				################ 보스 젠 시간 확인 ################
				if fixed_bossTime[i] <= now :
					fixed_bossTime[i] = fixed_bossTime[i]+datetime.timedelta(hours=int(fixed_bossData[i][5]), minutes=int(fixed_bossData[i][6]), seconds = int(0))
					fixed_bossFlag0[i] = False
					fixed_bossFlag[i] = False
					embed = discord.Embed(
							description= "```" + fixed_bossData[i][0] + fixed_bossData[i][4] + "```" ,
							color=0x00ff00
							)
					await client.get_channel(channel).send(embed=embed, tts=False)
					await PlaySound(voice_client1, './sound/' + fixed_bossData[i][0] + '젠.mp3')

			################ 일반 보스 확인 ################ 
			for i in range(bossNum):
				################ before_alert1 ################ 
				if bossTime[i] <= priv0 and bossTime[i] > priv:
					if basicSetting[3] != '0':
						if bossFlag0[i] == False:
							bossFlag0[i] = True
							if bossData[i][6] != '' :
								await client.get_channel(channel).send("```" + bossData[i][0] + ' ' + basicSetting[3] + '분 전 ' + bossData[i][3] + " [" +  bossTimeString[i] + "]" + '\n<' + bossData[i][6] + '>```', tts=False)
							else :
								await client.get_channel(channel).send("```" + bossData[i][0] + ' ' + basicSetting[3] + '분 전 ' + bossData[i][3] + " [" +  bossTimeString[i] + "]```", tts=False)
							await PlaySound(voice_client1, './sound/' + bossData[i][0] + '알림1.mp3')

				################ before_alert ################
				if bossTime[i] <= priv and bossTime[i] > now:
					if basicSetting[1] != '0' :
						if bossFlag[i] == False:
							bossFlag[i] = True
							if bossData[i][6] != '' :
								await client.get_channel(channel).send("```" + bossData[i][0] + ' ' + basicSetting[1] + '분 전 ' + bossData[i][3] + " [" +  bossTimeString[i] + "]" + '\n<' + bossData[i][6] + '>```', tts=False)
							else :
								await client.get_channel(channel).send("```" + bossData[i][0] + ' ' + basicSetting[1] + '분 전 ' + bossData[i][3] + " [" +  bossTimeString[i] + "]```", tts=False)
							await PlaySound(voice_client1, './sound/' + bossData[i][0] + '알림.mp3')

				################ 보스 젠 시간 확인 ################ 
				if bossTime[i] <= now :
					#print ('if ', bossTime[i])
					bossMungFlag[i] = True
					tmp_bossTime[i] = bossTime[i]
					tmp_bossTimeString[i] = tmp_bossTime[i].strftime('%H:%M:%S')
					tmp_bossDateString[i] = tmp_bossTime[i].strftime('%Y-%m-%d')
					bossTimeString[i] = '99:99:99'
					bossDateString[i] = '9999-99-99'
					bossTime[i] = now+datetime.timedelta(days=365)
					if bossData[i][6] != '' :
						embed = discord.Embed(
								description= "```" + bossData[i][0] + bossData[i][4] + '\n<' + bossData[i][6] + '>```' ,
								color=0x00ff00
								)
					else :
						embed = discord.Embed(
								description= "```" + bossData[i][0] + bossData[i][4] + "```" ,
								color=0x00ff00
								)
					await client.get_channel(channel).send(embed=embed, tts=False)
					await PlaySound(voice_client1, './sound/' + bossData[i][0] + '젠.mp3')

				################ 보스 자동 멍 처리 ################ 
				if bossMungFlag[i] == True:
					if (bossTime[i]+datetime.timedelta(days=-365)) <= aftr:
						if basicSetting[2] != '0':
							if int(basicSetting[17]) <= bossMungCnt[i] and int(basicSetting[17]) != 0:
								bossTime[i] = datetime.datetime.now()+datetime.timedelta(days=365, hours = int(basicSetting[0]))
								tmp_bossTime[i] =  datetime.datetime.now()+datetime.timedelta(days=365, hours = int(basicSetting[0]))
								bossTimeString[i] = '99:99:99'
								bossDateString[i] = '9999-99-99'
								tmp_bossTimeString[i] = '99:99:99'
								tmp_bossDateString[i] = '9999-99-99'
								bossFlag[i] = False
								bossFlag0[i] = False
								bossMungFlag[i] = False
								bossMungCnt[i] = 0
								if bossData[i][2] == '0':
									await client.get_channel(channel).send(f'```자동 미입력 횟수 {basicSetting[17]}회 초과! [{bossData[i][0]}] 삭제!```', tts=False)
									print ('자동미입력 횟수초과 <' + bossData[i][0] + ' 삭제완료>')
								else:
									await client.get_channel(channel).send(f'```자동 멍처리 횟수 {basicSetting[17]}회 초과! [{bossData[i][0]}] 삭제!```', tts=False)
									print ('자동멍처리 횟수초과 <' + bossData[i][0] + ' 삭제완료>')
								#await dbSave()
								
							else:
								################ 미입력 보스 ################
								if bossData[i][2] == '0':
									bossFlag[i] = False
									bossFlag0[i] = False
									bossMungFlag[i] = False
									bossMungCnt[i] = bossMungCnt[i] + 1
									tmp_bossTime[i] = bossTime[i] = nextTime = tmp_bossTime[i]+datetime.timedelta(hours=int(bossData[i][1]), minutes=int(bossData[i][5]))
									tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
									tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')
									await client.get_channel(channel).send("```" +  bossData[i][0] + ' 미입력 됐습니다.```', tts=False)
									embed = discord.Embed(
										description= '```다음 ' + bossData[i][0] + ' ' + bossTimeString[i] + '입니다.```',
										color=0xff0000
										)
									await client.get_channel(channel).send(embed=embed, tts=False)
									await PlaySound(voice_client1, './sound/' + bossData[i][0] + '미입력.mp3')
								################ 멍 보스 ################
								else :
									bossFlag[i] = False
									bossFlag0[i] = False
									bossMungFlag[i] = False
									bossMungCnt[i] = bossMungCnt[i] + 1
									tmp_bossTime[i] = bossTime[i] = nextTime = tmp_bossTime[i]+datetime.timedelta(hours=int(bossData[i][1]), minutes=int(bossData[i][5]))
									tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
									tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')
									await client.get_channel(channel).send("```" + bossData[i][0] + ' 멍 입니다.```')
									embed = discord.Embed(
										description= '```다음 ' + bossData[i][0] + ' ' + bossTimeString[i] + '입니다.```',
										color=0xff0000
										)
									await client.get_channel(channel).send(embed=embed, tts=False)
									await PlaySound(voice_client1, './sound/' + bossData[i][0] + '멍.mp3')

		await asyncio.sleep(1) # task runs every 60 seconds

#mp3 파일 생성함수(gTTS 이용, 남성목소리)
async def MakeSound(saveSTR, filename):
	
	tts = gTTS(saveSTR, lang = 'ko')
	tts.save('./' + filename + '.wav')
	
	'''
	try:
		encText = urllib.parse.quote(saveSTR)
		urllib.request.urlretrieve("https://clova.ai/proxy/voice/api/tts?text=" + encText + "%0A&voicefont=1&format=wav",filename + '.wav')
	except Exception as e:
		print (e)
		tts = gTTS(saveSTR, lang = 'ko')
		tts.save('./' + filename + '.wav')
		pass
	'''
#mp3 파일 재생함수	
async def PlaySound(voiceclient, filename):
	source = discord.FFmpegPCMAudio(filename)
	try:
		voiceclient.play(source)
	except discord.errors.ClientException:
		while voiceclient.is_playing():
			await asyncio.sleep(1)
	while voiceclient.is_playing():
		await asyncio.sleep(1)
	voiceclient.stop()
	source.cleanup()

#my_bot.db 저장하기
async def dbSave():
	global bossData
	global bossNum
	global bossTime
	global bossTimeString
	global bossDateString
	global bossMungFlag
	global bossMungCnt

	for i in range(bossNum):
		for j in range(bossNum):
			if bossTimeString[i] and bossTimeString[j] != '99:99:99':
				if bossTimeString[i] == bossTimeString[j] and i != j:
					tmp_time1 = bossTimeString[j][:6]
					tmp_time2 = (int(bossTimeString[j][6:]) + 1)%100
					if tmp_time2 < 10 :
						tmp_time22 = '0' + str(tmp_time2)
					elif tmp_time2 == 60 :
						tmp_time22 = '00'
					else :
						tmp_time22 = str(tmp_time2)
					bossTimeString[j] = tmp_time1 + tmp_time22
					
	datelist1 = bossTime
	
	datelist = list(set(datelist1))

	information1 = '----- 보스탐 정보 -----\n'
	for timestring in sorted(datelist):
		for i in range(bossNum):
			if timestring == bossTime[i]:
				if bossTimeString[i] != '99:99:99' or bossMungFlag[i] == True :
					if bossMungFlag[i] == True :
						if bossData[i][2] == '0' :
							information1 += ' - ' + bossData[i][0] + '(' + bossData[i][1] + '.' + bossData[i][5] + ') : ' + tmp_bossTime[i].strftime('%H:%M:%S') + ' @ ' + tmp_bossTime[i].strftime('%Y-%m-%d') + ' (미입력 ' + str(bossMungCnt[i]) + '회)' + ' * ' + bossData[i][6] + '\n'
						else : 
							information1 += ' - ' + bossData[i][0] + '(' + bossData[i][1] + '.' + bossData[i][5] + ') : ' + tmp_bossTime[i].strftime('%H:%M:%S') + ' @ ' + tmp_bossTime[i].strftime('%Y-%m-%d') + ' (멍 ' + str(bossMungCnt[i]) + '회)' + ' * ' + bossData[i][6] + '\n'
					else:
						if bossData[i][2] == '0' :
							information1 += ' - ' + bossData[i][0] + '(' + bossData[i][1] + '.' + bossData[i][5] + ') : ' + bossTimeString[i] + ' @ ' + bossDateString[i] + ' (미입력 ' + str(bossMungCnt[i]) + '회)' + ' * ' + bossData[i][6] + '\n'
						else : 
							information1 += ' - ' + bossData[i][0] + '(' + bossData[i][1] + '.' + bossData[i][5] + ') : ' + bossTimeString[i] + ' @ ' + bossDateString[i] + ' (멍 ' + str(bossMungCnt[i]) + '회)' + ' * ' + bossData[i][6] + '\n'
						
	try :
		contents = repo.get_contents("my_bot.db")
		repo.update_file(contents.path, "bossDB", information1, contents.sha)
	except GithubException as e :
		print ('save error!!')
		print(e.args[1]['message']) # output: This repository is empty.
		errortime = datetime.datetime.now()
		print (errortime)
		pass

#my_bot.db 불러오기
async def dbLoad():
	global LoadChk
	
	contents1 = repo.get_contents("my_bot.db")
	file_data = base64.b64decode(contents1.content)
	file_data = file_data.decode('utf-8')
	beforeBossData = file_data.split('\n')
	
	if len(beforeBossData) > 1:	
		for i in range(len(beforeBossData)-1):
			for j in range(bossNum):
				startPos = beforeBossData[i+1].find('-')
				endPos = beforeBossData[i+1].find('(')
				if beforeBossData[i+1][startPos+2:endPos] == bossData[j][0] :
				#if beforeBossData[i+1].find(bossData[j][0]) != -1 :
					tmp_mungcnt = 0
					tmp_len = beforeBossData[i+1].find(':')
					tmp_datelen = beforeBossData[i+1].find('@')
					tmp_msglen = beforeBossData[i+1].find('*')

					
					years1 = beforeBossData[i+1][tmp_datelen+2:tmp_datelen+6]
					months1 = beforeBossData[i+1][tmp_datelen+7:tmp_datelen+9]
					days1 = beforeBossData[i+1][tmp_datelen+10:tmp_datelen+12]
					
					hours1 = beforeBossData[i+1][tmp_len+2:tmp_len+4]
					minutes1 = beforeBossData[i+1][tmp_len+5:tmp_len+7]
					seconds1 = beforeBossData[i+1][tmp_len+8:tmp_len+10]
					
					now2 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))

					tmp_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
					tmp_now = tmp_now.replace(year = int(years1), month = int(months1), day = int(days1), hour=int(hours1), minute=int(minutes1), second = int(seconds1))

					tmp_now_chk = tmp_now + datetime.timedelta(minutes = int(basicSetting[2]))

					if tmp_now_chk < now2 : 
						deltaTime = datetime.timedelta(hours = int(bossData[j][1]), minutes = int(bossData[j][5]))
						while tmp_now_chk < now2 :
							tmp_now_chk = tmp_now_chk + deltaTime
							tmp_now = tmp_now + deltaTime
							tmp_mungcnt = tmp_mungcnt + 1

					if tmp_now_chk > now2 > tmp_now: #젠중.
						bossMungFlag[j] = True
						tmp_bossTime[j] = tmp_now
						tmp_bossTimeString[j] = tmp_bossTime[j].strftime('%H:%M:%S')
						tmp_bossDateString[j] = tmp_bossTime[j].strftime('%Y-%m-%d')
						bossTimeString[j] = '99:99:99'
						bossDateString[j] = '9999-99-99'
						bossTime[j] = tmp_bossTime[j] + datetime.timedelta(days=365)
					else:
						tmp_bossTime[j] = bossTime[j] = tmp_now
						tmp_bossTimeString[j] = bossTimeString[j] = bossTime[j].strftime('%H:%M:%S')
						tmp_bossDateString[j] = bossDateString[j] = bossTime[j].strftime('%Y-%m-%d')
						
					bossData[j][6] = beforeBossData[i+1][tmp_msglen+2:len(beforeBossData[i+1])]

					if beforeBossData[i+1][tmp_msglen-4:tmp_msglen-3] != 0 and beforeBossData[i+1][tmp_msglen-5:tmp_msglen-4] == ' ':
						bossMungCnt[j] = int(beforeBossData[i+1][tmp_msglen-4:tmp_msglen-3]) + tmp_mungcnt
					elif beforeBossData[i+1][tmp_msglen-5:tmp_msglen-4] != ' ':
						bossMungCnt[j] = int(beforeBossData[i+1][tmp_msglen-5:tmp_msglen-4] + beforeBossData[i+1][tmp_msglen-4:tmp_msglen-3]) + tmp_mungcnt
					else:
						bossMungCnt[j] = 0
		LoadChk = 0
		print ("<불러오기 완료>")
	else:
		#await client.get_channel(channel).send('<보스타임 정보가 없습니다.>', tts=False)
		LoadChk = 1
		print ("보스타임 정보가 없습니다.")

#고정보스 날짜저장
async def FixedBossDateSave():
	global fixed_bossData
	global fixed_bossTime
	global fixed_bossNum
	global FixedBossDateData
	global indexFixedBossname

	for i in range(fixed_bossNum):
		FixedBossDateData[indexFixedBossname[i] + 3] = 'startDate = '+ fixed_bossTime[i].strftime('%Y-%m-%d') + '\n'

	FixedBossDateDataSTR = ""
	for j in range(len(FixedBossDateData)):
		pos = len(FixedBossDateData[j])
		tmpSTR = FixedBossDateData[j][:pos-1] + '\r\n'
		FixedBossDateDataSTR += tmpSTR

	contents = repo.get_contents("fixed_boss.ini")
	repo.update_file(contents.path, "bossDB", FixedBossDateDataSTR, contents.sha)

#사다리함수		
async def LadderFunc(number, ladderlist, channelVal):
	if number < len(ladderlist):
		result_ladder = random.sample(ladderlist, number)
		result_ladderSTR = ','.join(map(str, result_ladder))
		embed = discord.Embed(
			title = "----- 당첨! -----",
			description= '```' + result_ladderSTR + '```',
			color=0xff00ff
			)
		await channelVal.send(embed=embed, tts=False)
	else:
		await channelVal.send('```추첨인원이 총 인원과 같거나 많습니다. 재입력 해주세요```', tts=False)

#data초기화
async def init_data_list(filename, first_line : str = "-----------"):
	try :
		contents = repo.get_contents(filename)
		repo.update_file(contents.path, "deleted list " + str(filename), first_line, contents.sha)
		print ('< 데이터 초기화 >')
	except GithubException as e :
		print ('save error!!')
		print(e.args[1]['message']) # output: This repository is empty.
		errortime = datetime.datetime.now()
		print (errortime)
		pass

#data저장
async def data_list_Save(filename, first_line : str = "-----------",  save_data : dict = {}):

	output_list = first_line+ '\n'
	for key, value in save_data.items():
		output_list += str(key) + ' ' + str(value) + '\n'

	try :
		contents = repo.get_contents(filename)
		repo.update_file(contents.path, "updated " + str(filename), output_list, contents.sha)
	except GithubException as e :
		print ('save error!!')
		print(e.args[1]['message']) # output: This repository is empty.
		errortime = datetime.datetime.now()
		print (errortime)
		pass

#서버(길드) 정보 
async def get_guild_channel_info():
	text_channel_name : list = []
	text_channel_id : list = []
	voice_channel_name : list = []
	voice_channel_id : list = []
	
	for guild in client.guilds:
		for text_channel in guild.text_channels:
			text_channel_name.append(text_channel.name)
			text_channel_id.append(str(text_channel.id))
		for voice_channel in guild.voice_channels:
			voice_channel_name.append(voice_channel.name)
			voice_channel_id.append(str(voice_channel.id))
	return text_channel_name, text_channel_id, voice_channel_name, voice_channel_id

#초성추출 함수
def convertToInitialLetters(text):
	CHOSUNG_START_LETTER = 4352
	JAMO_START_LETTER = 44032
	JAMO_END_LETTER = 55203
	JAMO_CYCLE = 588

	def isHangul(ch):
		return ord(ch) >= JAMO_START_LETTER and ord(ch) <= JAMO_END_LETTER
	
	def isBlankOrNumber(ch):
		return ord(ch) == 32 or ord(ch) >= 48 and ord(ch) <= 57

	def convertNomalInitialLetter(ch):
		dic_InitalLetter = {4352:"ㄱ"
							,4353:"ㄲ"
							,4354:"ㄴ"
							,4355:"ㄷ"
							,4356:"ㄸ"
							,4357:"ㄹ"
							,4358:"ㅁ"
							,4359:"ㅂ"
							,4360:"ㅃ"
							,4361:"ㅅ"
							,4362:"ㅆ"
							,4363:"ㅇ"
							,4364:"ㅈ"
							,4365:"ㅉ"
							,4366:"ㅊ"
							,4367:"ㅋ"
							,4368:"ㅌ"
							,4369:"ㅍ"
							,4370:"ㅎ"
							,32:" "
							,48:"0"
							,49:"1"
							,50:"2"
							,51:"3"
							,52:"4"
							,53:"5"
							,54:"6"
							,55:"7"
							,56:"8"
							,57:"9"
		}
		return dic_InitalLetter[ord(ch)]

	result = ""
	for ch in text:
		if isHangul(ch): #한글이 아닌 글자는 걸러냅니다.
			result += convertNomalInitialLetter(chr((int((ord(ch)-JAMO_START_LETTER)/JAMO_CYCLE))+CHOSUNG_START_LETTER))
		elif isBlankOrNumber(ch):
			result += convertNomalInitialLetter(chr(int(ord(ch))))

	return result

## 명치 예외처리	
def handle_exit():
	#print("Handling")
	client.loop.run_until_complete(client.logout())

	for t in asyncio.Task.all_tasks(loop=client.loop):
		if t.done():
		#t.exception()
			try:
			#print ('try :   ', t)
				t.exception()
			except asyncio.CancelledError:
			#print ('cancel :   ', t)
				continue
			continue
		t.cancel()
		try:
			client.loop.run_until_complete(asyncio.wait_for(t, 5, loop=client.loop))
			t.exception()
		except asyncio.InvalidStateError:
			pass
		except asyncio.TimeoutError:
			pass
		except asyncio.CancelledError:
			pass

# 봇이 구동되었을 때 동작되는 코드입니다.
@client.event
async def on_ready():
	global basicSetting

	global channel
	
	global voice_client1

	global channel_info
	global channel_name
	global channel_id
	global channel_voice_name
	global channel_voice_id
	global channel_type
	
	global chkvoicechannel
	global chflg
	
	global endTime
	global setting_channel_name
			
	print("Logged in as ") #화면에 봇의 아이디, 닉네임이 출력됩니다.
	print(client.user.name)
	print(client.user.id)
	print("===========")

	channel_name, channel_id, channel_voice_name, channel_voice_id = await get_guild_channel_info()

	await dbLoad()

	if str(basicSetting[6]) in channel_voice_id and str(basicSetting[7]) in channel_id:
		voice_client1 = await client.get_channel(basicSetting[6]).connect(reconnect=True)
		channel = basicSetting[7]

		setting_channel_name = client.get_channel(basicSetting[7]).name

		now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))

		print('< 접속시간 [' + now.strftime('%Y-%m-%d ') + now.strftime('%H:%M:%S') + '] >')
		print('< 텍스트채널 [' + client.get_channel(basicSetting[7]).name + '] 접속완료>')
		print('< 음성채널 [' + client.get_channel(basicSetting[6]).name + '] 접속완료>')
		if basicSetting[8] != "":
			if str(basicSetting[8]) in channel_id:
				print('< 사다리채널 [' + client.get_channel(int(basicSetting[8])).name + '] 접속완료 >')
			else:
				basicSetting[8] = ""
				print(f"사다리채널 ID 오류! [{command[28][0]} 사다리] 명령으로 재설정 바랍니다.")
		if basicSetting[11] != "":
			if str(basicSetting[11]) in channel_id:
				print('< 정산채널 [' + client.get_channel(int(basicSetting[11])).name + '] 접속완료>')
			else:
				basicSetting[11] = ""
				print(f"정산채널 ID 오류! [{command[28][0]} 정산] 명령으로 재설정 바랍니다.")
		if basicSetting[18] != "":
			if str(basicSetting[18]) in channel_id:
				print('< 척살채널 [' + client.get_channel(int(basicSetting[18])).name + '] 접속완료>')
			else:
				basicSetting[18] = ""
				print(f"척살채널 ID 오류! [{command[28][0]} 척살] 명령으로 재설정 바랍니다.")
		if basicSetting[19] != "":
			if str(basicSetting[19]) in channel_id:
				print('< 경주채널 [' + client.get_channel(int(basicSetting[19])).name + '] 접속완료>')
			else:
				basicSetting[19] = ""
				print(f"경주채널 ID 오류! [{command[28][0]} 경주] 명령으로 재설정 바랍니다.")
		if basicSetting[20] != "":
			if str(basicSetting[20]) in channel_id:
				print('< 아이템채널 [' + client.get_channel(int(basicSetting[20])).name + '] 접속완료>')
			else:
				basicSetting[20] = ""
				print(f"아이템채널 ID 오류! [{command[28][0]} 아이템] 명령으로 재설정 바랍니다.")
		if int(basicSetting[13]) != 0 :
			print('< 보탐봇 재시작 시간 ' + endTime.strftime('%Y-%m-%d ') + endTime.strftime('%H:%M:%S') + ' >')
			print('< 보탐봇 재시작 주기 ' + basicSetting[13] + '일 >')
		else :
			print('< 보탐봇 재시작 설정안됨 >')
		chflg = 1
	else:
		basicSetting[6] = ""
		basicSetting[7] = ""
		print(f"설정된 채널 값이 없거나 잘못 됐습니다. **[{command[0][0]}]** 명령어 먼저 입력하여 사용해주시기 바랍니다.")

	# 디스코드에는 현재 본인이 어떤 게임을 플레이하는지 보여주는 기능이 있습니다.
	# 이 기능을 사용하여 봇의 상태를 간단하게 출력해줄 수 있습니다.
	await client.change_presence(status=discord.Status.dnd, activity=discord.Game(name=command[1][0], type=1), afk=False)

while True:
	################ 보탐봇 입장 ################ 	
	@commands.has_permissions(manage_messages=True)
	@client.command(name=command[0][0], aliases=command[0][1:])
	async def join_(ctx):
		global basicSetting
		global chflg
		global voice_client1

		if basicSetting[7] == "":
			channel = ctx.message.channel.id #메세지가 들어온 채널 ID

			print ('[ ', basicSetting[7], ' ]')
			print ('] ', ctx.message.channel.name, ' [')

			inidata_textCH = repo.get_contents("test_setting.ini")
			file_data_textCH = base64.b64decode(inidata_textCH.content)
			file_data_textCH = file_data_textCH.decode('utf-8')
			inputData_textCH = file_data_textCH.split('\n')
			
			for i in range(len(inputData_textCH)):
				if inputData_textCH[i].startswith("textchannel ="):
					inputData_textCH[i] = 'textchannel = ' + str(channel) + '\r'
					basicSetting[7] = channel
					#print ('======', inputData_text[i])
			
			result_textCH = '\n'.join(inputData_textCH)
			
			#print (result_textCH)
			
			contents = repo.get_contents("test_setting.ini")
			repo.update_file(contents.path, "test_setting", result_textCH, contents.sha)

			await ctx.send(f"< 텍스트채널 [{ctx.message.channel.name}] 접속완료 >\n< 음성채널 접속 후 [{command[5][0]}] 명령을 사용 하세요 >", tts=False)
			
			print('< 텍스트채널 [' + client.get_channel(basicSetting[7]).name + '] 접속완료>')
			if basicSetting[6] != "":
				voice_client1 = await client.get_channel(basicSetting[6]).connect(reconnect=True)
				print('< 음성채널 [' + client.get_channel(basicSetting[6]).name + '] 접속완료>')
			if basicSetting[8] != "":
				if str(basicSetting[8]) in channel_id:
					print('< 사다리채널 [' + client.get_channel(int(basicSetting[8])).name + '] 접속완료 >')
				else:
					basicSetting[8] = ""
					print(f"사다리채널 ID 오류! [{command[28][0]} 사다리] 명령으로 재설정 바랍니다.")
			if basicSetting[11] != "":
				if str(basicSetting[11]) in channel_id:
					print('< 정산채널 [' + client.get_channel(int(basicSetting[11])).name + '] 접속완료>')
				else:
					basicSetting[11] = ""
					print(f"정산채널 ID 오류! [{command[28][0]} 정산] 명령으로 재설정 바랍니다.")
			if basicSetting[18] != "":
				if str(basicSetting[18]) in channel_id:
					print('< 척살채널 [' + client.get_channel(int(basicSetting[18])).name + '] 접속완료>')
				else:
					basicSetting[18] = ""
					print(f"척살채널 ID 오류! [{command[28][0]} 척살] 명령으로 재설정 바랍니다.")
			if basicSetting[19] != "":
				if str(basicSetting[19]) in channel_id:
					print('< 경주채널 [' + client.get_channel(int(basicSetting[19])).name + '] 접속완료>')
				else:
					basicSetting[19] = ""
					print(f"경주채널 ID 오류! [{command[28][0]} 경주] 명령으로 재설정 바랍니다.")
			if basicSetting[20] != "":
				if str(basicSetting[20]) in channel_id:
					print('< 아이템채널 [' + client.get_channel(int(basicSetting[20])).name + '] 접속완료>')
				else:
					basicSetting[20] = ""
					print(f"아이템채널 ID 오류! [{command[28][0]} 아이템] 명령으로 재설정 바랍니다.")
			if int(basicSetting[13]) != 0 :
				print('< 보탐봇 재시작 시간 ' + endTime.strftime('%Y-%m-%d ') + endTime.strftime('%H:%M:%S') + ' >')
				print('< 보탐봇 재시작 주기 ' + basicSetting[13] + '일 >')
			else :
				print('< 보탐봇 재시작 설정안됨 >')

			chflg = 1
		else:
			for guild in client.guilds:
				for text_channel in guild.text_channels:
					if basicSetting[7] == text_channel.id:
						curr_guild_info = guild

			emoji_list : list = ["⭕", "❌"]
			guild_error_message = await ctx.send(f"이미 **[{curr_guild_info.name}]** 서버 **[{setting_channel_name}]** 채널이 명령어 채널로 설정되어 있습니다.\n해당 채널로 명령어 채널을 변경 하시려면 ⭕ 그대로 사용하시려면 ❌ 를 눌러주세요.\n(10초이내 미입력시 기존 설정 그대로 설정됩니다.)", tts=False)

			for emoji in emoji_list:
				await guild_error_message.add_reaction(emoji)

			def reaction_check(reaction, user):
				return (reaction.message.id == guild_error_message.id) and (user.id == ctx.author.id) and (str(reaction) in emoji_list)
			try:
				reaction, user = await client.wait_for('reaction_add', check = reaction_check, timeout = 10)
			except asyncio.TimeoutError:
				return await ctx.send(f"시간이 초과됐습니다. **[{curr_guild_info.name}]** 서버 **[{setting_channel_name}]** 채널에서 사용해주세요!")

			if str(reaction) == "⭕":
				await voice_client1.disconnect()
				basicSetting[6] = ""
				basicSetting[7] = int(ctx.message.channel.id)

				print ('[ ', basicSetting[7], ' ]')
				print ('] ', ctx.message.channel.name, ' [')

				inidata_textCH = repo.get_contents("test_setting.ini")
				file_data_textCH = base64.b64decode(inidata_textCH.content)
				file_data_textCH = file_data_textCH.decode('utf-8')
				inputData_textCH = file_data_textCH.split('\n')
				
				for i in range(len(inputData_textCH)):
					if inputData_textCH[i].startswith("textchannel ="):
						inputData_textCH[i] = 'textchannel = ' + str(basicSetting[7]) + '\r'
				
				result_textCH = '\n'.join(inputData_textCH)
				
				contents = repo.get_contents("test_setting.ini")
				repo.update_file(contents.path, "test_setting", result_textCH, contents.sha)

				return await ctx.send(f"명령어 채널이 **[{ctx.author.guild.name}]** 서버 **[{ctx.message.channel.name}]** 채널로 새로 설정되었습니다.\n< 음성채널 접속 후 [{command[5][0]}] 명령을 사용 하세요 >")
			else:
				return await ctx.send(f"명령어 채널 설정이 취소되었습니다.\n**[{curr_guild_info.name}]** 서버 **[{setting_channel_name}]** 채널에서 사용해주세요!")

	################ 보탐봇 메뉴 출력 ################ 	
	@client.command(name=command[1][0], aliases=command[1][1:])
	async def menu_(ctx):
		if ctx.message.channel.id == basicSetting[7]:
			command_list = ''
			command_list += ','.join(command[2]) + '\n'     #!설정확인
			command_list += ','.join(command[3]) + '\n'     #!채널확인
			command_list += ','.join(command[4]) + ' [채널명]\n'     #!채널이동
			command_list += ','.join(command[5]) + ' ※ 관리자만 실행 가능\n'     #!소환
			command_list += ','.join(command[6]) + '\n'     #!불러오기
			command_list += ','.join(command[7]) + '\n'     #!초기화
			command_list += ','.join(command[8]) + '\n'     #!명치
			command_list += ','.join(command[9]) + '\n'     #!재시작
			command_list += ','.join(command[10]) + '\n'     #!미예약
			command_list += ','.join(command[11]) + ' [인원] [금액]\n'     #!분배
			command_list += ','.join(command[12]) + ' [뽑을인원수] [아이디1] [아이디2]...\n'     #!사다리
			command_list += ','.join(command[27]) + ' [아이디1] [아이디2]...(최대 12명)\n'     #!경주
			command_list += ','.join(command[35]) + ' [판매금액] (거래소세금)\n'     #!수수료
			command_list += ','.join(command[36]) + ' [거래소금액] [실거래금액] (거래소세금)\n'     #!페이백
			command_list += ','.join(command[13]) + ' [아이디]\n'     #!정산
			command_list += ','.join(command[14]) + ' 또는 ' + ','.join(command[14]) + ' 0000, 00:00\n'     #!보스일괄
			command_list += ','.join(command[15]) + '\n'     #!q
			command_list += ','.join(command[16]) + ' [할말]\n'     #!v
			command_list += ','.join(command[17]) + '\n'     #!리젠
			command_list += ','.join(command[18]) + '\n'     #!현재시간
			command_list += ','.join(command[24]) + '\n'     #!킬초기화
			command_list += ','.join(command[25]) + '\n'     #!킬횟수 확인
			command_list += ','.join(command[25]) + ' [아이디]\n'     #!킬
			command_list += ','.join(command[26]) + ' [아이디]\n'     #!킬삭제
			command_list += ','.join(command[33]) + ' [아이디] 또는 ' + ','.join(command[33]) + ' [아이디] [횟수]\n'     #!킬차감
			command_list += ','.join(command[29]) + '\n'     #!아이템 목록 초기화
			command_list += ','.join(command[30]) + '\n'     #!아이템 목록 확인
			command_list += ','.join(command[30]) + ' [아이템] 또는 ' + ','.join(command[30]) + ' [아이템] [개수]\n'     #!아이템 목록 입력
			command_list += ','.join(command[31]) + ' [아이템]\n'     #!아이템 목록에서 삭제
			command_list += ','.join(command[32]) + ' [아이템] 또는 ' + ','.join(command[32]) + ' [아이템] [개수]\n'     #!아이템 차감
			command_list += ','.join(command[19]) + '\n'     #!공지
			command_list += ','.join(command[19]) + ' [공지내용]\n'     #!공지
			command_list += ','.join(command[20]) + '\n'     #!공지삭제
			command_list += ','.join(command[21]) + ' [할말]\n'     #!상태
			command_list += ','.join(command[28]) + ' 사다리, 정산, 척살, 경주, 아이템\n'     #!채널설정
			command_list += ','.join(command[34]) + ' ※ 관리자만 실행 가능\n\n'     #서버나가기
			command_list += ','.join(command[22]) + '\n'     #보스탐
			command_list += ','.join(command[23]) + '\n'     #!보스탐
			command_list += '[보스명]컷 또는 [보스명]컷 0000, 00:00\n'  
			command_list += '[보스명] 컷 또는 [보스명] 컷 0000, 00:00\n'   
			command_list += '[보스명]멍 또는 [보스명]멍 0000, 00:00\n'     
			command_list += '[보스명]예상 또는 [보스명]예상 0000, 00:00\n' 
			command_list += '[보스명]삭제\n'     
			command_list += '[보스명]메모 [할말]\n'
			embed = discord.Embed(
					title = "----- 명령어 -----",
					description= '```' + command_list + '```',
					color=0xff00ff
					)
			embed.add_field(
					name="----- 추가기능 -----",
					value= '```- [보스명]컷/멍/예상  [할말] : 보스시간 입력 후 빈칸 두번!! 메모 가능\n- [보스명]컷 명령어는 초성으로 입력가능합니다.\n  ex)' + bossData[0][0] + '컷 => ' + convertToInitialLetters(bossData[0][0] +'컷') + ', ' + bossData[0][0] + ' 컷 => ' + convertToInitialLetters(bossData[0][0] +' 컷') + '```'
					)
			await ctx.send( embed=embed, tts=False)
		else:
			return

	################ 보탐봇 기본 설정확인 ################ 
	@client.command(name=command[2][0], aliases=command[2][1:])
	async def setting_(ctx):	
		#print (ctx.message.channel.id)
		if ctx.message.channel.id == basicSetting[7]:
			setting_val = '보탐봇버전 : Server Ver. 18 (2020. 7. 4.)\n'
			setting_val += '음성채널 : ' + client.get_channel(basicSetting[6]).name + '\n'
			setting_val += '텍스트채널 : ' + client.get_channel(basicSetting[7]).name +'\n'
			if basicSetting[8] != "" :
				setting_val += '사다리채널 : ' + client.get_channel(int(basicSetting[8])).name + '\n'
			if basicSetting[11] != "" :
				setting_val += '정산채널 : ' + client.get_channel(int(basicSetting[11])).name + '\n'
			if basicSetting[18] != "" :
				setting_val += '척살채널 : ' + client.get_channel(int(basicSetting[18])).name + '\n'
			if basicSetting[19] != "" :
				setting_val += '경주채널 : ' + client.get_channel(int(basicSetting[19])).name + '\n'
			if basicSetting[20] != "" :
				setting_val += '아이템채널 : ' + client.get_channel(int(basicSetting[20])).name + '\n'
			setting_val += '보스젠알림시간1 : ' + basicSetting[1] + ' 분 전\n'
			setting_val += '보스젠알림시간2 : ' + basicSetting[3] + ' 분 전\n'
			setting_val += '보스멍확인시간 : ' + basicSetting[2] + ' 분 후\n'
			embed = discord.Embed(
					title = "----- 설정내용 -----",
					description= f'```{setting_val}```',
					color=0xff00ff
					)
			embed.add_field(
					name="----- Special Thanks to. -----",
					value= '```총무님, 옹님```'
					)
			await ctx.send(embed=embed, tts=False)
		else:
			return

	################ 서버 채널 확인 ################ 
	@client.command(name=command[3][0], aliases=command[3][1:])
	async def chChk_(ctx):
		if ctx.message.channel.id == basicSetting[7]:
			channel_name, channel_id, channel_voice_name, channel_voice_id = await get_guild_channel_info()

			ch_information = []
			cnt = 0
			ch_information.append("")

			ch_voice_information = []
			cntV = 0
			ch_voice_information.append("")

			for guild in client.guilds:
				ch_information[cnt] = f"{ch_information[cnt]}👑  {guild.name}  👑\n"
				for i in range(len(channel_name)):
					for text_channel in guild.text_channels:
						if channel_id[i] == str(text_channel.id):
							if len(ch_information[cnt]) > 900 :
								ch_information.append("")
								cnt += 1
							ch_information[cnt] = f"{ch_information[cnt]}[{channel_id[i]}] {channel_name[i]}\n"

				ch_voice_information[cntV] = f"{ch_voice_information[cntV]}👑  {guild.name}  👑\n"
				for i in range(len(channel_voice_name)):
					for voice_channel in guild.voice_channels:
						if channel_voice_id[i] == str(voice_channel.id):
							if len(ch_voice_information[cntV]) > 900 :
								ch_voice_information.append("")
								cntV += 1
							ch_voice_information[cntV] = f"{ch_voice_information[cntV]}[{channel_voice_id[i]}] {channel_voice_name[i]}\n"
					
			######################

			if len(ch_information) == 1 and len(ch_voice_information) == 1:
				embed = discord.Embed(
					title = "----- 채널 정보 -----",
					description= '',
					color=0xff00ff
					)
				embed.add_field(
					name="< 택스트 채널 >",
					value= '```' + ch_information[0] + '```',
					inline = False
					)
				embed.add_field(
					name="< 보이스 채널 >",
					value= '```' + ch_voice_information[0] + '```',
					inline = False
					)

				await ctx.send( embed=embed, tts=False)
			else :
				embed = discord.Embed(
					title = "----- 채널 정보 -----\n< 택스트 채널 >",
					description= '```' + ch_information[0] + '```',
					color=0xff00ff
					)
				await ctx.send( embed=embed, tts=False)
				for i in range(len(ch_information)-1):
					embed = discord.Embed(
						title = '',
						description= '```' + ch_information[i+1] + '```',
						color=0xff00ff
						)
					await ctx.send( embed=embed, tts=False)
				embed = discord.Embed(
					title = "< 음성 채널 >",
					description= '```' + ch_voice_information[0] + '```',
					color=0xff00ff
					)
				await ctx.send( embed=embed, tts=False)
				for i in range(len(ch_voice_information)-1):
					embed = discord.Embed(
						title = '',
						description= '```' + ch_voice_information[i+1] + '```',
						color=0xff00ff
						)
					await ctx.send( embed=embed, tts=False)
		else:
			return

	################ 텍스트채널이동 ################ 
	@client.command(name=command[4][0], aliases=command[4][1:])
	async def chMove_(ctx):
		global basicSetting
		if ctx.message.channel.id == basicSetting[7]:
			msg = ctx.message.content[len(ctx.invoked_with)+1:]
			for i in range(len(channel_name)):
				if  channel_name[i] == msg:
					channel = int(channel_id[i])
					
			inidata_textCH = repo.get_contents("test_setting.ini")
			file_data_textCH = base64.b64decode(inidata_textCH.content)
			file_data_textCH = file_data_textCH.decode('utf-8')
			inputData_textCH = file_data_textCH.split('\n')
			
			for i in range(len(inputData_textCH)):
				if inputData_textCH[i].startswith('textchannel ='):
					inputData_textCH[i] = 'textchannel = ' + str(channel) + '\r'
					basicSetting[7] = int(channel)
			
			result_textCH = '\n'.join(inputData_textCH)

			contents = repo.get_contents("test_setting.ini")
			repo.update_file(contents.path, "test_setting", result_textCH, contents.sha)
			
			await ctx.send( f"명령어 채널이 < {ctx.message.channel.name} >에서 < {client.get_channel(channel).name} > 로 이동되었습니다.", tts=False)
			await client.get_channel(channel).send( f"< {client.get_channel(channel).name} 이동완료 >", tts=False)
		else:
			return

	################ 보탐봇 음성채널 소환 ################ 
	@commands.has_permissions(manage_messages=True)
	@client.command(name=command[5][0], aliases=command[5][1:])
	async def connectVoice_(ctx):
		global voice_client1
		global basicSetting
		if ctx.message.channel.id == basicSetting[7]:
			if ctx.voice_client is None:
				if ctx.author.voice:
					voice_client1 = await ctx.author.voice.channel.connect(reconnect = True)
				else:
					await ctx.send('음성채널에 먼저 들어가주세요.', tts=False)
					return
			else:
				if ctx.voice_client.is_playing():
					ctx.voice_client.stop()

				await ctx.voice_client.move_to(ctx.author.voice.channel)

			voice_channel = ctx.author.voice.channel

			print ('< ', basicSetting[6], ' >')
			print ('> ', client.get_channel(voice_channel.id).name, ' <')

			if basicSetting[6] == "":
				inidata_voiceCH = repo.get_contents("test_setting.ini")
				file_data_voiceCH = base64.b64decode(inidata_voiceCH.content)
				file_data_voiceCH = file_data_voiceCH.decode('utf-8')
				inputData_voiceCH = file_data_voiceCH.split('\n')

				for i in range(len(inputData_voiceCH)):
					if inputData_voiceCH[i].startswith('voicechannel ='):
						inputData_voiceCH[i] = 'voicechannel = ' + str(voice_channel.id) + '\r'
						basicSetting[6] = int(voice_channel.id)

				result_voiceCH = '\n'.join(inputData_voiceCH)

				contents = repo.get_contents("test_setting.ini")
				repo.update_file(contents.path, "test_setting", result_voiceCH, contents.sha)

			elif basicSetting[6] != int(voice_channel.id):
				inidata_voiceCH = repo.get_contents("test_setting.ini")
				file_data_voiceCH = base64.b64decode(inidata_voiceCH.content)
				file_data_voiceCH = file_data_voiceCH.decode('utf-8')
				inputData_voiceCH = file_data_voiceCH.split('\n')

				for i in range(len(inputData_voiceCH)):
					if inputData_voiceCH[i].startswith('voicechannel ='):
						inputData_voiceCH[i] = 'voicechannel = ' + str(voice_channel.id) + '\r'
						basicSetting[6] = int(voice_channel.id)

				result_voiceCH = '\n'.join(inputData_voiceCH)

				contents = repo.get_contents("test_setting.ini")
				repo.update_file(contents.path, "test_setting", result_voiceCH, contents.sha)

			await ctx.send('< 음성채널 [' + client.get_channel(voice_channel.id).name + '] 접속완료>', tts=False)
		else:
			return


	################ my_bot.db에 저장된 보스타임 불러오기 ################
	@client.command(name=command[6][0], aliases=command[6][1:])
	async def loadDB_(ctx):
		if ctx.message.channel.id == basicSetting[7]:
			await dbLoad()

			if LoadChk == 0:
				await ctx.send('<불러오기 완료>', tts=False)
			else:
				await ctx.send('<보스타임 정보가 없습니다.>', tts=False)
		else:
			return

	################ 저장된 정보 초기화 ################
	@client.command(name=command[7][0], aliases=command[7][1:])
	async def initVal_(ctx):
		global basicSetting
		global bossData
		global fixed_bossData

		global bossTime
		global tmp_bossTime
		global fixed_bossTime

		global bossTimeString
		global bossDateString
		global tmp_bossTimeString
		global tmp_bossDateString

		global bossFlag
		global bossFlag0
		global fixed_bossFlag
		global fixed_bossFlag0
		global bossMungFlag
		global bossMungCnt

		global FixedBossDateData
		global indexFixedBossname
			
		if ctx.message.channel.id == basicSetting[7]:
			basicSetting = []
			bossData = []
			fixed_bossData = []

			bossTime = []
			tmp_bossTime = []
			fixed_bossTime = []

			bossTimeString = []
			bossDateString = []
			tmp_bossTimeString = []
			tmp_bossDateString = []

			bossFlag = []
			bossFlag0 = []
			fixed_bossFlag = []
			fixed_bossFlag0 = []
			bossMungFlag = []
			bossMungCnt = []

			FixedBossDateData = []
			indexFixedBossname = []
			
			init()

			await dbSave()

			await ctx.send('< 초기화 완료 >', tts=False)
			print ("< 초기화 완료 >")
		else:
			return


	################ 명존쎄 ################ 
	@client.command(name=command[8][0], aliases=command[8][1:])
	async def mungchi_(ctx):
		global basicSetting
		global bossTimeString
		global bossDateString
		global bossFlag
		global bossFlag0
		global bossMungFlag

		if ctx.message.channel.id == basicSetting[7]:
			await ctx.send( '< 보탐봇 명치 맞고 숨 고르기 중! 잠시만요! >', tts=False)
			await dbSave()
			print("명치!")
			await voice_client1.disconnect()
			#client.clear()
			raise SystemExit
		else:
			return

	################ 보탐봇 재시작 ################ 
	@client.command(name=command[9][0], aliases=command[9][1:])
	async def restart_(ctx):
		global basicSetting
		global bossTimeString
		global bossDateString

		if ctx.message.channel.id == basicSetting[7]:
			if basicSetting[2] != '0':
				for i in range(bossNum):
					if bossMungFlag[i] == True:
						bossTimeString[i] = tmp_bossTime[i].strftime('%H:%M:%S')
						bossDateString[i] = tmp_bossTime[i].strftime('%Y-%m-%d')
			await dbSave()
			await data_list_Save("kill_list.ini", "-----척살명단-----", kill_Data)
			await data_list_Save("item_list.ini", "-----아이템목록-----", item_Data)
			await voice_client1.disconnect()
			#await FixedBossDateSave()
			#await client.get_channel(channel).send('<보탐봇 재시작 중... 갑자기 인사해도 놀라지마세요!>', tts=False)
			print("보탐봇강제재시작!")
			await asyncio.sleep(2)

			inidata_restart = repo_restart.get_contents("restart.txt")
			file_data_restart = base64.b64decode(inidata_restart.content)
			file_data_restart = file_data_restart.decode('utf-8')
			inputData_restart = file_data_restart.split('\n')

			if len(inputData_restart) < 3:	
				contents12 = repo_restart.get_contents("restart.txt")
				repo_restart.update_file(contents12.path, "restart_0", "restart\nrestart\nrestrat\n", contents12.sha)
			else:
				contents12 = repo_restart.get_contents("restart.txt")
				repo_restart.update_file(contents12.path, "restart_1", "", contents12.sha)
		else:
			return

	################ 미예약 보스타임 출력 ################ 
	@client.command(name=command[10][0], aliases=command[10][1:])
	async def nocheckBoss_(ctx):
		if ctx.message.channel.id == basicSetting[7]:
			tmp_boss_information = []
			tmp_cnt = 0
			tmp_boss_information.append('')
			
			for i in range(bossNum):
				if bossTimeString[i] == '99:99:99' and bossMungFlag[i] != True :
					if len(tmp_boss_information[tmp_cnt]) > 1800 :
						tmp_boss_information.append('')
						tmp_cnt += 1
					tmp_boss_information[tmp_cnt] = tmp_boss_information[tmp_cnt] + bossData[i][0] + ','

			if len(tmp_boss_information) == 1:
				if len(tmp_boss_information[0]) != 0:
					tmp_boss_information[0] = "```fix\n" + tmp_boss_information[0][:len(tmp_boss_information[0])-1] + "\n```"
				else :
					tmp_boss_information[0] = '``` ```'

				embed = discord.Embed(
						title = "----- 미예약 보스 -----",
						description= tmp_boss_information[0],
						color=0x0000ff
						)
				await ctx.send( embed=embed, tts=False)
			else:
				if len(tmp_boss_information[0]) != 0:
					if len(tmp_boss_information) == 1 :
						tmp_boss_information[0] = "```fix\n" + tmp_boss_information[0][:len(tmp_boss_information[0])-1] + "\n```"
					else:
						tmp_boss_information[0] = "```fix\n" + tmp_boss_information[0] + "\n```"
				else :
					tmp_boss_information[0] = '``` ```'

				embed = discord.Embed(
					title = "----- 미예약 보스 -----",
					description= tmp_boss_information[0],
					color=0x0000ff
					)
				await ctx.send( embed=embed, tts=False)
				for i in range(len(tmp_boss_information)-1):
					if len(tmp_boss_information[i+1]) != 0:
						if i == len(tmp_boss_information)-2:
							tmp_boss_information[i+1] = "```fix\n" + tmp_boss_information[i+1][:len(tmp_boss_information[i+1])-1] + "\n```"
						else:
							tmp_boss_information[i+1] = "```fix\n" + tmp_boss_information[i+1] + "\n```"							
					else :
						tmp_boss_information[i+1] = '``` ```'

					embed = discord.Embed(
							title = '',
							description= tmp_boss_information[i+1],
							color=0x0000ff
							)
					await ctx.send( embed=embed, tts=False)
		else:
			return

	################ 분배 결과 출력 ################ 
	@client.command(name=command[11][0], aliases=command[11][1:])
	async def bunbae_(ctx):
		if ctx.message.channel.id == basicSetting[7]:
			msg = ctx.message.content[len(ctx.invoked_with)+1:]
			separate_money = []
			separate_money = msg.split(" ")
			num_sep = floor(int(separate_money[0]))
			cal_tax1 = floor(float(separate_money[1])*0.05)
			
			real_money = floor(floor(float(separate_money[1])) - cal_tax1)
			cal_tax2 = floor(real_money/num_sep) - floor(float(floor(real_money/num_sep))*0.95)
			if num_sep == 0 :
				await ctx.send('```분배 인원이 0입니다. 재입력 해주세요.```', tts=False)
			else :
				embed = discord.Embed(
					title = "----- 분배결과! -----",
					description= '```1차 세금 : ' + str(cal_tax1) + '\n1차 수령액 : ' + str(real_money) + '\n분배자 거래소등록금액 : ' + str(floor(real_money/num_sep)) + '\n2차 세금 : ' + str(cal_tax2) + '\n인당 실수령액 : ' + str(floor(float(floor(real_money/num_sep))*0.95)) + '```',
					color=0xff00ff
					)
				await ctx.send(embed=embed, tts=False)
		else:
			return

	################ 사다리 결과 출력 ################ 
	@client.command(name=command[12][0], aliases=command[12][1:])
	async def ladder_(ctx):
		if ctx.message.channel.id == basicSetting[7] or ctx.message.channel.id == basicSetting[8]:
			msg = ctx.message.content[len(ctx.invoked_with)+1:]
			ladder = []
			ladder = msg.split(" ")
			try:
				num_cong = int(ladder[0])
				del(ladder[0])
			except ValueError:
				return await ctx.send('```뽑을 인원은 숫자로 입력바랍니다\nex)!사다리 1 가 나 다 ...```')
			await LadderFunc(num_cong, ladder, ctx)
		else:
			return

	################ 정산확인 ################ 
	@client.command(name=command[13][0], aliases=command[13][1:])
	async def jungsan_(ctx):
		if ctx.message.channel.id == basicSetting[7] or ctx.message.channel.id == basicSetting[11]:
			msg = ctx.message.content[len(ctx.invoked_with)+1:]
			if basicSetting[10] !="" and basicSetting[12] !="" and basicSetting[14] !="" and basicSetting[15] !="" and basicSetting[16] !=""  :
				SearchID = msg
				gc = gspread.authorize(credentials)
				wks = gc.open(basicSetting[12]).worksheet(basicSetting[14])

				wks.update_acell(basicSetting[15], SearchID)

				result = wks.acell(basicSetting[16]).value

				embed = discord.Embed(
						description= '```' + SearchID + ' 님이 받을 다이야는 ' + result + ' 다이야 입니다.```',
						color=0xff00ff
						)
				await ctx.send(embed=embed, tts=False)
		else:
			return

	################ 보스타임 일괄 설정 ################
	@client.command(name=command[14][0], aliases=command[14][1:])
	async def allBossInput_(ctx):
		global basicSetting
		global bossData
		global fixed_bossData

		global bossTime
		global tmp_bossTime

		global fixed_bossTime

		global bossTimeString
		global bossDateString
		global tmp_bossTimeString
		global tmp_bossDateString

		global bossFlag
		global bossFlag0
		global bossMungFlag
		global bossMungCnt
		
		if ctx.message.channel.id == basicSetting[7]:
			msg = ctx.message.content[len(ctx.invoked_with)+1:]
			for i in range(bossNum):
				tmp_msg = msg
				if len(tmp_msg) > 3 :
					if tmp_msg.find(':') != -1 :
						chkpos = tmp_msg.find(':')
						hours1 = tmp_msg[chkpos-2:chkpos]
						minutes1 = tmp_msg[chkpos+1:chkpos+3]
						now2 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
						tmp_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
						tmp_now = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
					else:
						chkpos = len(tmp_msg)-2
						hours1 = tmp_msg[chkpos-2:chkpos]
						minutes1 = tmp_msg[chkpos:chkpos+2]
						now2 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
						tmp_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
						tmp_now = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
				else:
					now2 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
					tmp_now = now2
					
				bossFlag[i] = False
				bossFlag0[i] = False
				bossMungFlag[i] = False
				bossMungCnt[i] = 1

				if tmp_now > now2 :
					tmp_now = tmp_now + datetime.timedelta(days=int(-1))
					
				if tmp_now < now2 : 
					deltaTime = datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))
					while now2 > tmp_now :
						tmp_now = tmp_now + deltaTime
						bossMungCnt[i] = bossMungCnt[i] + 1
					now2 = tmp_now
					bossMungCnt[i] = bossMungCnt[i] - 1
				else :
					now2 = now2 + datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))
							
				tmp_bossTime[i] = bossTime[i] = nextTime = now2
				tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
				tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')

			await dbSave()
			await dbLoad()
			await dbSave()
			
			await ctx.send('<보스 일괄 입력 완료>', tts=False)
			print ("<보스 일괄 입력 완료>")
		else:
			return


	################ 가장 근접한 보스타임 출력 ################ 
	@client.command(name=command[15][0], aliases=command[15][1:])
	async def nearTimeBoss_(ctx):
		if ctx.message.channel.id == basicSetting[7]:
			checkTime = datetime.datetime.now() + datetime.timedelta(days=1, hours = int(basicSetting[0]))
			
			datelist = []
			datelist2 = []
			ouput_bossData = []
			aa = []
			sorted_datelist = []

			for i in range(bossNum):
				if bossMungFlag[i] != True and bossTimeString[i] != '99:99:99' :
					datelist2.append(bossTime[i])

			for i in range(fixed_bossNum):
				if fixed_bossTime[i] < datetime.datetime.now() + datetime.timedelta(hours=int(basicSetting[0])+3):
					datelist2.append(fixed_bossTime[i])

			datelist = list(set(datelist2))

			for i in range(bossNum):
				if bossMungFlag[i] != True :
					aa.append(bossData[i][0])		                 #output_bossData[0] : 보스명
					aa.append(bossTime[i])                           #output_bossData[1] : 시간
					aa.append(bossTime[i].strftime('%H:%M:%S'))      #output_bossData[2] : 시간(00:00:00)
					ouput_bossData.append(aa)
				aa = []

			for i in range(fixed_bossNum):
				aa.append(fixed_bossData[i][0])                      #output_bossData[0] : 보스명
				aa.append(fixed_bossTime[i])                         #output_bossData[1] : 시간
				aa.append(fixed_bossTime[i].strftime('%H:%M:%S'))    #output_bossData[2] : 시간(00:00:00)
				ouput_bossData.append(aa)
				aa = []

			tmp_sorted_datelist = sorted(datelist)

			for i in range(len(tmp_sorted_datelist)):
				if checkTime > tmp_sorted_datelist[i]:
					sorted_datelist.append(tmp_sorted_datelist[i])
			
			if len(sorted_datelist) == 0:
				await ctx.send( '<보스타임 정보가 없습니다.>', tts=False)
			else : 
				result_lefttime = ''
				
				if len(sorted_datelist) > int(basicSetting[9]):
					for j in range(int(basicSetting[9])):
						for i in range(len(ouput_bossData)):
							if sorted_datelist[j] == ouput_bossData[i][1]:
								leftTime = ouput_bossData[i][1] - (datetime.datetime.now()  + datetime.timedelta(hours = int(basicSetting[0])))

								total_seconds = int(leftTime.total_seconds())
								hours, remainder = divmod(total_seconds,60*60)
								minutes, seconds = divmod(remainder,60)

								result_lefttime += '다음 ' + ouput_bossData[i][0] + '탐까지 %02d:%02d:%02d 남았습니다. ' % (hours,minutes,seconds) + '[' +  ouput_bossData[i][2] + ']\n'
				else :
					for j in range(len(sorted_datelist)):
						for i in range(len(ouput_bossData)):						
							if sorted_datelist[j] == ouput_bossData[i][1]:
								leftTime = ouput_bossData[i][1] - (datetime.datetime.now()  + datetime.timedelta(hours = int(basicSetting[0])))

								total_seconds = int(leftTime.total_seconds())
								hours, remainder = divmod(total_seconds,60*60)
								minutes, seconds = divmod(remainder,60)

								result_lefttime += '다음 ' + ouput_bossData[i][0] + '탐까지 %02d:%02d:%02d 남았습니다. ' % (hours,minutes,seconds) + '[' +  ouput_bossData[i][2] + ']\n'
				embed = discord.Embed(
					description= result_lefttime,
					color=0xff0000
					)
				await ctx.send( embed=embed, tts=False)
		else:
			return

	################ 음성파일 생성 후 재생 ################ 			
	@client.command(name=command[16][0], aliases=command[16][1:])
	async def playText_(ctx):
		if ctx.message.channel.id == basicSetting[7]:
			msg = ctx.message.content[len(ctx.invoked_with)+1:]
			sayMessage = msg
			await MakeSound(ctx.message.author.display_name +'님이, ' + sayMessage, './sound/say')
			await ctx.send("```< " + ctx.author.display_name + " >님이 \"" + sayMessage + "\"```", tts=False)
			await PlaySound(voice_client1, './sound/say.wav')
		else:
			return

	################ 리젠시간 출력 ################
	@client.command(name=command[17][0], aliases=command[17][1:])
	async def regenTime_(ctx):
		if ctx.message.channel.id == basicSetting[7]:
			await ctx.send(embed=regenembed, tts=False)
		else:
			return
			
	################ 현재시간 확인 ################ 
	@client.command(name=command[18][0], aliases=command[18][1:])
	async def currentTime_(ctx):
		if ctx.message.channel.id == basicSetting[7]:
			curruntTime = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
			embed = discord.Embed(
				title = '현재시간은 ' + curruntTime.strftime('%H') + '시 ' + curruntTime.strftime('%M') + '분 ' + curruntTime.strftime('%S')+ '초 입니다.',
				color=0xff00ff
				)
			await ctx.send( embed=embed, tts=False)
		else:
			return

	################ 공지 등록/확인 ################ 
	@client.command(name=command[19][0], aliases=command[19][1:])
	async def notice_(ctx):
		if ctx.message.channel.id == basicSetting[7]:
			msg = ctx.message.content.split(" ")
			if len(msg) > 1:
				sayMessage = " ".join(msg[1:])
				contents = repo.get_contents("notice.ini")
				repo.update_file(contents.path, "notice 등록", sayMessage, contents.sha)
				await ctx.send( '< 공지 등록완료 >', tts=False)
			else:
				notice_initdata = repo.get_contents("notice.ini")
				notice = base64.b64decode(notice_initdata.content)
				notice = notice.decode('utf-8')
				if notice != '' :
					embed = discord.Embed(
							description= str(notice),
							color=0xff00ff
							)
				else :
					embed = discord.Embed(
							description= '```등록된 공지가 없습니다.```',
							color=0xff00ff
							)
				await ctx.send(embed=embed, tts=False)
		else:
			return

	################ 공지 삭제 ################ 
	@client.command(name=command[20][0], aliases=command[20][1:])
	async def noticeDel_(ctx):
		if ctx.message.channel.id == basicSetting[7]:
			contents = repo.get_contents("notice.ini")
			repo.update_file(contents.path, "notice 삭제", '', contents.sha)
			await ctx.send( '< 공지 삭제완료 >', tts=False)
		else:
			return

	################ 봇 상태메세지 변경 ################ 
	@client.command(name=command[21][0], aliases=command[21][1:])
	async def botStatus_(ctx):
		if ctx.message.channel.id == basicSetting[7]:
			msg = ctx.message.content[len(ctx.invoked_with)+1:]
			sayMessage = msg
			await client.change_presence(status=discord.Status.dnd, activity=discord.Game(name=sayMessage, type=1), afk = False)
			await ctx.send( '< 상태메세지 변경완료 >', tts=False)
		else:
			return

	################ 보스타임 출력 ################ 
	@client.command(name=command[22][0], aliases=command[22][1:])
	async def bossTime_(ctx):
		if ctx.message.channel.id == basicSetting[7]:
			datelist = []
			datelist2 = []
			ouput_bossData = []
			aa = []
			
			for i in range(bossNum):
				if bossMungFlag[i] == True :
					datelist2.append(tmp_bossTime[i])
				else :
					datelist2.append(bossTime[i])

			for i in range(fixed_bossNum):
				if fixed_bossTime[i] < datetime.datetime.now() + datetime.timedelta(hours=int(basicSetting[0])+3):
					datelist2.append(fixed_bossTime[i])

			datelist = list(set(datelist2))

			tmp_boss_information = []
			tmp_cnt = 0
			tmp_boss_information.append('')

			for i in range(bossNum):
				if bossTimeString[i] == '99:99:99' and bossMungFlag[i] != True :
					if len(tmp_boss_information[tmp_cnt]) > 1000 :
						tmp_boss_information.append('')
						tmp_cnt += 1
					tmp_boss_information[tmp_cnt] = tmp_boss_information[tmp_cnt] + bossData[i][0] + ','
				else :
					aa.append(bossData[i][0])		                     #output_bossData[0] : 보스명
					if bossMungFlag[i] == True :
						aa.append(tmp_bossTime[i])                       #output_bossData[1] : 시간
						aa.append(tmp_bossTime[i].strftime('%H:%M:%S'))  #output_bossData[2] : 시간(00:00:00) -> 초빼기 : aa.append(tmp_bossTime[i].strftime('%H:%M'))  
						aa.append('-')	                                 #output_bossData[3] : -
					else :
						aa.append(bossTime[i])                           #output_bossData[1] : 시간
						aa.append(bossTime[i].strftime('%H:%M:%S'))      #output_bossData[2] : 시간(00:00:00) -> 초빼기 : aa.append(bossTime[i].strftime('%H:%M'))  
						aa.append('+')	                                 #output_bossData[3] : +
					aa.append(bossData[i][2])                            #output_bossData[4] : 멍/미입력 보스
					aa.append(bossMungCnt[i])	                         #output_bossData[5] : 멍/미입력횟수
					aa.append(bossData[i][6])	                         #output_bossData[6] : 메세지
					ouput_bossData.append(aa)
					aa = []

			for i in range(fixed_bossNum):
				aa.append(fixed_bossData[i][0])                      #output_bossData[0] : 보스명
				aa.append(fixed_bossTime[i])                         #output_bossData[1] : 시간
				aa.append(fixed_bossTime[i].strftime('%H:%M:%S'))    #output_bossData[2] : 시간(00:00:00) -> 초빼기 : aa.append(fixed_bossTime[i].strftime('%H:%M'))
				aa.append('@')                                       #output_bossData[3] : @
				aa.append(0)                                         #output_bossData[4] : 멍/미입력 보스
				aa.append(0)                                         #output_bossData[5] : 멍/미입력횟수
				aa.append("")                                        #output_bossData[6] : 메세지
				ouput_bossData.append(aa)
				aa = []

			boss_information = []
			cnt = 0
			boss_information.append('')

			for timestring in sorted(datelist):
				if len(boss_information[cnt]) > 1800 :
					boss_information.append('')
					cnt += 1
				for i in range(len(ouput_bossData)):
					if timestring == ouput_bossData[i][1]:
						if ouput_bossData[i][4] == '0' :
							if ouput_bossData[i][5] == 0 :
								boss_information[cnt] = boss_information[cnt] + ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' ' + ouput_bossData[i][6] + '\n'
							else :
								boss_information[cnt] = boss_information[cnt] + ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' (미 ' + str(ouput_bossData[i][5]) + '회)' + ' ' + ouput_bossData[i][6] + '\n'
						else : 
							if ouput_bossData[i][5] == 0 :
								boss_information[cnt] = boss_information[cnt] + ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' ' + ouput_bossData[i][6] + '\n'
							else :
								boss_information[cnt] = boss_information[cnt] + ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' (멍 ' + str(ouput_bossData[i][5]) + '회)' + ' ' + ouput_bossData[i][6] + '\n'

			if len(boss_information) == 1 and len(tmp_boss_information) == 1:
				###########################
				if len(boss_information[0]) != 0:
					boss_information[0] = "```diff\n" + boss_information[0] + "\n```"
				else :
					boss_information[0] = '``` ```'

				if len(tmp_boss_information[0]) != 0:
					tmp_boss_information[0] = "```fix\n" + tmp_boss_information[0][:len(tmp_boss_information[0])-1] + "\n```"
				else :
					tmp_boss_information[0] = '``` ```'

				embed = discord.Embed(
						title = "----- 보스탐 정보 -----",
						description= boss_information[0],
						color=0x0000ff
						)
				embed.add_field(
						name="----- 미예약 보스 -----",
						value= tmp_boss_information[0],
						inline = False
						)				
				await ctx.send( embed=embed, tts=False)
			else : 
				###########################일반보스출력
				if len(boss_information[0]) != 0:
					boss_information[0] = "```diff\n" + boss_information[0] + "\n```"
				else :
					boss_information[0] = '``` ```'

				embed = discord.Embed(
						title = "----- 보스탐 정보 -----",
						description= boss_information[0],
						color=0x0000ff
						)
				await ctx.send( embed=embed, tts=False)
				for i in range(len(boss_information)-1):
					if len(boss_information[i+1]) != 0:
						boss_information[i+1] = "```diff\n" + boss_information[i+1] + "\n```"
					else :
						boss_information[i+1] = '``` ```'

					embed = discord.Embed(
							title = '',
							description= boss_information[i+1],
							color=0x0000ff
							)
					await ctx.send( embed=embed, tts=False)
				###########################미예약보스출력
				if len(tmp_boss_information[0]) != 0:
					if len(tmp_boss_information) == 1 :
						tmp_boss_information[0] = "```fix\n" + tmp_boss_information[0][:len(tmp_boss_information[0])-1] + "\n```"
					else:
						tmp_boss_information[0] = "```fix\n" + tmp_boss_information[0] + "\n```"
				else :
					tmp_boss_information[0] = '``` ```'

				embed = discord.Embed(
					title = "----- 미예약 보스 -----",
					description= tmp_boss_information[0],
					color=0x0000ff
					)
				await ctx.send( embed=embed, tts=False)
				for i in range(len(tmp_boss_information)-1):
					if len(tmp_boss_information[i+1]) != 0:
						if i == len(tmp_boss_information)-2:
							tmp_boss_information[i+1] = "```fix\n" + tmp_boss_information[i+1][:len(tmp_boss_information[i+1])-1] + "\n```"
						else:
							tmp_boss_information[i+1] = "```fix\n" + tmp_boss_information[i+1] + "\n```"							
					else :
						tmp_boss_information[i+1] = '``` ```'

					embed = discord.Embed(
							title = '',
							description= tmp_boss_information[i+1],
							color=0x0000ff
							)
					await ctx.send( embed=embed, tts=False)

			await dbSave()
			await data_list_Save("kill_list.ini", "-----척살명단-----", kill_Data)
			await data_list_Save("item_list.ini", "-----아이템목록-----", item_Data)
		else:
			return

	################ 보스타임 출력(고정보스포함) ################ 
	@client.command(name=command[23][0], aliases=command[23][1:])
	async def bossTime_fixed_(ctx):
		if ctx.message.channel.id == basicSetting[7]:
			datelist = []
			datelist2 = []
			ouput_bossData = []
			aa = []
			fixed_datelist = []
			
			for i in range(bossNum):
				if bossMungFlag[i] == True :
					datelist2.append(tmp_bossTime[i])
				else :
					datelist2.append(bossTime[i])

			datelist = list(set(datelist2))

			tmp_boss_information = []
			tmp_cnt = 0
			tmp_boss_information.append('')

			for i in range(bossNum):
				if bossTimeString[i] == '99:99:99' and bossMungFlag[i] != True :
					if len(tmp_boss_information[tmp_cnt]) > 1800 :
						tmp_boss_information.append('')
						tmp_cnt += 1
					tmp_boss_information[tmp_cnt] = tmp_boss_information[tmp_cnt] + bossData[i][0] + ','
				else :
					aa.append(bossData[i][0])		                     #output_bossData[0] : 보스명
					if bossMungFlag[i] == True :
						aa.append(tmp_bossTime[i])                       #output_bossData[1] : 시간
						aa.append(tmp_bossTime[i].strftime('%H:%M:%S'))  #output_bossData[2] : 시간(00:00:00) -> 초빼기 : aa.append(tmp_bossTime[i].strftime('%H:%M'))
						aa.append('-')	                                 #output_bossData[3] : -
					else :
						aa.append(bossTime[i])                           #output_bossData[1] : 시간
						aa.append(bossTime[i].strftime('%H:%M:%S'))      #output_bossData[2] : 시간(00:00:00) -> 초빼기 : aa.append(bossTime[i].strftime('%H:%M'))
						aa.append('+')	                                 #output_bossData[3] : +
					aa.append(bossData[i][2])                            #output_bossData[4] : 멍/미입력 보스
					aa.append(bossMungCnt[i])	                         #output_bossData[5] : 멍/미입력횟수
					aa.append(bossData[i][6])	                         #output_bossData[6] : 메세지
					ouput_bossData.append(aa)
					aa = []

			for i in range(fixed_bossNum):
				fixed_datelist.append(fixed_bossTime[i])

			fixed_datelist = list(set(fixed_datelist))

			fixedboss_information = []
			cntF = 0
			fixedboss_information.append('')
					
			for timestring1 in sorted(fixed_datelist):
				if len(fixedboss_information[cntF]) > 1800 :
					fixedboss_information.append('')
					cntF += 1
				for i in range(fixed_bossNum):
					if timestring1 == fixed_bossTime[i]:
						if (datetime.datetime.now() + datetime.timedelta(hours=int(basicSetting[0]))).strftime('%Y-%m-%d') == fixed_bossTime[i].strftime('%Y-%m-%d'):
							tmp_timeSTR = fixed_bossTime[i].strftime('%H:%M:%S') #초빼기 : tmp_timeSTR = fixed_bossTime[i].strftime('%H:%M')
						else:
							tmp_timeSTR = '[' + fixed_bossTime[i].strftime('%Y-%m-%d') + '] ' + fixed_bossTime[i].strftime('%H:%M:%S') #초빼기 : tmp_timeSTR = '[' + fixed_bossTime[i].strftime('%Y-%m-%d') + '] ' + fixed_bossTime[i].strftime('%H:%M')
						fixedboss_information[cntF] = fixedboss_information[cntF] + tmp_timeSTR + ' : ' + fixed_bossData[i][0] + '\n'

			boss_information = []
			cnt = 0
			boss_information.append('')

			for timestring in sorted(datelist):
				if len(boss_information[cnt]) > 1800 :
					boss_information.append('')
					cnt += 1
				for i in range(len(ouput_bossData)):
					if timestring == ouput_bossData[i][1]:
						if ouput_bossData[i][4] == '0' :
							if ouput_bossData[i][5] == 0 :
								boss_information[cnt] = boss_information[cnt] + ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' ' + ouput_bossData[i][6] + '\n'
							else :
								boss_information[cnt] = boss_information[cnt] + ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' (미 ' + str(ouput_bossData[i][5]) + '회)' + ' ' + ouput_bossData[i][6] + '\n'
						else : 
							if ouput_bossData[i][5] == 0 :
								boss_information[cnt] = boss_information[cnt] + ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' ' + ouput_bossData[i][6] + '\n'
							else :
								boss_information[cnt] = boss_information[cnt] + ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' (멍 ' + str(ouput_bossData[i][5]) + '회)' + ' ' + ouput_bossData[i][6] + '\n'

			###########################고정보스출력
			if len(fixedboss_information[0]) != 0:
				fixedboss_information[0] = "```diff\n" + fixedboss_information[0] + "\n```"
			else :
				fixedboss_information[0] = '``` ```'
	
			embed = discord.Embed(
					title = "----- 고 정 보 스 -----",
					description= fixedboss_information[0],
					color=0x0000ff
					)
			await ctx.send( embed=embed, tts=False)
			for i in range(len(fixedboss_information)-1):
				if len(fixedboss_information[i+1]) != 0:
					fixedboss_information[i+1] = "```diff\n" + fixedboss_information[i+1] + "\n```"
				else :
					fixedboss_information[i+1] = '``` ```'

				embed = discord.Embed(
						title = '',
						description= fixedboss_information[i+1],
						color=0x0000ff
						)
				await ctx.send( embed=embed, tts=False)

			###########################일반보스출력
			if len(boss_information[0]) != 0:
				boss_information[0] = "```diff\n" + boss_information[0] + "\n```"
			else :
				boss_information[0] = '``` ```'

			embed = discord.Embed(
					title = "----- 보스탐 정보 -----",
					description= boss_information[0],
					color=0x0000ff
					)
			await ctx.send( embed=embed, tts=False)
			for i in range(len(boss_information)-1):
				if len(boss_information[i+1]) != 0:
					boss_information[i+1] = "```diff\n" + boss_information[i+1] + "\n```"
				else :
					boss_information[i+1] = '``` ```'

				embed = discord.Embed(
						title = '',
						description= boss_information[i+1],
						color=0x0000ff
						)
				await ctx.send( embed=embed, tts=False)

			###########################미예약보스출력
			if len(tmp_boss_information[0]) != 0:
				if len(tmp_boss_information) == 1 :
					tmp_boss_information[0] = "```fix\n" + tmp_boss_information[0][:len(tmp_boss_information[0])-1] + "\n```"
				else:
					tmp_boss_information[0] = "```fix\n" + tmp_boss_information[0] + "\n```"
			else :
				tmp_boss_information[0] = '``` ```'

			embed = discord.Embed(
				title = "----- 미예약 보스 -----",
				description= tmp_boss_information[0],
				color=0x0000ff
				)
			await ctx.send( embed=embed, tts=False)
			for i in range(len(tmp_boss_information)-1):
				if len(tmp_boss_information[i+1]) != 0:
					if i == len(tmp_boss_information)-2:
						tmp_boss_information[i+1] = "```fix\n" + tmp_boss_information[i+1][:len(tmp_boss_information[i+1])-1] + "\n```"
					else:
						tmp_boss_information[i+1] = "```fix\n" + tmp_boss_information[i+1] + "\n```"
				else :
					tmp_boss_information[i+1] = '``` ```'

				embed = discord.Embed(
						title = '',
						description= tmp_boss_information[i+1],
						color=0x0000ff
						)
				await ctx.send( embed=embed, tts=False)

			await dbSave()
			await data_list_Save("kill_list.ini", "-----척살명단-----", kill_Data)
			await data_list_Save("item_list.ini", "-----아이템목록-----", item_Data)
		else:
			return

	################ 킬초기화 ################ 
	@client.command(name=command[24][0], aliases=command[24][1:])
	async def killInit_(ctx):
		if ctx.message.channel.id == basicSetting[7] or ctx.message.channel.id == basicSetting[18]:
			global kill_Data

			kill_Data = {}
			
			await init_data_list('kill_list.ini', '-----척살명단-----')
			return await ctx.send( '< 킬 목록 초기화완료 >', tts=False)
		else:
			return

	################ 킬명단 확인 및 추가################ 
	@client.command(name=command[25][0], aliases=command[25][1:]) 
	async def killList_(ctx, *, args : str = None):
		if ctx.message.channel.id == basicSetting[7] or ctx.message.channel.id == basicSetting[18]:
			global kill_Data

			if not args:
				kill_output = ''
				for key, value in kill_Data.items():
					kill_output += ':skull_crossbones: ' + str(key) + ' : ' + str(value) + '번 따히!\n'

				if kill_output != '' :
					embed = discord.Embed(
							description= str(kill_output),
							color=0xff00ff
							)
				else :
					embed = discord.Embed(
							description= '등록된 킬 목록이 없습니다. 분발하세요!',
							color=0xff00ff
							)
				return await ctx.send(embed=embed, tts=False)

			if args in kill_Data:
				kill_Data[args] += 1
			else:
				kill_Data[args] = 1
					
			embed = discord.Embed(
					description= ':skull_crossbones: ' + args + ' 따히! [' + str(kill_Data[args]) + '번]\n',
					color=0xff00ff
					)
			return await ctx.send(embed=embed, tts=False)
		else:
			return

	################ 킬삭제 ################ 
	@client.command(name=command[26][0], aliases=command[26][1:])
	async def killDel_(ctx, *, args : str = None):
		if ctx.message.channel.id == basicSetting[7] or ctx.message.channel.id == basicSetting[18]:
			global kill_Data
			
			if not args:
				return await ctx.send( '```제대로 된 아이디를 입력해주세요!\n```', tts=False)
			
			if args in kill_Data:
				del kill_Data[args]
				return await ctx.send( ':angel: ' + args + ' 삭제완료!', tts=False)
			else :				
				return await ctx.send( '```킬 목록에 등록되어 있지 않습니다!\n```', tts=False)
		else:
			return

	################ 킬 차감 ################ 
	@client.command(name=command[33][0], aliases=command[33][1:]) 
	async def killSubtract_(ctx, *, args : str = None):
		if ctx.message.channel.id == basicSetting[7] or ctx.message.channel.id == basicSetting[18]:
			global kill_Data

			if not args:
				return await ctx.send(f'{command[33][0]} [아이디] 혹은 {command[33][0]} [아이디] [횟수] 양식에 맞춰 입력해주세요!', tts = False)

			input_data = args.split()
			
			if len(input_data) == 1:
				kill_name = args
				count = 1
			elif len(input_data) == 2:
				kill_name = input_data[0]
				try:
					count = int(input_data[1])
				except ValueError:
					return await ctx.send(f'[횟수]는 숫자로 입력바랍니다')
			else:
				return await ctx.send(f'{command[33][0]} [아이디] 혹은 {command[33][0]} [아이디] [횟수] 양식에 맞춰 입력해주세요!', tts = False)

			if kill_name in kill_Data:
				if kill_Data[kill_name] < int(count):
					return await ctx.send( f"등록된 킬 횟수[{str(kill_Data[kill_name])}번]보다 차감 횟수[{str(count)}번]가 많습니다. 킬 횟수에 맞게 재입력 바랍니다.", tts=False)
				else:
					kill_Data[kill_name] -= int(count)
			else:
				return await ctx.send( '```킬 목록에 등록되어 있지 않습니다!\n```', tts=False)
					
			embed = discord.Embed(
					description= f':angel: [{kill_name}] [{str(count)}번] 차감 완료! [잔여 : {str(kill_Data[kill_name])}번]\n',
					color=0xff00ff
					)
			
			if kill_Data[kill_name] == 0:
				del kill_Data[kill_name]

			return await ctx.send(embed=embed, tts=False)
		else:
			return

	################ 경주 ################ 
	@client.command(name=command[27][0], aliases=command[27][1:])
	async def race_(ctx):
		if ctx.message.channel.id == basicSetting[7] or ctx.message.channel.id == basicSetting[19]:
			msg = ctx.message.content[len(ctx.invoked_with)+1:]
			race_info = []
			fr = []
			racing_field = []
			str_racing_field = []
			cur_pos = []
			race_val = []
			random_pos = []
			racing_result = []
			output = ':camera: :camera: :camera: 신나는 레이싱! :camera: :camera: :camera:\n'
			#racing_unit = [':giraffe:', ':elephant:', ':tiger2:', ':hippopotamus:', ':crocodile:',':leopard:',':ox:', ':sheep:', ':pig2:',':dromedary_camel:',':dragon:',':rabbit2:'] #동물스킨
			#racing_unit = [':red_car:', ':taxi:', ':bus:', ':trolleybus:', ':race_car:', ':police_car:', ':ambulance:', ':fire_engine:', ':minibus:', ':truck:', ':articulated_lorry:', ':tractor:', ':scooter:', ':manual_wheelchair:', ':motor_scooter:', ':auto_rickshaw:', ':blue_car:', ':bike:', ':helicopter:', ':steam_locomotive:']  #탈것스킨
			#random.shuffle(racing_unit) 
			racing_member = msg.split(" ")

			racing_unit = []

			emoji = discord.Emoji
			emoji = ctx.message.guild.emojis

			for j in range(len(tmp_racing_unit)):
				racing_unit.append(':' + tmp_racing_unit[j] + ':')
				for i in range(len(emoji)):
					if emoji[i].name == tmp_racing_unit[j].strip(":"):
						racing_unit[j] = '<:' + tmp_racing_unit[j] + ':' + str(emoji[i].id) + '>'

			random.shuffle(racing_unit)

			field_size = 60
			tmp_race_tab = 35 - len(racing_member)
			if len(racing_member) <= 1:
				await ctx.send('레이스 인원이 2명보다 작습니다.')
				return
			elif len(racing_member) >= 13:
				await ctx.send('레이스 인원이 12명 초과입니다.')
				return
			else :
				race_val = random.sample(range(tmp_race_tab, tmp_race_tab+len(racing_member)), len(racing_member))
				random.shuffle(race_val)
				for i in range(len(racing_member)):
					fr.append(racing_member[i])
					fr.append(racing_unit[i])
					fr.append(race_val[i])
					race_info.append(fr)
					fr = []
					for i in range(field_size):
						fr.append(" ")
					racing_field.append(fr)
					fr = []

				for i in range(len(racing_member)):
					racing_field[i][0] = "|"
					racing_field[i][field_size-2] = race_info[i][1]
					if len(race_info[i][0]) > 5:
						racing_field[i][field_size-1] = "| " + race_info[i][0][:5] + '..'
					else:
						racing_field[i][field_size-1] = "| " + race_info[i][0]
					str_racing_field.append("".join(racing_field[i]))
					cur_pos.append(field_size-2)
				
				for i in range(len(racing_member)):
					output +=  str_racing_field[i] + '\n'

				result_race = await ctx.send(output + ':traffic_light: 3초 후 경주가 시작됩니다!')
				await asyncio.sleep(1)
				await result_race.edit(content = output + ':traffic_light: 2초 후 경주가 시작됩니다!')
				await asyncio.sleep(1)
				await result_race.edit(content = output + ':traffic_light: 1초 후 경주가 시작됩니다!')
				await asyncio.sleep(1)
				await result_race.edit(content = output + ':checkered_flag:  경주 시작!')								

				for i in range(len(racing_member)):
					test = random.sample(range(2,field_size-2), race_info[i][2])
					while len(test) != tmp_race_tab + len(racing_member)-1 :
						test.append(1)
					test.append(1)
					test.sort(reverse=True)
					random_pos.append(test)

				for j in range(len(random_pos[0])):
					if j%2 == 0:
						output =  ':camera: :camera_with_flash: :camera: 신나는 레이싱! :camera_with_flash: :camera: :camera_with_flash:\n'
					else :
						output =  ':camera_with_flash: :camera: :camera_with_flash: 신나는 레이싱! :camera: :camera_with_flash: :camera:\n'
					str_racing_field = []
					for i in range(len(racing_member)):
						temp_pos = cur_pos[i]
						racing_field[i][random_pos[i][j]], racing_field[i][temp_pos] = racing_field[i][temp_pos], racing_field[i][random_pos[i][j]]
						cur_pos[i] = random_pos[i][j]
						str_racing_field.append("".join(racing_field[i]))

					await asyncio.sleep(1) 

					for i in range(len(racing_member)):
						output +=  str_racing_field[i] + '\n'
					
					await result_race.edit(content = output + ':checkered_flag:  경주 시작!')
				
				for i in range(len(racing_field)):
					fr.append(race_info[i][0])
					fr.append((race_info[i][2]) - tmp_race_tab + 1)
					racing_result.append(fr)
					fr = []

				result = sorted(racing_result, key=lambda x: x[1])

				result_str = ''
				for i in range(len(result)):
					if result[i][1] == 1:
						result[i][1] = ':first_place:'
					elif result[i][1] == 2:
						result[i][1] = ':second_place:'
					elif result[i][1] == 3:
						result[i][1] = ':third_place:'
					elif result[i][1] == 4:
						result[i][1] = ':four:'
					elif result[i][1] == 5:
						result[i][1] = ':five:'
					elif result[i][1] == 6:
						result[i][1] = ':six:'
					elif result[i][1] == 7:
						result[i][1] = ':seven:'
					elif result[i][1] == 8:
						result[i][1] = ':eight:'
					elif result[i][1] == 9:
						result[i][1] = ':nine:'
					elif result[i][1] == 10:
						result[i][1] = ':keycap_ten:'
					else:
						result[i][1] = ':x:'
					result_str += result[i][1] + "  " + result[i][0] + "  "
					
				#print(result)
				await asyncio.sleep(1)
				return await result_race.edit(content = output + ':tada: 경주 종료!\n' + result_str)
		else:
			return

	################ 보탐봇 입장 ################ 	
	@client.command(name=command[28][0], aliases=command[28][1:])
	async def set_channel_(ctx):
		global basicSetting

		msg = ctx.message.content[len(ctx.invoked_with)+1:]
		channel = ctx.message.channel.id #메세지가 들어온 채널 ID

		if msg == '사다리' : #사다리 채널 설정
			inidata_textCH = repo.get_contents("test_setting.ini")
			file_data_textCH = base64.b64decode(inidata_textCH.content)
			file_data_textCH = file_data_textCH.decode('utf-8')
			inputData_textCH = file_data_textCH.split('\n')
			
			for i in range(len(inputData_textCH)):
				if inputData_textCH[i].startswith('ladderchannel'):
					inputData_textCH[i] = 'ladderchannel = ' + str(channel) + '\r'
					basicSetting[8] = channel
			result_textCH = '\n'.join(inputData_textCH)

			contents = repo.get_contents("test_setting.ini")
			repo.update_file(contents.path, "test_setting", result_textCH, contents.sha)

			print(f'< 사다리채널 [{ctx.message.channel.name}] 설정완료 >')
			return await ctx.send(f'< 사다리채널 [{ctx.message.channel.name}] 설정완료 >', tts=False)
		elif msg == '정산' :
			inidata_textCH = repo.get_contents("test_setting.ini")
			file_data_textCH = base64.b64decode(inidata_textCH.content)
			file_data_textCH = file_data_textCH.decode('utf-8')
			inputData_textCH = file_data_textCH.split('\n')
			
			for i in range(len(inputData_textCH)):
				if inputData_textCH[i].startswith('jungsanchannel'):
					inputData_textCH[i] = 'jungsanchannel = ' + str(channel) + '\r'
					basicSetting[11] = channel
			result_textCH = '\n'.join(inputData_textCH)

			contents = repo.get_contents("test_setting.ini")
			repo.update_file(contents.path, "test_setting", result_textCH, contents.sha)

			print(f'< 정산채널 [{ctx.message.channel.name}] 설정완료 >')
			return await ctx.send(f'< 정산채널 [{ctx.message.channel.name}] 설정완료 >', tts=False)			
		elif msg == '척살' :
			inidata_textCH = repo.get_contents("test_setting.ini")
			file_data_textCH = base64.b64decode(inidata_textCH.content)
			file_data_textCH = file_data_textCH.decode('utf-8')
			inputData_textCH = file_data_textCH.split('\n')
			
			for i in range(len(inputData_textCH)):
				if inputData_textCH[i].startswith('killchannel'):
					inputData_textCH[i] = 'killchannel = ' + str(channel) + '\r'
					basicSetting[18] = channel
			result_textCH = '\n'.join(inputData_textCH)

			contents = repo.get_contents("test_setting.ini")
			repo.update_file(contents.path, "test_setting", result_textCH, contents.sha)

			print(f'< 척살채널 [{ctx.message.channel.name}] 설정완료 >')
			return await ctx.send(f'< 척살채널 [{ctx.message.channel.name}] 설정완료 >', tts=False)
		elif msg == '경주' :
			inidata_textCH = repo.get_contents("test_setting.ini")
			file_data_textCH = base64.b64decode(inidata_textCH.content)
			file_data_textCH = file_data_textCH.decode('utf-8')
			inputData_textCH = file_data_textCH.split('\n')
			
			for i in range(len(inputData_textCH)):
				if inputData_textCH[i].startswith('racingchannel'):
					inputData_textCH[i] = 'racingchannel = ' + str(channel) + '\r'
					basicSetting[19] = channel
			result_textCH = '\n'.join(inputData_textCH)

			contents = repo.get_contents("test_setting.ini")
			repo.update_file(contents.path, "test_setting", result_textCH, contents.sha)

			print(f'< 경주채널 [{ctx.message.channel.name}] 설정완료 >')
			return await ctx.send(f'< 경주채널 [{ctx.message.channel.name}] 설정완료 >', tts=False)
		elif msg == '아이템' :
			inidata_textCH = repo.get_contents("test_setting.ini")
			file_data_textCH = base64.b64decode(inidata_textCH.content)
			file_data_textCH = file_data_textCH.decode('utf-8')
			inputData_textCH = file_data_textCH.split('\n')
			
			for i in range(len(inputData_textCH)):
				if inputData_textCH[i].startswith('itemchannel'):
					inputData_textCH[i] = 'itemchannel = ' + str(channel) + '\r'
					basicSetting[20] = channel
			result_textCH = '\n'.join(inputData_textCH)

			contents = repo.get_contents("test_setting.ini")
			repo.update_file(contents.path, "test_setting", result_textCH, contents.sha)

			print(f'< 아이템채널 [{ctx.message.channel.name}] 설정완료 >')
			return await ctx.send(f'< 아이템채널 [{ctx.message.channel.name}] 설정완료 >', tts=False)
		else :
			return await ctx.send(f'```올바른 명령어를 입력해주세요.```', tts=False)

	################ 아이템초기화 확인 ################ 
	@client.command(name=command[29][0], aliases=command[29][1:])
	async def itemInit_(ctx):
		if ctx.message.channel.id == basicSetting[7] or ctx.message.channel.id == basicSetting[20]:
			global item_Data

			item_Data = {}

			await init_data_list('item_list.ini', '-----아이템 목록-----')
			return await ctx.send( '< 아이템 목록 초기화완료 >', tts=False)
		else:
			return

	################ 아이템 목록 확인 및 추가 ################ 
	@client.command(name=command[30][0], aliases=command[30][1:]) 
	async def itemList_(ctx, *, args : str = None):
		if ctx.message.channel.id == basicSetting[7] or ctx.message.channel.id == basicSetting[20]:
			global item_Data
			
			if not args:
				sorted_item_list = sorted(item_Data.items(), key=lambda x: x[0])

				embed_list : list = []
				embed_index : int = 0
				embed_cnt : int = 0
				embed = discord.Embed(title = '', description = f'`{client.user.name}\'s 창고`', color = 0x00ff00)
				
				embed_list.append(embed)

				if len(sorted_item_list) > 0 :
					for item_id, count in sorted_item_list:
						embed_cnt += 1
						if embed_cnt > 24 :
							embed_cnt = 0
							embed_index += 1
							tmp_embed = discord.Embed(
								title = "",
								description = "",
								color=0x00ff00
								)
							embed_list.append(tmp_embed)
						embed_list[embed_index].add_field(name = item_id, value = count)
					embed_list[len(embed_list)-1].set_footer(text = f"전체 아이템 종류  :  {len(item_Data)}개")
					if len(embed_list) > 1:
						for embed_data in embed_list:
							await asyncio.sleep(0.1)
							await ctx.send(embed = embed_data)
						return
					else:
						return await ctx.send(embed=embed, tts=False)
				else :
					embed.add_field(name = '\u200b\n', value = '창고가 비었습니다.\n\u200b')
					return await ctx.send(embed=embed, tts=False)

			input_data = args.split()
			
			if len(input_data) == 1:
				item_name = args
				count = 1
			elif len(input_data) == 2:
				item_name = input_data[0]
				try:
					count = int(input_data[1])
				except ValueError:
					return await ctx.send(f'아이템 [개수]는 숫자로 입력바랍니다')
			else:
				return await ctx.send(f'{command[30][0]} [아이템명] 혹은 {command[30][0]} [아이템명] [개수] 양식에 맞춰 입력해주세요!', tts = False)	

			if item_name in item_Data:
				item_Data[item_name] += int(count)
			else:
				item_Data[item_name] = int(count)
					
			embed = discord.Embed(
					description= f':inbox_tray: **[{item_name}] [{str(count)}개]** 등록 완료! [잔여 : {str(item_Data[item_name])}개]\n',
					color=0xff00ff
					)
			return await ctx.send(embed=embed, tts=False)

		else:
			return

	################ 아이템 삭제 ################ 
	@client.command(name=command[31][0], aliases=command[31][1:])
	async def itemDel_(ctx, *, args : str = None):
		if ctx.message.channel.id == basicSetting[7] or ctx.message.channel.id == basicSetting[20]:
			global item_Data

			if not args:
				return await ctx.send( f'{command[31][0]} [아이템명] 양식에 맞춰 입력해주세요!', tts = False)

			if args in item_Data:
				del item_Data[args]
				embed = discord.Embed(
					description= ':outbox_tray: ' + args + ' 삭제완료!',
					color=0xff00ff
					)
				return await ctx.send(embed=embed, tts=False)
			else :				
				return await ctx.send( '```아이템 목록에 등록되어 있지 않습니다!\n```', tts=False)
		else:
			return

	################ 아이템 차감 ################ 
	@client.command(name=command[32][0], aliases=command[32][1:]) 
	async def itemSubtract_(ctx, *, args : str = None):
		if ctx.message.channel.id == basicSetting[7] or ctx.message.channel.id == basicSetting[20]:
			global item_Data

			if not args:
				return await ctx.send(f'{command[32][0]} [아이템명] 혹은 {command[32][0]} [아이템명] [개수] 양식에 맞춰 입력해주세요!', tts = False)

			input_data = args.split()
			
			if len(input_data) == 1:
				item_name = args
				count = 1
			elif len(input_data) == 2:
				item_name = input_data[0]
				try:
					count = int(input_data[1])
				except ValueError:
					return await ctx.send(f'아이템 [개수]는 숫자로 입력바랍니다')
			else:
				return await ctx.send(f'{command[32][0]} [아이템명] 혹은 {command[32][0]} [아이템명] [개수] 양식에 맞춰 입력해주세요!', tts = False)	

			if item_name in item_Data:
				if item_Data[item_name] < int(count):
					return await ctx.send( f"등록된 아이템 개수[{str(item_Data[item_name])}개]보다 차감 개수[{str(count)}개]가 많습니다. 등록 개수에 맞게 재입력 바랍니다.", tts=False)
				else:
					item_Data[item_name] -= int(count)
			else:
				return await ctx.send( '```아이템 목록에 등록되어 있지 않습니다!\n```', tts=False)
					
			embed = discord.Embed(
					description= f':outbox_tray: **[{item_name}] [{str(count)}개]** 차감 완료! [잔여 : {str(item_Data[item_name])}개]\n',
					color=0xff00ff
					)
			
			if item_Data[item_name] == 0:
				del item_Data[item_name]

			return await ctx.send(embed=embed, tts=False)
		else:
			return

	################ 서버 나가기 ################ 		
	@commands.has_permissions(manage_messages=True)
	@client.command(name=command[34][0], aliases=command[34][1:])
	async def leaveGuild_(ctx):
		if ctx.message.channel.id == basicSetting[7]:
			guild_list : str = ""
			guild_name : str = ""

			for i, gulid_name in enumerate(client.guilds):
				guild_list += f"`{i+1}.` {gulid_name}\n"

			embed = discord.Embed(
				title = "----- 서버 목록 -----",
				description = guild_list,
				color=0x00ff00
				)
			await ctx.send(embed = embed)

			try:
				await ctx.send(f"```떠나고 싶은 서버의 [숫자]를 입력하여 선택해 주세요```")
				message_result : discord.Message = await client.wait_for("message", timeout = 10, check=(lambda message: message.channel == ctx.message.channel and message.author == ctx.message.author))
			except asyncio.TimeoutError:
				return await ctx.send(f"```서버 선택 시간이 초과됐습니다! 필요시 명령어를 재입력해 주세요```")
				
			try:
				guild_name = client.guilds[int(message_result.content)-1].name
				await client.get_guild(client.guilds[int(message_result.content)-1].id).leave()
				return await ctx.send(f"```[{guild_name}] 서버에서 떠났습니다.!```")
			except ValueError:
				return			

	################ 수수료 계산기 ################ 
	@client.command(name=command[35][0], aliases=command[35][1:])
	async def tax_check(ctx, *, args : str = None):
		if ctx.message.channel.id == basicSetting[7] or ctx.message.channel.id == basicSetting[22]:
			if not args:
				return await ctx.send(f"**{command[35][0]} [판매금액] (거래소세금)** 양식으로 입력 해주세요\n※ 거래소세금은 미입력시 5%입니다.")
			
			input_money_data : list = args.split()
			len_input_money_data = len(input_money_data)

			try:
				for i in range(len_input_money_data):
					input_money_data[i] = int(input_money_data[i])
			except ValueError:
				return await ctx.send(f"**[판매금액] (거래소세금)**은 숫자로 입력 해주세요.")

			if len_input_money_data < 1 or len_input_money_data > 3:
				return await ctx.send(f"**{command[35][0]} [판매금액] (거래소세금)** 양식으로 입력 해주세요\n※ 거래소세금은 미입력시 5%입니다.")
			elif len_input_money_data == 2:
				tax = input_money_data[1]
			else:
				tax = 5

			price_first_tax = int(input_money_data[0] * ((100-tax)/100))
			price_second_tax = int(price_first_tax * ((100-tax)/100))
			price_rev_tax = int((input_money_data[0] * 100)/(100-tax)+0.5)

			embed = discord.Embed(
					title = f"🧮  수수료 계산결과 (세율 {tax}% 기준) ",
					description = f"",
					color=0x00ff00
					)
			embed.add_field(name = "⚖️ 수수료 지원", value = f"```등록가 : {price_rev_tax}\n수령가 : {input_money_data[0]}\n세 금 : {price_rev_tax-input_money_data[0]}```")
			embed.add_field(name = "⚖️ 1차 거래", value = f"```등록가 : {input_money_data[0]}\n정산가 : {price_first_tax}\n세 금 : {input_money_data[0]-price_first_tax}```")
			embed.add_field(name = "⚖️ 2차 거래", value = f"```등록가 : {price_first_tax}\n정산가 : {price_second_tax}\n세 금 : {price_first_tax-price_second_tax}```")
			return await ctx.send(embed = embed)
		else:
			return

	################ 페이백 계산기 ################ 
	@client.command(name=command[36][0], aliases=command[36][1:])
	async def payback_check(ctx, *, args : str = None):
		if ctx.message.channel.id == basicSetting[7] or ctx.message.channel.id == basicSetting[22]:
			if not args:
				return await ctx.send(f"**{command[36][0]} [거래소가격] [실거래가] (거래소세금)** 양식으로 입력 해주세요\n※ 거래소세금은 미입력시 5%입니다.")
			
			input_money_data : list = args.split()
			len_input_money_data = len(input_money_data)

			try:
				for i in range(len_input_money_data):
					input_money_data[i] = int(input_money_data[i])
			except ValueError:
				return await ctx.send(f"**[판매금액] (거래소세금)**은 숫자로 입력 해주세요.")

			if len_input_money_data < 2 or len_input_money_data > 4:
				return await ctx.send(f"**{command[36][0]} [거래소가격] [실거래가] (거래소세금)** 양식으로 입력 해주세요\n※ 거래소세금은 미입력시 5%입니다.")
			elif len_input_money_data == 3:
				tax = input_money_data[2]
			else:
				tax = 5

			price_reg_tax = int(input_money_data[0] * ((100-tax)/100))
			price_real_tax = int(input_money_data[1] * ((100-tax)/100))

			reault_payback = price_reg_tax - price_real_tax
			reault_payback1= price_reg_tax - input_money_data[1]

			embed = discord.Embed(
					title = f"🧮  페이백 계산결과1 (세율 {tax}% 기준) ",
					description = f"**```fix\n{reault_payback}```**",
					color=0x00ff00
					)
			embed.add_field(name = "⚖️ 거래소", value = f"```등록가 : {input_money_data[0]}\n정산가 : {price_reg_tax}\n세 금 : {input_money_data[0]-price_reg_tax}```")
			embed.add_field(name = "🕵️ 실거래", value = f"```등록가 : {input_money_data[1]}\n정산가 : {price_real_tax}\n세 금 : {input_money_data[1]-price_real_tax}```")
			await ctx.send(embed = embed)

			embed2 = discord.Embed(
					title = f"🧮  페이백 계산결과2 (세율 {tax}% 기준) ",
					description = f"**```fix\n{reault_payback1}```**",
					color=0x00ff00
					)
			embed2.add_field(name = "⚖️ 거래소", value = f"```등록가 : {input_money_data[0]}\n정산가 : {price_reg_tax}\n세 금 : {input_money_data[0]-price_reg_tax}```")
			embed2.add_field(name = "🕵️ 실거래", value = f"```내판가 : {input_money_data[1]}```")
			return await ctx.send(embed = embed2)
		else:
			return

	################ ?????????????? ################ 
	@client.command(name='!오빠')
	async def brother1_(ctx):
		await PlaySound(voice_client1, './sound/오빠.mp3')

	@client.command(name='!언니')
	async def sister_(ctx):
		await PlaySound(voice_client1, './sound/언니.mp3')

	@client.command(name='!형')
	async def brother2_(ctx):
		await PlaySound(voice_client1, './sound/형.mp3')
	
	@client.command(name='!TJ', aliases=['!tj'])
	async def TJ_(ctx):
		resultTJ = random.randrange(1,9)
		await PlaySound(voice_client1, './sound/TJ' + str(resultTJ) +'.mp3')


	@client.event
	async def on_command_error(ctx, error):
		if isinstance(error, CommandNotFound):
			return
		elif isinstance(error, discord.ext.commands.MissingRequiredArgument):
			return
		elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
			return await ctx.send(f"**[{ctx.message.content}]** 명령을 사용할 권한이 없습니다.!")
		raise error

	# 봇이 새로운 메시지를 수신했을때 동작되는 코드입니다.
	@client.event
	async def on_message(msg):
		await client.wait_until_ready()
		if msg.author.bot: #만약 메시지를 보낸사람이 봇일 경우에는
			return None #동작하지 않고 무시합니다.

		ori_msg = msg

		global channel
		
		global basicSetting
		global bossData
		global fixed_bossData

		global bossNum
		global fixed_bossNum
		global chkvoicechannel
		global chkrelogin

		global bossTime
		global tmp_bossTime

		global fixed_bossTime

		global bossTimeString
		global bossDateString
		global tmp_bossTimeString
		global tmp_bossDateString

		global bossFlag
		global bossFlag0
		global bossMungFlag
		global bossMungCnt
		
		global voice_client1
		
		global channel_info
		global channel_name
		global channel_id
		global channel_voice_name
		global channel_voice_id
		global channel_type
		
		global chflg
		global LoadChk
		
		global indexFixedBossname
		global FixedBossDateData
		
		global gc #정산
		global credentials	#정산

		global regenembed
		global command
		global kill_Data
		
		id = msg.author.id #id라는 변수에는 메시지를 보낸사람의 ID를 담습니다.
		
		if chflg == 1 :
			if client.get_channel(basicSetting[7]).id == msg.channel.id:
				channel = basicSetting[7]
				message = msg

				hello = message.content

				for i in range(bossNum):
					################ 보스 컷처리 ################ 
					if message.content.startswith(bossData[i][0] +'컷') or message.content.startswith(convertToInitialLetters(bossData[i][0] +'컷')) or message.content.startswith(bossData[i][0] +' 컷') or message.content.startswith(convertToInitialLetters(bossData[i][0] +' 컷')):
						if hello.find('  ') != -1 :
							bossData[i][6] = hello[hello.find('  ')+2:]
							hello = hello[:hello.find('  ')]
						else:
							bossData[i][6] = ''
							
						tmp_msg = bossData[i][0] +'컷'
						if len(hello) > len(tmp_msg) + 3 :
							if hello.find(':') != -1 :
								chkpos = hello.find(':')
								hours1 = hello[chkpos-2:chkpos]
								minutes1 = hello[chkpos+1:chkpos+3]
								now2 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
								tmp_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
								tmp_now = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
							else:
								chkpos = len(hello)-2
								hours1 = hello[chkpos-2:chkpos]
								minutes1 = hello[chkpos:chkpos+2]
								now2 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
								tmp_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
								tmp_now = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
						else:
							now2 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
							tmp_now = now2

						bossFlag[i] = False
						bossFlag0[i] = False
						bossMungFlag[i] = False
						bossMungCnt[i] = 0

						if tmp_now > now2 :
							tmp_now = tmp_now + datetime.timedelta(days=int(-1))
							
						if tmp_now < now2 : 
							deltaTime = datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))
							while now2 > tmp_now :
								tmp_now = tmp_now + deltaTime
								bossMungCnt[i] = bossMungCnt[i] + 1
							now2 = tmp_now
							bossMungCnt[i] = bossMungCnt[i] - 1
						else :
							now2 = now2 + datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))
									
						tmp_bossTime[i] = bossTime[i] = nextTime = now2
						tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
						tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')
						embed = discord.Embed(
								description= '```다음 ' + bossData[i][0] + ' ' + bossTimeString[i] + '입니다.```',
								color=0xff0000
								)
						await client.get_channel(channel).send(embed=embed, tts=False)

					################ 보스 멍 처리 ################ 

					if message.content.startswith(bossData[i][0] +'멍') or message.content.startswith(bossData[i][0] +' 멍'):
						if hello.find('  ') != -1 :
							bossData[i][6] = hello[hello.find('  ')+2:]
							hello = hello[:hello.find('  ')]
						else:
							bossData[i][6] = ''
							
						tmp_msg = bossData[i][0] +'멍'
						tmp_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))

						if len(hello) > len(tmp_msg) + 3 :
							temptime = tmp_now
							if hello.find(':') != -1 :
								chkpos = hello.find(':')
								hours1 = hello[chkpos-2:chkpos] 
								minutes1 = hello[chkpos+1:chkpos+3]					
								temptime = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
							else:
								chkpos = len(hello)-2
								hours1 = hello[chkpos-2:chkpos]
								minutes1 = hello[chkpos:chkpos+2]					
								temptime = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
							
							bossMungCnt[i] = 0
							bossFlag[i] = False
							bossFlag0[i] = False
							bossMungFlag[i] = False

							if temptime > tmp_now :
								temptime = temptime + datetime.timedelta(days=int(-1))

							if temptime < tmp_now :
								deltaTime = datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))
								while temptime < tmp_now :
									temptime = temptime + deltaTime
									bossMungCnt[i] = bossMungCnt[i] + 1

							tmp_bossTime[i] = bossTime[i] = temptime				

							tmp_bossTimeString[i] = bossTimeString[i] = temptime.strftime('%H:%M:%S')
							tmp_bossDateString[i] = bossDateString[i] = temptime.strftime('%Y-%m-%d')
							embed = discord.Embed(
									description= '```다음 ' + bossData[i][0] + ' ' + bossTimeString[i] + '입니다.```',
									color=0xff0000
									)
							await client.get_channel(channel).send(embed=embed, tts=False)
						else:
							if tmp_bossTime[i] < tmp_now :

								nextTime = tmp_bossTime[i] + datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))

								bossFlag[i] = False
								bossFlag0[i] = False
								bossMungFlag[i] = False
								bossMungCnt[i] = bossMungCnt[i] + 1

								tmp_bossTime[i] = bossTime[i] = nextTime				

								tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
								tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')
								embed = discord.Embed(
										description= '```다음 ' + bossData[i][0] + ' ' + bossTimeString[i] + '입니다.```',
										color=0xff0000
										)
								await client.get_channel(channel).send(embed=embed, tts=False)
							else:
								await client.get_channel(channel).send('```' + bossData[i][0] + '탐이 아직 안됐습니다. 다음 ' + bossData[i][0] + '탐 [' + tmp_bossTimeString[i] + '] 입니다```', tts=False)

						
				################ 예상 보스 타임 입력 ################ 

					if message.content.startswith(bossData[i][0] +'예상')  or message.content.startswith(bossData[i][0] +' 예상'):
						if hello.find('  ') != -1 :
							bossData[i][6] = hello[hello.find('  ')+2:]
							hello = hello[:hello.find('  ')]
						else:
							bossData[i][6] = ''
							
						tmp_msg = bossData[i][0] +'예상'
						if len(hello) > len(tmp_msg) + 4 :
							if hello.find(':') != -1 :
								chkpos = hello.find(':')
								hours1 = hello[chkpos-2:chkpos]
								minutes1 = hello[chkpos+1:chkpos+3]
								now2 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
								tmp_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
								tmp_now = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
							else:
								chkpos = len(hello)-2
								hours1 = hello[chkpos-2:chkpos]
								minutes1 = hello[chkpos:chkpos+2]
								now2 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
								tmp_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
								tmp_now = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
							
							bossFlag[i] = False
							bossFlag0[i] = False
							bossMungFlag[i] = False
							bossMungCnt[i] = 0

							if tmp_now < now2 :
								tmp_now = tmp_now + datetime.timedelta(days=int(1))

							tmp_bossTime[i] = bossTime[i] = nextTime = tmp_now
							tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
							tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')
							embed = discord.Embed(
									description= '```다음 ' + bossData[i][0] + ' ' + bossTimeString[i] + '입니다.```',
									color=0xff0000
									)
							await client.get_channel(channel).send(embed=embed, tts=False)
						else:
							await client.get_channel(channel).send('```' + bossData[i][0] +' 예상 시간을 입력해주세요.```', tts=False)
							
					################ 보스타임 삭제 ################
						
					if message.content == bossData[i][0] +'삭제' or message.content == bossData[i][0] +' 삭제':
						bossTime[i] = datetime.datetime.now()+datetime.timedelta(days=365, hours = int(basicSetting[0]))
						tmp_bossTime[i] =  datetime.datetime.now()+datetime.timedelta(days=365, hours = int(basicSetting[0]))
						bossTimeString[i] = '99:99:99'
						bossDateString[i] = '9999-99-99'
						tmp_bossTimeString[i] = '99:99:99'
						tmp_bossDateString[i] = '9999-99-99'
						bossFlag[i] = False
						bossFlag0[i] = False
						bossMungFlag[i] = False
						bossMungCnt[i] = 0
						await client.get_channel(channel).send('<' + bossData[i][0] + ' 삭제완료>', tts=False)
						await dbSave()
						print ('<' + bossData[i][0] + ' 삭제완료>')
					
					################ 보스별 메모 ################ 

					if message.content.startswith(bossData[i][0] +'메모 '):
						
						tmp_msg = bossData[i][0] +'메모 '
						
						bossData[i][6] = hello[len(tmp_msg):]
						await client.get_channel(channel).send('< ' + bossData[i][0] + ' [ ' + bossData[i][6] + ' ] 메모등록 완료>', tts=False)
						
					if message.content.startswith(bossData[i][0] +'메모삭제'):
						
						bossData[i][6] = ''
						await client.get_channel(channel).send('< ' + bossData[i][0] + ' 메모삭제 완료>', tts=False)

		await client.process_commands(ori_msg)

	client.loop.create_task(task())
	try:
		client.loop.run_until_complete(client.start(access_token))
	except SystemExit:
		handle_exit()
	except KeyboardInterrupt:
		handle_exit()
	#client.loop.close()
	#print("Program ended")
	#break

	print("Bot restarting")
	client = discord.Client(loop=client.loop)
	client = commands.Bot(command_prefix="", help_command = None, description='일상디코봇')
