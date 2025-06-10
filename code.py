import tkinter as t
import qrcode
import mysql.connector as mc
import csv
import os
from tkinter import messagebox
import re # re stands for "regular expression" module use  to name check


def selected():
        
        total=0
        selected_item=l1.curselection()# curselection gets index of selected item
        for i in selected_item:
                item_name=l1.get(i) #l1.get(i) gets the text(item name) from the listbox (l1) at position i.
                total+=items[item_name]
                
                total_label.config(text=f"Total Amount :={total}")
                global total_amount
                total_amount=total
                
def online_pay():
       
        upi="ambavalerutu-1@oksbi"
        
        Gpay_url=f"upi://pay?pa={upi}&pn=venktesh%20Hotel&am={total_amount}&cu=INR"
        PhonePay_url=f"upi://pay?pa={upi}&pn=venktesh%20Hotel&am={total_amount}"
        
        Gpay_qr=qrcode.make(Gpay_url)
        PhonePay_qr=qrcode.make(PhonePay_url)

        Gpay_qr.save('GPayHotel.png')
        PhonePay_qr.save('phonePayHotel.png')

        Gpay_qr.show()

def type_p():
     global v4
     v4=payment_var.get()
def save_info():
    global hotel_database, db

    hotel_database = mc.connect(host="localhost", user="root", password="harry123")
    print(hotel_database)

    db = hotel_database.cursor()
    db.execute("CREATE DATABASE IF NOT EXISTS Venkatesh_Hotel")
    db.execute("USE venkatesh_Hotel")
    db.execute("""
        CREATE TABLE IF NOT EXISTS hotel_info (
            Bill_No INT AUTO_INCREMENT PRIMARY KEY,
            Name VARCHAR(50),
            Contact_No varchar(20), 
            Amount INT,
            Payment_Type VARCHAR(20)
        )
    """)
def insert_d():
    v1 = e1.get()
    
    
    v3 = total_amount

    insert_q = "INSERT INTO Venkatesh_Hotel.hotel_info(Name, Contact_No, Amount, Payment_Type) VALUES (%s, %s, %s, %s)"
   
    v2 = str(e2.get())
    if len(v2) !=10 :
                    messagebox.showwarning("Warning","Please Enter correct Number")
    elif not  re.fullmatch(r'[a-zA-Z]+([a-zA-Z] +)*',v1):
                    messagebox.showwarning("Warning","Please Enter correct Name")
    else:
         db.execute(insert_q, (v1, v2, v3, v4))
         hotel_database.commit()
    
    e1.delete(0, 'end')
    e2.delete(0, 'end')


def all_d():
    save_info()
    insert_d()
            
       
root=t.Tk()
root.title("list box")
root.geometry("600x600")
root.config(bg='grey')
ll1=t.Label(root,text="Enter Customer Name :-",bg='red')
ll1.place(x=1,y=1)
e1=t.Entry(root)
e1.place(x=160,y=1)
ll2=t.Label(root,text="Enter Customer Contact No :-",bg='red')
ll2.place(x=1,y=30)
e2=t.Entry(root)
e2.place(x=160,y=30)
items={"Paneer Masala":120,"Paneer Tikka":180,"Palak Paneer":190,"Veg Maratha":200,"Kaju Paneer Masala":220,
              "Jira Rice":120,"Dal Tadka":80}

l1=t.Listbox(root,width=20,height=10,selectmode=t.MULTIPLE)
for i in items:
        l1.insert(t.END,i)
l1.place(x=1,y=50)

total_label=t.Label(root,text="Total Amount :=")
total_label.place(x=1,y=220)

b=t.Button(root,text="Calculate", width=10,height=5,command=selected)
b.place(x=1,y=350)

q=t.Button(root,text="Online Payment", width=15,height=5,command=online_pay)
q.place(x=250,y=350)

payment_var=t.StringVar()

on=t.Radiobutton(root,text=" Online", bg='red',fg='black',width=15,height=5,command=type_p,variable=payment_var,value="Online")
on.place(x=100,y=320)

of=t.Radiobutton(root,text=" Cash", bg='black',fg='red',width=15,height=5,command=type_p,variable=payment_var,value="Cash")
of.place(x=100,y=395)

s=t.Button(root,text="Save_info", width=15,height=5,command=all_d)
s.place(x=380,y=350)

root.mainloop()
