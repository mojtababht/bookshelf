from tkinter import *
import mysql.connector
class window (Tk):
    def __init__(self):
        super().__init__()
        self.geometry("500x500")
        self.title("book shelf")
        photo = PhotoImage(file="a.png")
        self.iconphoto(False,photo)
        self.options()

    def options(self):

        l1 = Label(self, text="Title")
        l1.place(x=10, y=10)
        l2 = Label(self, text="Author")
        l2.place(x=200, y=10)
        l3 = Label(self, text="Year")
        l3.place(x=10, y=50)
        l4 = Label(self, text="ISBN")
        l4.place(x=200, y=50)

        e1 = Entry(self)
        e1.place(x=50, y=10)
        e2 = Entry(self)
        e2.place(x=250, y=10)
        e3 = Entry(self)
        e3.place(x=50, y=50)
        e4 = Entry(self)
        e4.place(x=250, y=50)


        bt1 = Button(self, text="View All", width=13,command=lambda :bt1c())
        bt1.place(x=250, y=75)
        bt2 = Button(self, text="Search Entry", width=13,command=lambda :bt2c(e1.get(),e2.get(),e3.get(),e4.get()))
        bt2.place(x=250, y=105)
        bt3 = Button(self, text="Add Entry", width=13,command=lambda :bt3c(e4.get(),e1.get(),e2.get(),e3.get()))
        bt3.place(x=250, y=135)
        bt4 = Button(self, text="Update Entry", width=13,command=lambda :bt4c(e4.get(),e1.get(),e2.get(),e3.get()))
        bt4.place(x=250, y=165)
        bt5 = Button(self, text="Delete Selected", width=13,command=lambda :bt5c())
        bt5.place(x=250, y=195)
        bt6 = Button(self, text="Close", width=13,command=lambda :self.destroy())
        bt6.place(x=250, y=225)

        sb1 = Scrollbar(self)
        sb1.place(x=200, y=125)
        sb2=Scrollbar(self,orient=HORIZONTAL)
        sb2.place(x=85,y=250)

        self.textDP = Listbox(self,yscrollcommand=sb1.set,xscrollcommand=sb2.set)
        self.textDP.place(x=50, y=75)

        sb1.config(command=self.textDP.yview)
        sb2.config(command=self.textDP.xview)

class dbControler ():
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        mycursor1 = self.mydb.cursor()
        mycursor1.execute("create database if not exists bookshelf")
        mycursor1.close()
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bookshelf"
        )
        self.mycursor = self.mydb.cursor()
        self.mycursor.execute("create table if not exists books(ISBN int primary key,Title varchar(30),Author varchar(30),Year int)")
    def addbook(self,isbn,title,authur,year):

        sql = "insert into books(ISBN,Title ,Author,Year) values (%s,%s,%s,%s)"
        val = (isbn, title, authur, year)
        self.mycursor.execute(sql, val)
        self.mydb.commit()
    def showBooks(self,textDP):
        textDP.delete(0,END)
        self.mycursor.execute("select * from books")
        result=self.mycursor.fetchall()
        for i in result:
            textDP.insert(END,i)
    def searchBook(self,textDP,eT,eA,eY,eI):
        textDP.delete(0,END)
        if eY!="":
            ey=int(eY)
        else:
            ey=eY
        if eI!='':
            ei=int(eI)
        else:
            ei=eI
        sql='select * from books where Title = %s or Author = %s or Year = %s or ISBN =%s '
        val=(eT,eA,ey,ei)
        self.mycursor.execute(sql,val)
        result=self.mycursor.fetchall()
        for i in result:
            textDP.insert(END,i)
    def updateBook(self,win,isbn,title,author,year):
        val=win.textDP.get(win.textDP.curselection())
        val1=list(val)
        Isbnf=val1[0]
        if isbn!="":
            val1[0]=isbn
        if title!="":
            val1[1]=title
        if author!="":
            val1[2]=author
        if year!="":
            val1[3]=year
        val1.append(Isbnf)
        val2=tuple(val1)
        sql="update books set ISBN = %s ,Title = %s , Author = %s , Year = %s where ISBN = %s "
        self.mycursor.execute(sql,val2)
        self.mydb.commit()
    def deleteBook(self,win):
        val = win.textDP.get(win.textDP.curselection())
        isbn =val[0]
        val1=(isbn,)
        sql="delete from books where ISBN = %s"
        self.mycursor.execute(sql,val1)
        self.mydb.commit()



win =window()

dbc=dbControler()
def bt1c ():
    dbc.showBooks(win.textDP)
def bt2c(et,ea,ey,ei):
    dbc.searchBook(win.textDP,et,ea,ey,ei)
def bt3c (isbn,title,authur,year):
    dbc.addbook(isbn,title,authur,year)
def bt4c(isbn,title,authur,year):
    dbc.updateBook(win,isbn,title,authur,year)
def bt5c ():
    dbc.deleteBook(win)


win.mainloop()

