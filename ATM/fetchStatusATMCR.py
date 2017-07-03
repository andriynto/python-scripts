#!/usr/bin/python
#---------------------------------------
# fetchStatusATM.py
# (c) Jansen A. Simanullang, 11:15:55
# to be used with telegram-bot plugin
#---------------------------------------
# usage: fetchStatusATM 1234567
# script name followed by space and TID
#---------------------------------------

from BeautifulSoup import BeautifulSoup
import sys, time
import urllib2

from helperlibrary import *
#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
scriptDirectory = os.path.dirname(os.path.abspath(__file__)) + "/"
from loadConfig import readConfig
regionID = readConfig("Atmpro")['regionid'].upper()
regionName = readConfig("Atmpro")['regionname']
strHeaderLine = "\n---------------------------------\n"
#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

def getATMStats(table):

	soup = BeautifulSoup(str(table))
	
	rows = soup.findAll('tr')

	numRows = getRowsNumber(table)

	numCols = getColsNumber(table)

	numRowsHead = getRowsHeadNumber(table)

	#print numRowsHead, numRows
	msgBody = ""

	seqNo = 0
	
	for i in range (0, numRows):

		trs = BeautifulSoup(str(rows[i]))

		tdcells = trs.findAll("td")
		thcells = trs.findAll("th")

		#print len(tdcells), len(thcells)



		if tdcells:


			msgBody += "\n"+tdcells[0].getText().upper()+") "+ tdcells[1].getText()+", " + tdcells[2].getText().replace("HYOSUNG","HYOSUNG ") +"\nLOKASI: "+ tdcells[4].getText() +"\nAREA: "+ tdcells[6].getText() +"\n"+"\n"
	if msgBody == "":
		msgBody = "Tidak ada ATM CR di wilayah kerja Anda."
	return msgBody



def getATMStatsCRO(table):

	soup = BeautifulSoup(str(table))
	
	rows = soup.findAll('tr')

	numRows = getRowsNumber(table)

	numCols = getColsNumber(table)

	numRowsHead = getRowsHeadNumber(table)

	#print numRowsHead, numRows
	msgBody = ""

	seqNo = 0
	
	for i in range (0, numRows):

		trs = BeautifulSoup(str(rows[i]))

		tdcells = trs.findAll("td")
		thcells = trs.findAll("th")

		#print len(tdcells), len(thcells)


		if tdcells:

			if "ATM CENTER" in tdcells[6].getText():

				seqNo = seqNo +1

				msgBody += "\n"+str(seqNo)+") "+"CRO: " + tdcells[6].getText().replace("ATM CENTER (","").replace(")","")+ "\nTID: " +tdcells[1].getText()+", " + tdcells[2].getText().replace("HYOSUNG","HYOSUNG ") +"\nLOKASI: "+ tdcells[5].getText()+"\nDURASI: "+ tdcells[8].getText() +"\nUKER: "+tdcells[7].getText().upper()+"\n"
	if msgBody == "":
		msgBody = "Tidak ada ATM CR CRO kategori ini di wilayah kerja Anda."
	return msgBody


def getATMStatsUKO(table):

	soup = BeautifulSoup(str(table))
	
	rows = soup.findAll('tr')

	numRows = getRowsNumber(table)

	numCols = getColsNumber(table)

	numRowsHead = getRowsHeadNumber(table)

	#print numRowsHead, numRows
	msgBody = ""

	seqNo = 0

	
	for i in range (0, numRows):

		trs = BeautifulSoup(str(rows[i]))

		tdcells = trs.findAll("td")
		thcells = trs.findAll("th")

		#print len(tdcells), len(thcells)


		if tdcells:

			if "ATM CENTER" not in tdcells[6].getText():

				seqNo = seqNo +1

				msgBody += "\n"+str(seqNo)+") " + tdcells[7].getText().upper() + "\nTID: " + tdcells[1].getText()+", " + tdcells[2].getText().replace("HYOSUNG","HYOSUNG ") +"\nLOKASI: "+ tdcells[5].getText()+"\nDURASI: "+ tdcells[8].getText()+"\n"
	if msgBody == "":
		msgBody = "Tidak ada ATM CR UKO kategori ini di wilayah kerja Anda."
	return msgBody



msgBody =""

timestamp = "\nper "+ time.strftime("%d-%m-%Y pukul %H:%M")

if len(sys.argv) > 0:

	AREAID = sys.argv[1]

	strHeaderLine = "\n----------------------------------------------\n"

	if AREAID.isdigit():
	

		if msgBody:	

			msgBody = "cara penggunaan:\n!status cr [cro|uko]\nmengambil status ATM yang bermasalah pada Card Reader (CR)"
			print msgBody


	if AREAID.lower() == "cro":

		alamatURL = "http://172.18.65.42/statusatm/viewbyregionprobooscr.pl?REGID="+regionID+"&ERROR=CCR_ST&gr=Y"

		msgBody = getATMStatsCRO(table=getWidestTable(getTableList(fetchHTML(alamatURL))))

		if msgBody:	

			msgBody = strHeaderLine +"ATM CR GARANSI "+ AREAID.upper() +timestamp+ strHeaderLine + msgBody
			print msgBody

		alamatURL = "http://172.18.65.42/statusatm/viewbyregionprobooscr.pl?REGID="+regionID+"&ERROR=CCR_ST&gr=N"

		msgBody = getATMStatsCRO(table=getWidestTable(getTableList(fetchHTML(alamatURL))))

		if msgBody:	

			msgBody = strHeaderLine +"ATM CR NON GARANSI "+ AREAID.upper() +timestamp+ strHeaderLine + msgBody
			print msgBody

	if AREAID.lower() == "uko":

		alamatURL = "http://172.18.65.42/statusatm/viewbyregionprobooscr.pl?REGID="+regionID+"&ERROR=CCR_ST&gr=Y"

		msgBody = getATMStatsUKO(table=getWidestTable(getTableList(fetchHTML(alamatURL))))

		if msgBody:	

			msgBody = strHeaderLine +"ATM CR GARANSI "+ AREAID.upper() +timestamp+ strHeaderLine + msgBody
			print msgBody

		alamatURL = "http://172.18.65.42/statusatm/viewbyregionprobooscr.pl?REGID="+regionID+"&ERROR=CCR_ST&gr=N"

		msgBody = getATMStatsUKO(table=getWidestTable(getTableList(fetchHTML(alamatURL))))

		if msgBody:	

			msgBody = strHeaderLine +"ATM CR NON GARANSI "+ AREAID.upper() +timestamp+ strHeaderLine + msgBody
			print msgBody
