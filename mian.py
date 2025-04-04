import streamlit as st
import pandas as pd

# Sample Data (same as CSV content, but embedded)
sample_data = [
    {"Title": "The Alchemist", "Author": "Paulo Coelho", "Genre": "Fiction", "Rating": 4.5},
    {"Title": "Atomic Habits", "Author": "James Clear", "Genre": "Self-help", "Rating": 4.8},
    {"Title": "1984", "Author": "George Orwell", "Genre": "Dystopian", "Rating": 4.4},
    {"Title": "Sapiens", "Author": "Yuval Noah Harari", "Genre": "History", "Rating": 4.6},
    {"Title": "Clean Code", "Author": "Robert C. Martin", "Genre": "Programming", "Rating": 4.7},
]

# Use session state to store book data
if "books" not in st.session_state:
    st.session_state.books = pd.DataFrame(sample_data)

df = st.session_state.books

st.set_page_config(page_title="Books Library Manager")
st.title("📚 Books Library Manager")

# Sidebar Filters
st.sidebar.header("📌 Filters")
genres = st.sidebar.multiselect("Select Genre", options=df["Genre"].unique())
authors = st.sidebar.multiselect("Select Author", options=df["Author"].unique())
min_rating = st.sidebar.slider("Minimum Rating", 0.0, 5.0, 0.0, 0.5)

# Apply filters
filtered_df = df.copy()
if genres:
    filtered_df = filtered_df[filtered_df["Genre"].isin(genres)]
if authors:
    filtered_df = filtered_df[filtered_df["Author"].isin(authors)]
filtered_df = filtered_df[filtered_df["Rating"] >= min_rating]

# Search Bar
search = st.text_input("🔍 Search Book by Title")
if search:
    filtered_df = filtered_df[filtered_df["Title"].str.contains(search, case=False)]

# Show Table
st.subheader("📖 Books List")
st.dataframe(filtered_df, use_container_width=True)

# Add Book
st.subheader("➕ Add a New Book")
with st.form("add_book"):
    title = st.text_input("Title")
    author = st.text_input("Author")
    genre = st.text_input("Genre")
    rating = st.slider("Rating", 0.0, 5.0, 3.0, 0.5)
    submitted = st.form_submit_button("Add Book")
    if submitted:
        new_row = pd.DataFrame([[title, author, genre, rating]], columns=df.columns)
        st.session_state.books = pd.concat([df, new_row], ignore_index=True)
        st.success("Book added successfully!")
        st.experimental_rerun()

# Delete Book
st.subheader("🗑️ Delete a Book")
book_to_delete = st.selectbox("Select a book to delete", options=df["Title"].unique())
if st.button("Delete Book"):
    st.session_state.books = df[df["Title"] != book_to_delete]
    st.success("Book deleted successfully!")
    st.experimental_rerun()
