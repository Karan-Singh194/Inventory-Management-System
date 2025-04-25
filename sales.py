from tkinter import *
from tkinter import ttk
from employee import connect_database
from tkinter import messagebox
import os



def sales_form(window):


    sales_frame = Frame(width=1150, height=668)
    sales_frame.place(x=200, y=91)

    headinglabel = Label(sales_frame, text="Manage Sales Detail ", font=("roman new times", 16, "bold",), bg="#0f4d7d", fg="white")
    headinglabel.place(x=0, y=0, relwidth=1)

    back_button = Button(sales_frame, text="back", font=("roman new times", 10, 'bold'), cursor="hand2",
                         command=lambda: sales_frame.place_forget())
    back_button.place(x=2, y=31)

    search_frame = Frame(sales_frame, bg='white')
    search_frame.place(x=10, y=100)

    num_label = Label(search_frame, text='Invoice No.', font=('roman new time', 14), bg='white')
    num_label.grid(row=0, column=0, padx=(0, 15), sticky='w')

    search_entry = Entry(search_frame, font=('roman new time', 14), bg='lightyellow', width=13)
    search_entry.grid(row=0, column=1)

    list_frame = Frame(sales_frame, bd=3, relief=RIDGE)
    list_frame.place(x=10, y=170, width=200, height=330)

    scrolly = Scrollbar(list_frame, orient=VERTICAL)
    Sales_List = Listbox(list_frame, font=("goudy old style", 15), bg="white", yscrollcommand=scrolly.set)
    scrolly.pack(side=RIGHT, fill=Y)
    scrolly.config(command=Sales_List.yview)
    Sales_List.pack(fill=BOTH, expand=1)

    bill_Frame = Frame(sales_frame, bd=3, relief=RIDGE)
    bill_Frame.place(x=280, y=170, width=410, height=330)

    lbl_title2 = Label(bill_Frame, text="Customer Bill Area", font=("Goudy Old Style", 20), bg="orange")
    lbl_title2.pack(side=TOP, fill=X)

    scrolly2 = Scrollbar(bill_Frame, orient=VERTICAL)
    bill_area = Text(bill_Frame, bg="lightyellow", yscrollcommand=scrolly2.set)
    scrolly2.pack(side=RIGHT, fill=Y)
    scrolly2.config(command=bill_area.yview)
    bill_area.pack(fill=BOTH, expand=1)

    image_frame = Frame(sales_frame, bg='white')
    image_frame.place(x=690, y=200, width=450, height=337)

    sales_frame.logo_image = PhotoImage(file="cat2.png")
    logo_image_label = Label(image_frame, image=sales_frame.logo_image)
    logo_image_label.pack()

    def show():
        Sales_List.delete(0, END)
        for i in os.listdir('bill'):
            if i.endswith('.txt'):
                Sales_List.insert(END, i)

    def get_data(event):
        try:
            index_ = Sales_List.curselection()[0]
            file_name = Sales_List.get(index_)
            bill_area.delete('1.0', END)

            with open(f'bill/{file_name}', 'r') as fp:
                for line in fp:
                    bill_area.insert(END, line)
        except Exception as e:
            messagebox.showerror("Error", f"Unable to load bill: {e}")

    def search():
        query = search_entry.get().strip()
        if query == "":
            messagebox.showwarning("Input Error", "Please enter an Invoice Number")
            return

        found = False
        Sales_List.delete(0, END)
        for file in os.listdir('bill'):
            if file.endswith('.txt') and query in file:
                Sales_List.insert(END, file)
                found = True

        if not found:
            messagebox.showinfo("No Results", f"No bills found with Invoice No. containing '{query}'")

    def clear_search():
        search_entry.delete(0, END)
        show()
        bill_area.delete("1.0", END)

    search_button = Button(search_frame, text="Search", font=("roman new times", 14), bg="#0f4d7d", fg="white", width=8, cursor="hand2", command=search)
    search_button.grid(row=0, column=2, padx=15)

    clear_button = Button(search_frame, text="Clear", font=("roman new times", 14), bg="#0f4d7d", fg="white", width=8, cursor="hand2", command=clear_search)
    clear_button.grid(row=0, column=3)

    show_button = Button(search_frame, text="Show All", font=("roman new times", 14), bg="#0f4d7d", fg="white", width=8, cursor="hand2", command=show)
    show_button.grid(row=0, column=4, padx=15)

    Sales_List.bind("<ButtonRelease-1>", get_data)

    show()

    return sales_frame
