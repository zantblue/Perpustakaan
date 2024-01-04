import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import ttk

registered_members = []

class RegistrationDialog(simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="Username:").grid(row=0)
        tk.Label(master, text="Password:").grid(row=1)
        tk.Label(master, text="Pelajar (Y/N):").grid(row=2)
        tk.Label(master, text="Alamat:").grid(row=3)

        self.username_entry = tk.Entry(master)
        self.password_entry = tk.Entry(master, show="*")
        self.pelajar_var = tk.StringVar(value="N")
        self.pelajar_entry = ttk.Combobox(master, textvariable=self.pelajar_var, values=["Y", "N"])
        self.alamat_entry = tk.Entry(master)

        self.username_entry.grid(row=0, column=1)
        self.password_entry.grid(row=1, column=1)
        self.pelajar_entry.grid(row=2, column=1)
        self.alamat_entry.grid(row=3, column=1)

    def validate(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        pelajar = self.pelajar_var.get()
        alamat = self.alamat_entry.get()

        if not (username and password and pelajar and alamat):
            messagebox.showwarning("Peringatan", "Semua kolom harus diisi.")
            return False

        return True

    def apply(self):
        if not self.validate():
            return

        self.result = (
            self.username_entry.get(),
            self.password_entry.get(),
            self.pelajar_var.get(),
            self.alamat_entry.get()
        )
        
class LibrarySystem:
    def __init__(self, root, registered_members):
        self.root = root
        self.root.title("Sistem Perpustakaan")
        self.root.geometry("600x400")

        self.is_admin = False
        self.logged_in_user = None
        self.books = []
        self.members = registered_members  # Menggunakan daftar member yang disimpan secara global
        self.current_member_name = None  # Penanda untuk menyimpan nama anggota yang sedang digunakan

        self.create_login_screen()

    def create_login_screen(self):
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(pady=20)

        tk.Label(self.login_frame, text="Login sebagai:").grid(row=0, column=0, padx=10, pady=10)

        tk.Button(self.login_frame, text="Admin", command=self.admin_login).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(self.login_frame, text="Member", command=self.member_login).grid(row=1, column=1, padx=10, pady=10)

    def admin_login(self):
         # Tambahkan logika login admin di sini (gunakan username dan password)
        # Misalnya, untuk tujuan demonstrasi, kita anggap admin selalu berhasil login
        username = simpledialog.askstring("Login Admin", "Masukkan username admin:")
        password = simpledialog.askstring("Login Admin", "Masukkan password admin:")

        # Contoh validasi admin (username=admin, password=admin123)
        if username == "admin" and password == "admin123":
            self.is_admin = True
            self.create_admin_dashboard()
        else:
            messagebox.showwarning("Peringatan", "Login admin gagal. Coba lagi.")

    def member_login(self):
        # Tambahkan logika login atau register member di sini
        option = messagebox.askquestion("Login Member", "Apakah Anda sudah memiliki akun?")
        
        if option == 'yes':
            # Login
            username = simpledialog.askstring("Login Member", "Masukkan username member:")
            password = simpledialog.askstring("Login Member", "Masukkan password member:")
            
            # Contoh validasi member (gantilah dengan cara validasi yang sesuai)
            for member in self.members:
                if member['name'] == username and member['password'] == password:
                    self.is_admin = False
                    self.logged_in_user = member
                    self.current_member_name = member['name']  # Menyimpan nama anggota yang sedang digunakan
                    self.create_member_dashboard()
                    return
            messagebox.showwarning("Peringatan", "Login member gagal. Coba lagi.")
        else:
            # Register
            registration_dialog = RegistrationDialog(self.root)
            result = registration_dialog.result

            if result:
                new_username, new_password, is_student_str, address = result

                # Validasi apakah semua kolom telah diisi
                if not (new_username and new_password and is_student_str and address):
                    messagebox.showwarning("Peringatan", "Semua kolom harus diisi.")
                    return

                is_student = is_student_str.upper() == 'Y'

                # Simpan data member yang baru terdaftar
                new_member = {"name": new_username, "password": new_password, "address": address, "is_student": is_student}
                self.members.append(new_member)

                # Set username dan password untuk keperluan login
                username = new_username
                password = new_password

                self.is_admin = False
                self.logged_in_user = new_member
                self.create_member_dashboard()
    
    def show_registered_members(self):
        if self.is_admin:
            member_info = ""
            for i, member in enumerate(self.members, 1):
                member_info += f"Member {i}:\n"
                member_info += f"  Nama: {member['name']}\n"
                member_info += f"  Alamat: {member['address']}\n"
                member_info += f"  Status: {'Pelajar' if member['is_student'] else 'Bekerja'}\n"
            
            if member_info:
                messagebox.showinfo("Daftar Member Terdaftar", member_info)
            else:
                messagebox.showinfo("Daftar Member Terdaftar", "Belum ada member terdaftar.")
        else:
            messagebox.showwarning("Peringatan", "Anda bukan admin. Hak akses terbatas.")
        
    def create_admin_dashboard(self):
        self.login_frame.destroy()

        self.admin_frame = tk.Frame(self.root)
        self.admin_frame.pack(pady=20)

        tk.Label(self.admin_frame, text="Admin Dashboard").grid(row=0, column=0, padx=10, pady=10)
        tk.Button(self.admin_frame, text="Tambah Buku", command=self.add_book).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(self.admin_frame, text="Hapus Buku", command=self.remove_book).grid(row=2, column=0, padx=10, pady=10)
        tk.Button(self.admin_frame, text="Update Status Buku", command=self.update_book_status).grid(row=3, column=0, padx=10, pady=10)
        tk.Button(self.admin_frame, text="Lihat Member", command=self.show_members).grid(row=4, column=0, padx=10, pady=10)
        tk.Button(self.admin_frame, text="Lihat Daftar Member", command=self.show_registered_members).grid(row=5, column=0, padx=10, pady=10)
        tk.Button(self.admin_frame, text="Lihat Daftar Buku", command=self.show_books).grid(row=6, column=0, padx=10, pady=10)
        tk.Button(self.admin_frame, text="Logout", command=self.logout_admin).grid(row=7, column=0, padx=10, pady=10)

    def add_book(self):
        title = simpledialog.askstring("Tambah Buku", "Masukkan judul buku:")
        author = simpledialog.askstring("Tambah Buku", "Masukkan pengarang buku:")
        pages = simpledialog.askinteger("Tambah Buku", "Masukkan jumlah halaman buku:")
        shelf = simpledialog.askinteger("Tambah Buku", "Masukkan rak buku:")
        isbn = simpledialog.askstring("Tambah Buku", "Masukkan ISBN buku:")

        book_info = {"title": title, "author": author, "pages": pages, "shelf": shelf, "isbn": isbn, "status": "Tersedia"}
        self.books.append(book_info)
        messagebox.showinfo("Info", "Buku berhasil ditambahkan!")

    def remove_book(self):
        title = simpledialog.askstring("Hapus Buku", "Masukkan judul buku yang akan dihapus:")
        for book in self.books:
            if book["title"] == title:
                self.books.remove(book)
                messagebox.showinfo("Info", f"Buku '{title}' berhasil dihapus!")
                return
        messagebox.showwarning("Peringatan", f"Buku '{title}' tidak ditemukan!")

    def update_book_status(self):
        title = simpledialog.askstring("Update Status Buku", "Masukkan judul buku:")
        status = simpledialog.askstring("Update Status Buku", "Masukkan status baru (Tersedia/Tidak Tersedia):").capitalize()
        for book in self.books:
            if book["title"] == title:
                book["status"] = status
                messagebox.showinfo("Info", f"Status buku '{title}' berhasil diupdate menjadi {status}.")
                return
        messagebox.showwarning("Peringatan", f"Buku '{title}' tidak ditemukan!")

    def show_members(self):
        if self.is_admin:
            member_info = ""
            for member in self.members:
                member_info += f"Nama: {member['name']}, Alamat: {member['address']}, Status: {'Pelajar' if member['is_student'] else 'Bekerja'}\n"
            
            if member_info:
                messagebox.showinfo("Anggota Perpustakaan", member_info)
            else:
                messagebox.showinfo("Anggota Perpustakaan", "Belum ada anggota perpustakaan terdaftar.")
        else:
            messagebox.showwarning("Peringatan", "Anda bukan admin. Hak akses terbatas.")

    def create_member_dashboard(self):
        self.login_frame.destroy()

        self.member_frame = tk.Frame(self.root)
        self.member_frame.pack(pady=20)

        # Cek apakah anggota sudah login atau belum, jika sudah, tampilkan informasi anggota yang sedang digunakan
        if self.logged_in_user:
            tk.Label(self.member_frame, text=f"Akun yang digunakan: {self.logged_in_user['name']}").grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.member_frame, text="Member Dashboard").grid(row=0, column=0, padx=10, pady=10)
        tk.Button(self.member_frame, text="Pinjam Buku", command=self.borrow_book).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(self.member_frame, text="Kembalikan Buku", command=self.return_book).grid(row=2, column=0, padx=10, pady=10)
        tk.Button(self.member_frame, text="Lihat Daftar Buku", command=self.show_books).grid(row=3, column=0, padx=10, pady=10)
        tk.Button(self.member_frame, text="Logout", command=self.logout_member).grid(row=4, column=0, padx=10, pady=10)
        
    def show_books(self):
        books_info = ""
        for book in self.books:
            books_info += f"Judul: {book['title']}, Pengarang: {book['author']}, Status: {book['status']}\n"

        if books_info:
            messagebox.showinfo("Daftar Buku", books_info)
        else:
            messagebox.showinfo("Daftar Buku", "Belum ada buku yang ditambahkan.")

    def borrow_book(self):
        title = simpledialog.askstring("Pinjam Buku", "Masukkan judul buku yang akan dipinjam:")
        for book in self.books:
            if book["title"] == title and book["status"] == "Tersedia":
                book["status"] = "Dipinjam"
                book["borrower"] = self.current_member_name  # Menyimpan nama peminjam di informasi buku
                messagebox.showinfo("Info", f"Buku '{title}' berhasil dipinjam oleh {self.current_member_name}!")
                return
        messagebox.showwarning("Peringatan", f"Buku '{title}' tidak tersedia atau tidak ditemukan!")

    def return_book(self):
        if not self.logged_in_user:
            messagebox.showwarning("Peringatan", "Anda belum login. Silakan login terlebih dahulu.")
            return

        title = simpledialog.askstring("Kembalikan Buku", "Masukkan judul buku yang akan dikembalikan:")
        for book in self.books:
            if (
                book["title"] == title
                and book["status"] == "Dipinjam"
                and book["borrower"] == self.logged_in_user["name"]
            ):
                book["status"] = "Tersedia"
                book["borrower"] = None
                messagebox.showinfo(
                    "Info",
                    f"Buku '{title}' berhasil dikembalikan oleh {self.logged_in_user['name']}. Status buku diubah menjadi Tersedia.",
                )
                return
        messagebox.showwarning(
            "Peringatan",
            f"Buku '{title}' tidak dapat dikembalikan dikarenakan bukan anda yang meminjam",
        )
        
    def logout_admin(self):
        self.admin_frame.destroy()
        self.is_admin = False
        self.create_login_screen()

    def logout_member(self):
        self.member_frame.destroy()
        self.logged_in_user = None
        self.create_login_screen()

if __name__ == "__main__":
    registered_members = []

    root = tk.Tk()
    app = LibrarySystem(root, registered_members)
    root.mainloop()

