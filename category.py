from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from employee import connect_database

def select_data(event,invoice_entry,name_entry,description_text,treeview):
    
    index=treeview.selection()
    content=treeview.item(index)
    actual_contant=content['values']
    
    invoice_entry.delete(0,END)
    name_entry.delete(0,END)
    description_text.delete(1.0,END)

    invoice_entry.insert(0,actual_contant[0])
    name_entry.insert(0,actual_contant[1])
    description_text.insert(1.0,actual_contant[2])

def delete_category(treeview,id_entry,category_name_entry,description_text):
    index = treeview.selection()
    content=treeview.item(index)
    row=content['values']
    id=row[0]
    if not index:
        messagebox.showerror('Error','No row is selected')
        return
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('use inventory_system')
        cursor.execute('DELETE FROM category_data WHERE id=%s', id)
        connection.commit()
        treeview_data(treeview)
        clear(id_entry,category_name_entry,description_text)
        messagebox.showinfo('info','Record is deleted')
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally :
        cursor.close()
        connection.close()

def clear(id_entry,category_name_entry,description_text):
    id_entry.delete(0,END)
    category_name_entry.delete(0,END)
    description_text.delete(1.0,END)

def treeview_data(treeview):
    cursor,connection=connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('use inventory_system')
        cursor.execute('SELECT * FROM category_data')
        records=cursor.fetchall()
        treeview.delete(*treeview.get_children())
        for record in records:
            treeview.insert('',END,values=record)
    except Exception as e:
        messagebox.showerror('Error', f'error due to {e}')
    finally :
        cursor.close()
        connection.close()

def add_category(id,name,description,treeview,id_entry,category_name_entry,description_text):
    if id=='' or name=='' or description=='':
        messagebox.showerror('Error','All fields are required')
        return
    else:
        cursor,connection=connect_database()
        if not cursor or not connection:
            return
    try:
        cursor.execute('use inventory_system')
        cursor.execute('CREATE TABLE IF NOT EXISTS category_data (id INT PRIMARY KEY,name VARCHAR(100),description TEXT)')

        cursor.execute('SELECT * from category_data WHERE id=%s', (id))
        if cursor.fetchone():
            messagebox.showerror('Error', 'id already exists')
            return
        cursor.execute('INSERT INTO category_data VALUES (%s,%s,%s)',(id,name,description))
        connection.commit()
        clear(id_entry,category_name_entry,description_text)
        messagebox.showinfo('info','Data is inserted')
        treeview_data(treeview)

    except Exception as e:
        messagebox.showerror('Error', f'error due to {e}')
    finally :
        cursor.close()
        connection.close()
    


def category_form(window):
    global logo
    category_frame = Frame(width=1150, height=668)
    category_frame.place(x=200, y = 91)
    headinglabel=Label(category_frame, text="Manage Category Detail ", font=("roman new times", 16, "bold",), bg="#0f4d7d", fg="white")
    headinglabel.place(x=0,y=0,relwidth=1)


    back_button=Button(category_frame,text="back",font=("roman new times",10,'bold'),cursor="hand2",
                       command=lambda: category_frame.place_forget())
    back_button.place(x=2,y=31)


    logo=PhotoImage(file='data-structure.png')
    logo_label=Label(category_frame,image=logo,bg='white')
    logo_label.place(x=30,y=90)

    detail_frame=Frame(category_frame,bg='white')
    detail_frame.place(x=500,y=60)

    id_label=Label(detail_frame,text='Id',font=('roman new time',14),bg='white')
    id_label.grid(row=0,column=0,padx=20,sticky='w')
    id_entry=Entry(detail_frame,font=('roman new time',14),bg='lightyellow')
    id_entry.grid(row=0,column=1)

    caregory_name_label=Label(detail_frame,text='Category Name',font=('roman new time',14),bg='white')
    caregory_name_label.grid(row=1,column=0,padx=(20,40),sticky='w')
    category_name_entry=Entry(detail_frame,font=('roman new time',14),bg='lightyellow')
    category_name_entry.grid(row=1,column=1,pady=20)

    description_label=Label(detail_frame,text='Description',font=('roman new time',14),bg='white')
    description_label.grid(row=2,column=0,padx=20,sticky='nw')

    description_text=Text(detail_frame,font=('roman new time',14),bg='lightyellow',width=20,height=6,bd=2)
    description_text.grid(row=2,column=1)

    button_frame=Frame(category_frame,bg='white')
    button_frame.place(x=680,y=307)

    add_button=Button(button_frame,text="ADD",font=("roman new times",14), bg="#0f4d7d", fg="white",width=6, cursor="hand2",
                      command=lambda:add_category(id_entry.get(),category_name_entry.get(),description_text.get(1.0,END).strip(),treeview,
                                                  id_entry,category_name_entry,description_text))
    add_button.grid(row=0,column=0,padx=20)

    delete_button=Button(button_frame,text="Delete",font=("roman new times",14), bg="#0f4d7d", fg="white",width=6, cursor="hand2",
                         command=lambda:delete_category(treeview,id_entry,category_name_entry,description_text))
    delete_button.grid(row=0,column=1,padx=20)

    clear_button=Button(button_frame,text="Clear",font=("roman new times",14), bg="#0f4d7d", fg="white",width=6, cursor="hand2",
                        command=lambda:clear(id_entry,category_name_entry,description_text))
    clear_button.grid(row=0,column=2,padx=20)


    treeview_frame=Frame(category_frame,bg='white')
    treeview_frame.place(x=530,y=360,height=200,width=500)

    scrolly=Scrollbar(treeview_frame,orient=VERTICAL)
    scrollx=Scrollbar(treeview_frame,orient=HORIZONTAL)

    treeview=ttk.Treeview(treeview_frame,columns=('id', 'name', 'description'),show='headings',
                          yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
    
    scrolly.pack(side=RIGHT,fill=Y)
    scrollx.pack(side=BOTTOM,fill=X)

    scrolly.config(command=treeview.yview)
    scrollx.config(command=treeview.xview)

    treeview.pack(fill=BOTH,expand=1)

    treeview.heading('id', text='ID')
    treeview.heading('name', text='Category Name')
    treeview.heading('description', text='Description')

    treeview.column('id', width=80)
    treeview.column('name', width=140)
    treeview.column('description', width=300)
    treeview_data(treeview)
    treeview.bind('<ButtonRelease-1>',lambda event:select_data(event,id_entry,category_name_entry,description_text,treeview))
    return category_frame