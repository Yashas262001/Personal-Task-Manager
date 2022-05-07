import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import font
from tkcalendar import Calendar
from tkinter import messagebox

import mysql.connector

mydb=mysql.connector.connect(host="localhost",user="root",password="Yashas@2001",database="demo",auth_plugin="mysql_native_password")
cursor=mydb.cursor()
root=tk.Tk()
root.title("Personal Task Manager")
root.geometry("900x790")

def display(rows):
    trv.delete(*trv.get_children())
    for i in rows:
        trv.insert('','end',values=i)

def search():
    id=var1.get()
    name=var3.get()
    query="SELECT * FROM task WHERE task_id="+id
    cursor.execute(query)
    rows=cursor.fetchall()
    display(rows)

def clear():
   query="SELECT task_id,task_name,date,time,completed FROM task"
   cursor.execute(query)
   rows=cursor.fetchall()
   display(rows)

def pending_tasks():
    query="SELECT * FROM task WHERE completed='No'"
    cursor.execute(query)
    rows=cursor.fetchall()
    display(rows)

def completed_tasks():
    query="SELECT * FROM task WHERE completed='Yes'"
    cursor.execute(query)
    rows=cursor.fetchall()
    display(rows)

def getrow(event):
    rowid=trv.identify_row(event.y)
    item=trv.item(trv.focus())
    var2.set(item['values'][0])
    var3.set(item['values'][1])
    cal.get_displayed_month(item['values'][2])
    var5.set(item['values'][3])
    var6.set(item['values'][4])

def insert():
    id=var2.get()
    name=var3.get()
    date=cal.get_date()
    time=t1.get()+':'+t2.get()+':'+t3.get()
    completed_yes=var6.get()
    if completed_yes:
        query="INSERT INTO task(task_id,task_name,date,time,completed) VALUES(%s,%s,%s,%s,%s)"
        val=(id,name,date,time,'Yes')
        cursor.execute(query,val)
        clear()
    else:
        query="INSERT INTO task(task_id,task_name,date,time,completed) VALUES(%s,%s,%s,%s,%s)"
        val=(id,name,date,time,'No')
        cursor.execute(query,val)
        clear()
    mydb.commit()

def update():
    id=var2.get()
    name=var3.get()
    date=cal.get_date()
    time=t1.get()+':'+t2.get()+':'+t3.get()
    completed=var6.get()
    if messagebox.askyesno("Confirm Update?","Are you sure you want to update this task?"):
        if completed:
            query="UPDATE task SET task_name=%s,date=%s,time=%s,completed='Yes' WHERE task_id="+id
            val=(name,date,time)
        else:
            query="UPDATE task SET task_name=%s,date=%s,time=%s,completed='No' WHERE task_id="+id
            val=(name,date,time)
    else:
        return True
    cursor.execute(query,val)
    clear()
    mydb.commit()

def delete():
    id=var2.get()
    if messagebox.askyesno("Confirm Delete?","Are you sure you want to delete this task?"):
        query="DELETE FROM task WHERE task_id="+id
        cursor.execute(query)
        clear()
    else:
        return True
    mydb.commit()


#Tasks Section
wrapper1=tk.LabelFrame(root,text="Task List",font="Calibri 14 bold")
wrapper2=tk.LabelFrame(root,text="Search",font="Calibri 14 bold")
wrapper3=tk.LabelFrame(root,text="Task Description",font="Calibri 14 bold")

wrapper1.pack(fill="both",expand="yes",padx=20,pady=10)
wrapper2.pack(fill="both",expand="yes",padx=20,pady=10)
wrapper3.pack(fill="both",expand="yes",padx=20,pady=10)

trv=ttk.Treeview(wrapper1,columns=(1,2,3,4,5),show="headings",height="7")
trv.pack()
trv.column(1,width=60)
trv.column(5,width=90)
trv.column(2,width=300)
trv.heading(1,text="Task ID")
trv.heading(2,text="Tasks")
trv.heading(3,text="Date")
trv.heading(4,text="Time")
trv.heading(5,text="Completed")
trv.bind('<Double 1>',getrow)

style = ttk.Style()
style.configure('Treeview.Heading', foreground = 'black', font = ('Calibri', 12,'bold'))

#sb = Scrollbar(wrapper1, orient=VERTICAL)
#sb.pack(side=RIGHT, fill=Y)

#trv.config(yscrollcommand=sb.set)
#sb.config(command=trv.yview)


#Search Section
label1=tk.Label(wrapper2,text="Search",font = ('Calibri', 12,'bold'))
label1.pack(side=tk.LEFT, padx=10)
var1=StringVar()
entry1=tk.Entry(wrapper2,textvariable=var1)
entry1.pack(side=tk.LEFT,padx=6)
btn1=tk.Button(wrapper2,text="Search",command=search)
btn1.pack(side=tk.LEFT,padx=6)
btn2=tk.Button(wrapper2,text="Clear",command=clear)
btn2.pack(side=tk.LEFT,padx=6)
btn3=tk.Button(wrapper2,text="Pending Tasks",command=pending_tasks)
btn3.pack(side=tk.LEFT,padx=6)
btn4=tk.Button(wrapper2,text="Completed Tasks",command=completed_tasks)
btn4.pack(side=tk.LEFT,padx=6)


#Task Details
var2=StringVar()
var3=StringVar()
var4=StringVar()
var5=StringVar()
var6=IntVar()
var7=IntVar()
t1=StringVar()
t2=StringVar()
t3=StringVar()
label2=tk.Label(wrapper3,text="Task ID",font = ('Calibri', 12,'bold'))
label2.grid(row=0,column=0,padx=5,pady=0)
entry2=tk.Entry(wrapper3,textvariable=var2)
entry2.grid(row=0,column=1,padx=5,pady=10)
label3=tk.Label(wrapper3,text="Task Name",font = ('Calibri', 12,'bold'))
label3.grid(row=1,column=0,padx=5,pady=10)
entry3=tk.Entry(wrapper3,textvariable=var3)
entry3.grid(row=1,column=1,padx=5,pady=10)
label4=tk.Label(wrapper3,text="Date",font = ('Calibri', 12,'bold'))
label4.grid(row=2,column=0,padx=5,pady=10)
cal=Calendar(wrapper3,selectmode='day',year=2021,month=1,day=1)
cal.grid(column=1,row=2,padx=5,pady=10)
label5=tk.Label(wrapper3,text="Time",font = ('Calibri', 12,'bold'))

min_sb = Spinbox(wrapper3,from_=0,to=23,wrap=True,textvariable=t1,width=2,state="readonly",justify=CENTER)
sec_hour = Spinbox(wrapper3,from_=0,to=59,wrap=True,textvariable=t2,width=2,justify=CENTER)
sec = Spinbox(wrapper3,from_=0,to=59,wrap=True,textvariable=t3,width=2,justify=CENTER)

min_sb.grid(column=0,row=4,pady=10)
sec_hour.grid(column=1,row=4,pady=10)
sec.grid(column=2,row=4,pady=10)

label5.grid(row=3,column=0,padx=5,pady=10)
label6=tk.Label(wrapper3,text="Completed",font = ('Calibri', 12,'bold'))
label6.grid(row=5,column=0,padx=5,pady=10)
insert_btn=tk.Button(wrapper3,text="Insert",command=insert)
update_btn=tk.Button(wrapper3,text="Update",command=update)
delete_btn=tk.Button(wrapper3,text="Delete",command=delete)
check1=tk.Checkbutton(wrapper3,text="Yes",variable=var6)
check1.grid(column=1,row=5,padx=5,pady=10)
check2=tk.Checkbutton(wrapper3,text="No",variable=var7)
check2.grid(column=2,row=5,padx=5,pady=10)
insert_btn.grid(row=6,column=0,padx=5,pady=10)
update_btn.grid(row=6,column=1,padx=5,pady=10)
delete_btn.grid(row=6,column=2,padx=5,pady=10)

query="SELECT task_id,task_name,date,time,completed FROM task"
cursor.execute(query)
rows=cursor.fetchall()
display(rows)

root.mainloop()  