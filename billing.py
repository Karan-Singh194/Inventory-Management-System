from tkinter import *
from employee import connect_database
from tkinter import messagebox
from tkinter import ttk
import subprocess
import sys 
import time
price = 0
bill_amount = 0
formatted_value = 0
invoice = ''

def update():
    date_time=time.strftime(' %B, %d, %Y \t\t\t  %I:%M:%S %p on %A ')
    subtitlelabel.config(text=f"Welcome Employee \t\t\t\t {date_time}" )
    subtitlelabel.after(1000,update)

calculation = ""

def get_input(value):
    """Append the pressed button value to the calculation"""
    global calculation
    calculation += str(value)
    txt_cal_input.delete(0, END)
    txt_cal_input.insert(END, calculation)

def clear_cal():
    """Clear the calculator display"""
    global calculation
    calculation = ""
    txt_cal_input.delete(0, END)

def perform_cal():
    """Evaluate the entered expression and display the result"""
    global calculation
    try:
        result = eval(calculation)  # Evaluates the math expression
        txt_cal_input.delete(0, END)
        txt_cal_input.insert(END, str(result))
        calculation = str(result)  # Store result for further operations
    except:
        txt_cal_input.delete(0, END)
        txt_cal_input.insert(END, "Error")
        calculation = ""

        # ------------------------------

def show_all(treeview,search_entey):
    treeview_data(treeview)
    search_entey.delete(0,END)

def treeview_data(treeview):
    cursor,connection=connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('use inventory_system')
        cursor.execute('SELECT id, name ,  price , discount , discounted_price ,  quantity ,  status  FROM product_data')
        records=cursor.fetchall()
        treeview.delete(*treeview.get_children())
        for record in records:
            treeview.insert('',END,values=record)
    except Exception as e:
        messagebox.showerror('Error', f'error due to {e}')
    finally :
        cursor.close()
        connection.close()

def search_product(search_entry,treeview):
    if search_entry.get()==' ':
        messagebox.showwarning('Warning','Please enter the value to search')
    else:
        cursor,connection=connect_database()
        if not cursor or not connection:
            return
        cursor.execute('use inventory_system')
        cursor.execute(f'SELECT id, name ,  price , discount , discounted_price ,  quantity ,  status FROM product_data WHERE name=%s',search_entry.get())
        records=cursor.fetchall()
        if len(records)==0:
            messagebox.showerror('Error','No records found')
            return
        treeview.delete(*treeview.get_children())
        for record in records:
            treeview.insert('',END,values=record)




def on_product_select(event):
    global original_price  

    selected_item = treeview.selection()
    if selected_item:
        CartTable.selection_remove(CartTable.selection()) 
        item_values = treeview.item(selected_item)['values']
        product_name = item_values[1]  # Assuming Name is at index 3
        original_price = float(item_values[4])  # Assuming Price is at index 6
        stock = item_values[5]  # Assuming Stock is at index 7

        p_name_entry.config(state='normal')
        p_name_entry.delete(0, END)
        p_name_entry.insert(0, product_name)
        p_name_entry.config(state='readonly')

        p_price_entry.config(state='normal')
        p_price_entry.delete(0, END)
        p_price_entry.insert(0, f"{original_price:.2f}")  
        p_price_entry.config(state='readonly')

        p_qty_entry.delete(0, END)
        p_qty_entry.master.focus_set()  # Move focus away from p_qty_entry

        # Update the stock label dynamically
        lbl_inStock.config(text=f"In Stock: {stock}")

def on_cart_select(event): 

    selected_item = CartTable.selection()
    if selected_item:
        treeview.selection_remove(treeview.selection()) # remove focus selection from treeview
        item_values = CartTable.item(selected_item)['values']
        product_name = item_values[1]  # Assuming Name is at index 3
        original_price = float(item_values[2])  # Assuming Price is at index 6
        stock = item_values[3]  # Assuming Stock is at index 7

        p_name_entry.config(state='normal')
        p_name_entry.delete(0, END)
        p_name_entry.insert(0, product_name)
        p_name_entry.config(state='readonly')

        p_price_entry.config(state='normal')
        p_price_entry.delete(0, END)
        p_price_entry.insert(0, f"{original_price:.2f}")  
        p_price_entry.config(state='readonly')

        p_qty_entry.delete(0, END)
        p_qty_entry.master.focus_set()  # Move focus away from p_qty_entry

        # Update the stock label dynamically
        lbl_inStock.config(text=f"In Cart Stock: {stock}")



def update_price(event):
    try:
        qty_text = p_qty_entry.get().strip()
        if not qty_text.isdigit() or qty_text == "0":  
            p_price_entry.config(state='normal')
            p_price_entry.delete(0, END)
            p_price_entry.insert(0, f"{original_price:.2f}")  
            p_price_entry.config(state='readonly')
            return
        
        qty = int(qty_text)  
        
        # Prevent calculation when original price is reset
        if original_price == 0:
            p_price_entry.config(state='normal')
            p_price_entry.delete(0, END)
            p_price_entry.insert(0, "0.00")  
            p_price_entry.config(state='readonly')
            return

        total_price = qty * original_price  

        p_price_entry.config(state='normal')  
        p_price_entry.delete(0, END)  
        p_price_entry.insert(0, f"{total_price:.2f}")  
        p_price_entry.config(state='readonly')

    except:
        p_price_entry.config(state='normal')
        p_price_entry.delete(0, END)
        p_price_entry.insert(0, "0.00")  
        p_price_entry.config(state='readonly')



def clear_cart_fields():
    global original_price 
    original_price = 0  # Reset to prevent old price usage

    # Clear Product Name
    p_name_entry.config(state='normal')
    p_name_entry.delete(0, END)
    p_name_entry.config(state='readonly')

    # Reset Price to 0
    p_price_entry.config(state='normal')
    p_price_entry.delete(0, END)
    p_price_entry.insert(0, "")  
    p_price_entry.config(state='readonly')

    # Clear Quantity & Remove Focus
    p_qty_entry.delete(0, END)
    p_qty_entry.master.focus_set()  # Move focus away from p_qty_entry

    # Deselect TreeView and cartTable Selection ,clear stock
    treeview.selection_remove(treeview.selection()) 
    CartTable.selection_remove(CartTable.selection()) 
    lbl_inStock.config(text=f"In Stock: {''}") 



def add_or_update_cart():
         
    # Check if product name is filled (ensures a product is selected)
    if not p_name_entry.get():
        messagebox.showerror("Error", "Please select a product first!")
        return

    selected_item_p = treeview.selection()
    if not selected_item_p:
        messagebox.showerror("Error", "Please select a product first!")
        return
    
    # Get product details from selected treeview row
    item_data = treeview.item(selected_item_p, 'values')
    if not item_data:
        messagebox.showerror("Error", "Invalid product selection!")
        return
    
    id, name, price, discount, discounted_price, quantity, status = item_data

    # Validate quantity
    qty_text = p_qty_entry.get().strip()
    if not qty_text.isdigit() or int(qty_text) <= 0:
        messagebox.showerror("Error", "Enter a valid quantity!")
        return
    
    if status=='Inactive':
        messagebox.showerror("warrning", "Product is not avaliable")
        return 
    
    
    qty = int(qty_text)
    total_price = qty * float(discounted_price)
    bill_amount = qty * float(price)
    # Check if the product is already in the cart
    for row in CartTable.get_children():
        row_data = CartTable.item(row, 'values')
        if row_data and row_data[0] == id:  # Product exists
            # Update quantity and price
            CartTable.item(row, values=(id, name, discounted_price, qty, f"{total_price:.2f}",f"{bill_amount:.2f}"))
            messagebox.showinfo("Updated", f"{name} quantity updated in the cart!")
            bill_update()
            return

    # If product is not in the cart, add it
    CartTable.insert('', END, values=(id, name, discounted_price, qty, f"{total_price:.2f}",f"{bill_amount:.2f}"))
    messagebox.showinfo("Added", f"{name} added to cart!")

    # Update cart count dynamically
    cart_Title.config(text=f"Cart \t Total Products: [{len(CartTable.get_children())}]")
    bill_update()


def remove_cart():

    # Check if product name is filled (ensures a cart product is selected)
    if not p_name_entry.get():
        messagebox.showerror("Error", "Please select a product first!")
        return

    selected_item_c = CartTable.selection()
    if not selected_item_c:
        messagebox.showerror("Error", "Please select a cart productc first!")
        return
    
    # Get product details from selected treeview row
    item_data = CartTable.item(selected_item_c, 'values')
    if not item_data:
        messagebox.showerror("Error", "Invalid product selection!")
        return
    
    Id,Name ,Price ,Quantity,Total,bill_amount = item_data

    
    if selected_item_c:
        for item in selected_item_c:
            CartTable.delete(item)
    messagebox.showinfo("Done", " Cart Product remove")
    clear_cart_fields()
    cart_Title.config(text=f"Cart \t Total Products: [{len(CartTable.get_children())}]")
    bill_update()

def bill_update(): 
    global price
    global bill_amount
    global formatted_value

    price = 0
    bill_amount = 0
    formatted_value = 0

    for item_id in CartTable.get_children():
        values = CartTable.item(item_id, "values")
        price+=float(values[4])
        bill_amount+=float(values[5])
    net_pay_label.config(text=f"Net Pay\n{price}" )
    amnt_bill_label.config(text=f"Bill Amount\n{bill_amount}" )
    if price != 0 and bill_amount != 0:
        discount = ((bill_amount - price) / bill_amount) * 100
        formatted_value = float(f"{discount:.3g}")
        discount_label.config(text=f"Discount\n{formatted_value}%" )
    else:
        discount_label.config(text=f"Discount\n0%" )
    

def generate_bill():
    if name_entry.get() == '':
        messagebox.showerror("Error", "Enter Customer name")
        return
    elif contact_entry.get() == '':
        messagebox.showerror("Error", "Enter contact no.")
        return
    elif len(CartTable.get_children()) ==0:
            messagebox.showerror("Error",f"Please Add product to the Cart!!!")
            return
        

    # bill Top
    bill_top()

    # bill middle
    bill_middle()

    # bill bottom
    bill_bottom()

    fp=open(f'bill/{str(invoice)}.txt','w')
    fp.write(txt_bill_area.get('1.0',END))
    fp.close()
    messagebox.showinfo("Saved","Bill has been generated")
    chk_print=1

def bill_top():
    global invoice
    invoice=int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))
    bill_top_temp=f'''
\tInventory Management System
\tPhone No. 0000000000 , Gujarat-393010
{str("="*46)}
 Customer Name: {name_entry.get()}
 Ph. no. : {contact_entry.get()}
 Bill No. {str(invoice)}\t\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("="*46)}
 Product Name\t\t\tQTY\tPrice
{str("="*46)}
'''
    txt_bill_area.delete('1.0',END)
    txt_bill_area.insert('1.0',bill_top_temp)

def bill_bottom():
    bill_bottom_temp=f'''
{str("="*46)}
 Bill Amount\t\t\t\tRs.{bill_amount}
 Discount\t\t\t\tRs.{formatted_value}
 Net Pay\t\t\t\tRs.{price}
{str("="*46)}\n
'''
    txt_bill_area.insert(END,bill_bottom_temp)

def bill_middle():
    for item_id in CartTable.get_children():
        values = CartTable.item(item_id, "values")
        name = values[1]
        p = values[5]
        q = values[3]
        txt_bill_area.insert(END,"\n "+name+"\t\t\t"+q+"\tRs."+p)

def clear_all():
    clear_cart_fields()
    for item in CartTable.get_children():
        CartTable.delete(item)
    name_entry.delete(0, END)
    contact_entry.delete(0, END)
    txt_bill_area.delete('1.0',END)

#GUI PART OF BILLING 

window= Tk()

window.title("Billing")
window.geometry("1360x668+0+0")
window.resizable(0,0)
window.config(bg="white")


def logout():
    subprocess.Popen([sys.executable, "login.py"])
    window.destroy() 


bg_image=PhotoImage(file="inventory.png")
titleLabel=Label(window,image=bg_image,compound=LEFT,text=" Inventory Management System ",font=("times new roman", 30, "bold"),bg="#010c48",fg="white")
titleLabel.place(x=0,y=0,relwidth=1)


subtitlelabel=Label(window,text=f"Welcome admin\t\t Date : 10-02-2025\t\t Time : 08:20:30  PM ",  font=("times new roman", 10, "bold"),bg="#4d636d",fg="white")
subtitlelabel.place(x=0,y=70, relwidth=1)


logoutButton=Button(window, text="Logout",cursor="hand2", font=("times new roman", 16, "bold"),bg="red",fg="white",
                    command=lambda :logout())
logoutButton.place(x=1150,y=14)

        # product frame -------------------------


ProductFrame=Frame(window,bd=4,relief=RIDGE)
ProductFrame.place(x=5,y=100, width=410,height=540)

pTitle=Label(ProductFrame,text="All Products",font=("goudy old style",20,"bold"),bg="#262626",fg="white")
pTitle.pack(side=TOP,fill=X)

ProductFrame2=Frame(ProductFrame,bd=2,relief=RIDGE,bg="white")
ProductFrame2.place(x=2,y=42,width=398,height=90)

search_product_label=Label(ProductFrame2,text="Search Product | By Name",font=("times new roman",15,"bold"),bg="white",fg="green")
search_product_label.place(x=2,y=5)
        
search_label=Label(ProductFrame2,text="Product Name",font=("times new roman",15,"bold"),bg="white")
search_label.place(x=2,y=45)
search_entry=Entry(ProductFrame2,font=('roman new time',14, 'bold'),bg="lightyellow")
search_entry.place(x=128,y=47,width=150,height=22)

search_button=Button(ProductFrame2,text="Search",font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2",
                     command=lambda: search_product(search_entry,treeview))
search_button.place(x=285,y=45,width=100,height=25)

show_all_button=Button(ProductFrame2,text="Show All",font=("goudy old style",15),bg="#083531",fg="white",cursor="hand2"
                       ,command=lambda: show_all(treeview,search_entry))
show_all_button.place(x=285,y=10,width=100,height=25)

treeview_frame=Frame(ProductFrame,bd=3,relief=RIDGE)
treeview_frame.place(x=2,y=140,width=398,height=375)
scrolly=Scrollbar(treeview_frame,orient=VERTICAL)
scrollx=Scrollbar(treeview_frame,orient=HORIZONTAL)

treeview=ttk.Treeview(treeview_frame,columns=('id','name', 'price','discount','discounted_price', 'quantity', 'status'),show='headings',
                          yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)

scrolly.pack(side=RIGHT,fill=Y)
scrollx.pack(side=BOTTOM,fill=X)

scrolly.config(command=treeview.yview)
scrollx.config(command=treeview.xview)

treeview.pack(fill=BOTH,expand=1)

# Bind TreeView Selection Event
treeview.bind("<<TreeviewSelect>>", on_product_select)


treeview.heading('id', text='ID')
treeview.heading('name', text=' Product Name')
treeview.heading('price', text='Price')
treeview.heading('discount', text='Discount')
treeview.heading('discounted_price', text='Discounted_price')
treeview.heading('quantity', text='Quantity')
treeview.heading('status', text='Status')

treeview.column('id', width=20)
treeview.column('name', width=80)
treeview.column('price', width=50)
treeview.column('discount', width=20)
treeview.column('discounted_price', width=80)
treeview.column('quantity', width=20)
treeview.column('status', width=50)
treeview_data(treeview)



        #-------------- customer frame ---------------


CustomerFrame=Frame(window,bd=4,relief=RIDGE,bg="white")
CustomerFrame.place(x=420,y=100,width=530,height=70)

Title_custo=Label(CustomerFrame,text="Customer Details",font=("goudy old style",15),bg="lightgray")
Title_custo.pack(side=TOP,fill=X)

name_label=Label(CustomerFrame,text="Name",font=("times new roman",15),bg="white")
name_label.place(x=5,y=35)
name_entry=Entry(CustomerFrame,font=("times new roman",13),bg="lightyellow")
name_entry.place(x=80,y=35,width=180)
        
contact_label=Label(CustomerFrame,text="Contact No.",font=("times new roman",15),bg="white")
contact_label.place(x=270,y=35)
contact_entry=Entry(CustomerFrame,font=("times new roman",15),bg="lightyellow")
contact_entry.place(x=380,y=35,width=140)


        #--------------- calculator frame ---------------------

Cal_Cart_Frame=Frame(window,bd=2,relief=RIDGE,bg="white")
Cal_Cart_Frame.place(x=420,y=170,width=530,height=360)

Cal_Frame=Frame(Cal_Cart_Frame,bd=9,relief=RIDGE,bg="white")
Cal_Frame.place(x=5,y=10,width=268,height=340)

txt_cal_input=Entry(Cal_Frame,font=('arial',15,'bold'),width=21,bd=10,relief=GROOVE,justify=RIGHT)
txt_cal_input.grid(row=0,columnspan=4)


# Button Layout
button_texts = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('+', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('*', 3, 3),
    ('0', 4, 0), ('C', 4, 1), ('=', 4, 2), ('/', 4, 3)
]

# Creating buttons in a loop
for text, row, col in button_texts:
    Button(Cal_Frame, text=text, font=('arial', 15, 'bold'), bd=5, width=4, pady=10, cursor="hand2",
           command=lambda t=text: get_input(t) if t not in ['C', '='] else (clear_cal() if t == 'C' else perform_cal()))\
           .grid(row=row, column=col)
    
    #------------------ cart frame --------------------
Cart_Frame=Frame(Cal_Cart_Frame,bd=3,relief=RIDGE)
Cart_Frame.place(x=280,y=8,width=245,height=342)
cart_Title=Label(Cart_Frame,text="Cart \t Total Products: [0]",font=("goudy old style",15),bg="lightgray")
cart_Title.pack(side=TOP,fill=X)

scrolly=Scrollbar(Cart_Frame,orient=VERTICAL)
scrollx=Scrollbar(Cart_Frame,orient=HORIZONTAL)
CartTable = ttk.Treeview(Cart_Frame, columns=("Id", "Name", "Price", "Quantity","Total"), show="headings",
                         yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
scrollx.pack(side=BOTTOM,fill=X)
scrolly.pack(side=RIGHT,fill=Y)
scrollx.config(command=CartTable.xview)
scrolly.config(command=CartTable.yview)
CartTable.pack(fill=BOTH,expand=1)

CartTable.bind("<<TreeviewSelect>>", on_cart_select)


CartTable.heading("Id", text="ID")
CartTable.heading("Name", text="Product Name")
CartTable.heading("Price", text="Price")
CartTable.heading("Quantity", text="Quantity")
CartTable.heading("Total", text="Total Price")

# Set column widths
CartTable.column("Id", width=50)
CartTable.column("Name", width=150)
CartTable.column("Price", width=100)
CartTable.column("Quantity", width=100)
CartTable.column("Total", width=120)

# Pack the Cart Table inside the frame
CartTable.pack(fill="both", expand=True)

Add_CartWidgets_Frame=Frame(window,bd=2,relief=RIDGE,bg="white")
Add_CartWidgets_Frame.place(x=420,y=530,width=530,height=110)
                            
p_name_label=Label(Add_CartWidgets_Frame,text="Product Name",font=("times new roman",15),bg="white")
p_name_label.place(x=5,y=5)
p_name_entry=Entry(Add_CartWidgets_Frame,font=("times new roman",15),bg="lightyellow",state='readonly')
p_name_entry.place(x=5,y=35,width=190,height=22)

p_price_label=Label(Add_CartWidgets_Frame,text="Price Per Qty",font=("times new roman",15),bg="white")
p_price_label.place(x=230,y=5)
p_price_entry=Entry(Add_CartWidgets_Frame,font=("times new roman",15),bg="lightyellow",state='readonly')
p_price_entry.place(x=230,y=35,width=150,height=22)
                    
p_qty_label=Label(Add_CartWidgets_Frame,text="Quantity",font=("times new roman",15),bg="white")
p_qty_label.place(x=390,y=5)
p_qty_entry=Entry(Add_CartWidgets_Frame,font=("times new roman",15),bg="lightyellow")
p_qty_entry.place(x=390,y=35,width=120,height=22)

# Bind Quantity Entry to Update Price in Real-Time
p_qty_entry.bind("<KeyRelease>", update_price)

lbl_inStock=Label(Add_CartWidgets_Frame,text="In Stock",font=("times new roman",15),bg="white")
lbl_inStock.place(x=5,y=70)


clear_cart_button=Button(Add_CartWidgets_Frame,text="Clear",font=("times new roman",15,"bold"),bg="lightgray",cursor="hand2",
                          command=clear_cart_fields)
clear_cart_button.place(x=185,y=70,width=60,height=30)

remove_cart_button=Button(Add_CartWidgets_Frame,text="Remove",font=("times new roman",15,"bold"),bg="lightgray",cursor="hand2",
                          command=remove_cart)
remove_cart_button.place(x=255,y=70,width=90,height=30)

add_cart_button=Button(Add_CartWidgets_Frame,text="Add | Update",font=("times new roman",15,"bold"),bg="orange",cursor="hand2")
add_cart_button.place(x=350,y=70,width=140,height=30)
add_cart_button.config(command=add_or_update_cart)

        #------------------- billing area -------------------
billFrame=Frame(window,bd=2,relief=RIDGE,bg="white")
billFrame.place(x=953,y=100,width=400,height=410)

B_Title=Label(billFrame,text="Customer Bill Area",font=("goudy old style",20,"bold"),bg="#262626",fg="white")
B_Title.pack(side=TOP,fill=X)

scrolly=Scrollbar(billFrame,orient=VERTICAL)
scrolly.pack(side=RIGHT,fill=Y)

txt_bill_area=Text(billFrame,yscrollcommand=scrolly.set)
txt_bill_area.pack(fill=BOTH,expand=1)
scrolly.config(command=txt_bill_area.yview)

        #------------------- billing buttons -----------------------
billMenuFrame=Frame(window,bd=2,relief=RIDGE,bg="white")
billMenuFrame.place(x=953,y=520,width=400,height=140)

amnt_bill_label=Label(billMenuFrame,text="Bill Amount\n[0]",font=("goudy old style",15,"bold"),bg="#3f51b5",fg="white")
amnt_bill_label.place(x=2,y=5,width=120,height=70)

discount_label=Label(billMenuFrame,text="Discount\n[0%]",font=("goudy old style",15,"bold"),bg="#8bc34a",fg="white")
discount_label.place(x=124,y=5,width=120,height=70)

net_pay_label=Label(billMenuFrame,text="Net Pay\n[0]",font=("goudy old style",15,"bold"),bg="#607d8b",fg="white")
net_pay_label.place(x=246,y=5,width=160,height=70)

print_button=Button(billMenuFrame,text="Print",cursor="hand2",font=("goudy old style",15,"bold"),bg="lightgreen",fg="white")
print_button.place(x=2,y=80,width=120,height=50)

clear_all_button=Button(billMenuFrame,text="Clear All",cursor="hand2",font=("goudy old style",15,"bold"),bg="gray",fg="white",
                       command=clear_all)
clear_all_button.place(x=124,y=80,width=120,height=50)

generate_button=Button(billMenuFrame,text="Generate Bill",cursor="hand2",font=("goudy old style",15,"bold"),bg="#009688",fg="white",
                       command=generate_bill)
generate_button.place(x=246,y=80,width=160,height=50)


update()
window.mainloop()