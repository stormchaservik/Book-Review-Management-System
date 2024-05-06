from tkinter import *
import tkinter.messagebox
import mysql.connector
import mysql.connector
from mysql.connector import errorcode

cnxObj = mysql.connector.connect(user = "admin", password = "adminpass", host = "127.0.0.1")
dbCursor = cnxObj.cursor()


dbName = "bookreviews"

tables = {}

tables['booklist'] = (
    "CREATE TABLE `booklist` (`ID` int(10) PRIMARY KEY, `Title` varchar(50), `ISBN` varchar(15))"
)

tables['bookdetails'] = (
    "CREATE TABLE `bookdetails` (`ID` int(10), FOREIGN KEY (`ID`) REFERENCES booklist (`ID`), `Title` varchar(50), `Genre` varchar(15), `Author` varchar(30), `WordCount` int(10), `NoOfPages` int(5))"
)

tables['extrainfo'] = (
    "CREATE TABLE `extrainfo` (`ID` int(10), FOREIGN KEY (`ID`) REFERENCES booklist (`ID`), `AvgRating` decimal(2,2), `Sales` int(10))"
)

tables['reviews'] = (
    "CREATE TABLE `reviews` (`ID` int(10), FOREIGN KEY (`ID`) REFERENCES booklist (`ID`), `ReviewText` text, `Rating` int(1), `ReviewID` int(10) UNIQUE)"
)

tables ['reviewers'] = (
    "CREATE TABLE `reviewers` (`ID` int(10), FOREIGN KEY (`ID`) REFERENCES booklist (`ID`), `PersonID` int(10), `PersonName` varchar(30), `ReviewID` int(10), FOREIGN KEY (`ReviewID`) REFERENCES reviews (`ReviewID`))"
)


def createDatabase(dbCursor):
    try:
        dbCursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(dbName))
    
    except mysql.connector.Error as err:
        print("Failed to create database: {}".format(err))
        exit(1)

try:
    dbCursor.execute("USE {}".format(dbName))

except mysql.connector.Error as err:
    print("Database {} does not exist".format(dbName))
    
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        createDatabase(dbCursor)
        print("Database {} created successfully".format(dbName))
        cnxObj.database = dbName
    
    else:
        print(err)
        exit(1)

for tableName in tables:
    tableDesc = tables[tableName]
    try:
        print("Creating table {}: ".format(tableName), end='')
        dbCursor.execute(tableDesc)
    
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("Already exists")
        
        else:
            print(err.msg)
    
    else:
        print("OK")

addBook = ("INSERT INTO booklist (ID, Title, ISBN) VALUES (%s, %s, %s)")
addDetails = ("INSERT INTO bookdetails (ID, Title, Genre, Author, WordCount, NoOfPages) VALUES (%s, %s, %s, %s, %s, %s)")
addInfo = ("INSERT INTO extrainfo (ID, AvgRating, Sales) VALUES (%s, %s, %s)")
addReview = ("INSERT INTO reviews (ID, ReviewText, Rating) VALUES (%s, %s, %s)")
addReviewer = ("INSERT INTO reviewers (ID, PersonID, PersonName) VALUES (%s, %s, %s)")

deleteBook = ("DELETE FROM booklist WHERE ID = %s")
deleteDetails = ("DELETE FROM bookdetails WHERE ID = %s")
deleteInfo = ("DELETE FROM extrainfo WHERE ID = %s")
deleteReview = ("DELETE FROM reviews WHERE ID = %s")
deleteReviewer = ("DELETE FROM reviewers WHERE ID = %s")

dispBook = ("SELECT * FROM bookdetails")
dispReviews = ("SELECT reviews.ID, reviews.ReviewText, reviews.Rating, reviewers.PersonName from reviews INNER JOIN reviewers ON reviews.ID = reviewers.ID")


class bookReview:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Review Management System")
        self.root.geometry("1280x720")
        self.root.config(bg="black")

        ID = StringVar()
        Title = StringVar()
        ISBN = StringVar()
        Genre = StringVar()
        Author = StringVar()
        WordCount = StringVar()
        NoOfPages = StringVar()
        AvgRating = StringVar()
        Sales = StringVar()
        ReviewText = StringVar()
        ReviewID = StringVar()
        Rating = StringVar()
        PersonID = StringVar()
        PersonName = StringVar()

        def iExit():
            iExit = tkinter.messagebox.askyesno("Book Review Management System", "Do you want to exit?")
            if iExit > 0:
                root.destroy()
            return
        
        def clearData():
            self.txtID.delete(0, END)
            self.txtTitle.delete(0, END)
            self.txtISBN.delete(0, END)
            self.txtGenre.delete(0, END)
            self.txtAuthor.delete(0, END)
            self.txtWordCount.delete(0, END)
            self.txtNoOfPages.delete(0, END)
            self.txtAvgRating.delete(0, END)
            self.txtSales.delete(0, END)
            self.txtReviewText.delete(0, END)
            self.txtRating.delete(0, END)
            self.txtPersonID.delete(0, END)
            self.txtPersonName.delete(0, END)

        def insertBook():
            if(len(ID.get()) != 0):
                tkID = ID.get()
                tkTitle = Title.get()
                tkISBN = ISBN.get()
                book = (tkID, tkTitle, tkISBN)
                dbCursor.execute(addBook, book)
                cnxObj.commit()

        def insertDetails():
            if(len(ID.get()) != 0):
                tkID = ID.get()
                tkTitle = Title.get()
                tkAuthor = Author.get()
                tkGenre = Genre.get()
                tkWordCount = WordCount.get()
                tkNoOfPages = NoOfPages.get()
                bookDetails = (tkID, tkTitle, tkGenre, tkAuthor, tkWordCount, tkNoOfPages)
                dbCursor.execute(addDetails, bookDetails)
                cnxObj.commit()

        def insertReview():
            if(len(ID.get()) != 0):
                tkID = ID.get()
                tkReviewText = ReviewText.get()
                tkRating = Rating.get()
                tkPersonID = PersonID.get()
                tkPersonName = PersonName.get()
                review = (tkID, tkReviewText, tkRating)
                reviewer = (tkID, tkPersonID, tkPersonName)
                dbCursor.execute(addReview, review)
                dbCursor.execute(addReviewer, reviewer)
                cnxObj.commit()
        
        def displayBook():
            #if(len(ID.get()) != 0):
                #tkID = ID.get()
                #dist = (tkID,)
            dbCursor.execute(dispBook)
            self.txtboxDets.delete('1.0', END)
            for(ID, Title, Genre, Author, WordCount, NoOfPages) in dbCursor:
                self.txtboxDets.insert('1.0', "ID: {}, Title: {}, Genre: {}, Author: {}, WordCount: {}, NoOfPages: {} \n".format(ID, Title, Genre, Author, WordCount, NoOfPages))

        def displayReviews():
            #if(len(ID.get()) != 0):
                #tkID = ID.get()
                #dist = (tkID,)
            dbCursor.execute(dispReviews)
            self.txtboxDets.delete('1.0', END)
            for(ID, ReviewText, Rating, PersonName) in dbCursor:
                self.txtboxDets.insert('1.0', "ID: {}, ReviewText : {}, Rating: {}/10, PersonName: {} \n".format(ID, ReviewText, Rating, PersonName))
        
        def deleteData():
            if(len(ID.get()) != 0):
                tkID = ID.get()
                delt = (tkID,)
                dbCursor.execute(deleteDetails, delt)
                dbCursor.execute(deleteReview, delt)
                dbCursor.execute(deleteReviewer, delt)
                dbCursor.execute(deleteBook, delt)
                clearData()
                cnxObj.commit()
        
    
        MainFrame = Frame(self.root, bg = "azure3")
        MainFrame.grid()

        TFrame = Frame(MainFrame, bd = 4, padx = 54, pady = 16, bg = "azure4", relief = RIDGE)
        TFrame.pack(side = TOP)

        self.TFrame = Label(TFrame, font = ('Courier New', 36, 'bold'), text = "Book Review Management System", bg = 'azure4', fg = 'black')
        self.TFrame.grid()

        BFrame = Frame(MainFrame, bd = 3, width = 1300, height = 70, padx = 18, pady = 10, bg = 'azure3', relief = RIDGE)
        BFrame.pack(side = BOTTOM)

        DFrame = Frame(MainFrame, bd = 4, width = 1500, height = 800, padx = 20, pady = 20, bg = 'azure3', relief = RIDGE)
        DFrame.pack(side = BOTTOM)

        DFrameR = LabelFrame(DFrame, font = ('Courier New', 20, 'bold'), text = "Details \n", bg = 'azure3', fg = 'black', height = 700)
        DFrameR.pack(side = RIGHT)

        DFrameL = LabelFrame(DFrame, font = ('Courier New', 20, 'bold'), text = "Book Info \n", bg = 'azure3', fg = 'black', height = 700)
        DFrameL.pack(side = LEFT)

        self.lbID = Label(DFrameL, text = "ID", bg = 'azure3', fg = 'black')
        self.lbID.grid(row = 0, column = 0, sticky = W)
        self.txtID = Entry(DFrameL, textvariable = ID)
        self.txtID.grid(row = 0, column = 1)

        self.lbTitle = Label(DFrameL, text = "Title", bg = 'azure3', fg = 'black')
        self.lbTitle.grid(row = 1, column = 0, sticky = W)
        self.txtTitle = Entry(DFrameL, textvariable = Title)
        self.txtTitle.grid(row = 1, column = 1)

        self.lbISBN = Label(DFrameL, text = "ISBN", bg = 'azure3', fg = 'black')
        self.lbISBN.grid(row = 2, column = 0, sticky = W)
        self.txtISBN = Entry(DFrameL, textvariable = ISBN)
        self.txtISBN.grid(row = 2, column = 1)

        self.lbGenre = Label(DFrameL, text = "Genre", bg = 'azure3', fg = 'black')
        self.lbGenre.grid(row = 3, column = 0, sticky = W)
        self.txtGenre = Entry(DFrameL, textvariable = Genre)
        self.txtGenre.grid(row = 3, column = 1)

        self.lbAuthor = Label(DFrameL, text = "Author", bg = 'azure3', fg = 'black')
        self.lbAuthor.grid(row = 4, column = 0, sticky = W)
        self.txtAuthor = Entry(DFrameL, textvariable = Author)
        self.txtAuthor.grid(row = 4, column = 1)

        self.lbWordCount = Label(DFrameL, text = "Word Count", bg = 'azure3', fg = 'black')
        self.lbWordCount.grid(row = 5, column = 0, sticky = W)
        self.txtWordCount = Entry(DFrameL, textvariable = WordCount)
        self.txtWordCount.grid(row = 5, column = 1)

        self.lbNoOfPages = Label(DFrameL, text = "No. of Pages", bg = 'azure3', fg = 'black')
        self.lbNoOfPages.grid(row = 6, column = 0, sticky = W)
        self.txtNoOfPages = Entry(DFrameL, textvariable = NoOfPages)
        self.txtNoOfPages.grid(row = 6, column = 1)

        self.lbAvgRating = Label(DFrameL, text = "Avg. Rating", bg = 'azure3', fg = 'black')
        self.lbAvgRating.grid(row = 7, column = 0, sticky = W)
        self.txtAvgRating = Entry(DFrameL, textvariable = AvgRating)
        self.txtAvgRating.grid(row = 7, column = 1)

        self.lbSales = Label(DFrameL, text = "Sales", bg = 'azure3', fg = 'black')
        self.lbSales.grid(row = 8, column = 0, sticky = W)
        self.txtSales = Entry (DFrameL, textvariable = Sales)
        self.txtSales.grid(row = 8, column = 1)

        self.lbReviewText = Label(DFrameL, text = "Review Text", bg = 'azure3', fg = 'black')
        self.lbReviewText.grid(row = 9, column = 0, sticky = W)
        self.txtReviewText = Entry (DFrameL, textvariable = ReviewText)
        self.txtReviewText.grid(row = 9, column = 1)

        self.lbRating = Label(DFrameL, text = "Rating", bg = 'azure3', fg = 'black')
        self.lbRating.grid(row = 10, column = 0, sticky = W)
        self.txtRating = Entry (DFrameL, textvariable = Rating)
        self.txtRating.grid(row = 10, column = 1)

        self.lbPersonID = Label(DFrameL, text = "Person ID", bg = 'azure3', fg = 'black')
        self.lbPersonID.grid(row = 11, column = 0, sticky = W)
        self.txtPersonID = Entry (DFrameL, textvariable = PersonID)
        self.txtPersonID.grid(row = 11, column = 1)

        self.lbPersonName = Label(DFrameL, text = "Person Name", bg = 'azure3', fg = 'black')
        self.lbPersonName.grid(row = 12, column = 0, sticky = W)
        self.txtPersonName = Entry (DFrameL, textvariable = PersonName)
        self.txtPersonName.grid(row = 12, column = 1)

        self.txtboxDets = Text(DFrameR, bg = 'gray70', fg = 'black')
        self.txtboxDets.grid(row = 0, column = 0, sticky = W)


        self.btInsertBook = Button(BFrame, text = "Insert Book", command = insertBook)
        self.btInsertBook.grid(row = 0, column = 0)

        self.btInsertDetails = Button(BFrame, text = "Insert Details", command = insertDetails)
        self.btInsertDetails.grid(row = 0, column = 1)

        self.btInsertReview = Button (BFrame, text = "Insert Review", command = insertReview)
        self.btInsertReview.grid(row = 0, column = 2)

        self.btDispBook = Button(BFrame, text = "Display Book", command = displayBook)
        self.btDispBook.grid(row = 0, column = 3)

        self.btDispReview = Button(BFrame, text = "Display Review", command = displayReviews)
        self.btDispReview.grid(row = 0, column = 4)

        self.btDelete = Button(BFrame, text = "Delete Data", command = deleteData)
        self.btDelete.grid(row = 0, column = 6)

if __name__ == '__main__':
    root = Tk()
    book = bookReview(root)
    root.geometry("950x650")
    root.mainloop()