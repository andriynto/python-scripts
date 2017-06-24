#!/usr/bin/python
#---------------------------------------
# fetchStatusATMOFF.py
# (c) Jansen A. Simanullang, 11:15:55
# @BSD CITY: 14 Januari 2016 09:04:11 - 
# 22.11.2016 15:48 
# @MEDAN CITY: 24.06.2017
# to be used with telegram-bot plugin
#---------------------------------------
# usage: fetchStatusATMOFF cro/uko/kode cabang
# script name followed by cro/uko or branchCode
#---------------------------------------

from BeautifulSoup import BeautifulSoup
import os, sys, time
import urllib2
from operator import itemgetter

#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
scriptDirectory = os.path.dirname(os.path.abspath(__file__)) + "/"
from loadConfig import readConfig
regionID = readConfig("Atmpro")['regionid'].upper()
regionName = readConfig("Atmpro")['regionname']
strHeaderLine = "\n*----------------------------------------------*\n"
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


def getTOffline(table):

	soup = BeautifulSoup(str(table))
	rows = soup.findAll('tr')
	numRows = getRowsNumber(table)
	numCols = getColsNumber(table)
	numRowsHead = getRowsHeadNumber(table)

	#Initialize
	TOffline = []
	
	for i in range (0, numRows):

		trs = BeautifulSoup(str(rows[i]))
		tdcells = trs.findAll("td")
		thcells = trs.findAll("th")

		if tdcells:
			strTID = tdcells[1].getText()
			strLocation = tdcells[5].getText()
			strLocation = cleanUpLocation(strLocation)
			strArea = tdcells[7].getText()

			if ("ATM CENTER" in strArea) or ("VENDOR" in strArea):
				intCRO = 1
				namaCROUKO = cleanUpNamaCRO(strArea)
			else:
				intCRO = 0
				namaCROUKO = cleanupNamaUker(strArea)
				
			strCabang = tdcells[6].getText()
			strKodeCabang = strCabang[:4]
			strNamaCabang = strCabang[6:]
			TOffline.append((strKodeCabang, namaCROUKO, intCRO, strArea, strLocation, strTID, strNamaCabang))

	TOffline = sorted(TOffline, key=itemgetter(1, 3, 2), reverse = False)

	return TOffline 


def getTOfflineCabang(TOffline, branchCode):

	#Initialize
	msgBody = ""
	
	TOfflineKanca = []
	TOfflineUKO = []
	TOfflineCRO = []

	for i in range(0, len(TOffline)):
		if TOffline[i][0] == branchCode.zfill(4):
			strNamaCabang = cleanupNamaUker(TOffline[i][-1])
			TOfflineKanca.append(TOffline[i])

	for i in range(0, len(TOfflineKanca)):
		if TOfflineKanca[i][2] == 0:
			TID = TOfflineKanca[i][5]
			TOfflineUKO.append((TOfflineKanca[i][3], TID, getLastTunai(TID)))

	for i in range(0, len(TOfflineKanca)):
		if TOfflineKanca[i][2] == 1:
			TID = TOfflineKanca[i][5]
			TOfflineCRO.append((TOfflineKanca[i][1], TOfflineKanca[i][4], TID, getLastTunai(TID)))

	if TOfflineUKO or TOfflineCRO:
		msgBody = strHeaderLine +"ATM OFFLINE "+ strNamaCabang.upper() +timestamp+ strHeaderLine + msgBody + "\n"
	else:

		msgBody = strHeaderLine +"ATM OFFLINE "+ branchCode +timestamp+ strHeaderLine + msgBody + "\nTidak ada ATM kategori ini di wilayah Anda!"

	if TOfflineUKO:
		msgBody += "*[UKO]*\n"
		for i in range(0, len(TOfflineUKO)):
					msgBody += str(i+1)+" "+ str(TOfflineUKO[i][0])+", "+str(TOfflineUKO[i][1])+", "+durasiHinggaKini(str(TOfflineUKO[i][2]))+"\n"
		msgBody += "\n"			

	if TOfflineCRO:
		msgBody += "*[CRO]*\n"
		for i in range(0, len(TOfflineCRO)):
					msgBody += str(i+1)+" "+ str(TOfflineCRO[i][0]) +": "+str(TOfflineCRO[i][1])+", "+str(TOfflineCRO[i][2])+", "+durasiHinggaKini(str(TOfflineCRO[i][3]))+"\n"

	return 	msgBody


def getTOfflineCRO(TOffline, selectedCRO):

	#Initialize
	msgBody = ""
	seqNo = 0
	counter = 0
	TOfflineCRO = []
	arrCRO = ["BG", "G4S", "KEJAR", "SSI", "TAG"]

	if selectedCRO == 0:

		selectedCRO = "ALL"
		strCRO = "[*ALL CRO*]"

		for i in range(0, len(TOffline)):
			if TOffline[i][2] == 1:
				strNamaCabang = "*"+cleanupNamaUker(TOffline[i][-1])+"*"
				TID = TOffline[i][5]
				TOfflineCRO.append((TOffline[i][1], TOffline[i][4], TID, getLastTunai(TID)))

	elif selectedCRO in arrCRO:

		arrCRO = [""]
		arrCRO.append(selectedCRO)
		strCRO = "*["+selectedCRO+"]*"
	
		for i in range(0, len(TOffline)):

			if TOffline[i][1] == selectedCRO:
				strNamaCabang = cleanupNamaUker(TOffline[i][-1])
				TID = TOffline[i][1]
				TOfflineCRO.append((TOffline[i][1], TOffline[i][4], TID, getLastTunai(TID)))

	if TOfflineCRO:

		msgBody += strCRO+"\n"
		for i in range(0, len(TOfflineCRO)):

			if TOfflineCRO[i-1][0] != TOfflineCRO[i][0]:
				msgBody += "\n*[" + str(TOfflineCRO[i][0]) + "]*\n"
				seqNo = 0

			for j in range(0, len(arrCRO)):

				if str(TOfflineCRO[i][0]) == arrCRO[j]:
					seqNo += 1
					counter += 1
					msgBody += str(seqNo)+") "+ str(TOfflineCRO[i][1])+", "+str(TOfflineCRO[i][2])+", "+durasiHinggaKini(str(TOfflineCRO[i][3]))+"\n"

		msgBody += "\n"+regionName + "-[TOTAL OFFLINE CRO "+selectedCRO+"]: "+str(counter)

	return 	msgBody


def getTOfflineUKO(TOffline):

	#Initialize
	msgBody = ""
	seqNo = 0
	counter = 0
	TOfflineUKO = []

	for i in range(0, len(TOffline)):
	
		if TOffline[i][2] == 0:
			strNamaCabang = "*"+cleanupNamaUker(TOffline[i][-1])+"*"
			TID = TOffline[i][5]
			TOfflineUKO.append((strNamaCabang.upper(), TOffline[i][4], TID, getLastTunai(TID)))

	TOfflineUKO = sorted(TOfflineUKO, key=itemgetter(0), reverse = False)

	if TOfflineUKO:
	
		msgBody += "*[UKO]*\n"
		for i in range(0, len(TOfflineUKO)):
			if TOfflineUKO[i-1][0] != TOfflineUKO[i][0]:
				msgBody +=  "\n"+str(TOfflineUKO[i][0]) + "\n"
				seqNo = 0

			seqNo += 1
			counter += 1
			msgBody += str(seqNo)+") "+ str(TOfflineUKO[i][1])+", "+str(TOfflineUKO[i][2])+", "+durasiHinggaKini(str(TOfflineUKO[i][3]))+"\n"

		msgBody += "\n"+regionName + "-[TOTAL OFFLINE UKO]: "+str(counter)

	return 	msgBody

def getTOfflineACI(TOffline, selectedACI):
	# Alfamart, Ceriamart, Indomart

	msgBody = ""
	seqNo = 0
	counter = 0
	TOfflineACI = []

	for i in range(0, len(TOffline)):

		if selectedACI in TOffline[i][4]:
			seqNo += 1
			strNamaCabang = "*"+cleanupNamaUker(TOffline[i][-1])+"*"
			TID = TOffline[i][5]
			strLocation = TOffline[i][4]
			TOfflineACI.append((strNamaCabang.upper(), strLocation, TID, getLastTunai(TID)))

	TOfflineACI = sorted(TOfflineACI, key=itemgetter(0), reverse = False)
	seqNo = 0
	if TOfflineACI:
	
		if len(TOfflineACI) == 1:
			msgBody +=  "\n"+str(TOfflineACI[0][0]) + "\n"

		for i in range(0, len(TOfflineACI)):
			if TOfflineACI[i-1][0] != TOfflineACI[i][0]:
				msgBody +=  "\n"+str(TOfflineACI[i][0]) + "\n"
				seqNo = 0
			seqNo += 1
			counter += 1
			msgBody += str(seqNo)+") "+ str(TOfflineACI[i][1])+", "+str(TOfflineACI[i][2])+", "+durasiHinggaKini(str(TOfflineACI[i][3]))+"\n"

		msgBody += "\n"+regionName + "-[TOTAL OFFLINE "+selectedACI.upper()+"]: "+str(counter)

	return 	msgBody


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
	strLocation = strLocation.replace("JAKARTA 1","")
	strLocation = strLocation.replace("JAKARTA3","")
	strLocation = strLocation.replace("KANWIL 3","")
	strLocation = strLocation.replace("JAKARTA","")
	strLocation = strLocation.replace("JKT 3","")
	strLocation = strLocation.replace("JKT","")
	strLocation = strLocation.replace("PUBL","")
	strLocation = strLocation.replace("G4S ","")
	strLocation = strLocation.replace("TAG ","")
	strLocation = strLocation.replace("SSI ","")
	strLocation = strLocation.replace("CRO ","")
	strLocation = strLocation.replace("-","")
	strLocation = strLocation.strip()

	return strLocation

def getLastTunai(TID):

	alamatURL = "http://172.18.65.42/statusatm/viewatmdetail.pl?ATM_NUM="+ TID
	table = getLargestTable(getTableList(fetchHTML(alamatURL)))

	soup = BeautifulSoup(str(table))
	rows = soup.findAll('tr')
	numRows = getRowsNumber(table)
	msgBody = ""
	
	for i in range (0, numRows):
		trs = BeautifulSoup(str(rows[i]))
		tdcells = trs.findAll("td")
		if tdcells:
			if "TUNAI" in tdcells[0].getText().upper() :
					msgBody += tdcells[0].getText().upper()+": "+ tdcells[1].getText() +"\n"

	return msgBody.replace("SUKSES TRX. TUNAI:","").strip()


def durasiHinggaKini(strDate):

	from datetime import datetime
	format1 = '%d/%m/%Y %H:%M'
	span = datetime.now() - datetime.strptime(strDate.replace('_',' '), format1)
	return ':'.join(str(span).split('.')[:1]).replace('days','hari')



msgBody =""

timestamp = "\nper "+ time.strftime("%d-%m-%Y pukul %H:%M")

if len(sys.argv) > 0:

	alamatURL = "http://172.18.65.42/statusatm/viewbyoffline.pl?REGID=" + regionID + "&ERROR=DOWN_ST"

	try:
		AREAID = sys.argv[1]

		if AREAID.isdigit():

			alamatURL = "http://172.18.65.42/statusatm/viewbyoffline.pl?REGID=" + regionID + "&ERROR=DOWN_ST"
			TOffline = getTOffline(table=getWidestTable(getTableList(fetchHTML(alamatURL))))
			msgBody = getTOfflineCabang(TOffline, AREAID)
			if msgBody:	
				msgBody = strHeaderLine +"ATM OFF (< 6 JAM) "+ AREAID.upper() + msgBody
				print msgBody

			alamatURL = "http://172.18.65.42/statusatm/viewbyoffline2.pl?REGID=" + regionID + "&ERROR=DOWN_ST"
			TOffline = getTOffline(table=getWidestTable(getTableList(fetchHTML(alamatURL))))
			msgBody = getTOfflineCabang(TOffline, AREAID)
			if msgBody:
				msgBody = strHeaderLine +"ATM OFF (> 6 JAM)  "+ AREAID.upper() + msgBody
				print msgBody

			alamatURL = "http://172.18.65.42/statusatm/viewbyoffline3kurang45.pl?REGID=" + regionID + "&ERROR=DOWN_ST"
			TOffline = getTOffline(table=getWidestTable(getTableList(fetchHTML(alamatURL))))
			msgBody = getTOfflineCabang(TOffline, AREAID)
			if msgBody:
				msgBody = strHeaderLine +"ATM OFF (> 1 HARI)  "+ AREAID.upper() + msgBody
				print msgBody

	
		if AREAID[0].isalpha():

			if AREAID.upper() == "UKO":

				try:
		
					alamatURL = "http://172.18.65.42/statusatm/viewbyoffline.pl?REGID=" + regionID + "&ERROR=DOWN_ST"
					TOffline = getTOffline(table=getWidestTable(getTableList(fetchHTML(alamatURL))))
					msgBody = getTOfflineUKO(TOffline)

					if msgBody:	
						msgBody = strHeaderLine +"ATM OFF (< 6 JAM)  "+ AREAID.upper() + " - "+regionName+ timestamp+ strHeaderLine + msgBody
						print msgBody

					alamatURL = "http://172.18.65.42/statusatm/viewbyoffline2.pl?REGID=" + regionID + "&ERROR=DOWN_ST"
					TOffline = getTOffline(table=getWidestTable(getTableList(fetchHTML(alamatURL))))
					msgBody = getTOfflineUKO(TOffline)

					if msgBody:	
						msgBody = strHeaderLine +"ATM OFF (> 6 JAM)  "+ AREAID.upper() + " - "+regionName+ timestamp+ strHeaderLine + msgBody
						print msgBody

					alamatURL = "http://172.18.65.42/statusatm/viewbyoffline3kurang45.pl?REGID=" + regionID + "&ERROR=DOWN_ST"
					TOffline = getTOffline(table=getWidestTable(getTableList(fetchHTML(alamatURL))))
					msgBody = getTOfflineUKO(TOffline)

					if msgBody:	
						msgBody = strHeaderLine +"ATM OFF (> 1 HARI)  "+ AREAID.upper() + " - "+regionName+ timestamp+ strHeaderLine + msgBody
						print msgBody

				except:
					print "Ada kesalahan."

			elif AREAID.upper() == "CRO":

				try:
					alamatURL = "http://172.18.65.42/statusatm/viewbyoffline.pl?REGID=" + regionID + "&ERROR=DOWN_ST"
					TOffline = getTOffline(table=getWidestTable(getTableList(fetchHTML(alamatURL))))
					msgBody = getTOfflineCRO(TOffline, 0)

					if msgBody:	
						msgBody = strHeaderLine +"ATM OFF (< 6 JAM)  "+ AREAID.upper() + " - "+regionName+ timestamp+ strHeaderLine + msgBody
						print msgBody

					alamatURL = "http://172.18.65.42/statusatm/viewbyoffline2.pl?REGID=" + regionID + "&ERROR=DOWN_ST"
					TOffline = getTOffline(table=getWidestTable(getTableList(fetchHTML(alamatURL))))
					msgBody = getTOfflineCRO(TOffline, 0)

					if msgBody:	
						msgBody = strHeaderLine +"ATM OFF (> 6 JAM)  "+ AREAID.upper() + " - "+regionName+ timestamp+ strHeaderLine + msgBody
						print msgBody

					alamatURL = "http://172.18.65.42/statusatm/viewbyoffline3kurang45.pl?REGID=" + regionID + "&ERROR=DOWN_ST"
					TOffline = getTOffline(table=getWidestTable(getTableList(fetchHTML(alamatURL))))
					msgBody = getTOfflineCRO(TOffline, 0)

					if msgBody:	
						msgBody = strHeaderLine +"ATM OFF (> 1 HARI)  "+ AREAID.upper() + " - "+regionName+ timestamp+ strHeaderLine + msgBody
						print msgBody

				except:
					print "Ada kesalahan."

			else:

				try:
					alamatURL = "http://172.18.65.42/statusatm/viewbyoffline.pl?REGID=" + regionID + "&ERROR=DOWN_ST"
					TOffline = getTOffline(table=getWidestTable(getTableList(fetchHTML(alamatURL))))
					msgBody = getTOfflineACI(TOffline, AREAID.upper())
					if msgBody:	
						msgBody = strHeaderLine +"ATM OFF (< 6 JAM)  "+ AREAID.upper() + " - "+regionName+ timestamp+ strHeaderLine + msgBody
						print msgBody

					alamatURL = "http://172.18.65.42/statusatm/viewbyoffline2.pl?REGID=" + regionID + "&ERROR=DOWN_ST"
					TOffline = getTOffline(table=getWidestTable(getTableList(fetchHTML(alamatURL))))
					msgBody = getTOfflineACI(TOffline, AREAID.upper())
					if msgBody:	
						msgBody = strHeaderLine +"ATM OFF (> 6 JAM)  "+ AREAID.upper() + " - "+regionName+ timestamp+ strHeaderLine + msgBody
						print msgBody

					alamatURL = "http://172.18.65.42/statusatm/viewbyoffline3kurang45.pl?REGID=" + regionID + "&ERROR=DOWN_ST"
					TOffline = getTOffline(table=getWidestTable(getTableList(fetchHTML(alamatURL))))
					msgBody = getTOfflineACI(TOffline, AREAID.upper())
					if msgBody:	
						msgBody = strHeaderLine +"ATM OFF (> 1 HARI)  "+ AREAID.upper() + " - "+regionName+ timestamp+ strHeaderLine + msgBody
						print msgBody

				except:
					print "CRO tidak dikenal."

	except:

		print "ANDA belum meng-input kode UKO/ CRO."
