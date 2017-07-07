#!/usr/bin/python
#---------------------------------------
# ffetchStatusATMCL.py
# (c) Jansen A. Simanullang, 11:15:55
# @BSD City: Januari - November 2016
# @Medan City: June - July 2017
# to be used with telegram-bot plugin
#---------------------------------------
# usage #1: 
# ffetchStatusATMCL cro/uko/kode cabang
# script name followed by cro/uko or branchCode
# usage #2: ffetchStatusATMCL [cro/uko/kode cabang] [telegram_id]
# to send to telegram id directly
#---------------------------------------

from BeautifulSoup import BeautifulSoup
import os, sys, time
import urllib2
from operator import itemgetter
#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
scriptDirectory = os.path.dirname(os.path.abspath(__file__)) + "/"
from loadConfig import readConfig
from helperlibrary import *
atmproIP = readConfig("Atmpro")['ipaddress']
regionID = readConfig("Atmpro")['regionid']
regionName = readConfig("Atmpro")['regionname']
secretKey = readConfig("Telegram")['token']
Telebot = readConfig("Telegram")['username']
textLimit = int(readConfig("Telegram")['textlimit'])
behindProxy=int(readConfig("Internet")['behindproxy'])
strHeaderLine = "\n----------------------------------------------\n"
#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+



def getTCashLow(table):

	soup = BeautifulSoup(str(table))
	
	rows = soup.findAll('tr')

	numRows = getRowsNumber(table)

	numCols = getColsNumber(table)

	numRowsHead = getRowsHeadNumber(table)

	#Initialize

	TCashLow = []
	
	for i in range (0, numRows):

		trs = BeautifulSoup(str(rows[i]))

		tdcells = trs.findAll("td")
		thcells = trs.findAll("th")

		if tdcells:
			strTID = tdcells[1].getText()
			strLocation = tdcells[5].getText()
			strLocation = cleanUpLocation(strLocation)
			strArea = tdcells[6].getText()
			datLastTunai = tdcells[11].getText().strip()

			if ("ATM CENTER" in strArea) or ("VENDOR" in strArea):
				intCRO = 1
				namaCROUKO = cleanUpNamaCRO(strArea)
			else:
				intCRO = 0
				namaCROUKO = cleanupNamaUker(strArea)
				
			strCabang = tdcells[7].getText()
			strKodeCabang = strCabang[:4]
			strNamaCabang = strCabang[6:]


			TCashLow.append((strKodeCabang, namaCROUKO, intCRO, strArea, strLocation, strTID, strNamaCabang, datLastTunai))
			#TCashLow       ((#0:strKodeCabang, #1:namaCROUKO, #2:intCRO, #3:strArea, #4:strLocation, #5:strTID, #6:strNamaCabang, #7:datLastTunai))

	TCashLow = sorted(TCashLow, key=itemgetter(1, 3, 2), reverse = False)

	return TCashLow 


def getTCashLowCabang(TCashLow, branchCode):

	#Initialize
	msgBody = ""
	
	TCashLowKanca = []
	TCashLowUKO = []
	TCashLowCRO = []

	for i in range(0, len(TCashLow)):
		if TCashLow[i][0] == branchCode.zfill(4):
			strNamaCabang = cleanupNamaUker(TCashLow[i][6])
			TCashLowKanca.append(TCashLow[i])

	for i in range(0, len(TCashLowKanca)):
		if TCashLowKanca[i][2] == 0:
			TCashLowUKO.append((TCashLowKanca[i][3], TCashLowKanca[i][5]))

	for i in range(0, len(TCashLowKanca)):
		if TCashLowKanca[i][2] == 1:
			TCashLowCRO.append((TCashLowKanca[i][1], TCashLowKanca[i][4], TCashLowKanca[i][5]))

	if TCashLowUKO or TCashLowCRO:
		msgBody = strHeaderLine +"ATM CASH LOW "+ strNamaCabang.upper() +timestamp+ strHeaderLine + msgBody + "\n"
	else:

		msgBody = strHeaderLine +"ATM CASH LOW "+ branchCode +timestamp+ strHeaderLine + msgBody + "\nEXCELLENT WORK!\nALL ONLINE ATM IS READY TO DISPENSE MONEY!"

	if TCashLowUKO:
		msgBody += "*[UKO]*\n"
		for i in range(0, len(TCashLowUKO)):
					msgBody += str(i+1)+" "+ str(TCashLowUKO[i][0])+", "+str(TCashLowUKO[i][1])+"\n"
		msgBody += "\n"			

	if TCashLowCRO:
		msgBody += "*[CRO]*\n"
		for i in range(0, len(TCashLowCRO)):
					msgBody += str(i+1)+" "+ str(TCashLowCRO[i][0]) +": "+str(TCashLowCRO[i][1])+", "+str(TCashLowCRO[i][2])+"\n"

	return 	msgBody


def getTCashLowCRO(TCashLow, selectedCRO):

	#Initialize
	msgBody = ""
	seqNo = 0
	counter = 0
	TCashLowCRO = []
	arrCRO = ["BG", "G4S", "KEJAR", "SSI", "TAG"]

	if selectedCRO == 0:

		selectedCRO = "ALL"
		strCRO = "*[ALL CRO]*"

		for i in range(0, len(TCashLow)):
			if TCashLow[i][2] == 1:
				strNamaCabang = cleanupNamaUker(TCashLow[i][-1])
				TCashLowCRO.append((TCashLow[i][1], TCashLow[i][4], TCashLow[i][5], TCashLow[i][7]))


	elif selectedCRO in arrCRO:

		arrCRO = [""]
		arrCRO.append(selectedCRO)
		strCRO = "*["+selectedCRO+"]*"
	
		for i in range(0, len(TCashLow)):

			if TCashLow[i][1] == selectedCRO:
				strNamaCabang = cleanupNamaUker(TCashLow[i][-1])
				TCashLowCRO.append((TCashLow[i][1], TCashLow[i][4], TCashLow[i][5], TCashLow[i][7]))

	if TCashLowCRO:

		msgBody += strCRO+"\n"
		TCashLowCRO = sorted(TCashLowCRO, key=itemgetter(0,3), reverse = False)
		for i in range(0, len(TCashLowCRO)):

			if TCashLowCRO[i-1][0] != TCashLowCRO[i][0]:
				msgBody += "\n*[" + str(TCashLowCRO[i][0]) + "]*\n"
				seqNo = 0

			for j in range(0, len(arrCRO)):

				if str(TCashLowCRO[i][0]) == arrCRO[j]:
					seqNo += 1
					counter += 1
					msgBody += str(seqNo)+") "+ str(TCashLowCRO[i][1])+", "+str(TCashLowCRO[i][2])+", "+durasiLastTunai(str(TCashLowCRO[i][3]))+"\n"


		msgBody += "\n"+regionName + "-[TOTAL CASH LOW CRO "+selectedCRO+"]: "+str(counter)

	return 	msgBody


def getTCashLowUKO(TCashLow):

	#Initialize
	msgBody = ""
	seqNo = 0
	counter = 0
	TCashLowUKO = []

	for i in range(0, len(TCashLow)):
	
		if TCashLow[i][2] == 0:
			strNamaCabang = "*"+cleanupNamaUker(TCashLow[i][6])+"*"
			TCashLowUKO.append((strNamaCabang.upper(), TCashLow[i][4], TCashLow[i][5], TCashLow[i][7]))
			#TCashLow       ((#0:strKodeCabang, #1:namaCROUKO, #2:intCRO, #3:strArea, #4:strLocation, #5:strTID, #6:strNamaCabang, #7:datLastTunai))
	TCashLowUKO = sorted(TCashLowUKO, key=itemgetter(0), reverse = False)

	if TCashLowUKO:
		TCashLowUKO = sorted(TCashLowUKO, key=itemgetter(0,3), reverse = False)
		msgBody += "*[UKO]*\n"
		for i in range(0, len(TCashLowUKO)):
			if TCashLowUKO[i-1][0] != TCashLowUKO[i][0]:
				msgBody +=  "\n"+str(TCashLowUKO[i][0]) + "\n"
				seqNo = 0

			seqNo += 1
			counter += 1
			msgBody += str(seqNo)+") "+ str(TCashLowUKO[i][1])+", "+str(TCashLowUKO[i][2])+", "+durasiLastTunai(str(TCashLowUKO[i][3]))+"\n"

		msgBody += "\n"+regionName + "-[TOTAL CASH LOW UKO]: "+str(counter)

	return 	msgBody

msgBody =""

timestamp = "\nper "+ time.strftime("%d-%m-%Y pukul %H:%M")

if len(sys.argv) > 0:

	alamatURL = "http://atmpro.bri.co.id/statusatm/viewbyregionprob.pl?REGID="+regionID+"&ERROR=CSHLOW_ST"

	try:
		AREAID = sys.argv[1]
		try:
			telegram_id = sys.argv[2]
		except:
			AREAID = sys.argv[1]
			telegram_id = ""

		if AREAID.isdigit():

			TCashLow = getTCashLow(table=getWidestTable(getTableList(fetchHTML(alamatURL))))
			msgBody = getTCashLowCabang(TCashLow, AREAID)

			if msgBody:	
				print msgBody
				if telegram_id:
					TelegramTextSender(telegram_id, msgBody)

	
		if AREAID[0].isalpha():

			if AREAID.upper() == "UKO":

				try:

					TCashLow = getTCashLow(table=getWidestTable(getTableList(fetchHTML(alamatURL))))
					msgBody = getTCashLowUKO(TCashLow)

					if msgBody:	
						msgBody = strHeaderLine +"*ATM CASH LOW "+ AREAID.upper() + "* - "+regionName+ timestamp+ strHeaderLine + msgBody
						print msgBody.replace("**","") # double asterisk mark ("**") due to orphaned TID

						if telegram_id:
							TelegramTextSender(telegram_id, msgBody)

				except:
					print "Ada kesalahan."

			elif AREAID.upper() == "CRO":

				try:

					TCashLow = getTCashLow(table=getWidestTable(getTableList(fetchHTML(alamatURL))))
					msgBody = getTCashLowCRO(TCashLow, 0)

					if msgBody:	
						msgBody = strHeaderLine +"*ATM CASH LOW "+ AREAID.upper() + "* - "+regionName+ timestamp+ strHeaderLine + msgBody
						print msgBody
						if telegram_id:
							TelegramTextSender(telegram_id, msgBody)

				except:
					print "Ada kesalahan."

			else:

				try:

					TCashLow = getTCashLow(table=getWidestTable(getTableList(fetchHTML(alamatURL))))
					msgBody = getTCashLowCRO(TCashLow, AREAID.upper())

					if msgBody:	
						msgBody = strHeaderLine +"*ATM CASH LOW "+ AREAID.upper() + "* - "+regionName+ timestamp+ strHeaderLine + msgBody
						print msgBody
						if telegram_id:
							TelegramTextSender(telegram_id, msgBody)

				except:
					print "CRO tidak dikenal."

	except:

		print "ANDA belum meng-input kode UKO/ CRO."
