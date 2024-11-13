import tkinter as tk
from tkinter import messagebox, ttk
import psycopg2

# Connect to PostgreSQL database
def connect_db():
    try:
        conn = psycopg2.connect(
            user="postgres",    # Change to your PostgreSQL username
            password="Minh123456",  # Change to your password
            host="localhost",
            port="5432"
        )
        return conn
    except Exception as e:
        messagebox.showerror("Lỗi cơ sở dữ liệu", f"Lỗi kết nối với cơ sở dữ liệu: {e}")
        return None

# Function to add a book
def add_book():
    title = entry_title.get()
    author = entry_author.get()
    year = entry_year.get()
    genre = entry_genre.get()
    
    if not (title and author and year.isdigit() and genre):
        messagebox.showwarning("Lỗi", "Xin vui lòng điền chính xác vào tất cả các trường.")
        return
    
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO books (title, author, year, genre) VALUES (%s, %s, %s, %s)",
                    (title, author, int(year), genre))
        conn.commit()
        conn.close()
        reload_books()
        messagebox.showinfo("Thành công", "Đã thêm sách thành công.")

# Function to update selected book
def update_book():
    selected = book_tree.focus()
    if selected == "":
        messagebox.showwarning("Lỗi", "Vui lòng chọn một cuốn sách để cập nhật.")
        return
    
    title = entry_title.get()
    author = entry_author.get()
    year = entry_year.get()
    genre = entry_genre.get()

    if not (title and author and year.isdigit() and genre):
        messagebox.showwarning("Lỗi", "Vui lòng điền chính xác tất cả các trường.")
        return
    
    book_id = book_tree.item(selected)["values"][0]
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        cur.execute("UPDATE books SET title=%s, author=%s, year=%s, genre=%s WHERE id=%s",
                    (title, author, int(year), genre, book_id))
        conn.commit()
        conn.close()
        reload_books()
        messagebox.showinfo("Thành công", "Sách đã thêm thành công.")

# Function to delete selected book
def delete_book():
    selected = book_tree.focus()
    if selected == "":
        messagebox.showwarning("Lỗi", "Hãy chọn lại sách đã bị xóa.")
        return
    
    book_id = book_tree.item(selected)["values"][0]
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM books WHERE id=%s", (book_id,))
        conn.commit()
        conn.close()
        reload_books()
        messagebox.showinfo("Thành công", "Sách đã được xóa thành công.")

# Function to reload book list
def reload_books():
    for row in book_tree.get_children():
        book_tree.delete(row)
    
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM books")
        rows = cur.fetchall()
        for row in rows:book_tree.insert("", "end", values=row)
        conn.close()

# Create main window
root = tk.Tk()
root.title("Quản lý thư viện")

# Input fields
tk.Label(root, text="Tên sách").grid(row=0, column=0)
entry_title = tk.Entry(root)
entry_title.grid(row=0, column=1)

tk.Label(root, text="Tác giả").grid(row=1, column=0)
entry_author = tk.Entry(root)
entry_author.grid(row=1, column=1)

tk.Label(root, text="Năm xuất bản").grid(row=2, column=0)
entry_year = tk.Entry(root)
entry_year.grid(row=2, column=1)

tk.Label(root, text="Thể loại").grid(row=3, column=0)
entry_genre = tk.Entry(root)
entry_genre.grid(row=3, column=1)

# Buttons
btn_add = tk.Button(root, text="Thêm sách", command=add_book)
btn_add.grid(row=4, column=0)

btn_update = tk.Button(root, text="Cập nhật sách", command=update_book)
btn_update.grid(row=4, column=1)

btn_delete = tk.Button(root, text="Xóa sách", command=delete_book)
btn_delete.grid(row=4, column=2)

btn_reload = tk.Button(root, text="Khởi động lại danh sách", command=reload_books)
btn_reload.grid(row=4, column=3)

# Treeview for displaying books
book_tree = ttk.Treeview(root, columns=("ID", "Title", "Author", "Year", "Genre"), show="headings")
book_tree.heading("ID", text="ID")
book_tree.heading("Title", text="Tên sách")
book_tree.heading("Author", text="Tác giả")
book_tree.heading("Year", text="Năm xuất bản")
book_tree.heading("Genre", text="Thể loại")
book_tree.grid(row=5, column=0, columnspan=4)

# Initialize the book list
reload_books()

root.mainloop()