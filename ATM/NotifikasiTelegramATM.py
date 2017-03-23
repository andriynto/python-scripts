# -*- coding: utf-8 -*-
#!/usr/bin/python
#---------------------------------------
# NotifikasiTelegramATM.py
# (c) Jansen A. Simanullang
# 06.10.2015 - 08.03.2017 14:04
# to be used with cron and MariaDB
#---------------------------------------
# Python usage:
# NotifikasiTelegramATM
#---------------------------------------


from urllib import urlopen
from BeautifulSoup import BeautifulSoup
import os, sys, time, urlparse, smtplib
import urllib, urllib2, pymysql
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage


################################################################################################
firstURL='http://172.18.65.42/statusatm/dashboard_3.pl?ERROR=CLOSE_ST'
RegionName = "JAKARTA III"
################################################################################################

scriptDirectory = os.path.dirname(os.path.abspath(__file__)) + "/"

asciiArt="""
	   ▄▄▄▄▄▄▄▄▄
        ▄█████████████▄ 
█████  █████████████████  █████
▐████▌ ▀███▄       ▄███▀ ▐████▌
 █████▄  ▀███▄   ▄███▀  ▄█████
 ▐██▀███▄  ▀███▄███▀  ▄███▀██▌    
  ███▄▀███▄  ▀███▀  ▄███▀▄███ 
  ▐█▄▀█▄▀███ ▄─▀─▄ ███▀▄█▀▄█▌
   ███▄▀█▄██ ██▄██ ██▄█▀▄███
    ▀███▄▀██ █████ ██▀▄███▀
   █▄ ▀█████ █████ █████▀ ▄█
   ███        ███	 ███
   ███▄    ▄█ ███ █▄	▄███
   █████ ▄███ ███ ███▄ █████
   █████ ████ ███ ████ █████
   █████ ████ ███ ████ █████
   █████ ████ ███ ████ █████
   █████ ████▄▄▄▄▄████ █████
    ▀███ █████████████ ███▀
      ▀█ ███ ▄▄▄▄▄ ███ █▀
         ▀█▌▐█████▌▐█▀
            ███████
"""

asciiArt="""
	   ▄▄▄▄▄▄▄▄▄
        ▄█████████████▄ 
█████  █████████████████  █████
▐████▌ ▀███▄       ▄███▀ ▐████▌
 █████▄  ▀███▄   ▄███▀  ▄█████    NOTIFIKASI ATM via TELEGRAM
"""

asciiArt = asciiArt +" ▐██▀███▄  ▀███▄███▀  ▄███▀██▌    "+RegionName
asciiArt = asciiArt +"""
  ███▄▀███▄  ▀███▀  ▄███▀▄███     
  ▐█▄▀█▄▀███ ▄▀ ▀▄ ███▀▄█▀▄█▌     (c) JANSEN SIMANULLANG
   ███▄▀█▄██ ██ ██ ██▄█▀▄███      MEI 2015 - JANUARI 2017
    ▀███▄▀██ ██ ██ ██▀▄███▀
   █▄ ▀█████ █████ █████▀ ▄█        \__/  \__/  \__/  \__/  \__/  \__/
   ███        ███	 ███      __/  \__/  \__/  \__/  \__/  \__/  \_
   ███▄    ▄█ ███ █▄	▄███        \__/  \__/  \__/  \__/  \__/  \__/ 
   █████ ▄███ ███ ███▄ █████     \__/  \__/  \__/  \__/  \__/  \__/  \_
   █████ ████ ███ ████ █████        \__/  \__/  \__/  \__/  \__/  \__/ 
   █████ ████ ███ ████ █████     \__/  \__/  \__/  \__/  \__/  \__/  \_ 
   █████ ████ ███ ████ █████        \__/  \__/  \__/  \__/  \__/  \__/ 
   █████ ████▄▄▄▄▄████ █████     \__/  \__/  \__/  \__/  \__/  \__/   
    ▀███ █████████████ ███▀    __/  \__/  \__/  \__/  \__/  \__/  \__/
      ▀█ ███ ▄▄▄▄▄ ███ █▀     /  \__/  \__/  \__/  \__/  \__/  \__/  
         ▀█▌▐█████▌▐█▀        \__/  \__/  \__/  \__/  \__/  \__/  \__/
            ███████        \__/  \__/  \__/  \__/  \__/  \__/  \__/  
"""
"""
  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \_
__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/ 
  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \_
__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/ 
  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \_
__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/ 
  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \_
__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/ 
  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \_
__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/ 
  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \_
__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/ 
  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \_
__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/ 
  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \_
__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/ 
  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \_
__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/ 
  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \_
__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/ 
  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \_
__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/ 
  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \_
"""
def clearScreen():

	if os.name == 'posix':
		os.system('clear')
	else:
		os.system('cls')

def welcomeScreen():
	
	clearScreen()

	print asciiArt


def countDomainLevel(alamatURL):

	intDomainDepth = alamatURL.count('/') - 2*alamatURL.count('//')

	return intDomainDepth



def getDomainParts(alamatURL):

	parts = alamatURL.split('//')

	protocol = parts [0]

	arrDomainParts = parts[1].split('/', countDomainLevel(alamatURL))

	return protocol, arrDomainParts
	


def nLevelDomain(alamatURL, n):

	protocol, arrDomainParts = getDomainParts(alamatURL)

	urlnLevelDomain = ""

	for i in range (0, n):

		urlnLevelDomain = urlnLevelDomain + arrDomainParts[i]+"/"

	urlnLevelDomain = protocol + "//" + urlnLevelDomain

	return urlnLevelDomain



def getQueryContent(alamatURL, strQuery):
	
	parsed = urlparse.urlparse(alamatURL)
	QueryContent = str(urlparse.parse_qs(parsed.query)[strQuery][0])
	return QueryContent



def cleanUpHTML(strHTML):

	URLdomain = nLevelDomain(alamatURL, 1)
	URLdomain2 = nLevelDomain(alamatURL, 2)
	
	# fixing broken HTML
	strHTML = strHTML.replace('</tr><td>',"</tr><tr><td>")
	strHTML = strHTML.replace('</td></tr><td>','</td></tr><tr><td>')
	strHTML = strHTML.replace('<table class=fancy>','</td></tr></table><table class=fancy>')
	strHTML = strHTML.replace('</th>\n</tr>',"</th></tr><tr>")
	strHTML = strHTML.replace('</tr>\n\n<td>',"</tr><tr><td>")


	strHTML = strHTML.replace(' bgcolor>', '>')
	strHTML = strHTML.replace('<table class=fancy>','</td></tr></table><table class=fancy>')


	# translating relative to absolute reference
	strHTML = strHTML.replace('@import "/','@import "'+URLdomain)
	strHTML = strHTML.replace('href="/','href="'+URLdomain)
	strHTML = strHTML.replace("href='/","href='"+URLdomain)
	strHTML = strHTML.replace("href='./",'href="'+URLdomain)
	strHTML = strHTML.replace("href='../","href='"+URLdomain2)

	return strHTML
	


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



def getTableList(strHTML):

	#print "\ngetting Table List...\n"

	mysoup = BeautifulSoup(strHTML)

	arrTable = mysoup.findAll('table')

	#print "there are:", len(arrTable), "tables."

	return arrTable



def getStyleList(strHTML):

	#print "\ngetting Style List...\n"

	mysoup = BeautifulSoup(strHTML)

	arrStyle = mysoup.findAll('link', rel = "stylesheet" )

	strStyle = ""

	for i in range (0, len(arrStyle)):

		strStyle = strStyle + str(arrStyle[i])
	
	return strStyle



def getHeading(strHTML):

	#print "\ngetting Heading...\n"

	strHTML = cleanUpHTML(strHTML)

	mysoup = BeautifulSoup(strHTML)

	heading1 = mysoup.findAll('h1')

	if heading1 != []:

		strHeading = heading1[0].getText().upper()
		strHeading = strHeading.replace("BY REGION", RegionName)


	heading3 = mysoup.findAll('h3')

	if heading3 != []:

		strHeading = heading3[0].getText().upper()
		strHeading = strHeading.replace("REGION: "+RegionName+" - ", "")
		strHeading = strHeading.replace("FOR REGION", "")



	else:
		strHeading = 'AVAILABILITY ATM BRI ' + RegionName
	

	#
	strHeading = strHeading.replace("LIST OF", "")

	# avoid semicolon, slash and double space by deleting them
	strHeading = strHeading.replace(":", "")
	strHeading = strHeading.replace("/", " ")
	strHeading = strHeading.replace("  ", " ")

	return strHeading.strip()



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
		#print ">> the largest from table list is chosen."

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
		#print ">> the widest from table list is chosen."

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



def fileCreate(strNamaFile, strData):
	f = open(strNamaFile, "w")
	f.writelines(str(strData))
	f.close()


    
def fileAppend(strNamaFile, strData):
	f = open(strNamaFile, "a")
	f.writelines(str(strData))
	f.close()



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


def getNamaFile(strHTML):

	strHeading = getHeading(strHTML)

	protocol, arrDomainParts = getDomainParts(alamatURL) 

	namaSkrip = arrDomainParts[-1].split('?')[0].replace('.pl','')

	strNamaFile = strHeading + "-" + namaSkrip +".html"

	strNamaFile = prepareDirectory('OUTPUT') + strNamaFile

	return strNamaFile



def prepareFile(strNamaFile):

	#print "preparing HTML file as canvas...", strNamaFile, "\n"

	strHTML = fetchHTML(alamatURL)


	strData = '<HTML><HEAD><TITLE>MONITORING ATM '+ RegionName +'</TITLE><META HTTP-EQUIV="REFRESH" CONTENT="3600">' + getStyleList(strHTML) + '</HEAD><body>'

	strData = strData + "<h1>"+ getHeading(strHTML) + "</h1><h3>per tanggal " + time.strftime("%d.%m.%Y jam %H:%M:%S") + "</h3>"

   	fileCreate(strNamaFile, strData)


def prepareTextFile(strNamaFile, strData):

	#print "preparing Text file...\n"

	strNamaFile = prepareDirectory('OUTPUT') + strNamaFile

	fileCreate(strNamaFile, strData)

	return strNamaFile




def getHTMLnWritefromURLList(strNamaFile, arrURL):

	strHTML = ""

	strHTML = '<div id="content"><table class="tabel2">'

	fileAppend(strNamaFile, strHTML)
	
	strHTMLTableContents = ""

	for i in range (0, 1):

		alamatURL = arrURL[i]

		arrTable = getTableList(fetchHTML(alamatURL))

		table = getLargestTable(arrTable)

		strHTMLTableContents = strHTMLTableContents + getTableContents(table)
		
	strHTML = getTableHeader(table) + strHTMLTableContents	

	fileAppend(strNamaFile, strHTML)	

		
	for i in range (1, len(arrURL)):

		alamatURL = arrURL[i]

		arrTable = getTableList(fetchHTML(alamatURL))

		table = getLargestTable(arrTable)

		strHTMLTableContents = getTableContents(table)

		fileAppend(strNamaFile, strHTMLTableContents)

	strHTML = '</table></div>'

	fileAppend(strNamaFile, strHTML)

	###
	
	#print "\a\n>>>>FILE CREATED :\n", strNamaFile, "<<<<\a\n"

	### TODO: play a beep sound
		


def ExtractLinksToFile(alamatURL):

	strHTML = fetchHTML(alamatURL)
	
	strNamaFile = getNamaFile(strHTML) 

	prepareFile(strNamaFile)

	arrTable = getTableList(strHTML)

	table = getLargestTable(arrTable)

	arrURL = [alamatURL]

	getHTMLnWritefromURLList(strNamaFile, arrURL)



def extractURL(strHTML):

	# this function finds all non-'0" links
	# nLevelDomain(alamatURL, 3)  --> http://172.18.65.42/monitorATM/dashboardNew/

	URLdomain = nLevelDomain(alamatURL, 0) 

	mysoup = BeautifulSoup(strHTML)

	arrURL = mysoup.findAll('a')

	numZeros = 0

	indexZero = [None]

	for i in range(0, len(arrURL)):

		if arrURL[i].getText() == "0":
			
			numZeros = numZeros + 1
			indexZero.append(i)

		else:

			arrURL[i] = arrURL[i].get('href')
		
	#print "We have", len(arrURL), "URLs."

	if numZeros:

		indexZero.remove(None)

		#print "There are", numZeros, "URLs containing zero at index:", indexZero

		for i in range (0, len(indexZero)):

			# there is a shift of index after every removal of list components

			arrURL.remove(arrURL[indexZero[i]-i])


		#print "So, we have remaining", len(arrURL), "URLs to fetch."

	return arrURL



def prepareDirectory(strOutputDir):
	# siapkan struktur direktori untuk penyimpanan data
	# struktur direktori adalah ['OUTPUT', 'ATM', '2015', '04-APR', 'DAY-28'] makes './OUTPUT/ATM/2015/04-APR/DAY-28'

	arrDirectoryStructure = [strOutputDir, 'ATM', time.strftime("%Y"), time.strftime("%m-%b").upper() , "DAY-"+time.strftime("%d")]

	fullPath = scriptDirectory

	for i in range (0, len(arrDirectoryStructure)):
	
		fullPath = fullPath + arrDirectoryStructure[i] + "/"

		if not os.path.exists(fullPath):

			#print "creating directories:", arrDirectoryStructure[i]
			os.mkdir(fullPath)
			os.chdir(fullPath)

	#print fullPath

	return fullPath

def readBranchCode():

	arrBranchCode = []
	arrBranchName = []

	fName = scriptDirectory +"conf/branchCode.888"
		
	f = open(fName)

	for baris in f.readlines():

		col = baris.strip().split("|")
		arrBranchCode.append(col[0])
		arrBranchName.append(col[1])


	f.close()

	return arrBranchCode, arrBranchName

def getBranchCode(alamatURL):

	strHTML = fetchHTML(alamatURL)

	table = getWidestTable(getTableList(strHTML))

	soup = BeautifulSoup(str(table))
	
	rows = soup.findAll('tr')

	numRows = getRowsNumber(table)

	numRowsHead = getRowsHeadNumber(table)

	if numRows == numRowsHead:

		#print "waiting the page to show data"
		#time.sleep(60)
		arrBranchCode, arrBranchName = readBranchCode()

		

	arrBranchCode = [None]*numRows
	arrBranchName = [None]*numRows

	for i in range (numRowsHead, numRows):

		trs = BeautifulSoup(str(rows[i]))
		tdcells = trs.findAll("td")

		try:

			if tdcells[1].getText().isdigit():

				arrBranchCode[i] = tdcells[1].getText()
				arrBranchName[i] = tdcells[2].getText().upper()
				#createfile

		except:
			print "tidak ada data"

	try:	
	# remove unnecessary items containing None in the 1st, 2nd and the last
		arrBranchCode.remove(arrBranchCode[0])
		arrBranchCode.remove(arrBranchCode[0])
		arrBranchCode.remove(arrBranchCode[-1])

		arrBranchName.remove(arrBranchName[0])
		arrBranchName.remove(arrBranchName[0])
		arrBranchName.remove(arrBranchName[-1])

	except IndexError:
		pass
		

	return arrBranchCode, arrBranchName

def getBranchURL(arrBranchCode):

	arrBranchURL=[None] * len(arrBranchCode)

	for i in range(0, len(arrBranchCode)):
		
		arrBranchURL[i] = "http://172.18.65.42/statusatm/viewbybranch6.pl?AREA_ID="+arrBranchCode[i]

		#print arrBranchURL[i]
	
	return arrBranchURL

def getBranchPage(alamatURL):
	
	try:
		strHTML = fetchHTML(alamatURL)

		table = getWidestTable(getTableList(strHTML))
	except:
		table = getBranchPage(alamatURL)

	return table

#-------------------------------------------------------

def durasiHinggaKini(strDate):

	from datetime import datetime
	format1 = '%d/%m/%Y %H:%M'
	span = datetime.now() - datetime.strptime(strDate.replace('_',' '), format1)
	return ':'.join(str(span).split('.')[:1])

def getColIndex(table, strSearchKey1, strSearchKey2):

	# fungsi ini untuk mendapatkan nomor indeks kolom yang mengandung satu kata kunci

	numCols = getColsNumber(table)
	numRowsHead = getRowsHeadNumber(table)

	soup = BeautifulSoup(str(table))
	rows = soup.findAll('tr')

	colIndex1 = -1

	for i in range (0, 1):

		trs = BeautifulSoup(str(rows[i]))
		thcells = trs.findAll("th")
			
		for i in range (0, len(thcells)):

			if ("colspan" in str(thcells[i]) and thcells[i].findAll('a')[0].getText().upper() == strSearchKey1.upper()):

				intColSpan = int(thcells[i]['colspan'])

				print i, intColSpan

				colIndex1 = (i-1) * intColSpan + 1

				
			elif ("rowspan" in str(thcells[i]) and thcells[i].getText().upper() == strSearchKey1.upper()):

				intColSpan = 1

				colIndex1 = (i-1) * intColSpan + 1 

				print i, "rowspan"
	#colIndex2 = 0
	for i in range (1, 2):
					
		soup = BeautifulSoup(str(rows[i]))
		thcells2 = soup.findAll("th")

		# the length must be limited to the colindex of the above search
		maxIndex = len(thcells2)
		maxIndex = colIndex1 - 1

		for i in range (0, maxIndex):
		
			if thcells2[i].getText().upper() == strSearchKey2.upper():
				colIndex2 = i+2 # the factor +2 is due to the two columns with the rowspan before
				


				
	print "we got the col index = (", colIndex1, ") from ", numCols-1, "index for search key ='"+strSearchKey1+"'"
	print "we got the col index = (", colIndex2, ") from ", numCols-1, "index for search key ='"+strSearchKey2+"'"
	return colIndex2

#-------------------------------------------------------
def getATMProbStats(table):

	#print "getting List of ATMs requires attention..."
	
	soup = BeautifulSoup(str(table))
	
	rows = soup.findAll('tr')

	numRows = getRowsNumber(table)

	numRowsHead = getRowsHeadNumber(table)

	msgBody = ""

	numCOUKO = 0
	numCOCRO = 0
	numCLUKO = 0
	numCLCRO = 0
	numDFUKO = 0
	numDFCRO = 0
	numOOSUKO = 0
	numOOSCRO = 0
	numCOMUKO = 0
	numCOMCRO = 0
	numCCRUKO = 0
	numCCRCRO = 0

	arrCOUKO = []
	arrCOCRO = []
	arrCLUKO = []
	arrCLCRO = []
	arrDFUKO = []
	arrDFCRO = []
	arrOOSUKO = []
	arrOOSCRO = []
	arrCOMUKO = []
	arrCOMCRO = []
	arrCCRUKO = []
	arrCCRCRO = []


	for i in range (numRowsHead, numRows):

		trs = BeautifulSoup(str(rows[i]))
		tdcells = trs.findAll("td")

#----------- COM

		if tdcells[7].getText() == "OFFLINE":

			tid = tdcells[1].getText()
			last = tdcells[12].getText()
			if last:
				durasi = durasiHinggaKini(last)
			else:
				durasi = ''
			tidlocation = cleanupLocation(tdcells[5].getText())

			strPengelola, strSupervisi = getPengelolaSupervisi(tid)

			if ("ATM CENTER" in strPengelola or "VENDOR" in strPengelola):

				numCOMCRO = numCOMCRO + 1

				arrCOMCRO.append(str(numCOMCRO) + ") " + tid + "\t" + tidlocation + ", " + cleanupLocation(strPengelola)+ ", " + durasi)
			else:
				numCOMUKO = numCOMUKO + 1
				
				arrCOMUKO.append(str(numCOMUKO) + ") " + tid + "\t" + tidlocation + ", " + cleanupLocation(strPengelola)+ ", " + durasi)


#----------- CO

		if tdcells[8].getText() == "CASH OUT":

			tid = tdcells[1].getText()
			last = tdcells[12].getText()
			if last:
				durasi = durasiHinggaKini(last)
			else:
				durasi = ''
			tidlocation = cleanupLocation(tdcells[5].getText())

			strPengelola, strSupervisi = getPengelolaSupervisi(tid)

			if ("ATM CENTER" in strPengelola or "VENDOR" in strPengelola):

				numCOCRO = numCOCRO + 1

				arrCOCRO.append(str(numCOCRO) + ") " + tid + "\t" + tidlocation + ", " + cleanupLocation(strPengelola)+ ", " + durasi)
			else:
				numCOUKO = numCOUKO + 1
				
				arrCOUKO.append(str(numCOUKO) + ") " + tid + "\t" + tidlocation + ", " + cleanupLocation(strPengelola)+ ", " + durasi)
	
#----------- CL
		if tdcells[9].getText() == "LOW":

			tid = tdcells[1].getText()
			last = tdcells[12].getText()
			if last:
				durasi = durasiHinggaKini(last)
			else:
				durasi = ''
			tidlocation = cleanupLocation(tdcells[5].getText())

			strPengelola, strSupervisi = getPengelolaSupervisi(tid)

			if ("ATM CENTER" in strPengelola or "VENDOR" in strPengelola):

				numCLCRO = numCLCRO + 1

				arrCLCRO.append(str(numCLCRO) + ") " + tid + "\t" + tidlocation + ", " + cleanupLocation(strPengelola)+ ", " + durasi)
			else:
				numCLUKO = numCLUKO + 1
				
				arrCLUKO.append(str(numCLUKO) + ") " + tid + "\t" + tidlocation + ", " + cleanupLocation(strPengelola)+ ", " + durasi)
	

#----------- CCR

		if tdcells[10].getText() == "CARD READER":

			tid = tdcells[1].getText()
			last = tdcells[12].getText()
			if last:
				durasi = durasiHinggaKini(last)
			else:
				durasi = ''
			tidlocation = cleanupLocation(tdcells[5].getText())

			strPengelola, strSupervisi = getPengelolaSupervisi(tid)

			if ("ATM CENTER" in strPengelola or "VENDOR" in strPengelola):

				numCCRCRO = numCCRCRO + 1

				arrCCRCRO.append(str(numCCRCRO) + ") " + tid + "\t" + tidlocation + ", " + cleanupLocation(strPengelola)+ ", " + durasi)
			else:
				numCCRUKO = numCCRUKO + 1
				
				arrCCRUKO.append(str(numCCRUKO) + ") " + tid + "\t" + tidlocation + ", " + cleanupLocation(strPengelola)+ ", " + durasi)

#----------- DISP STATUS/ DF
		if tdcells[11].getText() == "FAIL":

			tid = tdcells[1].getText()
			last = tdcells[12].getText()
			if last:
				durasi = durasiHinggaKini(last)
			else:
				durasi = ''
			tidlocation = cleanupLocation(tdcells[5].getText())

			strPengelola, strSupervisi = getPengelolaSupervisi(tid)

			if ("ATM CENTER" in strPengelola or "VENDOR" in strPengelola):

				numDFCRO = numDFCRO + 1

				arrDFCRO.append(str(numDFCRO) + ") " + tid + "\t" + tidlocation + ", " + cleanupLocation(strPengelola)+ ", " + durasi)
			else:
				numDFUKO = numDFUKO + 1
				
				arrDFUKO.append(str(numDFUKO) + ") " + tid + "\t" + tidlocation + ", " + cleanupLocation(strPengelola)+ ", " + durasi)
	



#-----------
	#arrOOSUKO.remove(arrOOSUKO[0])
	#arrOOSCRO.remove(arrOOSCRO[0])
	#arrCOUKO.remove(arrCOUKO[0])
	#arrCOCRO.remove(arrCOCRO[0])
	#arrCLUKO.remove(arrCLUKO[0])
	#arrCLCRO.remove(arrCLCRO[0])
	#arrDFUKO.remove(arrDFUKO[0])
	#arrDFCRO.remove(arrDFCRO[0])

	if ((numOOSUKO > 0) or (numCOUKO > 0) or (numCLUKO > 0) or (numDFUKO > 0) or (numCOMUKO > 0) or (numCCRUKO > 0)):
		
		msgBody = msgBody + "\n*[PROBLEM ATM UKO]*\n"

	if numCOUKO:

		msgBody = msgBody + "\n*CASH OUT*: "+str(numCOUKO) + "\n" + "\n".join(arrCOUKO) + "\n"

	if numCLUKO:

		msgBody = msgBody + "\n*CASH LOW*: "+str(numCLUKO) + "\n" + "\n".join(arrCLUKO) + "\n"

	if numDFUKO:

		msgBody = msgBody + "\n*DISPENSER FAILURE*: "+str(numDFUKO) + "\n" + "\n".join(arrDFUKO) + "\n"

	if numOOSUKO:

		msgBody = msgBody + "\n*OOS*: "+str(numOOSUKO) + "\n" + "\n".join(arrOOSUKO) + "\n"

	if numCOMUKO:

		msgBody = msgBody + "\n*COM*: "+str(numCOMUKO) + "\n" + "\n".join(arrCOMUKO) + "\n"

	if numCCRUKO:

		msgBody = msgBody + "\n*CCR*: "+str(numCCRUKO) + "\n" + "\n".join(arrCCRUKO) + "\n"


	if (numOOSCRO !=0 or numCOCRO !=0 or numCLCRO !=0 or numDFCRO !=0 or numCOMCRO !=0 or numCCRCRO !=0):
		
		msgBody = msgBody + "\n*[PROBLEM ATM CRO]*\n"

	if numCOCRO:

		msgBody = msgBody + "\n*CASH OUT*: "+str(numCOCRO) + "\n" + "\n".join(arrCOCRO) + "\n"

	if numCLCRO:

		msgBody = msgBody + "\n*CASH LOW*: "+str(numCLCRO) + "\n" + "\n".join(arrCLCRO) + "\n"

	if numDFCRO:

		msgBody = msgBody + "\n*DISPENSER FAILURE*: "+str(numDFCRO) + "\n" + "\n".join(arrDFCRO) + "\n"

	if numOOSCRO:

		msgBody = msgBody + "\n*OOS*: "+str(numOOSCRO) + "\n" + "\n".join(arrOOSCRO) + "\n"

	if numCOMCRO:

		msgBody = msgBody + "\n*COM*: "+str(numCOMCRO) + "\n" + "\n".join(arrCOMCRO) + "\n"

	if numCCRCRO:

		msgBody = msgBody + "\n*CCR*: "+str(numCCRCRO) + "\n" + "\n".join(arrCCRCRO) + "\n"

	if msgBody:

		msgBody = msgBody
	else:

		msgBody = "\n*EXCELLENT WORK! EVERYTHING IS OKAY!*"

	return msgBody

def cleanupLocation(tidlocation):
	tidlocation = tidlocation.replace("("," (")
	tidlocation = tidlocation.replace(") ("," ")
	tidlocation = tidlocation.replace(" ]","]")
	tidlocation = tidlocation.replace("-"," ")
	tidlocation = tidlocation.replace("BG III (","(BG III ")
	tidlocation = tidlocation.replace("(SWADARMA SARANA (","(SSI ")
	tidlocation = tidlocation.replace("BRINGIN GIGANTARA","BG")
	tidlocation = tidlocation.replace("ATM CENTER ( ","(")
	tidlocation = tidlocation.replace("ATM CENTER","")
	tidlocation = tidlocation.replace("JAKARTA UNIT","UNIT")
	tidlocation = tidlocation.replace("JAKARTA KCP","KCP")
	tidlocation = tidlocation.replace("JAKARTA KC","KC")
	tidlocation = tidlocation.replace("JAKARTA KK","KK")
	tidlocation = tidlocation.replace("JAKARTA 1 ","")
	tidlocation = tidlocation.replace("JAKARTA 2 ","")
	tidlocation = tidlocation.replace("JAKARTA 3 ","")
	tidlocation = tidlocation.replace("JAKARTA3 ","")
	tidlocation = tidlocation.replace("KANWIL 3 ","")
	tidlocation = tidlocation.replace("JKT 1","")
	tidlocation = tidlocation.replace("JKT 2","")
	tidlocation = tidlocation.replace("JKT 3","")
	tidlocation = tidlocation.replace("JKT1 ","")	
	tidlocation = tidlocation.replace("JKT2 ","")
	tidlocation = tidlocation.replace("JKT3 ","")
	tidlocation = tidlocation.replace("JAK 3","")
	tidlocation = tidlocation.replace("JAK3 ","")
	tidlocation = tidlocation.replace("BRI ","")
	tidlocation = tidlocation.replace("( ","(")
	tidlocation = tidlocation.replace("  "," ")

	return tidlocation.strip()

def getPengelolaSupervisi(strTID):

	try:	
		strURL = "http://172.18.65.42/statusatm/viewatmdetail.pl?ATM_NUM="+strTID

		strHTML = fetchHTML(strURL)

		table = getLargestTable(getTableList(strHTML))

		strHTMLTableRows = getSpecificRows(table, getRowIndex(table, "Replenish By"))

		mysoup = BeautifulSoup(strHTMLTableRows)

		arrTDs = mysoup.findAll('td')
	
		strPengelola = arrTDs[1].getText()
		
		strHTMLTableRows = getSpecificRows(table, getRowIndex(table, "KC Supervisi"))

		mysoup = BeautifulSoup(strHTMLTableRows)

		arrTDs = mysoup.findAll('td')

		strSupervisi = arrTDs[1].getText()

	except IndexError:
	
		strPengelola, strSupervisi = getPengelolaSupervisi(strTID)

	except RuntimeError:

		strPengelola, strSupervisi = "---", "KANWIL BRI JAKARTA III"

	return strPengelola, strSupervisi



def getAvailBranch(branchCode):

	try:	
		strURL = 'http://172.18.65.42/statusatm/dashboard_cabang.pl?REGID=15&REGNAME=Jakarta%20III'

		strHTML = fetchHTML(strURL)

		table = getLargestTable(getTableList(strHTML))

		strHTMLTableRows = getSpecificRows(table, getRowIndex(table, branchCode))

		mysoup = BeautifulSoup(strHTMLTableRows)

		arrTDs = mysoup.findAll('td')

		percentAvail = arrTDs[37].getText()
		

	except IndexError:
	
		percentAvail = getAvailBranch(branchCode)

	return percentAvail


def colorPercent(percentAvail):

	strColor = str(percentAvail)

	if percentAvail >= 0.00:
		strColor = "Merah"
	if percentAvail >= 87.00:
		strColor = "Kuning"
	if percentAvail >= 93.00:
		strColor = "Hijau Muda"
	if percentAvail >= 97.00:
		strColor = "Hijau Tua"


	return strColor


def mailNotifikasiATM(toaddrs, msgSubject, msgBody):

	msg = MIMEMultipart()

	fromaddr = 'Monitoring ATM Kanwil BRI Jakarta 3 <monitoratm.jkt3@corp.bri.co.id>'

	msg["From"] = fromaddr
	msg["To"] = toaddrs
	msg["Subject"] = msgSubject


	part1 = MIMEText(msgBody, 'plain')

	msg.attach(part1)


	print msg

	try:

	    server = smtplib.SMTP("webmail1.bri.co.id:587")

	    print "connecting to mail server..."
	    server.starttls()

	    username ='monitoratm.jkt3'
	    password ='monitoratm.jkt3'

	    print "logging into mail server"
	    server.login(username,password)
	    
	    print "sending mail..."
	    server.sendmail(fromaddr, toaddrs, msg.as_string())

	    server.quit()
	    print "mail sent successfully."

	except:

	    print "ooops... something went wrong!"


def TelegramCLISender(telegramName, strNamaFile):

	telegramCommand = 'echo "send_text '+telegramName+' '+strNamaFile+'" | nc 127.0.0.1 8885'
	telegramCommand = 'proxychains telegram-cli -W -e "send_text '+telegramName+' '+strNamaFile+'"'
	print telegramCommand + "\n"
	os.system(telegramCommand)
	
	#telegramName = 'Jansen_Simanullang'
	#os.system('echo "send_text Jansen_Simanullang '+strNamaFile+'" | nc 127.0.0.1 888')
	#TelegramCLISender(telegramName, strNamaFile)



def TelegramBotSender(chat_id, strText):

	secretKey = "115651882:AAGDNzHXwLKNqOWmHWC8vMXg-Vy_fZD0350"

	encText=urllib.quote_plus(strText)

	strURL = "https://api.telegram.org/bot"+secretKey+"/sendMessage?parse_mode=Markdown&chat_id="+chat_id+"&text="+urllib.quote_plus(strText)
	# comment out this line below for testing purposes
	#print strURL
	os.system('proxychains w3m -dump "'+ strURL+'"')



def readTextFile(strNamaFile):

	fText = open(strNamaFile)

	strText = ""
					
	for baris in fText.readlines():

		strText += baris

	fText.close()

	return strText



def prepareMessage(alamatURL):

	msgBody = "no message"
	table = ""

	try:

		table = getBranchPage(alamatURL)

		msgBody = getATMProbStats(getBranchPage(alamatURL))

		#print "@@@@@@@@@@@\n"+msgBody+"@@@@@@@@@@@"

		

	except IndexError:
		
		print "site data not yet ready, sleeping for thirty seconds..."

		time.sleep(30)

		msgBody = prepareMessage(alamatURL)


	return msgBody



def NotifikasiATM():

	global alamatURL, strHTML, RegionName, table, arrBranchCode

	alamatURL = firstURL

	strHTML = fetchHTML(firstURL)

	table = getWidestTable(getTableList(strHTML))

	strHTMLTableRows = getSpecificRows(table, getRowIndex(table, RegionName))

	arrURL = extractURL(strHTMLTableRows)
	
	alamatURL = arrURL[0] 	# dapatkan dashboard wilayah yang diinginkan saja

	#print alamatURL #--> alamat URL se-Kanwil yang diinginkan
		
	arrBranchCode, arrBranchName = getBranchCode(alamatURL)

	arrBranchURL = getBranchURL(arrBranchCode)

	print "Mengirimkan notifikasi "

	for i in range(0, len(arrBranchURL)):
	
		msgSubject = "*NOTIFIKASI ATM "+arrBranchName[i] +"* ("+ arrBranchCode[i] +")\n"+time.strftime("%d.%m.%Y-%H:%M")

		percentAvail = getAvailBranch(arrBranchCode[i])

		strColor = colorPercent(percentAvail)

		availText = "------------------------------------\nAvailability = " + percentAvail +"% -- "+ strColor

		msgBody = msgSubject +"\n"+ availText +"\n"+ str(prepareMessage(arrBranchURL[i]))

		print msgBody
		

		# create text file in the output folder
		strNamaFile = ""

		strData = msgBody

		strNamaFile = prepareTextFile(arrBranchCode[i], strData)

		conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='br1j4k4rt43', db='mantel')

		cur = conn.cursor()

		cur.execute('select telegram_id from notif1 where branchcode like "'+arrBranchCode[i]+'" and active="1"')


		for row in cur:

			telegram_id =(row[0])
			#------------------------------------
			# only for verbose debugging purpose
			kur = conn.cursor()
			kur.execute('select telegram_name from mantab where telegram_id="'+telegram_id+'"')

			for baris in kur:

				telegram_name = baris[0]

			kur.close()
			#print "chat_id", chat_id
			#------------------------------------



			# sending using @jak3bot

			strText = readTextFile(strNamaFile)

			print "\n--------------------------------------------------\n"


			print arrBranchName[i]+"--->: "+ telegram_name + "            \r"
			#print readTextFile(strNamaFile)
			

			TelegramBotSender(telegram_id, strText)

		cur.close()
		conn.close()

clearScreen()
welcomeScreen()
NotifikasiATM()
