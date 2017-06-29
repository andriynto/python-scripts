#!/usr/bin/python
#---------------------------------------
# fetchStatusATMNonTunai.py
# (c) Jansen A. Simanullang, 11:15:55
# @BSD City: 14 Januari 2016 09:04:11
# 13 Agustus 2016 13:58:28 - 15:30, 16:33
# 28 November 2016 14:36 # asterisks added
# @Medan City: 24.06.2017
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
regionID = readConfig("Atmpro")['regionid']
regionName = readConfig("Atmpro")['regionname']
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
	
		msgBody += "*[UKO]*\n"
		for i in range(0, len(TNonTunaiUKO)):
			if TNonTunaiUKO[i-1][0] != TNonTunaiUKO[i][0]:
				msgBody +=  "\n"+str(TNonTunaiUKO[i][0]) + "\n"
				seqNo = 0

			seqNo += 1
			counter += 1
			msgBody += str(seqNo)+") "+ str(TNonTunaiUKO[i][1])+", "+str(TNonTunaiUKO[i][2])+", "+durasiLastTunai(str(TNonTunaiUKO[i][3]).replace("_"," "))+"\n"

		msgBody += "\n"+regionName + "-[TOTAL NONTUNAI UKO]: "+str(counter)

	return 	msgBody

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

	return strText.strip()

def cleanupNamaUker(namaUker):


	namaUker = namaUker.replace("JAKARTA ","")
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
	strLocation = strLocation.strip()

	return strLocation



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
						print msgBody.replace("**","").replace("MEDAN ","").replace("MDN ","").replace("UNIT ","U ")

				except:
					print "Ada kesalahan."

			elif AREAID.upper() == "CRO":

				try:

					TNonTunai = getTNonTunai(table=getWidestTable(getTableList(fetchHTML(alamatURL))))
					msgBody = getTNonTunaiCRO(TNonTunai, 0)

					if msgBody:	
						msgBody = strHeaderLine +"*ATM NON TUNAI "+ AREAID.upper() + "* - "+regionName+ timestamp+ strHeaderLine + msgBody
						print msgBody.replace("MEDAN ","").replace("MDN ","")

				except:
					print "Ada kesalahan."

			else:

				try:

					TNonTunai = getTNonTunai(table=getWidestTable(getTableList(fetchHTML(alamatURL))))
					msgBody = getTNonTunaiCRO(TNonTunai, AREAID.upper())

					if msgBody:	
						msgBody = strHeaderLine +"*ATM NON TUNAI "+ AREAID.upper() + " - "+regionName+ timestamp+ strHeaderLine + msgBody
						print msgBody

				except:
					print "CRO tidak dikenal."

	except:

		print "ANDA belum meng-input kode UKO/ CRO."
