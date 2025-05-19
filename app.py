import streamlit as st
import pandas as pd
from datetime import datetime

# Set Page Config
st.set_page_config(page_title="Personal Library Instructor", page_icon="📚", layout="centered")

# Load or Initialize Book Data
try:
    df = pd.read_csv("library_books.csv")
except FileNotFoundError:
    df = pd.DataFrame(columns=["Title", "Author", "Genre", "Status", "Added On", "Rating", "Review"])

# Custom HTML & CSS Styling
st.markdown("""
    <style>
        body { background-color: #f4f4f4; font-family: Arial, sans-serif; }
        .container { max-width: 900px; margin: auto; padding: 20px; background: lightblue; border-radius: 10px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); text-align: center; }
        h1 { color: #4A90E2; text-align: center; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; text-align: center; }
        th, td { padding: 10px; border: 1px solid #ddd; text-align: center; }
        th { background: #4A90E2; color: white; }
        .footer { text-align: center; margin-top: 20px; font-size: 18px; }
        .btn { background: #4A90E2; color: white; padding: 10px 15px; border: none; border-radius: 5px; cursor: pointer; text-align: center; }
        .btn:hover { background: #357ABD; }
    </style>
    <div class='container'>
        <h1>📚 Personal Library Instructor by krish</h1>
    </div>
""", unsafe_allow_html=True)

# Centered UI
st.header("📖 Your Library")
if not df.empty:
    st.dataframe(df.style.set_properties(**{'text-align': 'center'}))

# Add a New Book
st.subheader("➕ Add a New Book")
title = st.text_input("Book Title")
author = st.text_input("Author")
genre = st.text_input("Genre")
status = st.selectbox("Status", ["Unread", "Reading", "Completed"])
rating = st.slider("Rating", 1, 5, 3)
review = st.text_area("Write a Review")
add_book = st.button("Add Book", key="add_book")

if add_book and title and author:
    new_data = pd.DataFrame([[title, author, genre, status, datetime.now().strftime("%Y-%m-%d"), rating, review]], 
                             columns=["Title", "Author", "Genre", "Status", "Added On", "Rating", "Review"])
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv("library_books.csv", index=False)
    st.success("Book added successfully!")
    st.rerun()

# Update Book Status and Rating
st.subheader("🔄 Update Book Details")
if not df.empty:
    book_to_update = st.selectbox("Select Book", df["Title"])
    new_status = st.selectbox("New Status", ["Unread", "Reading", "Completed"])
    new_rating = st.slider("New Rating", 1, 5, 3)
    new_review = st.text_area("Update Review")
    update_book = st.button("Update Details", key="update_status")
    if update_book:
        df.loc[df["Title"] == book_to_update, "Status"] = new_status
        df.loc[df["Title"] == book_to_update, "Rating"] = new_rating
        df.loc[df["Title"] == book_to_update, "Review"] = new_review
        df.to_csv("library_books.csv", index=False)
        st.success("Details updated!")
        st.rerun()

# Delete a Book
st.subheader("❌ Delete a Book")
if not df.empty:
    book_to_delete = st.selectbox("Select Book to Delete", df["Title"])
    delete_book = st.button("Delete Book", key="delete_book")
    if delete_book:
        df = df[df["Title"] != book_to_delete]
        df.to_csv("library_books.csv", index=False)
        st.success("Book deleted!")
        st.rerun()

