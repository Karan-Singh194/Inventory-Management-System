from tkinter import *
from employee import employee_form
from employee import connect_database
from supplier import supplier_form
from category import category_form
from product import product_form
from sales import sales_form
from tkinter import messagebox
import time
import subprocess
import sys 
import os


def update():

    cursor,connection=connect_database()
    if not cursor or not connection:
        return
    cursor.execute('use inventory_system')
    cursor.execute('SELECT * FROM employee_data')
    emp_records=cursor.fetchall()
    total_emp_count_label.config(text=len(emp_records))

    cursor.execute('use inventory_system')
    cursor.execute('SELECT * FROM supplier_data')
    supplier_records=cursor.fetchall()
    total_supplier_count_label.config(text=len(supplier_records))

    cursor.execute('use inventory_system')
    cursor.execute('SELECT * FROM category_data')
    cate_records=cursor.fetchall()
    total_category_count_label.config(text=len(cate_records))

    folder_path = r"bill/"
    txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
    # print("Number of .txt files:", len(txt_files))
    total_sales_count_label.config(text=len(txt_files))

    cursor.execute('use inventory_system')
    cursor.execute('SELECT * FROM product_data')
    pro_records=cursor.fetchall()
    total_product_count_label.config(text=len(pro_records))


    date_time=time.strftime('%B %d, %Y \t\t\t  %I:%M:%S %p on %A ')
    subtitlelabel.config(text=f"Welcome Admin {date_time}" )
    subtitlelabel.after(1000,update)


def tax_window():
    def save_tax():
        value=tax_count.get()
        cursor,connection=connect_database()
        if not cursor or not connection:
            return
        cursor.execute('use inventory_system')
        cursor.execute('CREATE TABLE IF NOT EXISTS tax_table (id INT primary key,tax DECIMAL(5,2))')
        cursor.execute('SELECT id from tax_table WHERE id=1')
        if cursor.fetchone():
            cursor.execute('UPDATE tax_table SET tax=%s WHERE id=1', value)
        else :
            cursor.execute('INSERT INTO tax_table (id,tax) VALUES(1,%s)', value)
        connection.commit()
        messagebox.showinfo('Success', f'Tax is set to {value}% and saved successfully.', parent=tax_root)
    tax_root=Toplevel()
    tax_root.title('Tax window')
    tax_root.geometry('300x200')
    tax_root.grab_set()
    tax_percentage=Label(tax_root,text="Enter Tax Percentage(%)",font=('arial', 12))
    tax_percentage.pack(pady=10)
    tax_count=Spinbox(tax_root,from_=0, to=100, font=('arial', 12))
    tax_count.pack(pady=10)
    save_button= Button(tax_root,text='Save',font=('arial', 12,'bold'),bg='#4d636d', fg='white', width=10,cursor='hand2',
                        command=save_tax)
    save_button.pack(pady=20)

current_frame=None
def show_form(form_function):
    global current_frame
    if current_frame:
        current_frame.place_forget()
    current_frame=form_function(window)


#GUI PART

window= Tk()

window.title("Dashboard")
window.geometry("1350x768+0+0")
window.resizable(0,0)
window.config(bg="white")


def logout():
    subprocess.Popen([sys.executable, "login.py"])
    window.destroy() 


bg_image=PhotoImage(file="inventory.png")
titleLabel=Label(window,image=bg_image,compound=LEFT,text=" Inventory Management System ",font=("times new roman", 30, "bold"),bg="#010c48",fg="white")
titleLabel.place(x=0,y=0,relwidth=1)


subtitlelabel=Label(window,text=f"Date : 10-02-2025\t\t Time : 08:20:30  PM ", 
                     font=("times new roman", 11, "bold"),bg="#4d636d",fg="white")
subtitlelabel.place(x=0,y=70, relwidth=1)


logoutButton=Button(window, text="Logout",cursor="hand2", font=("times new roman", 16, "bold"),bg="red",fg="white",
                    command=lambda :logout())
logoutButton.place(x=1150,y=14)


leftframe=Frame(window)
leftframe.place(x=0,y=91, width=200, height=540)

inventory_boy=PhotoImage(file="inventory_boy.png")
imagelabel=Label(leftframe,image=inventory_boy)
imagelabel.pack()

manulabel=Label(leftframe,text="Menu",font=("times new roman", 20, "bold"),bg="#009688",fg="white")
manulabel.pack(fill=X)

employee_icon=PhotoImage(file="employee.png")
employee_Button=Button(leftframe,image=employee_icon,compound=LEFT,text=" Employees",cursor="hand2",
                        font=("times new Roman", 20, 'bold'),anchor=W,padx=10,command=lambda :show_form(employee_form))
employee_Button.pack(fill=X)

Supplier_icon=PhotoImage(file="Supplier.png")
Supplier_Button=Button(leftframe,image=Supplier_icon,compound=LEFT,text=" Suppliers",cursor="hand2",
                        font=("times new Roman", 20, 'bold'),anchor=W,padx=10, command=lambda: show_form(supplier_form))
Supplier_Button.pack(fill=X)

Category_icon=PhotoImage(file="Category.png")
Category_Button=Button(leftframe,image=Category_icon,compound=LEFT,text=" Categorys",cursor="hand2",
                        font=("times new Roman", 20, 'bold'),anchor=W,padx=10,command=lambda: show_form(category_form))
Category_Button.pack(fill=X)

Product_icon=PhotoImage(file="Product.png")
Product_Button=Button(leftframe,image=Product_icon,compound=LEFT,text=" Products",cursor="hand2",
                       font=("times new Roman", 20, 'bold'),anchor=W,padx=10,command=lambda: show_form(product_form))
Product_Button.pack(fill=X)

sales_icon=PhotoImage(file="Sales.png")
sales_Button=Button(leftframe,image=sales_icon,compound=LEFT,text=" Sales",cursor="hand2",
                     font=("times new Roman", 20, 'bold'),anchor=W,padx=10,command=lambda: show_form(sales_form))
sales_Button.pack(fill=X)

tax_icon=PhotoImage(file="Sales.png")
tax_Button=Button(leftframe,image=tax_icon,compound=LEFT,text=" Tax",cursor="hand2",
                     font=("times new Roman", 20, 'bold'),anchor=W,padx=10,command=lambda: tax_window())
tax_Button.pack(fill=X)

exit_icon=PhotoImage(file="exit.png")
exit_Button=Button(leftframe,image=exit_icon,compound=LEFT,text=" Exit",cursor="hand2", 
                   font=("times new Roman", 20, 'bold'),anchor=W,padx=10,command=lambda: exit(window))
exit_Button.pack(fill=X)


emp_frame=Frame(window, bg="#2C3E50", bd=3, relief=RIDGE)
emp_frame.place(x=400, y=105, height=170, width=280)
total_emp_icon=PhotoImage(file="total_emp.png")
total_emp_icon_label=Label(emp_frame,image=total_emp_icon, bg="#2C3E50")
total_emp_icon_label.pack(pady=10)

total_emp_label=Label(emp_frame, text= "Total Employees",font=("times new Roman", 15, 'bold'), bg="#2C3E50", fg="white")
total_emp_label.pack()

total_emp_count_label=Label(emp_frame, text= "0",font=("times new Roman", 30, 'bold'), bg="#2C3E50", fg="white")
total_emp_count_label.pack()



category_frame=Frame(window, bg="#2C3E50", bd=3, relief=RIDGE)
category_frame.place(x=800, y=105, height=170, width=280)
total_category_icon=PhotoImage(file="total_category.png")
total_category_icon_label=Label(category_frame,image=total_category_icon, bg="#2C3E50")
total_category_icon_label.pack(pady=10)

total_category_label=Label(category_frame, text= "Total Category",font=("times new Roman", 15, 'bold'), bg="#2C3E50", fg="white")
total_category_label.pack()

total_category_count_label=Label(category_frame, text= "0",font=("times new Roman", 30, 'bold'), bg="#2C3E50", fg="white")
total_category_count_label.pack()



supplier_frame=Frame(window, bg="#2C3E50", bd=3, relief=RIDGE)
supplier_frame.place(x=400, y=300, height=170, width=280)

total_supplier_icon=PhotoImage(file="total_suppliers.png")
total_supplier_icon_label=Label(supplier_frame,image=total_supplier_icon, bg="#2C3E50")
total_supplier_icon_label.pack(pady=10)

total_supplier_label=Label(supplier_frame, text= "Total Supplier",font=("times new Roman", 15, 'bold'), bg="#2C3E50", fg="white")
total_supplier_label.pack()

total_supplier_count_label=Label(supplier_frame, text= "0",font=("times new Roman", 30, 'bold'), bg="#2C3E50", fg="white")
total_supplier_count_label.pack()



product_frame=Frame(window, bg="#2C3E50", bd=3, relief=RIDGE)
product_frame.place(x=800, y=300, height=170, width=280)
total_product_icon=PhotoImage(file="total_product.png")
total_product_icon_label=Label(product_frame,image=total_product_icon, bg="#2C3E50")
total_product_icon_label.pack(pady=10)

total_product_label=Label(product_frame, text= "Total Product",font=("times new Roman", 15, 'bold'), bg="#2C3E50", fg="white")
total_product_label.pack()

total_product_count_label=Label(product_frame, text= "0",font=("times new Roman", 30, 'bold'), bg="#2C3E50", fg="white")
total_product_count_label.pack()



sales_frame=Frame(window, bg="#2C3E50", bd=3, relief=RIDGE)
sales_frame.place(x=590, y=490, height=170, width=280)
total_sales_icon=PhotoImage(file="total_sales.png")
total_sales_icon_label=Label(sales_frame,image=total_sales_icon, bg="#2C3E50")
total_sales_icon_label.pack(pady=10)

total_sales_label=Label(sales_frame, text= "Total Sales",font=("times new Roman", 15, 'bold'), bg="#2C3E50", fg="white")
total_sales_label.pack()

total_sales_count_label=Label(sales_frame, text= "0",font=("times new Roman", 30, 'bold'), bg="#2C3E50", fg="white")
total_sales_count_label.pack()

update()


window.mainloop()