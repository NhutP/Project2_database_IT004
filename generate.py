import numpy as np
import string
import random
import os
from datetime import datetime
import mysql.connector
import threading
from tkinter import *
from tkinter import messagebox
import time

#get path of this file
filePath =  os.path.dirname(os.path.abspath(__file__))

#DECLARE DATA
#number of name need to be generated
numOfNames = int(1e6)
#list of numerical digits
digits = string.digits
#list of letters in alphabets
letters = string.ascii_letters

#GENERATE CODES FOR BOTH STUDENTS AND SCHOOLS

#FIRST generate a single code with given size
generateCode = lambda size: ''.join(random.choice(digits) for x in range(size))

#THEN generate the list of codes
def generateRandomCode(quantity, option = 'student'):
    '''
    generate lists of random codes\n\n
    quantity: quantity to generate\n
    option: type of code: 'student', 'identity' and 'school' for student code, identity code and school code respectively\n    
    student code has length 8 and identity code has length 12 and school code is 4\n\n
    return a list of code
    '''
    randomCode = []
    sizeofCode = 0

    #set length of code by the option
    if option == 'student':
        sizeofCode = 8
    elif option == 'identity':
        sizeofCode = 12
    elif option == 'school':
        sizeofCode = 4

    #generate the random code until we get enough
    while(len(set(randomCode)) < quantity):
        for i in range(quantity):
            randomCode.append(generateCode(sizeofCode))
    
    #return the list of names with excact quantity 
    return list(set(randomCode))[0:quantity]

#GENERATE RANDOM ADRESSES FOR BOTH STUDENTS AND SCHOOLS

#FIRST, generate a single address with given size
generateRandomAddress = lambda size : ''.join(random.choice(letters) for itt in range(size))

#THEN generate list of complet addresses
def generateAddress(quantity):
    '''
    generate random address has a format: 'Số ... Đường ... Quận ... Thành phố ...'\n\n 
    quantity: quantity to gennerate\n\n
    return list of addresses
    '''
    return ['Số ' + generateCode(2) + ' Đường ' + generateRandomAddress(np.random.randint(3,6)) +\
             ' Quận ' + generateRandomAddress(np.random.randint(3,6)) + ' TP ' +\
                generateRandomAddress(np.random.randint(3,6)) for i in range(quantity)]



#GENERATE STUDENT NAMES

#FIRST, read 3 components from prepared file
def readFile(fileName):
    '''
    take the file name and return list containing data in that file\n
    mainly used to read name list in the prepared txt file
    '''

    with open(filePath + "\\Prepared_data_for_generating\\" + fileName, 'r', encoding='utf-8') as reader:#open file
        data = reader.read().split('\n')#read data in file
    # clear the redundant white space of the result 
    return [data[i].strip() for i in range(len(data))]


#THEN generte complete names
def generateRandomStudentName(quantity):
    '''
    generate list of random name for students\n\n
    quantity: quantity to generate\n\n
    return 2 lists of surnames and names based on prepared txt file\n
    '''

    #get prepared data for 3 components by using previous function
    #get surnames from prepared txt file
    surName = readFile('surname.txt')
    #get middle names from prepared txt file
    middleName = readFile('middle_name.txt')
    #get last names from prepared txt file
    lastName = readFile('last_name.txt')

    #create 2 list to store result
    randomNames = []
    randomSurnames = []

    #create random index array for 3 components
    surNameRandIndex = np.random.randint(0, len(surName), quantity)
    middleNameRandIndex = np.random.randint(0, len(middleName), quantity)
    lastNameRandIndex = np.random.randint(0, len(lastName), quantity)
    numberOfWord = np.random.randint(0, 2, quantity) #0 means there are 3 words in a name, 1 means 4
    
    #start generating random names using 3 parts surname, middle name and last name
    for i in range(quantity):
        #using random index array generated previously
        #base on these array, take the index in each parts and form a name
        #add a first middle name
        tempName = middleName[middleNameRandIndex[i]] + ' '

        #if name has 4 words, add 1 more middle name
        if numberOfWord[i] == 1:
            tempName += middleName[np.random.randint(0, len(middleName))] + ' '
        
        #add the last name and append to the random name list
        tempName += lastName[lastNameRandIndex[i]]
        randomNames.append(tempName)

        #add the surname to random surname list
        randomSurnames.append(surName[surNameRandIndex[i]])
    #return 2 result lists
    return randomSurnames, randomNames


#generate random day of birth for students
def generateDayOfBirth(quantity):
    '''
    quantity: quantity to generate\n\n
    return list of random day of birth
    '''

    #length of each monts, 0 stands for january, 1 for february,......
    daysinMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 30]

    #generate year
    randomBirthYear = np.random.randint(1990, 2005, quantity)
    #generate month
    randomBirthMonth = np.random.randint(1, 13, quantity)  
    #generate day based on month
    randomBirthDay = np.array([np.random.randint(1, daysinMonth[i - 1] + 1) for i in randomBirthMonth])

    #set the date format
    dateFormat = "%Y-%m-%d"
    #concatenate 3 components and make complete birthdays
    return [datetime.strptime('-'.join([str(randomBirthYear[i]), str(randomBirthMonth[i]), str(randomBirthDay[i])]), dateFormat).strftime(dateFormat) for i in range(quantity)]

#generate learning information
def generateLearningInformation(studentCode, schoolCode, studentBirthDay):
    '''
    generate students' school years and marks\n
    studentCode: list of student codes\n
    schoolCode: list of school codes\n\n
    return 2 list 
    the first list contains school code of student school with index correspoding to index of students\n
    the second list contains dictionaries\n
    each dictionary has key is student code and value is another sub-dictionary\n
    each sub-dictionary has key is student school year and value is the mark of student in this school year
    '''
    
    #take the quantity of students (by studentCode)
    studentQuantity = len(studentCode)

    #take the quantity of schools (by schoolCode)
    schoolQuantity = len(schoolCode)

    learningInformation = []
    studentSchool = {}

    #number of years when students study at school
    numberOfYears = np.random.randint(2,4, studentQuantity)
    
    #iterate students
    for studentIndex in range(studentQuantity):
        #create dictionary hold student's learning information
        studentLearnInfo = {}
        #generate a school for student
        studentSchool[studentCode[studentIndex]] = schoolCode[np.random.randint(0, schoolQuantity)]
        
        #years each student spent to study at school (which was recored)
        tempnumofyears = numberOfYears[studentIndex]
        studentBirth = studentBirthDay[studentIndex][0:4]
        
        #generate school years
        for j in range(tempnumofyears):
            studentLearnInfo[str(int(studentBirth) + j + 16) + '-' + str(int(studentBirth) + j + 17)] = round(10 - np.random.uniform(0, 6), 1)
        
        learningInformation.append(studentLearnInfo)
    return studentSchool, learningInformation


#START TO GENERATE DATA

print('Generating data, please wait...')
#get school names from prepared file
schoolName = readFile('school_name.txt')
#get quantity of schools
numOfSchools = len(schoolName)

# GENERATE INFORMATION FOR SCHOOLS
#generate school code
randomSchoolCodes = generateRandomCode(numOfSchools, option='school')

#generate school adress
randomSchoolAddress = generateAddress(numOfSchools)

#GENERATE INFORMATION FOR STUDENTS
#get the result after generating random names
randomSurnames, randomNames = generateRandomStudentName(quantity= numOfNames)

#generate student codes and identity codes
randomStudentCodes = generateRandomCode(numOfNames, option= 'student')
randomIdentityCodes = generateRandomCode(numOfNames, option= 'identity')

#generate day of birth
randomDayOfBirth = generateDayOfBirth(numOfNames)

#generate random student address
randomStudentAddress = generateAddress(numOfNames)

#generate learningInformation for students
schoolOfStudent, learningInformation = generateLearningInformation(randomStudentCodes, randomSchoolCodes, randomDayOfBirth)


#CONCATENATE COMPONENTS TO MAKE COMPLETE QUERRIES FOR 3 TABLES

#create querry to insert to TRUONG table
QuerryforTruongTable = 'insert into TRUONG values \n'
for i in range(numOfSchools):
    QuerryforTruongTable += f'("{randomSchoolCodes[i]}", "{schoolName[i]}", "{randomSchoolAddress[i]}"),\n'

QuerryforTruongTable = QuerryforTruongTable[0 : len(QuerryforTruongTable) - 2] + ';'

#create querry to insert to HS table
QuerryforHocsinhTable = []
SingleQuerryforHocsinhTable = 'insert into HS values \n'
for i in range(numOfNames):
    #for each student, concatenate code, surname, name, birth, address to form a insert querry
    SingleQuerryforHocsinhTable += f'("{randomStudentCodes[i]}", "{randomSurnames[i]}", "{randomNames[i]}", "{randomIdentityCodes[i]}", "{randomDayOfBirth[i]}", "{randomStudentAddress[i]}"),\n'
    if (i + 1) % 1000 == 0:
        SingleQuerryforHocsinhTable = SingleQuerryforHocsinhTable[0 : len(SingleQuerryforHocsinhTable) - 2] + ';\n'
        QuerryforHocsinhTable.append(SingleQuerryforHocsinhTable)
        SingleQuerryforHocsinhTable = 'insert into HS values \n'

#get complete status by using score (complete when score >= 5)
getCompleteStatus = lambda Score : 'HT' if Score >= 5 else 'KHT'

#get rank by score of student
def getRank(score):
    '''
    get rank of student (XS, G, K, TB, Y)\n\n
    score: score of student\n\n
    return string represent student rank
    '''
    #check range of score and take approriate result
    if score >= 9:
        return 'XS'
    elif score >= 8:
        return 'G'
    elif score >= 7:
        return 'K'
    elif score >= 5:
        return 'TB' 
    else:
        return 'Y'

#create querry to insert to HOC table
QuerryforHocTable = []
singleQuerryforHocTable = 'insert into HOC values\n'
for i in range(numOfNames):
    #for each student, random the school years and random score
    #get rank, complete status
    #concatenate theese components to form an insert querry
    tempQuerries = []
    studentinfp = f'("{schoolOfStudent[randomStudentCodes[i]]}", "{randomStudentCodes[i]}", '
    for year, score in learningInformation[i].items():
        queery = studentinfp + f'"{year}", {score}, ' + '"' + str(getRank(score)) + '"' + ', "' + getCompleteStatus(score) + '"),\n'
        tempQuerries.append(queery)

    #for each school year, make the different querry
    for que in tempQuerries:
        singleQuerryforHocTable += que

    if (i + 1) % 1000 == 0:
        QuerryforHocTable.append(singleQuerryforHocTable[0: len(singleQuerryforHocTable) - 2] + ';\n')
        singleQuerryforHocTable = 'insert into HOC values\n'

print('\nData is ready')
time.sleep(2)

def connect():
  global hostName
  global userName
  global passw

  try:
    #get the entried password
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
    hostName=entryHost.get().strip()
    userName= entryUsername.get().strip()
    passw= entriedpassWord
    insertData()
  #if can not connect raise an exception and warn
  except mysql.connector.Error:
    messagebox.showerror(title = 'Error', message='Check host name, username, password provided', icon='error')

#execute querry created previously to insert data
def insertDataDatabase(databaseName):
    #connect to mysql     
    databaseInsert = mysql.connector.connect(
        host= hostName,
        user= userName,
        password=passw,
        database= databaseName
    )
        
    #create a cursor
    cursor = databaseInsert.cursor()

    #INSERT DATA TO 3 TABLES

    #insert to TRUONG table
    cursor.execute(QuerryforTruongTable)
    databaseInsert.commit()

    #insert to HS table
    for insertQuerry in QuerryforHocsinhTable:
        cursor.execute(insertQuerry)
        databaseInsert.commit()
    
    #insert to HOC table
    for insertQuerry in QuerryforHocTable:
        cursor.execute(insertQuerry)
        databaseInsert.commit()

    cursor.close()
    databaseInsert.close()

#use multi threading to process faster
def insertData():
    '''
    insert data to database
    '''
    mainWindow.withdraw()    
    print('Connected to MYSQL\nInserting, please wait...')

    #create threads
    thread1 = threading.Thread(target=insertDataDatabase, args=('TRUONGHOC1',))
    thread2 = threading.Thread(target=insertDataDatabase, args=('TRUONGHOC2',))
    
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    print('\nInserted sucessfully')
    mainWindow.destroy()

#Design window for user to connect to MYSQL
#create main window
#create entrybox and label for login area
def loginArea(window, displayedText,y,  defaultValue = '', showtype= None,):
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
