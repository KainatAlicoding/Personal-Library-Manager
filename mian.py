import streamlit as st
import pandas as pd
import os

# CSV file path
data_file = "data/books.csv"

# Load data
def load_data():
    if os.path.exists(data_file):
        return pd.read_csv(data_file)
    else:
        return pd.DataFrame(columns=["Title", "Author", "Genre", "Rating"])

# Save data
def save_data(df):
    df.to_csv(data_file, index=False)

# App title
st.set_page_config(page_title="Books Library Manager")
st.title("📚 Books Library Manager")

# Load existing data
df = load_data()

# Sidebar filters
st.sidebar.header("📌 Filters")
genres = st.sidebar.multiselect("Select Genre", options=df["Genre"].unique())
authors = st.sidebar.multiselect("Select Author", options=df["Author"].unique())
min_rating = st.sidebar.slider("Minimum Rating", 0.0, 5.0, 0.0, 0.5)

# Filter data
filtered_df = df.copy()
if genres:
    filtered_df = filtered_df[filtered_df["Genre"].isin(genres)]
if authors:
    filtered_df = filtered_df[filtered_df["Author"].isin(authors)]
filtered_df = filtered_df[filtered_df["Rating"] >= min_rating]

# Search bar
search = st.text_input("🔍 Search Book by Title")
if search:
    filtered_df = filtered_df[filtered_df["Title"].str.contains(search, case=False)]

# Show table
st.subheader("📖 Books List")
st.dataframe(filtered_df, use_container_width=True)

# Add new book
st.subheader("➕ Add a New Book")
with st.form("book_form"):
    title = st.text_input("Title")
    author = st.text_input("Author")
    genre = st.text_input("Genre")
    rating = st.slider("Rating", 0.0, 5.0, 3.0, 0.5)
    submitted = st.form_submit_button("Add Book")
    if submitted:
        new_row = pd.DataFrame([[title, author, genre, rating]], columns=df.columns)
        df = pd.concat([df, new_row], ignore_index=True)
        save_data(df)
        st.success("Book added successfully!")
        st.experimental_rerun()

# Delete book
st.subheader("🗑️ Delete a Book")
book_to_delete = st.selectbox("Select a book to delete", options=df["Title"].unique())
if st.button("Delete Book"):
    df = df[df["Title"] != book_to_delete]
    save_data(df)
    st.success("Book deleted successfully!")
    st.experimental_rerun()