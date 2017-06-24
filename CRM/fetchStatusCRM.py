#!/usr/bin/python
#---------------------------------------
# fetchStatusCDM.py
# (c) Jansen A. Simanullang, 15.08.2015
# to be used with telegram-bot plugin
# 24.06.2017
#---------------------------------------
# usage: fetchStatusCDM [tid]
# script name followed by space and TID
# example: fetchStatusCDM 2008
#---------------------------------------

from BeautifulSoup import BeautifulSoup
import sys

#tid="2008"

def getCDMStatusPage(strTID):

	from pyvirtualdisplay import Display
	from selenium import webdriver

	display = Display(visible=0, size=(800, 600))
	display.start()

	# now Firefox will run in a virtual display. 
	# you will not see the browser.
	browser = webdriver.Firefox()

	alamatURL = 'http://172.18.65.42/monitorcdm/'

	browser.get(alamatURL)

	browser.title

	browser.find_elements_by_css_selector("input[type='radio'][value='GUEST']")[0].click()
	browser.find_element_by_class_name('tbutton').click()
	browser.get(alamatURL)

	browser.get('http://172.18.65.42/monitorcdm/?_module_=search_tid')
	form_textfield = browser.find_element_by_name('_termid_')
	form_textfield.send_keys(strTID)

	browser.find_element_by_class_name('tbutton').click()


	strHTML = browser.page_source
	#print strHTML
	browser.quit()
	display.stop()

	return strHTML

strHTML = getCDMStatusPage("2008")

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

	if table:
		print ">> the widest from table list is chosen."

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

def asterisk(strText):

	strText = strText.replace("OK","*OK*")
	strText = strText.replace("FAIL","*FAIL*")
	strText = strText.replace("OUT","*OUT*")
	strText = strText.replace("LOW","*LOW*")

	return strText

def getCDMStats(table):

	soup = BeautifulSoup(str(table))
	
	rows = soup.findAll('tr')

	numRows = getRowsNumber(table)

	numRowsHead = getRowsHeadNumber(table)

	#print numRowsHead, numRows

	msgBody = ""
	
	for i in range (0, numRows):

		trs = BeautifulSoup(str(rows[i]))

		tdcells = trs.findAll("td")
		thcells = trs.findAll("th")

		#print len(tdcells), len(thcells)

		if thcells:

			msgBody += "\n*" + thcells[0].getText().upper() + "*\n----------------------------------\n"

		if tdcells:

			if len(tdcells) > 1:

				msgBody += tdcells[0].getText().upper()+": "+ asterisk(tdcells[1].getText()) +"\n"


	return msgBody.replace("_"," ")


if len(sys.argv) > 0:

	strTID = sys.argv[1]

	arrTable = getTableList(getCDMStatusPage(strTID))


	# GENERAL INFO
	msgBody = getCDMStats(table=arrTable[-3])

	print msgBody

	# PARAMETER & TRX INFO
	msgBody = getCDMStats(table=arrTable[-2])

	print msgBody

	# HW INFO
	
	msgBody = getCDMStats(table=arrTable[-1])

	print msgBody
