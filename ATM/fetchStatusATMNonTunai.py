#!/usr/bin/python
#---------------------------------------
# fetchStatusATMNonTunai.py
# (c) Jansen A. Simanullang, 11:15:55
# @BSD City: 14 Januari 2016 09:04:11
# 13 Agustus 2016 13:58:28 - 15:30, 16:33
# 28 November 2016 14:36 # asterisks added
# @Medan City: 30.06.2017
# to be used with telegram-bot plugin
#---------------------------------------
# usage: fetchStatusATMNonTunai cro/uko/kode cabang
# script name followed by cro/uko or branchCode
#---------------------------------------

from BeautifulSoup import BeautifulSoup
import os, sys, time
import urllib2
from operator import itemgetter
#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
scriptDirectory = os.path.dirname(os.path.abspath(__file__)) + "/"
from loadConfig import readConfig
from helperlibrary import *
regionID = readConfig("Atmpro")['regionid']
regionName = readConfig("Atmpro")['regionname']
strHeaderLine = "\n----------------------------------------------\n"
#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+


def getTNonTunai(table):

	soup = BeautifulSoup(str(table))
	
	rows = soup.findAll('tr')

	numRows = getRowsNumber(table)

	numCols = getColsNumber(table)

	numRowsHead = getRowsHeadNumber(table)

	#Initialize

	TNonTunai = []
	
	for i in range (0, numRows):

		trs = BeautifulSoup(str(rows[i]))

		tdcells = trs.findAll("td")
		thcells = trs.findAll("th")

		if tdcells:
			strTID = tdcells[1].getText()
			strLocation = tdcells[4].getText()
			strLocation = cleanUpLocation(strLocation)
			strArea = tdcells[5].getText()
			datLastTunai = tdcells[8].getText().strip()

			if ("ATM CENTER" in strArea) or ("VENDOR" in strArea):
				intCRO = 1
				namaCROUKO = cleanUpNamaCRO(strArea)
			else:
				intCRO = 0
				namaCROUKO = cleanupNamaUker(strArea)
				
			strCabang = tdcells[6].getText()
			strKodeCabang = strCabang[:4]
			strNamaCabang = strCabang[6:]


			TNonTunai.append((strKodeCabang, namaCROUKO, intCRO, strArea, strLocation, strTID, strNamaCabang, datLastTunai))
			#TNonTunai       ((#0:strKodeCabang, #1:namaCROUKO, #2:intCRO, #3:strArea, #4:strLocation, #5:strTID, #6:strNamaCabang, #7:datLastTunai))

	TNonTunai = sorted(TNonTunai, key=itemgetter(1, 3, 2), reverse = False)

	return TNonTunai 


def getTNonTunaiCabang(TNonTunai, branchCode):

	#Initialize
	msgBody = ""
	
	TNonTunaiKanca = []
	TNonTunaiUKO = []
	TNonTunaiCRO = []

	for i in range(0, len(TNonTunai)):
		if TNonTunai[i][0] == branchCode.zfill(4):
			strNamaCabang = cleanupNamaUker(TNonTunai[i][6])
			TNonTunaiKanca.append(TNonTunai[i])

	for i in range(0, len(TNonTunaiKanca)):
		if TNonTunaiKanca[i][2] == 0:
			TNonTunaiUKO.append((TNonTunaiKanca[i][3], TNonTunaiKanca[i][5]))

	for i in range(0, len(TNonTunaiKanca)):
		if TNonTunaiKanca[i][2] == 1:
			TNonTunaiCRO.append((TNonTunaiKanca[i][1], TNonTunaiKanca[i][4], TNonTunaiKanca[i][5]))

	if TNonTunaiUKO or TNonTunaiCRO:
		msgBody = strHeaderLine +"ATM NON TUNAI "+ strNamaCabang.upper() +timestamp+ strHeaderLine + msgBody + "\n"
	else:

		msgBody = strHeaderLine +"ATM NON TUNAI "+ branchCode +timestamp+ strHeaderLine + msgBody + "\nEXCELLENT WORK!\nALL ONLINE ATM IS READY TO DISPENSE MONEY!"

	if TNonTunaiUKO:
		msgBody += "*[UKO]*\n"
		for i in range(0, len(TNonTunaiUKO)):
					msgBody += str(i+1)+" "+ str(TNonTunaiUKO[i][0])+", "+str(TNonTunaiUKO[i][1])+"\n"
		msgBody += "\n"			

	if TNonTunaiCRO:
		msgBody += "*[CRO]*\n"
		for i in range(0, len(TNonTunaiCRO)):
					msgBody += str(i+1)+" "+ str(TNonTunaiCRO[i][0]) +": "+str(TNonTunaiCRO[i][1])+", "+str(TNonTunaiCRO[i][2])+"\n"

	return 	msgBody


def getTNonTunaiCRO(TNonTunai, selectedCRO):

	#Initialize
	msgBody = ""
	seqNo = 0
	counter = 0
	TNonTunaiCRO = []
	arrCRO = ["BG", "G4S", "KEJAR", "SSI", "TAG"]

	if selectedCRO == 0:

		selectedCRO = "ALL"
		strCRO = "*[ALL CRO]*"

		for i in range(0, len(TNonTunai)):
			if TNonTunai[i][2] == 1:
				strNamaCabang = cleanupNamaUker(TNonTunai[i][-1])
				TNonTunaiCRO.append((TNonTunai[i][1], TNonTunai[i][4], TNonTunai[i][5], TNonTunai[i][7]))


	elif selectedCRO in arrCRO:

		arrCRO = [""]
		arrCRO.append(selectedCRO)
		strCRO = "*["+selectedCRO+"]*"
	
		for i in range(0, len(TNonTunai)):

			if TNonTunai[i][1] == selectedCRO:
				strNamaCabang = cleanupNamaUker(TNonTunai[i][-1])
				TNonTunaiCRO.append((TNonTunai[i][1], TNonTunai[i][4], TNonTunai[i][5], TNonTunai[i][7]))

	if TNonTunaiCRO:

		msgBody += strCRO+"\n"
		TNonTunaiCRO = sorted(TNonTunaiCRO, key=itemgetter(0,3), reverse = False)
		for i in range(0, len(TNonTunaiCRO)):

			if TNonTunaiCRO[i-1][0] != TNonTunaiCRO[i][0]:
				msgBody += "\n*[" + str(TNonTunaiCRO[i][0]) + "]*\n"
				seqNo = 0

			for j in range(0, len(arrCRO)):

				if str(TNonTunaiCRO[i][0]) == arrCRO[j]:
					seqNo += 1
					counter += 1
					msgBody += str(seqNo)+") "+ str(TNonTunaiCRO[i][1])+", "+str(TNonTunaiCRO[i][2])+", "+durasiLastTunai(str(TNonTunaiCRO[i][3]))+"\n"


		msgBody += "\n"+regionName + "-[TOTAL NONTUNAI CRO "+selectedCRO+"]: "+str(counter)

	return 	msgBody


def getTNonTunaiUKO(TNonTunai):

	#Initialize
	msgBody = ""
	seqNo = 0
	counter = 0
	TNonTunaiUKO = []

	for i in range(0, len(TNonTunai)):
	
		if TNonTunai[i][2] == 0:
			strNamaCabang = "*"+cleanupNamaUker(TNonTunai[i][6])+"*"
			TNonTunaiUKO.append((strNamaCabang.upper(), TNonTunai[i][4], TNonTunai[i][5], TNonTunai[i][7]))
			#TNonTunai       ((#0:strKodeCabang, #1:namaCROUKO, #2:intCRO, #3:strArea, #4:strLocation, #5:strTID, #6:strNamaCabang, #7:datLastTunai))
	TNonTunaiUKO = sorted(TNonTunaiUKO, key=itemgetter(0), reverse = False)

	if TNonTunaiUKO:
		TNonTunaiUKO = sorted(TNonTunaiUKO, key=itemgetter(0,3), reverse = False)
		msgBody += "*[UKO]*\n"
		for i in range(0, len(TNonTunaiUKO)):
			if TNonTunaiUKO[i-1][0] != TNonTunaiUKO[i][0]:
				msgBody +=  "\n"+str(TNonTunaiUKO[i][0]) + "\n"
				seqNo = 0

			seqNo += 1
			counter += 1
			msgBody += str(seqNo)+") "+ str(TNonTunaiUKO[i][1])+", "+str(TNonTunaiUKO[i][2])+", "+durasiLastTunai(str(TNonTunaiUKO[i][3]))+"\n"

		msgBody += "\n"+regionName + "-[TOTAL NONTUNAI UKO]: "+str(counter)

	return 	msgBody

msgBody =""

timestamp = "\nper "+ time.strftime("%d-%m-%Y pukul %H:%M")

if len(sys.argv) > 0:

	alamatURL = "http://172.18.65.42/statusatm/viewbyupnontunai.pl?REGID="+regionID

	try:
		AREAID = sys.argv[1]

		if AREAID.isdigit():

			TNonTunai = getTNonTunai(table=getWidestTable(getTableList(fetchHTML(alamatURL))))
			msgBody = getTNonTunaiCabang(TNonTunai, AREAID)

			if msgBody:	
				print msgBody

	
		if AREAID[0].isalpha():

			if AREAID.upper() == "UKO":

				try:

					TNonTunai = getTNonTunai(table=getWidestTable(getTableList(fetchHTML(alamatURL))))
					msgBody = getTNonTunaiUKO(TNonTunai)

					if msgBody:	
						msgBody = strHeaderLine +"*ATM NON TUNAI "+ AREAID.upper() + "* - "+regionName+ timestamp+ strHeaderLine + msgBody
						print msgBody.replace("**","") # double asterisk mark ("**") due to orphaned TID

				except:
					print "Ada kesalahan."

			elif AREAID.upper() == "CRO":

				try:

					TNonTunai = getTNonTunai(table=getWidestTable(getTableList(fetchHTML(alamatURL))))
					msgBody = getTNonTunaiCRO(TNonTunai, 0)

					if msgBody:	
						msgBody = strHeaderLine +"*ATM NON TUNAI "+ AREAID.upper() + "* - "+regionName+ timestamp+ strHeaderLine + msgBody
						print msgBody

				except:
					print "Ada kesalahan."

			else:

				try:

					TNonTunai = getTNonTunai(table=getWidestTable(getTableList(fetchHTML(alamatURL))))
					msgBody = getTNonTunaiCRO(TNonTunai, AREAID.upper())

					if msgBody:	
						msgBody = strHeaderLine +"*ATM NON TUNAI "+ AREAID.upper() + "* - "+regionName+ timestamp+ strHeaderLine + msgBody
						print msgBody

				except:
					print "CRO tidak dikenal."

	except:

		print "ANDA belum meng-input kode UKO/ CRO."
