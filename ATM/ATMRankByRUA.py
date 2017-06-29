#!/usr/bin/python
#---------------------------------------
# ATMAll.py
# (c) Jansen A. Simanullang, 01.08.2016
# @BSD CITY: 11.08.2016 15:38
# @Medan City: 29.06.2017
#---------------------------------------
# usage: python ATMAll.py
#---------------------------------------
from BeautifulSoup import BeautifulSoup
import os, requests, time, urlparse, sys
import urllib2, pdfkit, xlwt, xlutils
from operator import itemgetter
from xlwt import *
#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
scriptDirectory = os.path.dirname(os.path.abspath(__file__)) + "/"
from loadConfig import readConfig
regionID = readConfig("Atmpro")['regionid']
regionName = readConfig("Atmpro")['regionname']
jumlahKanca=24
strHeaderLine = "\n----------------------------------------------\n"
#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#---------------------------------------
scriptDirectory = os.path.dirname(os.path.abspath(__file__)) + os.sep

def welcomeScreen():

	if os.name == "posix":
		os.system("clear")
	else:
		os.system("cls")

	#print "TABULAR ATM RELIABILITY, UTILITY & AVAILABILITY \n\n\n"


def fetchHTML(alamatURL):

	#print "fetching HTML from URL...\n", alamatURL
	strHTML = urllib2.urlopen(urllib2.Request(alamatURL, headers={ 'User-Agent': 'Mozilla/5.0' })).read()
	strHTML = strHTML.decode("windows-1252")

	strHTML = strHTML.encode('ascii', 'ignore')
	mysoup = BeautifulSoup(strHTML)
	
	#print ">> URL fetched."

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



def getNumCols(table):

	# bagaimana cara menentukan berapa jumlah kolomnya?

	soup = BeautifulSoup(str(table))

	numCols = len(soup.findAll('tbody')[0].findAll('tr')[0].findAll('td'))

	#print "number of columns is", numCols

	return numCols



def getNumRows(table):

	# bagaimana cara menentukan berapa jumlah kolomnya?

	numRows = len(table.findAll(lambda tag: tag.name == 'tr' and tag.findParent('table') == table))
	
	return numRows



def getNumRowsHead(table):

	# bagaimana cara menentukan berapa jumlah baris yang terpakai sebagai header?

	soup = BeautifulSoup(str(table))
	head = soup.findAll('thead')

	numRowsHead = 0

	for i in range (0, len(head)):

		numRowsHead += len(head[i].findAll('tr'))

	#print "there is", len(head), "header with", numRowsHead, "rows"
		
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
	
	numRows = getNumRows(table)
	numRowsHead = getNumRowsHead(table)
	numCols = getNumCols(table)
	
	return numRows, numRowsHead, numCols



def getSpecificRow(table, rowIndex):

	#print "Let's take a look at the specific rows of index", rowIndex

	soup = BeautifulSoup(str(table))
	rows = soup.findAll('tr')
	strHTMLTableRows = ""

	for i in range (rowIndex, rowIndex+1):

		strHTMLTableRows = str(rows[i])
	
	return strHTMLTableRows



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



def getSpecificRows(table, rowIndex):

	print "Let's take a look at the specific rows of index", rowIndex

	soup = BeautifulSoup(str(table))
	rows = soup.findAll('tr')
	strHTMLTableRows = ""

	for i in range (rowIndex, rowIndex+1):

		strHTMLTableRows = str(rows[i])
	
	return strHTMLTableRows



def getTableContents(table):

	numRows = getNumRows(table)
	numRowsHead = getNumRowsHead(table)

	soup = BeautifulSoup(str(table))
	rows = soup.findAll('tr')
	#print len(rows)
	strHTMLTableContents = ""
	TReliability = []

	# RANKING PROBLEM ATM
	#print "\n# RANKING RELIABILITY ATM\n"

	for i in range (2, numRows-1):

		trs = BeautifulSoup(str(rows[i]))
	
		tdcells = trs.findAll("td")

		kodeCabang = tdcells[1].getText()

		dText = tdcells[2].getText()

		namaCabang = cleanupNamaUker(dText.upper())
		#---------------------------------------
		textATM = tdcells[3].getText()
		if (textATM) != '':
			ATM = int(tdcells[3].getText()) 
		else:			
			ATM = 0
		#---------------------------------------
		textRelia = tdcells[4].getText()
		if (textRelia) != '':
			RELIA = float(tdcells[4].getText()) 
		else:			
			RELIA = 0
		#---------------------------------------


		#print kodeCabang, namaCabang, AVAIL

		TReliability.append((kodeCabang, namaCabang, ATM, RELIA))
		TReliability = sorted(TReliability, key=itemgetter(3, 2, 1), reverse = True)


	# RANKING UTILITY ATM
	#print "\n# RANKING UTILITY ATM\n"
	TUtility = []

	for i in range (2, numRows-1):

		trs = BeautifulSoup(str(rows[i]))
	
		tdcells = trs.findAll("td")

		kodeCabang = tdcells[1].getText()

		dText = tdcells[2].getText()

		namaCabang = cleanupNamaUker(dText.upper())
		#---------------------------------------
		textUP = tdcells[12].getText()
		if (textUP) != '':
			UP = int(tdcells[12].getText()) 
		else:			
			UP = 0
		#---------------------------------------
		textTunai = tdcells[13].getText()
		if (textTunai) != '':
			TUNAI = int(tdcells[13].getText()) 
		else:			
			TUNAI = 0
		#---------------------------------------
		textNonTunai = tdcells[14].getText()
		if (textNonTunai) != '':
			NONTUNAI = int(tdcells[14].getText()) 
		else:			
			NONTUNAI = 0
		#---------------------------------------
		textUtil = tdcells[5].getText()
		if (textUtil) != '':
			UTILITY = float(tdcells[5].getText()) 
		else:			
			UTILITY = 0
		#---------------------------------------
		#print "{0:.0f}".format(PERCENT), NONTUNAI, ATM 

		TUtility.append((kodeCabang, namaCabang, UP, TUNAI, NONTUNAI, UTILITY))
		TUtility = sorted(TUtility, key=itemgetter(5, 1), reverse = True)


	# RANKING AVAILABILITY ATM
	#print "\n# RANKING AVAILABILITY ATM\n"
	TAvailability = []

	for i in range (2, numRows-1):

		trs = BeautifulSoup(str(rows[i]))
	
		tdcells = trs.findAll("td")

		kodeCabang = tdcells[1].getText()

		dText = tdcells[2].getText()

		namaCabang = cleanupNamaUker(dText.upper())
		#---------------------------------------
		textATM = tdcells[3].getText()
		if (textATM) != '':
			ATM = int(tdcells[3].getText()) 
		else:			
			ATM = 0
		#---------------------------------------
		textAvail = tdcells[6].getText()
		if (textAvail) != '':
			AVAIL = float(tdcells[6].getText()) 
		else:			
			AVAIL = 0
		#---------------------------------------


		#print kodeCabang, namaCabang, AVAIL

		TAvailability.append((kodeCabang, namaCabang, ATM, AVAIL))
		TAvailability = sorted(TAvailability, key=itemgetter(3, 2, 1), reverse = True)

		#print TAvailability

	return TReliability, TUtility, TAvailability



def getColIndex(table, strSearchKey1, strSearchKey2):

	# fungsi ini untuk mendapatkan nomor indeks kolom yang mengandung satu kata kunci

	numCols = getNumCols(table)
	numRowsHead = getNumRowsHead(table)

	soup = BeautifulSoup(str(table))
	rows = soup.findAll('tr')

	colIndex1 = -1

	for i in range (0, 1):

		trs = BeautifulSoup(str(rows[i]))
		thcells = trs.findAll("th")
			
		for i in range (0, len(thcells)):

			if ("colspan" in str(thcells[i]) and thcells[i].findAll('a')[0].getText().upper() == strSearchKey1.upper()):

				intColSpan = int(thcells[i]['colspan'])

				#print i, intColSpan

				colIndex1 = (i-1) * intColSpan + 1

				
			elif ("rowspan" in str(thcells[i]) and thcells[i].getText().upper() == strSearchKey1.upper()):

				intColSpan = 1

				colIndex1 = (i-1) * intColSpan + 1 

				#print i, "rowspan"
	#colIndex2 = 0
	for i in range (1, 2):
					
		soup = BeautifulSoup(str(rows[i]))
		thcells2 = soup.findAll("th")

		# the length must be limited to the colindex of the above search
		maxIndex = len(thcells2)
		maxIndex = colIndex1 - 1

		for i in range (0, maxIndex):
		
			if thcells2[i].getText().upper() == strSearchKey2.upper():
				colIndex2 = i+3 # the factor +3 is due to the two columns with the rowspan before
				


				
	#print "we got the col index = (", colIndex1, ") from ", numCols-1, "index for search key ='"+strSearchKey1+"'"
	#print "we got the col index = (", colIndex2, ") from ", numCols-1, "index for search key ='"+strSearchKey2+"'"
	return colIndex2



def cleanupNamaUker(namaUker):


	namaUker = namaUker.replace("JAKARTA ","")
	namaUker = namaUker.replace("Jakarta ","")
	namaUker = namaUker.replace("JKT ","")
	namaUker = namaUker.replace("KANCA ","")
	namaUker = namaUker.replace("KC ","")

	return namaUker.strip()




def getRowInterest(table, keyword):

	strHTMLTableRows = getSpecificRow(table, getRowIndex(table, keyword))
	
	mysoup = BeautifulSoup(strHTMLTableRows)

	arrTDs = mysoup.findAll('td')

	return arrTDs[1].getText()


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
	print "\n\n\n\n",UTILITY, type(UTILITY), strColor

	return strColor


def prepareDirectory(strOutputDir):
	# siapkan struktur direktori untuk penyimpanan data
	# struktur direktori adalah ['OUTPUT', 'EDC', '2015', '04-APR', 'DAY-28'] makes './OUTPUT/EDC/2015/04-APR/DAY-28'

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


def putDataXL(offRow, offCol, TReliability, TUtility, TAvailability):

	book = xlwt.Workbook()

	# add new colour to palette and set RGB colour value
	xlwt.add_palette_colour("sky_blue_10", 0x21)
	book.set_colour_RGB(0x21, 153,204,255)
	xlwt.add_palette_colour("blue_classic", 0x22)
	book.set_colour_RGB(0x22, 207,231,245)
	xlwt.add_palette_colour("hijau_tua", 0x23)
	book.set_colour_RGB(0x23, 0,204,0)
	xlwt.add_palette_colour("hijau_muda", 0x24)
	book.set_colour_RGB(0x24, 153,255,153)
	xlwt.add_palette_colour("kuning", 0x25)
	book.set_colour_RGB(0x25, 255,255,0)
	xlwt.add_palette_colour("merah", 0x26)
	book.set_colour_RGB(0x26, 255,51,51)


	sheet1 = book.add_sheet('PERINGKAT ATM', cell_overwrite_ok = True)
	sheet1.row(0).height_mismatch = True
	sheet1.row(0).height = 360
	styleTitle = 'pattern: pattern solid, fore_colour white;'
	styleTitle += 'align: vertical center, horizontal center, wrap on;'
	styleTitle += 'font: name Tahoma, height 280, bold 1;'

	lastCol = 15
	sheet1.write_merge(offRow, offRow, offCol, lastCol, 'ATM PRO ' + regionName , xlwt.easyxf(styleTitle))
	shiftDown = 1

	sheet1.row(1).height_mismatch = True
	sheet1.row(1).height = 360
	sheet1.write_merge(offRow+shiftDown, offRow+shiftDown, offCol, lastCol, 'posisi tanggal ' +time.strftime("%d/%m/%Y-%H:%M") , xlwt.easyxf(styleTitle))
	contentAlignmentHorz = ["center", "right", "center", "center", "center", "center", "center", "center", "center" , "center"]


	def styler(strColor,  fontHeight):

		styleHeader = 'pattern: pattern solid, fore_colour '+strColor+';'
		styleHeader += 'align: vertical center, horizontal center, wrap on;'
		styleHeader += 'borders: top thin, bottom thin;'
		styleHeader += 'font: name Tahoma, height '+str(fontHeight)+', bold 1;'
				
		return styleHeader


	def makeHeader(xRow, yCol, jenisTabel):

		arrJudul = ["CODE", "BRANCH", "ATM", "%"]

		sheet1.write_merge(xRow+2*shiftDown, xRow+2*shiftDown, yCol, yCol+len(arrJudul)-1, 'RANKING ' + jenisTabel, xlwt.easyxf(styler('sky_blue_10', 240)))

		for i in range (0, len(arrJudul)):

			sheet1.write(xRow+3*shiftDown , i+yCol, arrJudul[i], xlwt.easyxf(styler('blue_classic', 180)))


	# TABULASI RANKING RELIABILITY  ----------------------------------------------------
	makeHeader(offRow, offCol, 'BY RELIABILITY')
	sheet1.col(offCol+0).width = 5*315
	sheet1.col(offCol+1).width = 22*315
	sheet1.col(offCol+2).width = 6*315
	sheet1.col(offCol+3).width = 8*315


	for i in range (0, len(TReliability)):
		#print len(TReliability[i])
		for j in range(0,len(TReliability[i])):

			strColor = colorRelia(TReliability[i][3])
			contentStyle = 'font: name Tahoma, height 180;'
			contentStyle += 'pattern: pattern solid, fore_colour '+strColor+';'
			contentStyle += 'align: horiz '+contentAlignmentHorz[j]
			style = xlwt.easyxf(contentStyle)

			cellContent = TReliability[i][j]
			if cellContent	== 0:
				cellContent = '-'

			sheet1.write(i+offRow+4*shiftDown, j+offCol, cellContent, style)

	# UTILITY ----------------------------------------------------

	shiftLeft = (4) + 1

	def makeHeader2(xRow, yCol, jenisTabel):

		sheet1.write_merge(xRow+2*shiftDown, xRow+2*shiftDown, yCol, yCol+5, 'RANKING ' + jenisTabel, xlwt.easyxf(styler('sky_blue_10', 240)))
	
		arrJudul = ["CODE", "BRANCH", "UP", "TUNAI", "NON", "%"]

		for i in range (0, len(arrJudul)):

			sheet1.write(xRow+3*shiftDown , i+yCol, arrJudul[i], xlwt.easyxf(styler('blue_classic', 180)))



	makeHeader2(offRow, offCol+shiftLeft, "BY UTILITY")
	sheet1.col(offCol+shiftLeft-1).width = 2*315
	sheet1.col(offCol+shiftLeft+0).width = 5*315
	sheet1.col(offCol+shiftLeft+1).width = 22*315
	sheet1.col(offCol+shiftLeft+2).width = 6*315
	sheet1.col(offCol+shiftLeft+3).width = 6*315
	sheet1.col(offCol+shiftLeft+4).width = 6*315
	sheet1.col(offCol+shiftLeft+5).width = 7*315



	for k in range (0, len(TUtility)):

		for l in range(0,len(TUtility[k])):

			strColor = colorUtility(TUtility[k][5])
			contentStyle = 'font: name Tahoma, height 180;'
			contentStyle += 'pattern: pattern solid, fore_colour '+strColor+';'
			contentStyle += 'align: horiz '+contentAlignmentHorz[l]

			cellContent = TUtility[k][l]
			if cellContent	== 0:
				cellContent = '-'

			style = xlwt.easyxf(contentStyle)
			sheet1.write(k+offRow+4*shiftDown, l+offCol+shiftLeft, cellContent, style)

	# AVAILABILITY ----------------------------------------------------

	shiftLeft = (4) + 1 + (6) + 1

	def makeHeader3(xRow, yCol, jenisTabel):

		sheet1.write_merge(xRow+2*shiftDown, xRow+2*shiftDown, yCol, yCol+3, 'RANKING ' + jenisTabel, xlwt.easyxf(styler('sky_blue_10', 240)))
	
		arrJudul = ["CODE", "BRANCH", "ATM", "%"]

		for i in range (0, len(arrJudul)):

			sheet1.write(xRow+3*shiftDown , i+yCol, arrJudul[i], xlwt.easyxf(styler('blue_classic', 180)))



	makeHeader3(offRow, offCol+shiftLeft, "BY AVAILABILITY")
	#print TAvailability
	sheet1.col(offCol+shiftLeft-1).width = 2*315
	sheet1.col(offCol+shiftLeft+0).width = 5*315
	sheet1.col(offCol+shiftLeft+1).width = 22*315
	sheet1.col(offCol+shiftLeft+2).width = 6*315
	sheet1.col(offCol+shiftLeft+3).width = 9*315

	for m in range (0, len(TAvailability)):

		for n in range(0,len(TAvailability[m])):

			strColor = colorAvail(TAvailability[m][3])
			contentStyle = 'font: name Tahoma, height 180;'
			contentStyle += 'pattern: pattern solid, fore_colour '+strColor+';'
			contentStyle += 'align: horiz '+contentAlignmentHorz[n]

			style = xlwt.easyxf(contentStyle)
			sheet1.write(m+offRow+4*shiftDown, n+offCol+shiftLeft, TAvailability[m][n], style)


	style = xlwt.easyxf(styler('sky_blue_10', 240))
	#TOTAL 1
	sheet1.write(jumlahKanca+4, 0, '', style)	
	sheet1.write(jumlahKanca+4, 1, 'RELIABILITY', style)
	sheet1.write(jumlahKanca+4, 2, Formula("SUM(C5:C"+str(jumlahKanca+4)+")"), style)	
	sheet1.write(jumlahKanca+4, 3, Formula("SUM(D5:D"+str(jumlahKanca+4)+")"), style)	
	#TOTAL 2
	sheet1.write(jumlahKanca+4, 5, '', style)	
	sheet1.write(jumlahKanca+4, 6, 'UTILITY', style)	
	sheet1.write(jumlahKanca+4, 7, Formula("SUM(H5:H"+str(jumlahKanca+4)+")"), style)	
	sheet1.write(jumlahKanca+4, 8, Formula("SUM(I5:I"+str(jumlahKanca+4)+")"), style)	
	sheet1.write(jumlahKanca+4, 9, Formula("SUM(J5:J"+str(jumlahKanca+4)+")"), style)	
	sheet1.write(jumlahKanca+4, 10, Formula("I"+str(jumlahKanca+5)+"/H"+str(jumlahKanca+5)+"*100"), style)	
	#TOTAL 2
	sheet1.write(jumlahKanca+4, 12, '', style)
	sheet1.write(jumlahKanca+4, 13, 'AVAILABILITY', style)	
	sheet1.write(jumlahKanca+4, 14, Formula("SUM(O5:O"+str(jumlahKanca+4)+")"), style)	

	lastRow = jumlahKanca+5

	for i in range(5, lastRow):

		strFormula = "PRODUCT(C" + str(i)+ ":D"+str(i)+")"
		sheet1.write(i-1, 4, Formula(strFormula), xlwt.easyxf('font: color white;'))

		strFormula = "PRODUCT(O" + str(i)+ ":P"+str(i)+")"
		sheet1.write(i-1, 16, Formula(strFormula), xlwt.easyxf('font: color white;'))

	style = xlwt.easyxf(styler('sky_blue_10', 240), num_format_str= '0.00')
	sheet1.write(jumlahKanca+4, 3, Formula("SUM(E5:E"+str(jumlahKanca+4)+")/C"+str(jumlahKanca+5)+""), style )
	sheet1.write(jumlahKanca+4, 15, Formula("SUM(Q5:Q"+str(jumlahKanca+4)+")/O"+str(jumlahKanca+5)+""), style )



	sheet1.write_merge(lastRow, lastRow, offCol, offCol+15, 'TARGET UTILITY & AVAILABILITY = 99%' , xlwt.easyxf(styleTitle + 'borders: top thin, bottom thin;'))

	namaFileXLS = prepareDirectory("OUTPUT") + "ATM ALL-" + regionName +time.strftime("-%Y%m%d-%H")+'.xls'

	book.save(namaFileXLS)
	os.system('libreoffice '+namaFileXLS.replace(" ","\ "))


	
def main():


	alamatURL = 'http://atmpro.bri.co.id/statusatm/dashboard_cabang.pl?REGID='+regionID+'&REGNAME='+regionName
	strHTML = fetchHTML(alamatURL)
	table = getLargestTable(getTableList(strHTML))
	TReliability, TUtility, TAvailability = getTableContents(table)
	putDataXL(0, 0, TReliability, TUtility, TAvailability)

main()
