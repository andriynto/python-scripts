#!/usr/bin/python
#---------------------------------------
# fetchStatusATMDF.py
# (c) Jansen A. Simanullang, 11:15:55
#     updated 22.10.2015 17:05
# to be used with telegram-bot plugin
#---------------------------------------
# usage: fetchStatusATMDF 1234567
# script name followed by space and TID/UKO/CRO
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

def getATMStats(table, AREAID):

	soup = BeautifulSoup(str(table))
	
	rows = soup.findAll('tr')

	numRows = getRowsNumber(table)

	numCols = getColsNumber(table)

	numRowsHead = getRowsHeadNumber(table)

	#print numRowsHead, numRows
	msgBody = ""
	counterATM = 0
	
	for i in range (0, numRows):

		trs = BeautifulSoup(str(rows[i]))

		tdcells = trs.findAll("td")
		thcells = trs.findAll("th")

		#print len(tdcells), len(thcells)



		if tdcells and (AREAID in tdcells[7].getText()):
			counterATM +=1
		
			msgBody += "\n"+str(counterATM)+") "+ tdcells[1].getText()+", " + tdcells[2].getText().replace("HYOSUNG","HYOSUNG ") +"\nLOKASI: "+ tdcells[5].getText() +"\nDURASI: "+ tdcells[9].getText() +"\nKETERANGAN:\n"+ tdcells[8].getText().strip() +"\n"

	if msgBody == "":
		msgBody = "Tidak ada ATM DF dalam kategori ini di wilayah kerja Anda."

	return msgBody



def getATMStatsCRO(table, AREAID):

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

				msgBody += "\n"+str(seqNo)+") " + tdcells[7].getText() + "\nCRO: "+ tdcells[6].getText().replace("ATM CENTER","").replace("(","").replace(")","")+ "\n\nTID:" +tdcells[1].getText()+", " + tdcells[2].getText().replace("HYOSUNG","HYOSUNG ") +"\nLOKASI: "+ tdcells[5].getText() +"\nDURASI: "+ tdcells[9].getText().replace("days", "hari ").replace("hours","jam") + "\n"

				if tdcells[9].getText():

					msgBody += "KETERANGAN:\n"+ tdcells[8].getText().lower() + "\n"

	if msgBody == "":
		msgBody = "Tidak ada ATM DF CRO kategori ini di wilayah kerja Anda."

	return msgBody


def getATMStatsUKO(table, AREAID):

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

				msgBody += "\n"+str(seqNo)+") "+ tdcells[7].getText() + "\n" + tdcells[1].getText()+", " + tdcells[2].getText().replace("HYOSUNG","HYOSUNG ") +"\n\nLOKASI: "+ tdcells[5].getText() +"\nDURASI: "+ tdcells[9].getText().replace("days", "hari ").replace("hours","jam") +"\n"

				if tdcells[9].getText():

					msgBody += "KETERANGAN:\n"+ tdcells[8].getText().lower() + "\n"

	if msgBody == "":
		msgBody = "Tidak ada ATM DF UKO kategori ini di wilayah kerja Anda."

	return msgBody



msgBody =""
timestamp = "\nper "+ time.strftime("%d-%m-%Y pukul %H:%M")

if len(sys.argv) > 0:

	AREAID = sys.argv[1]

	strHeaderLine = "\n-----------------------------------\n"

	if AREAID.isdigit():

		alamatURL = "http://172.18.65.42/statusatm/viewbyregionprobdf1.pl?REGID="+regionID+"&ERROR=DISP_ST"

		msgBody = getATMStats(table=getWidestTable(getTableList(fetchHTML(alamatURL))), AREAID=AREAID)

		if msgBody:	

			msgBody = strHeaderLine +"ATM DF <= 5 hari  "+ AREAID + timestamp + strHeaderLine + msgBody
			print msgBody

		alamatURL = "http://172.18.65.42/statusatm/viewbyregionprobdf2.pl?REGID="+regionID+"&ERROR=DISP_ST"

		msgBody = getATMStats(table=getWidestTable(getTableList(fetchHTML(alamatURL))), AREAID=AREAID)

		if msgBody:	

			msgBody = strHeaderLine +"ATM DF 6-15 hari "+ AREAID + timestamp + strHeaderLine + msgBody
			print msgBody

		alamatURL = "http://172.18.65.42/statusatm/viewbyregionprobdf3.pl?REGID="+regionID+"&ERROR=DISP_ST"

		msgBody = getATMStats(table=getWidestTable(getTableList(fetchHTML(alamatURL))), AREAID=AREAID)

		if msgBody:	

			msgBody = strHeaderLine +"ATM DF >= 16 hari "+ AREAID + timestamp + strHeaderLine + msgBody
			print msgBody

	if AREAID.lower() == "cro":

		alamatURL = "http://172.18.65.42/statusatm/viewbyregionprobdf1.pl?REGID="+regionID+"&ERROR=DISP_ST"

		msgBody = getATMStatsCRO(table=getWidestTable(getTableList(fetchHTML(alamatURL))), AREAID=AREAID)

		if msgBody:	

			msgBody = strHeaderLine +"ATM DF <= 5 hari  "+ AREAID + timestamp + strHeaderLine + msgBody
			print msgBody

		alamatURL = "http://172.18.65.42/statusatm/viewbyregionprobdf2.pl?REGID="+regionID+"&ERROR=DISP_ST"

		msgBody = getATMStatsCRO(table=getWidestTable(getTableList(fetchHTML(alamatURL))), AREAID=AREAID)

		if msgBody:	

			msgBody = strHeaderLine +"ATM DF 6-15 hari "+ AREAID + timestamp + strHeaderLine + msgBody
			print msgBody

		alamatURL = "http://172.18.65.42/statusatm/viewbyregionprobdf3.pl?REGID="+regionID+"&ERROR=DISP_ST"

		msgBody = getATMStatsCRO(table=getWidestTable(getTableList(fetchHTML(alamatURL))), AREAID=AREAID)

		if msgBody:	

			msgBody = strHeaderLine +"ATM DF >= 16 hari "+ AREAID + timestamp + strHeaderLine + msgBody
			print msgBody

	if AREAID.lower() == "uko":

		alamatURL = "http://172.18.65.42/statusatm/viewbyregionprobdf1.pl?REGID="+regionID+"&ERROR=DISP_ST"

		msgBody = getATMStatsUKO(table=getWidestTable(getTableList(fetchHTML(alamatURL))), AREAID=AREAID)

		if msgBody:	

			msgBody = strHeaderLine +"ATM DF <= 5 hari  "+ AREAID + timestamp + strHeaderLine + msgBody
			print msgBody

		alamatURL = "http://172.18.65.42/statusatm/viewbyregionprobdf2.pl?REGID="+regionID+"&ERROR=DISP_ST"

		msgBody = getATMStatsUKO(table=getWidestTable(getTableList(fetchHTML(alamatURL))), AREAID=AREAID)

		if msgBody:	

			msgBody = strHeaderLine +"ATM DF 6-15 hari "+ AREAID + timestamp + strHeaderLine + msgBody
			print msgBody

		alamatURL = "http://172.18.65.42/statusatm/viewbyregionprobdf3.pl?REGID="+regionID+"&ERROR=DISP_ST"

		msgBody = getATMStatsUKO(table=getWidestTable(getTableList(fetchHTML(alamatURL))), AREAID=AREAID)

		if msgBody:	

			msgBody = strHeaderLine +"ATM DF >= 16 hari "+ AREAID + timestamp + strHeaderLine + msgBody
			print msgBody

