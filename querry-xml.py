import pandas as pd
import os
from lxml import etree
from tkinter import *
from tkinter import filedialog, ttk, messagebox
import urllib.parse

#get path of this file
filePath =  os.path.dirname(os.path.abspath(__file__))
fileXMLPath = ''

#element names to read
columsName = ['HovaTen' ,'NTNS', 'DIEMTB', 'XEPLOAI', 'KETQUA']

#schools name
with open(filePath+'\\Prepared_data_for_generating\\school_name.txt', 'r', encoding='utf-8') as reader:
  schoolName = reader.read().split('\n')

#use xPath to get data
def readXMLByXpath(linktoXML, columns, miniPoint, maxiPoint):
    '''
    read the information from XML file using XPath expression\n\n
    return a dataframe with data read from XML file using xPath expression\n\n
    linktoXML: the link to XML file\n
    columns: colums of the table\n
    miniPoint: minimum mark\n
    maxiPoint: maximum mark\n
    '''
    data = etree.parse(linktoXML)
    dataDict = {}
    
    #create a dictionary holds all value of each student and store respectively 
    for column in columns:
        dataDict[column] = []   

    #select all node with name Hoc_sinh
    students = data.xpath('//Hoc_sinh')

    #use xPath expression
    #for each student, read all attributes and add to the list
    for student in students:
        for column in columns:
            #select all node in each student have the column's name
            value = student.xpath(column)
            #add to the dictionary
            dataDict[column].append(value[0].text)    

    #convert numerical string to float type
    for i in range(len(dataDict['DIEMTB'])):
        dataDict['DIEMTB'][i] = float(dataDict['DIEMTB'][i])

    #convert read information to dataframe
    tempResult = pd.DataFrame(dataDict)

    #filter the point range 
    filteredResult = tempResult[(tempResult['DIEMTB'] >= miniPoint) & (tempResult['DIEMTB'] <= maxiPoint)]
    return filteredResult

def chooseFile():
    global fileXMLPath
    fileXMLPath = filedialog.askopenfilename(title= 'choose file', 
                                          filetypes=(("XML files","*.XML"),), 
                                          initialdir= filePath + '\\XML')
    #if user choose a file
    try:
        resetEntry()
    #if user do not choose any file
    except IndexError:
        return

#reset entry information when a button is clicked
def resetEntry():    
    def clearEntry(entryBox):
        entryBox.delete(0, END)
    #clear entry boxes
    clearEntry(entryDatabase)
    clearEntry(entrySchool)
    clearEntry(entryRank)
    clearEntry(entryYear)
    #split the file name to components and modify
    fileName= fileXMLPath.replace('/', '\\')
    fileName = fileName.split('\\')
    fileName= fileName[len(fileName) - 1]
    fileName= fileName.split('-')
    #write on entry boxes new file information
    entryDatabase.insert(0, fileName[0])
    entrySchool.insert(0, fileName[1].replace('_', ' '))
    entryYear.insert(0, fileName[2] + '-' + fileName[3])
    entryRank.insert(0, fileName[4][0: len(fileName[4]) - 4])

def getLatestFile():
    '''
    get the information of the latest XML file\n
    '''
    global fileXMLPath
    with open(filePath + '\\Prepared_data_for_generating\\latest_created _file.txt', 'r', encoding='utf-8') as reader:
        fileXMLPath = filePath + '\\XML\\' + reader.read()
    resetEntry()

def printResult():
    '''
    get the data from required input\n
    return a dataframe and execution time
    '''    
    try:
        miniMark = float(entryminiMark.get())
        maxiMark = float(entrymaxiMark.get())
    #raise exception if marks are not valid
    except ValueError:
        messagebox.showerror(title= 'Lỗi', message='Thông tin ngưỡng điểm không hợp lệ.', icon= 'error')
        return 
    
    resulttext = Label(mainWindow, text='Kết quả', font = ('Arial',15,'bold'), bg='#F3E5AB')
    resulttext.grid(row=8, column=0, columnspan=3)

    result = readXMLByXpath(linktoXML= fileXMLPath, columns=columsName, miniPoint= float(entryminiMark.get()), maxiPoint= float(entrymaxiMark.get()))

    #if data frame is empty, show error
    if result.empty:
        messagebox.showerror(title = 'Lỗi', message='Kết quả rỗng\n Kiểm tra lại thông tin', icon='error')
    else:
        resultDisplay = ttk.Treeview(mainWindow, columns=(1,2,3,4,5), show='headings')
        columns = result.columns
        
        #modify heading in tree view
        for i in range(len(columns)):
            resultDisplay.heading(i+ 1, text= columns[i])

        #modify column size
        resultDisplay.column(1, width=250)
        resultDisplay.column(2, width=150)
        resultDisplay.column(3, width=50)
        resultDisplay.column(4, width=80)
        resultDisplay.column(5, width=70)

        #display the treeview
        resultDisplay.grid(row=9, column=0, columnspan=3)
        resultDisplay.tag_configure("myfont", font=("Arial", 12))

        # Insert data into the Treeview
        for i, row in result.iterrows():
            values = row.values.tolist()
            resultDisplay.insert("", "end", values=values, tags='myfont') 


def getFileandResult():
    '''
    Get the link to file from entry boxes and print the result
    '''
    global fileXMLPath
    #get the information and format it
    fileXMLPath = filePath + '\\XML\\'\
                + entryDatabase.get() + '-'\
                + entrySchool.get().replace(' ', '_') + '-'\
                + entryYear.get() + '-'\
                + entryRank.get() + '.xml'

    fileXMLPath = urllib.parse.unquote(fileXMLPath)

    #check if the link exist
    #if exist, print the result
    if os.path.exists(fileXMLPath):
        printResult()
    else: 
        messagebox.showerror(title= 'Lỗi', message='Không tìm thấy file.\nNhập lại thông tin.', icon= 'error')

#create a window for user
mainWindow = Tk()
mainWindow.geometry('600x600')
mainWindow.title('Read XML')
mainWindow.config(bg='#F1E5AC')
mainWindow.resizable(False, False) 

#create lists for user can choose easily
  # create a function to handle menu item selection
def handle_menu_selection(entry, menu_item):
    entry.delete(0, END)
    entry.insert(0, menu_item)

#variable that will hold the value typed by user
DatabaseChooseVariable = StringVar(mainWindow)  
schoolChooseVariable = StringVar(mainWindow)
yearChooseVariable = StringVar(mainWindow)
rankChooseVariable = StringVar(mainWindow)

#decide whether to export XML file or not
exportXML = BooleanVar()

#create an area for user to type information
def entryArea(window, displayedText,values,y, variableList):
    '''
    create entry area for user
    '''
    #create an entry label
    entryLabel = Label(window, text = displayedText, font = ('Arial',15,'bold'), anchor='center',bg='#F1E5AC')
    entryLabel.grid(row=y, column=0)
    #create an entry box
    entryBox = Entry(window ,font = ('Arial', 20),fg= 'black')
    entryBox.grid(row= y, column=1)
    #make a selection
    selectOption = OptionMenu(window,variableList, *values, command=lambda selected_option: handle_menu_selection(entryBox, selected_option))
    selectOption.config(width=1, height=1, bg='black', activebackground= 'green', fg= 'black', activeforeground='green')
    selectOption.configure()
    selectOption.grid(row=y, column=2)

    return entryLabel, entryBox, selectOption

Label(mainWindow, text = 'ĐỌC FILE XML', font = ('Arial',15,'bold'), bg='#F1E5AC').grid(row= 0, column=0, columnspan=3)
#get the database name
databaseLabel, entryDatabase, DatabaseOption = entryArea(mainWindow, 'Database', ('TRUONGHOC1', 'TRUONGHOC2'), 1, DatabaseChooseVariable)

#get the school name
schoolLabel, entrySchool, schoolOption = entryArea(mainWindow, 'Trường', schoolName, 2, schoolChooseVariable)

#get the school year
yearLabel, entryYear, yearOption = entryArea(mainWindow, 'Năm học', [str(i) + '-' + str(i + 1) for i in range(2006, 2023, 1)], 3, yearChooseVariable)

#get rank information
rankLabel, entryRank, rankOption = entryArea(mainWindow, 'Xếp loại', ['XS', 'G', 'K', 'TB', 'Y'], 4, rankChooseVariable)

#get minimum mark
minimarkLabel=Label(mainWindow, text = 'Điểm thấp nhất', font = ('Arial',15,'bold'), bg='#F1E5AC')
minimarkLabel.grid(row=5, column=0)
entryminiMark = Entry(mainWindow, font = ('Arial', 20),fg= 'black')
entryminiMark.grid(row=5, column=1)

#get maximum mark
maximarkLabel=Label(mainWindow, text = 'Điểm cao nhất', font = ('Arial',15,'bold'), bg='#F1E5AC')
maximarkLabel.grid(row=6, column=0)
entrymaxiMark = Entry(mainWindow, font = ('Arial', 20),fg= 'black')
entrymaxiMark.grid(row=6, column=1)

#buttons to search and read file, find file and read latest file
Button(mainWindow, text = 'Tìm file', font = ('Arial',15,'bold'), command= chooseFile, activebackground='blue')\
.grid(row= 7, column = 0, columnspan=1)
Button(mainWindow, text = 'Đọc file', font = ('Arial',15,'bold'), command= getFileandResult, activebackground='blue')\
.grid(row= 7, column = 1, columnspan=1)
Button(mainWindow, text = 'File mới nhất', font = ('Arial',15,'bold'), command= getLatestFile, activebackground='blue')\
.grid(row= 7, column = 2, columnspan=1)        
mainWindow.mainloop()