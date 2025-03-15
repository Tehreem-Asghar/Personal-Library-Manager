import pymongo
from dotenv import load_dotenv
import streamlit as st
load_dotenv()

string_connection= st.secrets["api"]["key"]

# Connect to MongoDB
client = pymongo.MongoClient(string_connection)
db = client["LibraryDB"]
collection = db["Books"]

def add_book():
       title = input("Enter book title: ")
       author = input("Enter author: ")
       year = input("Enter publication year: ")
       genre = input("Enter genre: ")
       added_by = input("Your name (for ownership): ")
       read_status = input("Have you read this book? (yes/no): ").lower() == "yes"
       
       book = {
           "title": title,
           "author": author,
           "year": int(year),
           "genre": genre,
           "read": read_status,
           "added_by": added_by
       }
       collection.insert_one(book)
       print("✅ Book added successfully!")

def remove_book():
       title = input("Enter book title to remove: ")
       user_name = input("Enter your name for confirmation: ")
       result = collection.delete_one({"title": title, "added_by": user_name})
       if result.deleted_count > 0:
           print("🗑 Book removed successfully!")
       else:
           print("❌ Book not found or you don’t have permission to delete it!")

def search_book():
       search_by = input("Search by (title/author): ").lower()
       query = input("Enter search query: ")
       books = collection.find({search_by: query})
       
       found = False
       for book in books:
           found = True
           print(f"📖 {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {'✅ Read' if book['read'] else '❌ Not Read'}")
       
       if not found:
           print("❌ No books found!")

def all_books():
       books = collection.find({}, {"_id": 0, "added_by": 0})
       for book in books:
           print(f"📖 {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {'✅ Read' if book['read'] else '❌ Not Read'}")

def library_stats():
       total_books = collection.count_documents({})
       read_books = collection.count_documents({"read": True})
       percentage_read = (read_books / total_books * 100) if total_books > 0 else 0
       print(f"📚 Total books: {total_books}")
       print(f"✅ Books Read: {read_books}")
       print(f"📊 Percentage Read: {percentage_read:.2f}%")

while True:
       print("\n📚 Library Manager CLI")
       print("1. Add Book")
       print("2. Remove Book")
       print("3. Search Book")
       print("4. Show All Books")
       print("5. Library Statistics")
       print("6. Exit")
       
       choice = input("Choose an option: ")
       
       if choice == "1":
           add_book()
       elif choice == "2":
           remove_book()
       elif choice == "3":
           search_book()
       elif choice == "4":
           all_books()
       elif choice == "5":
           library_stats()
       elif choice == "6":
           print("Goodbye! 👋")
           break
       else:
           print("❌ Invalid choice! Try again.")