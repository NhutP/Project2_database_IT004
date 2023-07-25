import mysql.connector
import pandas as pd
import time 
import os
from tkinter import *
from tkinter import messagebox, ttk

#get path of this file
filePath =  os.path.dirname(os.path.abspath(__file__))

with open(filePath+'\\Prepared_data_for_generating\\school_name.txt', 'r', encoding='utf-8') as reader:
  schoolName = reader.read().split('\n')

def retrieveDataByQuerry(columnsName, databaseName, querry, measureTime=False):
  '''
  execute a querry\n\n
  databaseName: name of database to retrieve data\n
  querry: querry (string) to execute\n
  measureTime: whether include execution time at the out put or not\n\n
  return data retrieved from database and execution time (if require)
  '''

  #mark the starting time
  startingTime = time.time()
  try:
    database = mysql.connector.connect(
        host=entryHost.get().strip(),
        user=entryUsername.get().strip(),
        password=entryPassword.get(),
        database= databaseName
    )
    cursor = database.cursor()
    #execute the querry
    cursor.execute(querry)
    retrievedData = []

    for i in  cursor:
      retrievedData.append(i)

    #mark the finishing time
    finishingTime = time.time()
    retrievedDF = pd.DataFrame(retrievedData, columns= columnsName)

    cursor.close()
    database.close()

    #add time measure if need
    if measureTime:
        return retrievedDF, round(finishingTime - startingTime, 2)
    return retrievedDF

  #raise exception if error
  except mysql.connector.Error:
    messagebox.showerror(title = 'Error', message='Thông tin không hợp lệ, vui lòng kiểm tra lại.', icon='error')


#retrieve data base on required attributes 
def retrieveData(databaseName, schoolName, schoolYear, rank, measureTime= True, exportXML=False):
  '''
  get the data from database based on required information\n\n
  databaseName: name of database\n
  schoolName: name of school that student study\n
  schoolYear: year such that student result is recorded\n
  rank: 'XS' 'G' 'K' 'TB' 'Y'\n
  measureTime: set True if want to take execution time at out put\n
  exportXML: set True if want to export data XML file\n
  '''
  #construct a querry to retrieve data
  querry = f'Select concat_ws(" ", HO, TEN), NTNS, DIEMTB, XEPLOAI, KETQUA from \
            (Select * from HOC where NAMHOC = "{schoolYear}" and XEPLOAI = "{rank}" and MATR = (Select MATR from TRUONG where TRUONG.TENTR = "{schoolName}")) hocdaloctruong\
            join HS on HS.MAHS = hocdaloctruong.MAHS'
  
  #execute a querry and get result dataframe
  result, time = retrieveDataByQuerry(['HovaTen' ,'NTNS', 'DIEMTB', 'XEPLOAI', 'KETQUA'], databaseName=databaseName, querry=querry, measureTime=measureTime)

  #export a xml file if required
  if exportXML and (not result.empty):
    schoolNameFile = schoolName.replace(' ', '_')
    result.to_xml(filePath + f'\\XML\\{databaseName}-{schoolNameFile}-{schoolYear}-{rank}.xml', index=False, row_name= 'Hoc_sinh', encoding= 'utf-8')#,  attr_cols=['HovaTen' ,'NTNS', 'DIEMTB', 'XEPLOAI', 'KETQUA'])
    with open(filePath + '\\Prepared_data_for_generating\\latest_created _file.txt', 'w', encoding='utf-8') as writer:
      writer.write(f'{databaseName}-{schoolNameFile}-{schoolYear}-{rank}.xml')
  #return result and execution time
  return result, time


#conncet to mysql
def connect():
  '''
  connect to mysql based on provided information
  '''
  try:
    #get the entried password
    global entriedpassWord
    entriedpassWord = entryPassword.get()

    #connect to database Truonghoc1
    databaseTH1 = mysql.connector.connect(
        host=entryHost.get().strip(),
        user=entryUsername.get().strip(),
        password=entriedpassWord,
        database= 'TRUONGHOC1'
    )

    #conncet to database Truonghoc2
    databaseTH2 = mysql.connector.connect(
        host=entryHost.get().strip(),
        user=entryUsername.get().strip(),
        password=entriedpassWord,
        database= 'TRUONGHOC2'
    )
    
    #open querry window if connect sucessfully
    openQuerryWindow()

  #if can not connect raise an exception and warn
  except mysql.connector.Error:
    messagebox.showerror(title = 'Error', message='Check host name, username, password provided', icon='error')
  
def openQuerryWindow():
  '''
  open a new window to retrieve data
  '''
  #create a querry windoe
  global querryWindow 

  #hide main window
  mainWindow.withdraw()
  #create a querry window
  querryWindow = Toplevel(mainWindow)
  querryWindow.geometry('550x600')
  querryWindow.title('Truy xuat du lieu')
  querryWindow.config(background= '#CFECEC')
  querryWindow.resizable(False, False)
  #display buttons and entry boxes to the window
  Label(querryWindow, text = 'Nhập thông tin cần truy xuất', font = ('Arial',15,'bold'), bg='#CFECEC').grid(row= 0, column = 0, columnspan=3)

  #create lists for user can choose easily
  # create a function to handle menu item selection
  def handle_menu_selection(entry, menu_item):
    entry.delete(0, END)
    entry.insert(0, menu_item)

  #variable that will hold the value typed by user
  DatabaseChooseVariable = StringVar(querryWindow)  
  schoolChooseVariable = StringVar(querryWindow)
  yearChooseVariable = StringVar(querryWindow)
  rankChooseVariable = StringVar(querryWindow)
  
  #decide whether to export XML file or not
  exportXML = BooleanVar()

  #create an area for user to type information
  def entryArea(window, displayedText, values, y, variableResult):
    '''
    create entry area for user to type input\n\n
    window: window to display widget\n
    displayedText: text to display on label\n
    values: a list containing values for user to choose\n
    y: row\n
    variableResult: store input from user
    '''

    #create an entry label
    entryLabel = Label(window, text = displayedText, font = ('Arial',15,'bold'), bg='#CFECEC', anchor='center')
    entryLabel.grid(row=y, column=0)
    #create an entry box
    entryBox = Entry(window ,font = ('Arial', 20),fg= 'black')
    entryBox.grid(row= y, column=1)
    #make a selection
    selectOption = OptionMenu(window,variableResult, *values, command=lambda selected_option: handle_menu_selection(entryBox, selected_option))
    selectOption.config(width=1, height=1, bg='black', activebackground= 'green', fg= 'black', activeforeground='green')
    selectOption.configure()
    selectOption.grid(row=y, column=2)

    return entryLabel, entryBox, selectOption
  
  #get the database name
  databaseLabel, entryDatabase, DatabaseOption = entryArea(querryWindow, '        Database        ', ('TRUONGHOC1', 'TRUONGHOC2'), 1, DatabaseChooseVariable)

  #get the school name
  schoolLabel, entrySchool, schoolOption = entryArea(querryWindow, '        Trường        ', schoolName, 2, schoolChooseVariable)

  #get the school year
  yearLabel, entryYear, yearOption = entryArea(querryWindow, '        Năm học        ', [str(i) + '-' + str(i + 1) for i in range(2006, 2023, 1)], 3, yearChooseVariable)

  #get rank information
  rankLabel, entryRank, rankOption = entryArea(querryWindow, '        Xếp loại        ', ['XS', 'G', 'K', 'TB', 'Y'], 4, rankChooseVariable)

  
  #print result information
  def printQuerry():
    '''
    get the data from required input\n
    return a datafram and execution time
    '''    

    #retrieve data
    try:
      result, time = retrieveData(entryDatabase.get().strip().upper(), entrySchool.get().strip().upper()\
                    , entryYear.get().strip().upper(), entryRank.get().strip().upper(), exportXML=exportXML.get())
      resulttext = Label(querryWindow, text='Kết quả', font = ('Arial',15,'bold'), bg='#CFECEC')
      resulttext.grid(row=7, column=0, columnspan=3)
    except TypeError:
      return
    
    #if data frame is empty, show error
    if result.empty:
      messagebox.showerror(title = 'Lỗi', message='Không tìm thấy dữ liệu\n Kiểm tra lại thông tin', icon='error')
      return
    else:
      resultDisplay = ttk.Treeview(querryWindow, columns=(1,2,3,4,5), show='headings')
      columns = result.columns
      
      #modify heading in tree view
      for i in range(len(columns)):
        resultDisplay.heading(i+ 1, text= columns[i])

      #modify column size
      resultDisplay.column(1, width=200)
      resultDisplay.column(2, width=120)
      resultDisplay.column(3, width=50)
      resultDisplay.column(4, width=80)
      resultDisplay.column(5, width=70)

      #display the treeview
      resultDisplay.grid(row=8, column=0, columnspan=3)
      resultDisplay.tag_configure("myfont", font=("Arial", 12))

      # Insert data into the Treeview
      for i, row in result.iterrows():
        values = row.values.tolist()
        resultDisplay.insert("", "end", values=values, tags='myfont') 
      Label(querryWindow, text= 'Thời gian truy xuất', font=('Arial',15,'bold'), bg='#CFECEC').grid(row=9, column=0)
      Label(querryWindow, font=('Arial',15,'bold'), text= str(time) + ' giây', bg='#CFECEC').grid(row=9, column=1)

  #check whether export XML file or not
  Checkbutton(querryWindow, text= 'Xuất file XML',font=('Arial', 15, 'bold'), variable= exportXML, bg='#CFECEC').grid(row=5, column=0, columnspan=3)
  Button(querryWindow, text= 'Truy xuất', font = ('Arial',15,'bold'), command= printQuerry, activebackground='green', bg='#CFECEC').grid(row=6, column=0, columnspan=3)
  
  #if the queey window close, go back to main window
  querryWindow.protocol("WM_DELETE_WINDOW", goBackToMain)

#show the main window when the queey window is closed
def goBackToMain():
  mainWindow.deiconify()
  querryWindow.destroy()

#create entrybox and label for login area
def loginArea(window, displayedText,y,  defaultValue = '', showtype= None,):
  '''
  create login Area for user
  '''
  loginLabel = Label(window, text = displayedText, font = ('Arial',15,'bold'))
  loginLabel.grid(row=y, column=0)

  entry = Entry(window, font = ('Arial', 20),fg= 'blue')
  if showtype:
    entry.config(show= showtype)

  entry.grid(row=y, column=1)
  entry.insert(0, defaultValue)

  return loginLabel, entry

#CREATE A WINDOW TO GET INFORMATION FROM USER
#create main window
mainWindow = Tk()
mainWindow.geometry("300x200")
mainWindow.title('Connect to MYSQL')
mainWindow.resizable(False, False)

#connect label
Label(mainWindow, text = 'Connect to MYSQL', font = ('Arial',15,'bold'))\
.grid(row = 0, column=0, columnspan= 2)

#enter Host
hostLabel, entryHost = loginArea(mainWindow, 'Hostname', 1, 'localhost')

#enter username
usernameLabel, entryUsername = loginArea(mainWindow, 'Username', 2, 'root')

#enter password
passwordLabel, entryPassword= loginArea(mainWindow, 'Password', 3, showtype='*')

#login button
passwordsubmitButton = Button(mainWindow, text = 'Connect',font = ('Arial',15,'bold'), command= connect ,activebackground='blue')
passwordsubmitButton.grid(row=4, column=0, columnspan=2)

#display a window
mainWindow.mainloop()

