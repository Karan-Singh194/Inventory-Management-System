from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import messagebox
from employee import connect_database


def show_all(treeview,search_entey,search_combobox):
    treeview_data(treeview)
    search_combobox.set('Search By')
    search_entey.delete(0,END)

def search_product(search_combobox,search_entry,treeview):
    if search_combobox.get()=='Search By':
        messagebox.showwarning('Warning','Please select an option')
    elif search_entry.get()=='':
        messagebox.showwarning('Warning','Please enter the value to search')
    else:
        cursor,connection=connect_database()
        if not cursor or not connection:
            return
        cursor.execute('use inventory_system')
        cursor.execute(f'SELECT * FROM product_data WHERE {search_combobox.get()}=%s',search_entry.get())
        records=cursor.fetchall()
        if len(records)==0:
            messagebox.showerror('Error','No records found')
            return
        treeview.delete(*treeview.get_children())
        for record in records:
            treeview.insert('',END,values=record)


def clear(category_combobox,supplier_combobox,name_entry, price_entry, quantity_entry, status_combobox,treeview,discount_spinbox):
    treeview.selection_remove(treeview.selection())
    category_combobox.set("Select")
    supplier_combobox.set("Select")
    name_entry.delete(0,END)
    price_entry.delete(0,END)
    quantity_entry.delete(0,END)
    status_combobox.set("Select Status")
    discount_spinbox.delete(0,END)
    discount_spinbox.insert(0,0)

def delete_product(treeview,category_combobox,supplier_combobox,name_entry, price_entry, quantity_entry, status_combobox,discount_spinbox):
    index=treeview.selection()

    if not index:
        messagebox.showerror('Error','no row selected')
        return
    
    dict=treeview.item(index)
    content=dict['values']
    id=content[0]

    ans=messagebox.askyesno('Confirm','Do you really want to delete?')
    if ans:
        cursor,connection=connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('use inventory_system')
            cursor.execute('DELETE FROM product_data WHERE id=%s ', id)
            connection.commit()
            treeview_data(treeview)
            clear(category_combobox,supplier_combobox,name_entry, price_entry, quantity_entry, status_combobox,treeview,discount_spinbox)
            messagebox.showinfo('info', 'Record is Deleted')
        except Exception as e:
            messagebox.showerror('Error', f'error due to {e}')
        finally :
            cursor.close()
            connection.close()

def select_data(event,category_combobox,supplier_combobox,name_entry, price_entry, quantity_entry, status_combobox,treeview,discount_spinbox):
    
    index=treeview.selection()

    name_entry.delete(0,END)
    price_entry.delete(0,END)
    quantity_entry.delete(0,END)
    discount_spinbox.delete(0,END)

    dict=treeview.item(index)
    content=dict['values']

    category_combobox.set(content[1])
    supplier_combobox.set(content[2])
    name_entry.insert(0,content[3])
    price_entry.insert(0,content[4])
    discount_spinbox.insert(0,content[5])
    quantity_entry.insert(0,content[7])
    status_combobox.set(content[8])

def update_product(category,supplier,name, price, discount,quantity, status,treeview,category_combobox
                   ,supplier_combobox,name_entry, price_entry, quantity_entry, status_combobox,discount_spinbox):
    index=treeview.selection()

    if not index:
        messagebox.showerror('Error','no row selected')
        return
    cursor,connection=connect_database()
    if not cursor or not connection:
        return
    
    dict=treeview.item(index)
    content=dict['values']
    id=content[0]

    cursor.execute('use inventory_system')
    cursor.execute('SELECT * FROM product_data WHERE id=%s',id)
    current_data=cursor.fetchone()
    current_data=current_data[1:]
    current_data=list(current_data)
    current_data[3]=str(current_data[3])
    current_data[4]=str(current_data[4])
    del current_data[5]
    current_data=tuple(current_data)


    quantity=int(quantity)
    new_data=(category,supplier,name,price,discount,quantity,status)


    if current_data==new_data:
        messagebox.showinfo('info', 'No changes detected')
        return 
    
    discounted_price=round(float(price)*(1-float(discount)/100),2)
    cursor.execute('UPDATE product_data SET category=%s, supplier=%s, name=%s, price=%s,discount=%s,discounted_price=%s,quantity=%s,status=%s WHERE id=%s',
                       (category,supplier,name, price,discount,discounted_price, quantity, status,id))
        
    connection.commit()
    clear(category_combobox,supplier_combobox,name_entry, price_entry, quantity_entry, status_combobox,treeview,discount_spinbox)
    messagebox.showinfo('Info', 'Data is Updated')
    treeview_data(treeview)

def treeview_data(treeview):
    cursor,connection=connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('use inventory_system')
        cursor.execute('SELECT * FROM product_data')
        records=cursor.fetchall()
        treeview.delete(*treeview.get_children())
        for record in records:
            treeview.insert('',END,values=record)
    except Exception as e:
        messagebox.showerror('Error', f'error due to {e}')
    finally :
        cursor.close()
        connection.close()

def fetch_supplier_category(category_combobox,supplier_combobox):
    category_option=[]
    supplier_option=[]
    cursor,connection=connect_database()
    if not cursor or not connection:
        return
    cursor.execute('USE inventory_system')

    cursor.execute('SELECT name from category_data')
    names=cursor.fetchall()
    if len(names)>0:
        category_combobox.set('Select')
        for name in names:
            category_option.append(name[0])
        category_combobox.config(values=category_option)

    cursor.execute('SELECT name from supplier_data')
    names=cursor.fetchall()
    if len(names)>0:
        supplier_combobox.set('Select')
        for name in names:
            supplier_option.append(name[0])
        supplier_combobox.config(values=supplier_option)

    # except Exception as e:
    #     messagebox.showerror('Error', f'error due to {e}')
    # finally :
    #     cursor.close()
    #     connection.close()

def add_product(category,supplier,name, price,discount, quantity, status,treeview,
                category_combobox,supplier_combobox,name_entry, price_entry, quantity_entry, status_combobox,discount_spinbox):
    if category=='Empty':
        messagebox.showerror('Error', 'Please add Categories')
    elif supplier=='Empty':
        messagebox.showerror('Error', 'Please add Supplier')
    elif category=='Select' or supplier=='Select' or name=='' or price=='' or quantity=='' or status=='Select Status':
        messagebox.showerror('Error', 'All fields are required')
    else:
        cursor,connection=connect_database()
        if not cursor or not connection:
            return
        cursor.execute('USE inventory_system')
        cursor.execute('CREATE TABLE IF NOT EXISTS product_data (id INT AUTO_INCREMENT PRIMARY KEY,category VARCHAR(100),'
        'supplier VARCHAR(100),name VARCHAR(100),price DECIMAL(10,2), quantity INT, status VARCHAR(50))')

        cursor.execute('SELECT * from product_data WHERE category=%s AND supplier=%s AND name=%s',(category,supplier,name))
        existing_product=cursor.fetchone()
        if existing_product:
            messagebox.showerror('Warning','Product already exists')
            return
        discounted_price=round(float(price)*(1-float(discount)/100),2)
        cursor.execute('INSERT INTO product_data (category,supplier,name, price, discount, discounted_price, quantity, status) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)'
                       ,(category,supplier,name, price,discount, discounted_price, quantity, status))
        connection.commit()
        clear(category_combobox,supplier_combobox,name_entry, price_entry, quantity_entry, status_combobox,treeview,discount_spinbox)
        messagebox.showinfo('Success','Data is added successfully')
        treeview_data(treeview)




def product_form(window):
    product_frame = Frame(width=1150, height=668)
    product_frame.place(x=200, y = 91)

    back_button=Button(product_frame,text="back",font=("roman new times",10,"bold"),cursor="hand2",
                       command=lambda: product_frame.place_forget())
    back_button.place(x=2,y=6)

    left_frame=Frame(product_frame,bg='white',bd=2,relief=RIDGE)
    left_frame.place(x=10,y=50)

    headinglabel=Label(left_frame, text="Manage Product Detail ", font=("roman new times", 16, "bold",), bg="#0f4d7d", fg="white")
    headinglabel.grid(row = 0, columnspan=2,sticky='we')

    category_label=Label(left_frame,text='Category',font=('roman new time',14),bg='white')
    category_label.grid(row=1,column=0,padx=20,sticky='w')
    category_combobox=ttk.Combobox(left_frame,font=('roman new time',14),width=18,state="readonly")
    category_combobox.grid(row=1,column=1,pady=30)
    category_combobox.set('Empty')

    supplier_label=Label(left_frame,text='Supplier',font=('roman new time',14),bg='white')
    supplier_label.grid(row=2,column=0,padx=20,sticky='w')
    supplier_combobox=ttk.Combobox(left_frame,font=('roman new time',14),width=18,state="readonly")
    supplier_combobox.grid(row=2,column=1)
    supplier_combobox.set('Empty')

    name_label=Label(left_frame,text='Name',font=('roman new time',14),bg='white')
    name_label.grid(row=3,column=0,padx=20,sticky='w')
    name_entry=Entry(left_frame,font=('roman new time',14))
    name_entry.grid(row=3,column=1,pady=30)

    price_label=Label(left_frame,text='Price',font=('roman new time',14),bg='white')
    price_label.grid(row=4,column=0,padx=20,sticky='w')
    price_entry=Entry(left_frame,font=('roman new time',14))
    price_entry.grid(row=4,column=1,)

    discount_label=Label(left_frame,text='Discount(%)',font=('roman new time',14),bg='white')
    discount_label.grid(row=5,column=0,pady=(30,0))
    discount_spinbox=Spinbox(left_frame,from_=0, to=100, font=('roman new time',14),width=19)
    discount_spinbox.grid(row=5,column=1,pady=(30,0))

    quantity_label=Label(left_frame,text='Quantity',font=('roman new time',14),bg='white')
    quantity_label.grid(row=7,column=0,padx=30,sticky='w')
    quantity_entry=Entry(left_frame,font=('roman new time',14))
    quantity_entry.grid(row=7,column=1,pady=30)

    status_label=Label(left_frame,text='Status',font=('roman new time',14),bg='white')
    status_label.grid(row=8,column=0,padx=30,sticky='w')
    status_combobox=ttk.Combobox(left_frame,values=('Active','Inactive'),font=('roman new time',14),width=18,state="readonly")
    status_combobox.grid(row=8,column=1)
    status_combobox.set('Select Status')

    button_frame=Frame(left_frame,bg='white')
    button_frame.grid(row=9,columnspan=2,pady=(30,10))

    add_button=Button(button_frame,text="Add",font=("roman new times",14), bg="#0f4d7d", fg="white",width=6, cursor="hand2",
                      command=lambda:add_product(category_combobox.get(),supplier_combobox.get(),name_entry.get(),price_entry.get(),
                                                 discount_spinbox.get(),quantity_entry.get(),status_combobox.get(),treeview,category_combobox,
                                                 supplier_combobox,name_entry, price_entry, quantity_entry, status_combobox,discount_spinbox))
    add_button.grid(row=0,column=0,padx=10)

    update_button=Button(button_frame,text="Update",font=("roman new times",14), bg="#0f4d7d", fg="white",width=6, cursor="hand2",
                         command=lambda:update_product(category_combobox.get(),supplier_combobox.get(),name_entry.get(),price_entry.get(),
                                                 discount_spinbox.get(),quantity_entry.get(),status_combobox.get(),treeview,category_combobox,supplier_combobox,
                                                 name_entry, price_entry, quantity_entry, status_combobox,discount_spinbox))
    update_button.grid(row=0,column=1,padx=10)

    delete_button=Button(button_frame,text="Delete",font=("roman new times",14), bg="#0f4d7d", fg="white",width=6, cursor="hand2",
                         command=lambda:delete_product(treeview,category_combobox,supplier_combobox,name_entry, price_entry, quantity_entry, status_combobox,discount_spinbox))
    delete_button.grid(row=0,column=2,padx=10)

    clear_button=Button(button_frame,text="Clear",font=("roman new times",14), bg="#0f4d7d", fg="white",width=6, cursor="hand2",
                        command=lambda: clear(category_combobox,supplier_combobox,name_entry, price_entry, quantity_entry, status_combobox,treeview,discount_spinbox))
    clear_button.grid(row=0,column=3,padx=10)

    search_frame=LabelFrame(product_frame,text='Search Product',font=("roman new times",14,'bold'),bg='white')
    search_frame.place(x=420,y=40)

    search_combobox=ttk.Combobox(search_frame,values=('Category','Supplier','Name', 'Status'),font=('roman new time',14),width=18,state="readonly")
    search_combobox.grid(row=0,column=0,padx=10)
    search_combobox.set('Search By')

    search_entry=Entry(search_frame,font=('roman new time',14, 'bold'),width=16)
    search_entry.grid(row=0,column=1)

    search_button=Button(search_frame,text="Search",font=("roman new times",14), bg="#0f4d7d", fg="white",width=6, cursor="hand2",
                         command=lambda:search_product(search_combobox,search_entry,treeview))
    search_button.grid(row=0,column=2,padx=(10,0),pady=10)

    show_button=Button(search_frame,text="Show All",font=("roman new times",14), bg="#0f4d7d", fg="white",width=6, cursor="hand2",
                       command=lambda:show_all(treeview,search_entry,search_combobox))
    show_button.grid(row=0,column=3,padx=10)

    treeview_frame=Frame(product_frame,bg='white')
    treeview_frame.place(x=420,y=130,width=610,height=430)

    scrolly=Scrollbar(treeview_frame,orient=VERTICAL)
    scrollx=Scrollbar(treeview_frame,orient=HORIZONTAL)

    treeview=ttk.Treeview(treeview_frame,columns=('id','category','supplier','name', 'price','discount','discounted_price', 'quantity', 'status'),show='headings',
                          yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)

    scrolly.pack(side=RIGHT,fill=Y)
    scrollx.pack(side=BOTTOM,fill=X)

    scrolly.config(command=treeview.yview)
    scrollx.config(command=treeview.xview)

    treeview.pack(fill=BOTH,expand=1)

    treeview.heading('id', text='ID')
    treeview.heading('category', text='Category')
    treeview.heading('supplier', text='Supplier')
    treeview.heading('name', text=' Product Name')
    treeview.heading('price', text='Price')
    treeview.heading('discount', text='Discount')
    treeview.heading('discounted_price', text='Discounted_price')
    treeview.heading('quantity', text='Quantity')
    treeview.heading('status', text='Status')
    fetch_supplier_category(category_combobox,supplier_combobox)
    treeview_data(treeview)
    treeview.bind('<ButtonRelease-1>',lambda event:select_data(event,category_combobox,supplier_combobox,name_entry, 
                                                               price_entry, quantity_entry, status_combobox,treeview,discount_spinbox))
    return product_frame
    