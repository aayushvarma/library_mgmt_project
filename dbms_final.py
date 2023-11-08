import streamlit as st
import mysql.connector

# Function to connect to the MySQL database and fetch data for a specified table
def fetch_data(table_name):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="dees",
            database="lib_mgmt"
        )
        cursor = connection.cursor()

        # Replace 'your_table' with the actual table name
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        data = cursor.fetchall()

        connection.close()

        # Display the fetched data in a Streamlit table
        st.table(data)

    except mysql.connector.Error as error:
        st.error(f"Error: {error}")
    
# Function to call the Cust_Membership function in MySQL
def call_cust_membership_function(customer_id):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="dees",
            database="lib_mgmt"
        )
        cursor = connection.cursor()

        # Replace the query with a call to the Cust_Membership function
        query = f"SELECT Cust_Membership({customer_id})"
        cursor.execute(query)
        data = cursor.fetchall()

        connection.close()

        return data[0][0] if data else "No data found"

    except mysql.connector.Error as error:
        return f"Error: {error}"

def fetch_admin_data():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="dees",
            database="lib_mgmt"
        )
        cursor = connection.cursor()

        # SQL query to fetch full name and emails of Admins
        query = "SELECT CONCAT(First_Name, ' ', Last_Name) AS Full_Name, Email FROM admin"
        cursor.execute(query)
        data = cursor.fetchall()

        connection.close()

        # Display the fetched data in a Streamlit table
        st.table(data)

    except mysql.connector.Error as error:
        st.error(f"Error: {error}")


def update_book_availability(isbn, action):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="dees",
            database="lib_mgmt"
        )
        cursor = connection.cursor()

        if action == "checkout":
            # Check if the book is available
            cursor.execute("SELECT * FROM books WHERE ISBN = %s AND Availability = 'In stock'", (isbn,))
            book = cursor.fetchone()

            if book:
                # If the book is available, update its availability
                cursor.execute("UPDATE books SET Availability = 'Checked out' WHERE ISBN = %s", (isbn,))
                connection.commit()
                st.success(f"Book with ISBN {isbn} has been checked out.")
            else:
                st.error(f"Book with ISBN {isbn} is not available for check-out.")

        elif action == "return":
            # Check if the book has been checked out
            cursor.execute("SELECT * FROM books WHERE ISBN = %s AND Availability = 'Checked out'", (isbn,))
            book = cursor.fetchone()

            if book:
                # If the book was checked out, update its availability
                cursor.execute("UPDATE books SET Availability = 'In stock' WHERE ISBN = %s", (isbn,))
                connection.commit()
                st.success(f"Book with ISBN {isbn} has been returned.")
            else:
                st.error(f"Book with ISBN {isbn} is not marked as checked out.")

        else:
            st.error("Invalid action specified.")

        connection.close()  

    except mysql.connector.Error as error:
        st.error(f"Error: {error}")

def add_new_book(isbn, title, author, category):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="dees",
            database="lib_mgmt"
        )
        cursor = connection.cursor()

        # Check if the book with the given ISBN already exists
        cursor.execute("SELECT * FROM books WHERE ISBN = %s", (isbn,))
        existing_book = cursor.fetchone()

        if existing_book:
            st.warning(f"Book with ISBN {isbn} already exists in the database.")
        else:
            # Insert the new book into the database
            cursor.execute("INSERT INTO books (ISBN, Title, Author, Category, Availability) VALUES (%s, %s, %s, %s, 'In stock')", (isbn, title, author, category))
            connection.commit()
            st.success(f"Book with ISBN {isbn} has been added to the database.")

        connection.close()

    except mysql.connector.Error as error:
        st.error(f"Error: {error}")

# Function to remove an existing book from the database
def remove_book(isbn):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="dees",
            database="lib_mgmt"
        )
        cursor = connection.cursor()

        # Check if the book with the given ISBN exists
        cursor.execute("SELECT * FROM books WHERE ISBN = %s", (isbn,))
        existing_book = cursor.fetchone()

        if existing_book:
            # Remove the book from the database
            cursor.execute("DELETE FROM books WHERE ISBN = %s", (isbn,))
            connection.commit()
            st.success(f"Book with ISBN {isbn} has been removed from the database.")
        else:
            st.warning(f"Book with ISBN {isbn} does not exist in the database.")

        connection.close()

    except mysql.connector.Error as error:
        st.error(f"Error: {error}")


st.title("Welcome to PES Library Portal")

if st.button("Check available books"):
    st.subheader("Viewing Books table")
    fetch_data("books")  # Pass the table name "books"

st.subheader("View Membership Status")

customer_id = st.number_input("Enter Customer ID",min_value=1, max_value=10, step=1, format="%d")

if st.button("View Membership"):
    result = call_cust_membership_function(customer_id)
    st.write(f"Membership Type: {result}")

if st.button("View Admin Data"):
    st.subheader("Viewing full name and emails of Admins")
    fetch_admin_data()

# Input field for ISBN
isbn = st.text_input("Enter ISBN")

# Button to check out the book
if st.button("Check Out"):
    update_book_availability(isbn, "checkout")

# Button to return the book
if st.button("Return"):
    update_book_availability(isbn, "return")

st.subheader("Add a New Book")
new_isbn = st.text_input("New ISBN")
new_title = st.text_input("Title")
new_author = st.text_input("Author")
new_category = st.text_input("Category")

# Button to add a new book
if st.button("Add New Book"):
    add_new_book(new_isbn, new_title, new_author, new_category)

# Input field to remove an existing book
st.subheader("Remove an Existing Book")
remove_isbn = st.text_input("ISBN of the Book to Remove")

# Button to remove an existing book
if st.button("Remove Book"):
    remove_book(remove_isbn)
