from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import messagebox
import pandas as pd
import pymysql
from sqlalchemy import create_engine

def download_employee_data():
    cursor, connection = connect_database()
    
    if not cursor or not connection:
        return  

    try:

        cursor.execute("USE inventory_system")

        db_url = "mysql+pymysql://root:1234@localhost/inventory_system"
        engine = create_engine(db_url)

        query = "SELECT * FROM employee_data"
        df = pd.read_sql(query, con=engine)  

        excel_file = "employee_data.xlsx"
        df.to_excel(excel_file, index=False)

        messagebox.showinfo("Success", f"Employee data downloaded successfully as {excel_file}!")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

    finally:
        cursor.close()
        connection.close()



def connect_database():
    try:
        connection=pymysql.connect(host="localhost", user="root", password="1234")
        cursor = connection.cursor()
    except:
        messagebox.showerror('Error', 'Database connectivity issue , open mysql command line client')
        return None, None

    return cursor,connection

def create_database_table():
    cursor,connection=connect_database()
    cursor.execute("CREATE DATABASE IF NOT EXISTS inventory_system")
    cursor.execute("USE inventory_system")
    cursor.execute("CREATE Table IF NOT EXISTS employee_data (empid INT PRIMARY KEY, name VARCHAR(100), email VARCHAR(100), "
                   "gender  VARCHAR(50), dob  VARCHAR(30), contact  VARCHAR(30), employment_type  VARCHAR(50),education VARCHAR(50),"
                   " work_shift  VARCHAR(50),address  VARCHAR(100), doj  VARCHAR(50), salary  VARCHAR(50), user_type  VARCHAR(50),"
                    " password  VARCHAR(50))" )


connect_database()

def treeview_data():
    cursor,connection=connect_database()
    if not cursor or not connection:
        return
    cursor.execute('use inventory_system')
    
    try:
        cursor.execute('SELECT * FROM employee_data')
        employee_record=cursor.fetchall()
        employee_treeview.delete(*employee_treeview.get_children())
        for record in employee_record:
            employee_treeview.insert('',END,values=record)
    except Exception as e:
        messagebox.showerror('Error', f'error due to {e}')
    finally :
        cursor.close()
        connection.close()
        

def select_data(event,empid_entry,name_entry,email_entry,gender_combobox,dob_date_entry,contact_entry,employment_type_combobox,
                education_combobox,work_shift_combobox,address_text,doj_date_entry,salary_entry,usertype_combobox,password_entry):
    
    index=employee_treeview.selection()
    content=employee_treeview.item(index)
    row=content['values']
    clear_fields(empid_entry,name_entry,email_entry,gender_combobox,dob_date_entry,contact_entry,employment_type_combobox,
                education_combobox,work_shift_combobox,address_text,doj_date_entry,salary_entry,usertype_combobox,password_entry,False)
    
    empid_entry.insert(0,row[0])
    name_entry.insert(0,row[1])
    email_entry.insert(0,row[2])
    gender_combobox.set(row[3])
    dob_date_entry.set_date(row[4])
    contact_entry.insert(0,row[5])
    employment_type_combobox.set(row[6])
    education_combobox.set(row[7])
    work_shift_combobox.set(row[8])
    address_text.insert(1.0,row[9])
    doj_date_entry.set_date(row[10])
    salary_entry.insert(0,row[11])
    usertype_combobox.set(row[12])
    password_entry.insert(0,row[13])


def add_employee(empid,name,email,gender,dob,contact,employment_type,education,work_shift,address,doj,salary,user_type,password,
                 empid_entry,name_entry,email_entry,gender_combobox,dob_date_entry,contact_entry,
                        employment_type_combobox,education_combobox,work_shift_combobox,address_text,doj_date_entry,salary_entry,
                        usertype_combobox,password_entry):
    if (empid=='' or name=='' or email=='' or gender=='SELECT'or contact=='' or employment_type=='SELECT' or education=='SELECT' or work_shift=='SELECT' or 
        address=='\n' or salary=='' or user_type=='SELECT' or password==''):
        messagebox.showerror('Error', 'all fields are required')
        return
    else :
        cursor,connection=connect_database()
        if not cursor or not connection:
            return
        cursor.execute('use inventory_system')
        try:
            cursor.execute('SELECT empid from employee_data WHERE empid=%s', (empid))
            if cursor.fetchone():
                messagebox.showerror('Error', 'id already exists')
                return
            address=address.strip()
            cursor.execute('INSERT INTO employee_data VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                        (empid,name,email,gender,dob,contact,employment_type,education,work_shift,address,doj,salary,user_type,password))
            connection.commit()
            treeview_data()
            clear_fields(empid_entry,name_entry,email_entry,gender_combobox,dob_date_entry,contact_entry,
                        employment_type_combobox,education_combobox,work_shift_combobox,address_text,doj_date_entry,salary_entry,
                        usertype_combobox,password_entry,True)
            messagebox.showinfo('Success', 'data is inserted successfully')

        except Exception as e:
            messagebox.showerror('Error', f'error due to {e}')

        finally :
            cursor.close()
            connection.close()
            

def clear_fields(empid_entry,name_entry,email_entry,gender_combobox,dob_date_entry,contact_entry,
                employment_type_combobox,education_combobox,work_shift_combobox,address_text
                ,doj_date_entry,salary_entry,usertype_combobox,password_entry,check):
    empid_entry.delete(0,END)
    name_entry.delete(0,END)
    email_entry.delete(0,END)
    gender_combobox.set('SELECT')
    from datetime import date
    dob_date_entry.set_date(date.today())
    contact_entry.delete(0,END)
    employment_type_combobox.set('SELECT')
    education_combobox.set('SELECT')
    work_shift_combobox.set('SELECT')
    address_text.delete(1.0,END)
    from datetime import date
    doj_date_entry.set_date(date.today())
    salary_entry.delete(0,END)
    usertype_combobox.set('SELECT')
    password_entry.delete(0,END)
    if check:    
        employee_treeview.selection_remove(employee_treeview.selection())


def update_employee(empid,name,email,gender,dob,contact,employment_type,education,work_shift,address,doj,salary,user_type,password,
                    empid_entry,name_entry,email_entry,gender_combobox,dob_date_entry,contact_entry,
                        employment_type_combobox,education_combobox,work_shift_combobox,address_text,doj_date_entry,salary_entry,
                        usertype_combobox,password_entry):
    selected=employee_treeview.selection()
    if not selected:
        messagebox.showerror('Error', 'No row is selected')
    else:
        cursor,connection=connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('use inventory_system')
            cursor.execute('Select * from employee_data WHERE empid=%s', (empid,))
            current_data=cursor.fetchone()
            current_data=current_data[1:]
        
            address=address.strip()

            new_data=(name,email,gender,dob,contact,employment_type,education,work_shift,address,doj,salary,user_type,password)
            
            if current_data==new_data:
                messagebox.showinfo('information', 'No changes detected')
                return
            cursor.execute('UPDATE employee_data SET name=%s,email=%s,gender=%s,dob=%s,contact=%s,employment_type=%s,education=%s,'
                            'work_shift=%s,address=%s,doj=%s,salary=%s,user_type=%s,password=%s WHERE empid=%s',
                            (name,email,gender,dob,contact,employment_type,education,work_shift,address,doj,salary,user_type,password,empid,))
            connection.commit()
            treeview_data()
            clear_fields(empid_entry,name_entry,email_entry,gender_combobox,dob_date_entry,contact_entry,
                        employment_type_combobox,education_combobox,work_shift_combobox,address_text,doj_date_entry,salary_entry,
                        usertype_combobox,password_entry,True)
            messagebox.showinfo('Success', 'Data is update Successfully')

        except Exception as e:
            messagebox.showerror('Error', f'error due to {e}')
        finally :
            cursor.close()
            connection.close()


def delete_employee(empid,empid_entry,name_entry,email_entry,gender_combobox,dob_date_entry,contact_entry,
                        employment_type_combobox,education_combobox,work_shift_combobox,address_text,doj_date_entry,salary_entry,
                        usertype_combobox,password_entry):
    selected=employee_treeview.selection()
    if not selected:
        messagebox.showerror('Error', 'No row is selected')
    else:
        result=messagebox.askyesno("Confirm", 'Do you really want to delete the record')
        if result:
            cursor,connection=connect_database()
            if not cursor or not connection:
                return
            try:
                cursor.execute('use inventory_system')
                cursor.execute('DELETE FROM employee_data where empid=%s', (empid,))
                connection.commit()
                treeview_data()
                clear_fields(empid_entry,name_entry,email_entry,gender_combobox,dob_date_entry,contact_entry,
                        employment_type_combobox,education_combobox,work_shift_combobox,address_text,doj_date_entry,salary_entry,
                        usertype_combobox,password_entry,True)
                messagebox.showinfo('Success', 'Record is deleted')
            except Exception as e:
                messagebox.showerror('Error', f'error due to {e}')

            finally :
                cursor.close()
                connection.close()


def serach_employee(search_option,value):
    if search_option=='Search By':
        messagebox.showerror('Error', 'No option is selected')
    elif value=='':
        messagebox.showerror('Error', 'Enter the value of search')
    else:
        search_option=search_option.replace(' ','_')
        cursor,connection=connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('use inventory_system')
            cursor.execute(f'SELECT * FROM employee_data  WHERE {search_option} LIKE %s', f'%{value}%')
            records=cursor.fetchall()
            employee_treeview.delete(*employee_treeview.get_children())
            for record in records:
                employee_treeview.insert('',END,value=record)
        except Exception as e:
            messagebox.showerror('Error', f'error due to {e}')

        finally :
            cursor.close()
            connection.close()
        
def show_all(search_entry,search_combobox):
    treeview_data()
    search_entry.delete(0,END)
    search_combobox.set('Search By')

            


def employee_form(window):
    global employee_treeview

    employee_frame = Frame(width=1150, height=668)
    employee_frame.place(x=200, y = 91)
    headinglabel=Label(employee_frame, text="Manage Employee Detail ", font=("roman new times", 16, "bold",), bg="#0f4d7d", fg="white")
    headinglabel.place(x=0,y=0,relwidth=1)

    top_frame=Frame(employee_frame,bg="white")
    top_frame.place(x=0,y=35,relwidth=1,height=235)
    search_frame=Frame(top_frame,bg="white")
    search_frame.pack()

    back_button=Button(top_frame,text="back",font=("roman new times",10,"bold"),cursor="hand2",command=lambda: employee_frame.place_forget())
    back_button.place(x=2,y=2)

    search_combobox=ttk.Combobox(search_frame,values=('Empid', 'NAME', 'EMAIL', 'Employment type', 'Education', 'Work shif'),font=("roman new times",12),state="readonly",cursor="hand2")
    search_combobox.set("Search By")
    search_combobox.grid(row=0,column=0,padx=20)

    serach_entry=Entry(search_frame,font=("roman new times",12), bg="lightyellow",cursor="hand2")
    serach_entry.grid(row=0, column=1,padx=20)
    
    search_button=Button(search_frame,text="Search",font=("roman new times",10,"bold"), bg="#0f4d7d", fg="white",width=10,cursor="hand2",
                         command=lambda: serach_employee(search_combobox.get(),serach_entry.get()))
    search_button.grid(row=0,column=2,padx=20)

    show_button=Button(search_frame,text="Show All",font=("roman new times",10,"bold"), bg="#0f4d7d", fg="white",width=10,cursor="hand2",
                       command=lambda:show_all(serach_entry,search_combobox))
    show_button.grid(row=0,column=3)

    horizontal_scrollbar=Scrollbar(top_frame,orient=HORIZONTAL)
    vertical_scrollbar=Scrollbar(top_frame,orient=VERTICAL)
    employee_treeview=ttk.Treeview(top_frame, columns=('empid','name', 'email','gender','dob','contact','employment_type','education',
                                                        'work_shift', 'address','doj','salary','user_type'),show='headings'
    ,yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
    

    horizontal_scrollbar.pack(side=BOTTOM,fill=X)
    vertical_scrollbar.pack(side=RIGHT,fill=Y,pady=(10,0))
    horizontal_scrollbar.config(command=employee_treeview.xview)
    vertical_scrollbar.config(command=employee_treeview.yview)
    employee_treeview.pack(pady=(10,0))

    employee_treeview.heading('empid', text='Empid')
    employee_treeview.heading('name', text='NAME')
    employee_treeview.heading('email', text='EMAIL')
    employee_treeview.heading('gender', text='GENDER')
    employee_treeview.heading('dob', text='DOB')
    employee_treeview.heading('contact', text='CONTACT')
    employee_treeview.heading('employment_type', text='EMPLOYMENT_TYPE')
    employee_treeview.heading('education', text='EDUCATION')
    employee_treeview.heading('work_shift', text='WORK_SHIFT')
    employee_treeview.heading('address', text='ADDRESS')
    employee_treeview.heading('doj', text='DATE OF JOINING')
    employee_treeview.heading('salary', text='SALARY')
    employee_treeview.heading('user_type', text='USER_TYPE')

    employee_treeview.column('empid', width='60')
    employee_treeview.column('name', width='140')
    employee_treeview.column('email', width='180')
    employee_treeview.column('gender', width='80')
    employee_treeview.column('dob', width='100')
    employee_treeview.column('contact', width='100')
    employee_treeview.column('employment_type', width='120')
    employee_treeview.column('education', width='120')
    employee_treeview.column('work_shift', width='100')
    employee_treeview.column('address', width='200')
    employee_treeview.column('doj', width='110')
    employee_treeview.column('salary', width='140')
    employee_treeview.column('user_type', width='120')

    treeview_data()


    detail_frame=Frame(employee_frame)
    detail_frame.place(x=10, y=280)

    empid_label=Label(detail_frame, text='EmpId',font=("roman new times",12))
    empid_label.grid(row=0,column=0,pady=20,padx=10, sticky='w')
    empid_entry=Entry(detail_frame,font=("roman new times",12), bg="lightyellow",cursor="hand2")
    empid_entry.grid(row=0, column=1,padx=20)

    name_label=Label(detail_frame, text='Name',font=("roman new times",12))
    name_label.grid(row=0,column=2,pady=20,padx=10, sticky='w')
    name_entry=Entry(detail_frame,font=("roman new times",12), bg="lightyellow",cursor="hand2")
    name_entry.grid(row=0, column=3,padx=20)

    email_label=Label(detail_frame, text='Email',font=("roman new times",12))
    email_label.grid(row=0,column=4,pady=20,padx=10, sticky='w')
    email_entry=Entry(detail_frame,font=("roman new times",12), bg="lightyellow",cursor="hand2")
    email_entry.grid(row=0, column=5,padx=20)


    gender_label=Label(detail_frame, text='Gender',font=("roman new times",12))
    gender_label.grid(row=1,column=0,pady=20,padx=10, sticky='w')
    gender_combobox=ttk.Combobox(detail_frame,values=('MALE', 'FEMALE', 'OTHER'),font=("roman new times",12),state="readonly",cursor="hand2")
    gender_combobox.set("SELECT")
    gender_combobox.grid(row=1,column=1,padx=20)

    dob_label=Label(detail_frame, text='DATE OF BIRTH',font=("roman new times",12))
    dob_label.grid(row=1,column=2,pady=20,padx=10, sticky='w')
    dob_date_entry=DateEntry(detail_frame,width=18,font=("roman new times",12),state="readonly",date_pattern='dd/mm/yyyy')
    dob_date_entry.grid(row=1,column=3)

    contact_label=Label(detail_frame, text='CONTACT',font=("roman new times",12))
    contact_label.grid(row=1,column=4,pady=20,padx=10, sticky='w')
    contact_entry=Entry(detail_frame,font=("roman new times",12), bg="lightyellow",cursor="hand2")
    contact_entry.grid(row=1, column=5,padx=20)


    employment_type_label=Label(detail_frame, text='Employment Type',font=("roman new times",12))
    employment_type_label.grid(row=2,column=0,pady=20,padx=10, sticky='w')
    employment_type_combobox=ttk.Combobox(detail_frame,values=('Full Time', 'Part Time','Casual', 'Contract','Intern'),font=("roman new times",12),state="readonly",cursor="hand2")
    employment_type_combobox.set("SELECT")
    employment_type_combobox.grid(row=2,column=1,padx=20)


    education_label=Label(detail_frame, text='Education',font=("roman new times",12))
    education_label.grid(row=2,column=2,pady=10,padx=10,sticky='w')
    education_combobox=ttk.Combobox(detail_frame,values=('B-Tech', 'M-Tech', 'B.Com','M.Com'),font=("roman new times",12),state="readonly",cursor="hand2")
    education_combobox.set("SELECT")
    education_combobox.grid(row=2,column=3,padx=20)


    work_shift_label=Label(detail_frame, text='Work Shift',font=("roman new times",12))
    work_shift_label.grid(row=2,column=4,pady=10,padx=10,sticky='w')
    work_shift_combobox=ttk.Combobox(detail_frame,values=('Morning', 'Afternoon', 'Evening','Night'),font=("roman new times",12),state="readonly",cursor="hand2")
    work_shift_combobox.set("SELECT")
    work_shift_combobox.grid(row=2,column=5,padx=20)

    address_label=Label(detail_frame, text='Address',font=("roman new times",12))
    address_label.grid(row=3,column=0,pady=20,padx=10, sticky='w')
    address_text=Text(detail_frame,width=20,height=3,font=("roman new times",12), bg="lightyellow",cursor="hand2")
    address_text.grid(row=3, column=1,padx=20)

    doj_label=Label(detail_frame, text='DATE OF Joining',font=("roman new times",12))
    doj_label.grid(row=3,column=2,pady=20,padx=10, sticky='w')
    doj_date_entry=DateEntry(detail_frame,width=18,font=("roman new times",12),state="readonly",date_pattern='dd/mm/yyyy')
    doj_date_entry.grid(row=3,column=3)

    salary_label=Label(detail_frame, text='Salary',font=("roman new times",12))
    salary_label.grid(row=3,column=4,pady=20,padx=10, sticky='w')
    salary_entry=Entry(detail_frame,font=("roman new times",12), bg="lightyellow",cursor="hand2")
    salary_entry.grid(row=3, column=5,padx=20)

    usertype_label=Label(detail_frame, text='USER TYPE',font=("roman new times",12))
    usertype_label.grid(row=4,column=2,pady=10,padx=10,sticky='w')
    usertype_combobox=ttk.Combobox(detail_frame,values=('Employee', 'Admin'),font=("roman new times",12),state="readonly",cursor="hand2")
    usertype_combobox.set("SELECT")
    usertype_combobox.grid(row=4,column=3,padx=20)
    
    password_label=Label(detail_frame, text='Password',font=("roman new times",12))
    password_label.grid(row=4,column=4,pady=20,padx=10, sticky='w')
    password_entry=Entry(detail_frame,font=("roman new times",12), bg="lightyellow",cursor="hand2")
    password_entry.grid(row=4, column=5,padx=20)


    button_frame=Frame(employee_frame)
    button_frame.place(x=250, y=610)

    add_button=Button(button_frame,text="ADD",font=("roman new times",10,"bold"), bg="#0f4d7d", fg="white",width=10, cursor="hand2", 
                        command=lambda: add_employee(empid_entry.get(),name_entry.get(),email_entry.get(),gender_combobox.get(),dob_date_entry.get(),contact_entry.get(),
                        employment_type_combobox.get(),education_combobox.get(),work_shift_combobox.get(),address_text.get(1.0,END)
                        ,doj_date_entry.get(),salary_entry.get(),usertype_combobox.get(),password_entry.get(),
                        empid_entry,name_entry,email_entry,gender_combobox,dob_date_entry,contact_entry,
                        employment_type_combobox,education_combobox,work_shift_combobox,address_text,doj_date_entry,salary_entry,
                        usertype_combobox,password_entry
                        ))
    
    add_button.grid(row=0,column=0,padx=20)


    update_button=Button(button_frame,text="UPDATE",font=("roman new times",10,"bold"), bg="#0f4d7d", fg="white",width=10,cursor="hand2",
                         command=lambda: update_employee(empid_entry.get(),name_entry.get(),email_entry.get(),gender_combobox.get(),dob_date_entry.get(),contact_entry.get(),
                        employment_type_combobox.get(),education_combobox.get(),work_shift_combobox.get(),address_text.get(1.0,END)
                        ,doj_date_entry.get(),salary_entry.get(),usertype_combobox.get(),password_entry.get(),
                        empid_entry,name_entry,email_entry,gender_combobox,dob_date_entry,contact_entry,
                        employment_type_combobox,education_combobox,work_shift_combobox,address_text,doj_date_entry,salary_entry,
                        usertype_combobox,password_entry))
    
    update_button.grid(row=0,column=1,padx=20)


    delete_button=Button(button_frame,text="Delete",font=("roman new times",10,"bold"), bg="#0f4d7d", fg="white",width=10,cursor="hand2",
                         command=lambda: delete_employee(empid_entry.get(),empid_entry,name_entry,email_entry,gender_combobox,dob_date_entry,contact_entry,
                        employment_type_combobox,education_combobox,work_shift_combobox,address_text,doj_date_entry,salary_entry,
                        usertype_combobox,password_entry))
    delete_button.grid(row=0,column=2,padx=20)

    clear_button=Button(button_frame,text="Clear",font=("roman new times",10,"bold"), bg="#0f4d7d", fg="white",width=10,cursor="hand2",
                        command=lambda: clear_fields(empid_entry,name_entry,email_entry,gender_combobox,dob_date_entry,contact_entry,
                        employment_type_combobox,education_combobox,work_shift_combobox,address_text,doj_date_entry,salary_entry,
                        usertype_combobox,password_entry,True))
    
    clear_button.grid(row=0,column=3,padx=20)

    download_button = Button(button_frame, text="Download",font=("roman new times",10,"bold"), bg="#0f4d7d", fg="white",width=10,cursor="hand2",
                              command=lambda:download_employee_data())
    download_button.grid(row=0,column=4,padx=20)


    employee_treeview.bind('<ButtonRelease-1>',lambda event:select_data(event,empid_entry,name_entry,email_entry,gender_combobox,dob_date_entry,contact_entry,employment_type_combobox,
                        education_combobox,work_shift_combobox,address_text,doj_date_entry,salary_entry,usertype_combobox,password_entry))
    create_database_table()
    return employee_frame