import pymongo
import streamlit as st
from dotenv import load_dotenv
import pandas as pd  # Import Pandas for DataFrame
load_dotenv()


string_connection= st.secrets["api"]["key"]


# Connect to MongoDB
client = pymongo.MongoClient(string_connection)

db = client["LibraryDB"]
collection = db["Books"]

st.header("Welcome to Library Manager 📚")

st.sidebar.title("📚 Library Manager")

# Sidebar Navigation Menu
option = st.sidebar.radio("Choose an option:", [
    "Home",
    "Add Book 📖",
    "Remove a Book 🗑",
    "Search Book 🏸",
    "All Books 📚",
    "Library Statistics 📊"
])

if option == "Home":
    st.write("**Books are not just stories; they are doors to new worlds. 📖✨**")
    st.write("Every page you turn is a new adventure. 🌍 ")
    st.write("Every story teaches a new lesson. 📚")
    st.write("Every book is a friend that never leaves you. 💙")
    st.image("https://images.unsplash.com/photo-1512820790803-83ca734da794", use_container_width=True)  # Books-related image

elif option == "Add Book 📖":
    # Add a book
    st.header("Add a Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=0, step=1)
    genre = st.text_input("Genre")
    added_by = st.text_input("Your Name (Used for Book Ownership)")  # Store user name
    read_status = st.checkbox("Have you read this book?")

    if st.button("Add Book"):
        if title and author and year and genre and added_by:
            book = {
                "title": title,
                "author": author,
                "year": year,
                "genre": genre,
                "read": read_status,
                "added_by": added_by  # Store the user who added the book
            }
            collection.insert_one(book)
            st.success("✅ Book added successfully!")
        else:
            st.error("⚠️ Please fill all fields.")

elif option == "Remove a Book 🗑":
    # Remove a book
    st.header("Remove a Book")
    remove_title = st.text_input("Enter book title to remove")
    user_name = st.text_input("Enter your name to confirm")

    if st.button("Remove Book"):
        result = collection.delete_one({"title": remove_title, "added_by": user_name})  # Check if the user is the owner
        if result.deleted_count > 0:
            st.success("🗑 Book removed successfully!")
        else:
            st.error("❌ Book not found or you don't have permission to delete it!")

elif option == "Search Book 🏸":
    # Search for a book
    st.header("Search for a Book")
    search_option = st.radio("Search by:", ["Title", "Author"])
    search_query = st.text_input("Enter search query")

    if st.button("Search"):
        if search_option == "Title":
            books = collection.find({"title": search_query})
        else:
            books = collection.find({"author": search_query})

        results = list(books)
        if results:
            for book in results:
                st.write(f"📖 {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {'✅ Read' if book.get('read') else '❌ Not Read'} (Added by: {book['added_by']})")
        else:
            st.error("❌ No books found!")


# elif option == "All Books 📚":
#     # Display all books
#     st.header("All Books")
#     books = list(collection.find())  # Convert cursor to list
    
#     if books:  # Check if list is not empty
#         for book in books:
#             st.write(f"📖 {book.get('title', 'Unknown')} by {book.get('author', 'Unknown')} ({book.get('year', 'N/A')}) - {book.get('genre', 'Unknown')} - {'✅ Read' if book.get('read') else '❌ Not Read'} ")
#     else:
#         st.warning("📭 No books found in the library.")



elif option == "All Books 📚":
    # Display all books
    st.header("All Books")
    books = list(collection.find({}, {"_id": 0, "added_by": 0}))  # Exclude "_id" and "added_by"

    if books:
        # Convert books list to DataFrame
        df = pd.DataFrame(books)

        # Rename columns for better readability
        df.rename(columns={
            "title": "Title",
            "author": "Author",
            "year": "Year",
            "genre": "Genre",
            "read": "Read Status"
        }, inplace=True)

        # Convert Read Status to readable format
        df["Read Status"] = df["Read Status"].apply(lambda x: "✅ Yes" if x else "❌ No")

        # Display the DataFrame as a table
        st.dataframe(df, use_container_width=True)

    else:
        st.warning("📭 No books found in the library.")

elif option == "Library Statistics 📊":
    # Display statistics
    st.header("Library Statistics")
    total_books = collection.count_documents({})
    read_books = collection.count_documents({"read": True})
    percentage_read = (read_books / total_books * 100) if total_books > 0 else 0

    st.write(f"📚 Total books: {total_books}")
    st.write(f"✅ Books Read: {read_books}")
    st.write(f"📊 Percentage Read: {percentage_read:.2f}%")
