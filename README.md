📦 Inventory Management System
A comprehensive Inventory Management System built using Python (Tkinter) and MySQL, designed to streamline retail or small business operations with features for both admins and employees.

🔑 Features

- **Secure Login System**
  - Role-based login: **Admin** (access to dashboard) and **Employee** (access to billing)
- **Admin Dashboard**
  - Manage employees, products, suppliers, categories, and view sales data
  ![Alt text](screenshot/1 login.png)
- **Billing System**
  - Easy-to-use interface for employees to create bills and manage transactions
- **Product & Cart Management**
  - Add products to cart, calculate total, and generate sales entries
- **Database Integration**
  - Uses **MySQL** for backend data storage
- **Modular Design**
  - Each core functionality is handled in separate Python files

🛠️ Technologies Used
Python (Tkinter for GUI)
  - Tkinter (GUI)
  - PIL (Image handling)
  - OS & datetime modules
MySQL
PIL (for image handling)



📁 Project Structure
inventory_system/
├── dashboard.py
├── employee.py
├── product.py
├── category.py
├── supplier.py
├── sales.py
├── billing.py
└── bill.txt


🚀 How to Run
Clone the repo
Ensure MySQL is installed and database is set up
Install required Python libraries
Run dashboard.py to start the system



🙌 Contributions
Feel free to fork the project, submit issues, or suggest new features.

📄 License
This project is open-source and free to use for educational purposes.
