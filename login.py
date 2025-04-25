from tkinter import *
from tkinter import messagebox
import subprocess
import sys 
from employee import connect_database



def login():
    username = entry_username.get()
    password = entry_password.get()

    # Database connection
    cursor, connection = connect_database()
    if not cursor or not connection:
        return

    cursor.execute("USE inventory_system")
    query = "SELECT user_type, name FROM employee_data WHERE empid = %s AND password = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()

    connection.close()

    if result:
        user_type = result[0]
        
        
        if user_type == "Admin":
            subprocess.Popen([sys.executable, "dashboard.py"])
            window.destroy()

        elif user_type == "Employee":
            subprocess.Popen([sys.executable, "billing.py"]) 
            window.destroy()
            
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")




def clear_fields():
    entry_username.delete(0, END)
    entry_password.delete(0, END)

def on_hover(button, color):
    button.config(bg=color)

# Create login window
window = Tk()
window.title("Login")
window.geometry("1300x731+0+0")
window.resizable(0,0)
window.config(bg='white')

# # Background Image
bg_icon = PhotoImage(file="bg1.png",)
bg_icon_label = Label(window, image=bg_icon)
bg_icon_label.pack()
# bg_icon_label.place(x=655, y=15,height=521, width=405)

bgg_frame = Frame(window, bg='white')
bgg_frame.place(x=740, y=315, height=420, width=560)
bgg_icon = PhotoImage(file="bg5.png",)
bgg_icon_label = Label(bgg_frame, image=bgg_icon)
bgg_icon_label.pack()


# Login Frame

login_frame = Frame(window, bg="white", bd=3, relief="ridge")
login_frame.place(x=190, y=265, height=250, width=285)

# Header
heading_label = Label(login_frame, text="Login Board", font=("Segoe UI", 12, "bold"), 
                      bg="#010c48", fg="white", pady=5)
heading_label.grid(row=0,column=0, columnspan=3, sticky='we')


# Username Field
empid_label = Label(login_frame, text="User ID :", bg="white", font=('Segoe UI', 11))
empid_label.grid(row=1, column=1, padx=(20,5), pady=15, sticky='w')

entry_username = Entry(login_frame, font=("Segoe UI", 10), width=20, relief="solid", bd=1)
entry_username.grid(row=1, column=2, padx=(5,30), pady=10,sticky='w')

# Password Field
password_label = Label(login_frame, text="Password :", bg="white", font=('Segoe UI', 11))
password_label.grid(row=2, column=1, padx=(20,5), pady=15, sticky='w')

entry_password = Entry(login_frame, font=("Segoe UI", 10), width=20, relief="solid", bd=1, show="*")
entry_password.grid(row=2, column=2, padx=(5,30), pady=10,sticky='w')

# Buttons
login_button = Button(login_frame, text="Login", font=("Segoe UI", 10, "bold"), 
                      bg="#010c48", fg="white", width=8, relief="raised", cursor="hand2", command=login)
login_button.grid(row=3, column=1, padx=(40,0), pady=10,sticky='e')

clear_button = Button(login_frame, text="Clear", font=("Segoe UI", 10, "bold"), 
                      bg="#010c48", fg="white", width=8, relief="raised", cursor="hand2", command=clear_fields)
clear_button.grid(row=3, column=2, padx=(20,5), pady=10,sticky='w')

login_button.bind("<Enter>", lambda e: on_hover(login_button, "#1565C0"))
login_button.bind("<Leave>", lambda e: on_hover(login_button, "#010c48"))

clear_button.bind("<Enter>", lambda e: on_hover(clear_button, "#1565C0"))
clear_button.bind("<Leave>", lambda e: on_hover(clear_button, "#010c48"))

window.mainloop()
