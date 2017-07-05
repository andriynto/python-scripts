# -*- coding: utf-8 -*-
#!/usr/bin/python
#---------------------------------------
# helperlibrary.py
# (c) Jansen A. Simanullang
# @Medan City, Juni-Juli 2017
#---------------------------------------
# Python usage:
#
# to be imported by clause:
# from helperlibrary import function_name
#
# not to be called by command line
#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
from BeautifulSoup import BeautifulSoup
import os, sys, time
import urllib, urllib2, requests

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

def fetchHTML(alamatURL):
	# fungsi ini hanya untuk mengambil stream string HTML dari alamat URL yang akan dimonitor
	# Content-Type utf-8 raises an error when meets strange character
	#print "fetching HTML from URL...\n", alamatURL
	strHTML = urllib2.urlopen(urllib2.Request(alamatURL, headers={ 'User-Agent': 'Mozilla/5.0' })).read()

	strHTML = strHTML.decode("windows-1252")

	strHTML = strHTML.encode('ascii', 'ignore')

	strHTML = cleanUpHTML(strHTML)

	mysoup = BeautifulSoup(strHTML)
	
	#print ">> URL fetched."

	return strHTML



def cleanUpHTML(strHTML):

	# fixing broken HTML
	strHTML = strHTML.replace('</tr><td>',"</tr><tr><td>")
	strHTML = strHTML.replace('</td></tr><td>','</td></tr><tr><td>')
	strHTML = strHTML.replace('<table class=fancy>','</td></tr></table><table class=fancy>')
	strHTML = strHTML.replace('</th>\n</tr>',"</th></tr><tr>")
	strHTML = strHTML.replace('</tr>\n\n<td>',"</tr><tr><td>")


	strHTML = strHTML.replace(' bgcolor>', '>')
	strHTML = strHTML.replace('<table class=fancy>','</td></tr></table><table class=fancy>')


	return strHTML


def getStyleList(strHTML):

	#print "\ngetting Style List...\n"

	mysoup = BeautifulSoup(strHTML)

	arrStyle = mysoup.findAll('link', rel = "stylesheet" )

	strStyle = ""

	for i in range (0, len(arrStyle)):

		strStyle = strStyle + str(arrStyle[i])
	
	return strStyle


def getTableList(strHTML):

	#print "\ngetting Table List...\n"

	mysoup = BeautifulSoup(strHTML)

	arrTable = mysoup.findAll('table')

	#print "there are:", len(arrTable), "tables."

	return arrTable



def getLargestTable(arrTable):

	# pilihlah tabel yang terbesar yang memiliki jumlah baris terbanyak

	largest_table = None

	max_rows = 0

	for table in arrTable:

		# cek satu per satu jumlah baris yang ada pada masing-masing tabel dalam array kumpulan tabel
		# simpan dalam variabel bernama numRows

		numRows = len(table.findAll(lambda tag: tag.name == 'tr' and tag.findParent('table') == table))
		
		# jika jumlah baris pada suatu tabel lebih besar daripada '0' maka jadikan sebagai max_rows sementara
		# proses ini diulangi terus menerus maka max_rows akan berisi jumlah baris terbanyak

		if numRows > max_rows:
			
		        largest_table = table
			max_rows = numRows

	# ini hanya mengembalikan penyebutan 'tabel terbesar' hanya sebagai 'tabel'

	table = largest_table

	#if table:
	#	print ">> the largest from table list is chosen."

	return table



def getWidestTable(arrTable):

	# pilihlah tabel yang terbesar yang memiliki jumlah baris terbanyak

	widest_table = None

	max_cols = 0

	for table in arrTable:

		# cek satu per satu jumlah baris yang ada pada masing-masing tabel dalam array kumpulan tabel
		# simpan dalam variabel bernama numRows

		numCols = len(table.contents[1])
		
		# jika jumlah baris pada suatu tabel lebih besar daripada '0' maka jadikan sebagai max_rows sementara
		# proses ini diulangi terus menerus maka max_rows akan berisi jumlah baris terbanyak

		if numCols > max_cols:
			
		        widest_table = table
			max_cols = numCols

	# ini hanya mengembalikan penyebutan 'tabel terbesar' hanya sebagai 'tabel'

	table = widest_table

	#if table:
	#	print ">> the widest from table list is chosen."

	return table



def getColsNumber(table):

	# bagaimana cara menentukan berapa jumlah kolomnya?

	numCols = len(table.contents[1])
	
	return numCols



def getRowsNumber(table):

	# bagaimana cara menentukan berapa jumlah kolomnya?

	numRows = len(table.findAll(lambda tag: tag.name == 'tr' and tag.findParent('table') == table))
	
	return numRows



def getRowsHeadNumber(table):

	# bagaimana cara menentukan berapa jumlah baris yang terpakai sebagai header?

	soup = BeautifulSoup(str(table))
	rows = soup.findAll('tr')
	numRows = len(table.findAll(lambda tag: tag.name == 'tr' and tag.findParent('table') == table))

	# inisialisasi variabel numRowsHead sebagai jumlah baris yang mengandung header

	numRowsHead = 0	
	
	# periksa satu per satu setiap baris

	for i in range (0, numRows):
		
		# apabila dalam suatu baris tertentu terdapat tag <th>
		if rows[i].findAll('th'):
			
			# maka numRows bertambah 1
			numRowsHead = i + 1


	# hasil akhir fungsi getTableDimension ini menghasilkan jumlah baris, jumlah baris yang terpakai header, jumlah kolom dan isi tabel itu sendiri

	return numRowsHead


def getNumRowsFoot(table):

	# bagaimana cara menentukan berapa jumlah baris yang terpakai sebagai footer?

	soup = BeautifulSoup(str(table))
	foot = soup.findAll('tfoot')

	numRowsFoot = 0

	for i in range (0, len(foot)):

		numRowsFoot += len(foot[i].findAll('tr'))

	#print "there is", len(foot), "footer with", numRowsFoot, "rows"
		
	return numRowsFoot


def getTableDimension(table):
	
	numRows = getRowsNumber(table)
	numRowsHead = getRowsHeadNumber(table)
	numCols = getColsNumber(table)
	
	return numRows, numRowsHead, numCols




def getTableHeader(table):

	numRowsHead = getRowsHeadNumber(table)

	soup = BeautifulSoup(str(table))
	rows = soup.findAll('tr', limit=numRowsHead)
	strHTMLTableHeader = ""
	
	for i in range (0, numRowsHead):

		strHTMLTableHeader = strHTMLTableHeader + str(rows[i])
	
	return strHTMLTableHeader



def getRowInterest(table, keyword):

	strHTMLTableRows = getSpecificRow(table, getRowIndex(table, keyword))
	
	mysoup = BeautifulSoup(strHTMLTableRows)

	arrTDs = mysoup.findAll('td')

	return arrTDs[1].getText()




def getSpecificRows(table, rowIndex):

	#print "Let's take a look at the specific rows of index", rowIndex

	soup = BeautifulSoup(str(table))
	rows = soup.findAll('tr')
	strHTMLTableRows = ""

	for i in range (rowIndex, rowIndex+1):

		strHTMLTableRows = str(rows[i])
	
	return strHTMLTableRows



def getTableContents(table):

	numRows = getRowsNumber(table)
	numRowsHead = getRowsHeadNumber(table)

	soup = BeautifulSoup(str(table))
	rows = soup.findAll('tr')
	strHTMLTableContents = ""

	for i in range (numRowsHead, numRows):

		strHTMLTableContents = strHTMLTableContents + str(rows[i])
	
	return strHTMLTableContents



def getRowIndex(table, strSearchKey):

	# fungsi ini untuk mendapatkan nomor indeks baris yang mengandung satu kata kunci

	soup = BeautifulSoup(str(table))
	rows = soup.findAll('tr')
	
	numRows = len(table.findAll(lambda tag: tag.name == 'tr' and tag.findParent('table') == table))

	rowIndex = 0

	for i in range (0, numRows):

		trs = BeautifulSoup(str(rows[i]))
		tdcells = trs.findAll("td")
			
		for j in range (0, len(tdcells)):

			if tdcells[j].getText().upper() == strSearchKey.upper():
				
				rowIndex = i

				#print "we got the index = ", rowIndex, "from ", numRows, "for search key ='"+strSearchKey+"'"
	return rowIndex


def durasiLastTunai(strDate):

	from datetime import datetime
	strDate = strDate.replace('_',' ')

	if strDate:
		if "-" in strDate:

			format1 = '%Y-%m-%d %H:%M:%S'

		elif "/" in strDate:

			format1 = '%d/%m/%Y %H:%M'

		span = datetime.now() - datetime.strptime(strDate, format1)
		strResult = ':'.join(str(span).split('.')[:1]).replace('days','hari').replace('day','hari')
	else:
		strResult = "0"
	return strResult

def cleanUpNamaCRO(strText):

	strText = strText.replace("ATM CENTER","")
	strText = strText.replace("(","")
	strText = strText.replace(")","")
	strText = strText.replace("BRINGIN GIGANTARA","BG")
	strText = strText.replace("BG III","BG")
	strText = strText.replace("BG II","BG")
	strText = strText.replace("SWADARMA SARANA","SSI")
	strText = strText.replace("SECURICOR","G4S")
	strText = strText.replace("VENDOR CRO II BG MEDAN","BG")
	strText = strText.replace("9842-BG","BG")
	strText = strText.replace("9831-VENDOR CRO SSI MEDAN","SSI")
	strText = strText.replace("9849-VENDOR CRO III KEJAR MEDAN","KEJAR")
	strText = strText.replace("[","")

	if "BG" in strText:
		strText = strText.replace(strText, "BG")

	if "KEJAR" in strText:
		strText = strText.replace(strText, "KEJAR")

	if "SSI" in strText:
		strText = strText.replace(strText, "SSI")

	if "TAG" in strText:
		strText = strText.replace(strText, "TAG")

	if "G4S" in strText:
		strText = strText.replace(strText, "G4S")

	return strText.strip()


def cleanupNamaUker(namaUker):


	namaUker = namaUker.replace("JAKARTA","")
	namaUker = namaUker.replace("Jakarta ","") 
	namaUker = namaUker.replace("JKT ","")
	namaUker = namaUker.replace("KANCA ","")
	namaUker = namaUker.replace("KC ","")

	return namaUker.strip()


def cleanUpLocation(strLocation):

	strLocation = strLocation.replace("JKT3","")
	strLocation = strLocation.replace("INDOMARET","IDM")
	strLocation = strLocation.replace("JAK 3","")
	strLocation = strLocation.replace("JAKARTA 3","")
	strLocation = strLocation.replace("JAKARTA3","")
	strLocation = strLocation.replace("JKT 3","")
	strLocation = strLocation.replace("PUBL","")
	strLocation = strLocation.replace("G4S ","")
	strLocation = strLocation.replace("TAG ","")
	strLocation = strLocation.replace("SSI ","")
	strLocation = strLocation.replace("CRO ","")
	strLocation = strLocation.replace("-","")
	strLocation = strLocation.replace("MEDAN ","")
	strLocation = strLocation.replace("MDN ","")
	strLocation = strLocation.replace("UNIT ","U ")
	strLocation = strLocation.replace("[","")
	strLocation = strLocation.strip()

	return strLocation


def colorAvail(percentAvail):

	strColor = ""

	if percentAvail >= 0.00:
		strColor = "merah"
	if percentAvail > 87.00:
		strColor = "kuning"
	if percentAvail > 96.00:
		strColor = "hijau_muda"
	if percentAvail > 98.00:
		strColor = "hijau_tua"


	return strColor


def colorRelia(RELIA):

	strColor = ""

	if RELIA >= 0.00:
		strColor = "merah"
	if RELIA > 87.00:
		strColor = "kuning"
	if RELIA > 96.00:
		strColor = "hijau_muda"
	if RELIA > 98.00:
		strColor = "hijau_tua"


	return strColor

def colorUtility(UTILITY):

	strColor = ""

	if UTILITY >= 0.00:
		strColor = "merah"
	if UTILITY >= 87.00:
		strColor = "kuning"
	if UTILITY >= 96.00:
		strColor = "hijau_muda"
	if UTILITY >= 98.00:
		strColor = "hijau_tua"

	return strColor

def TelegramBotSender(chat_id, strText):

	encText=urllib.quote_plus(strText)

	strURL = "https://api.telegram.org/bot"+secretKey+"/sendMessage?parse_mode=Markdown&chat_id="+chat_id+"&text="+urllib.quote_plus(strText)

	if behindProxy:

		os.system('proxychains w3m -dump "'+ strURL+'"')
	else:
		os.system('w3m -dump "'+ strURL+'"')


def TelegramTextSender(telegram_id, strText):
	#fungsi ini untuk mengatasi batasan telegram text 4096 karakter

	strText = strText.replace("**","")

	if len(strText) <= textLimit:

		TelegramBotSender(telegram_id, strText)
	else:
		step = textLimit
		
		for i in range(0, len(strText), textLimit):

			slice = strText[i:step]
			TelegramBotSender(telegram_id, slice)
			print slice
			step += textLimit
