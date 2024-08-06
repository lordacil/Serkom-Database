import os
import mysql.connector
from mysql.connector import errorcode
import hashlib
from prettytable import PrettyTable
from colorama import init, Fore, Style, Back
import time

# Inisialisasi colorama untuk warna terminal
init()

def clear_screen():
    # Membersihkan terminal untuk Windows atau Linux/macOS
    os.system('cls' if os.name == 'nt' else 'clear')

def create_connection():
    # Membuat koneksi ke database MySQL
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='perpustakaan',
            charset='utf8mb4',
            collation='utf8mb4_general_ci'
        )
        return connection
    except mysql.connector.Error as err:
        # Menangani kesalahan koneksi
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print(Fore.RED + "Something is wrong with your user name or password" + Style.RESET_ALL)
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print(Fore.RED + "Database does not exist" + Style.RESET_ALL)
        else:
            print(Fore.RED + str(err) + Style.RESET_ALL)
        return None

def hash_password(password):
    # Meng-hash password menggunakan SHA-256
    return hashlib.sha256(password.encode()).hexdigest()

def register():
    # Fungsi untuk registrasi pengguna baru
    clear_screen()
    print("\n================================")
    print(Fore.BLUE+"Silahkan isi data sesuai format!"+Style.RESET_ALL+Style.BRIGHT)
    print("================================\n")

    username = input("Masukkan username: ")
    password = input("Masukkan password: ")
    nama = input("Masukkan nama anggota: ")
    alamat = input("Masukkan alamat: ")
    tanggal_lahir = input("Masukkan tanggal lahir (YYYY-MM-DD): ")
    email = input("Masukkan email: ")

    connection = create_connection()
    cursor = connection.cursor()

    # Query untuk menambahkan data anggota baru
    sql_anggota = "INSERT INTO Anggota (nama, alamat, tanggal_lahir, email) VALUES (%s, %s, %s, %s)"
    val_anggota = (nama, alamat, tanggal_lahir, email)
    cursor.execute(sql_anggota, val_anggota)
    anggota_id = cursor.lastrowid

    # Query untuk menambahkan data user baru dengan role 'anggota'
    sql_user = "INSERT INTO Users (username, password, anggota_id, role) VALUES (%s, %s, %s, 'anggota')"
    val_user = (username, hash_password(password), anggota_id)
    cursor.execute(sql_user, val_user)

    connection.commit()
    cursor.close()
    connection.close()
    print(Fore.GREEN + "\n[ Pendaftaran berhasil! ]" + Style.RESET_ALL)
    time.sleep(2)
    clear_screen()

def login():
    # Fungsi untuk login pengguna
    clear_screen()
    print("\n==================================")
    print(Fore.BLUE+"Silahkan masukan data untuk Login!"+Style.RESET_ALL+Style.BRIGHT)
    print("==================================\n")

    username = input("Masukkan username: ")
    password = input("Masukkan password: ")

    connection = create_connection()
    cursor = connection.cursor()

    # Query untuk mengambil data user berdasarkan username
    sql = "SELECT password, anggota_id, role, (SELECT nama FROM Anggota WHERE id = Users.anggota_id) as nama FROM Users WHERE username = %s"
    cursor.execute(sql, (username,))
    result = cursor.fetchone()

    # Memeriksa apakah password sesuai
    if result and result[0] == hash_password(password):
        print(Fore.GREEN + "\n[ Login berhasil! ]" + Style.RESET_ALL)
        time.sleep(2)
        clear_screen()
        return result[1], result[2], result[3]
    else:
        print(Fore.RED + "\n[ Username atau password salah! ]" + Style.RESET_ALL)
        time.sleep(2)
        clear_screen()
        return None, None, None

def add_kategori():
    # Fungsi untuk menambahkan kategori buku baru
    clear_screen()
    nama = input("Masukkan nama kategori buku: ")
    connection = create_connection()
    cursor = connection.cursor()
    
    # Query untuk menambahkan data kategori baru
    sql = "INSERT INTO Kategori (nama) VALUES (%s)"
    val = (nama,)
    cursor.execute(sql, val)
    connection.commit()
    cursor.close()
    connection.close()
    print(Fore.GREEN + "\n[ Kategori berhasil ditambahkan! ]" + Style.RESET_ALL)
    time.sleep(2)
    clear_screen()

def add_buku():
    # Fungsi untuk menambahkan buku baru
    clear_screen()
    connection = create_connection()
    cursor = connection.cursor()

    # Tampilkan daftar kategori untuk referensi pengguna
    cursor.execute("SELECT id, nama FROM Kategori")
    kategori_result = cursor.fetchall()
    print(Style.BRIGHT+"Daftar Kategori Buku:")
    table_kategori = PrettyTable(["ID", "Nama"])
    for row in kategori_result:
        table_kategori.add_row(row)
    print(table_kategori.get_string())

    print("")
    judul = input("Masukkan judul buku: ")
    pengarang = input("Masukkan pengarang: ")
    tahun_terbit = input("Masukkan tahun terbit: ")
    kategori_id = input("Masukkan ID kategori: ")

    # Cek apakah ID kategori ada di database
    if kategori_id.strip() == "":
        print(Fore.RED + "ID kategori tidak boleh kosong!" + Style.RESET_ALL)
    else:
        cursor.execute("SELECT COUNT(*) FROM Kategori WHERE id = %s", (kategori_id,))
        count = cursor.fetchone()[0]
        if count == 0:
            print(Fore.RED + "\n[ ID kategori tidak ditemukan! ]" + Style.RESET_ALL)
        else:
            # Query untuk menambahkan data buku baru
            sql = "INSERT INTO Buku (judul, pengarang, tahun_terbit, kategori_id) VALUES (%s, %s, %s, %s)"
            val = (judul, pengarang, tahun_terbit, kategori_id)
            cursor.execute(sql, val)
            connection.commit()
            print(Fore.GREEN + "\n[ Buku berhasil ditambahkan! ]" + Style.RESET_ALL)

    cursor.close()
    connection.close()
    time.sleep(2)
    clear_screen()

def add_anggota():
    # Fungsi untuk menambahkan anggota baru
    clear_screen()
    nama = input("Masukkan nama anggota: ")
    alamat = input("Masukkan alamat: ")
    tanggal_lahir = input("Masukkan tanggal lahir (YYYY-MM-DD): ")
    email = input("Masukkan email: ")
    connection = create_connection()
    cursor = connection.cursor()
    
    # Query untuk menambahkan data anggota baru
    sql = "INSERT INTO Anggota (nama, alamat, tanggal_lahir, email) VALUES (%s, %s, %s, %s)"
    val = (nama, alamat, tanggal_lahir, email)
    cursor.execute(sql, val)
    connection.commit()
    cursor.close()
    connection.close()
    print(Fore.GREEN + "\n[ Anggota berhasil ditambahkan! ]" + Style.RESET_ALL)
    time.sleep(2)
    clear_screen()

def add_peminjaman(anggota_id, nama):
    # Fungsi untuk menambahkan peminjaman baru
    clear_screen()
    connection = create_connection()
    cursor = connection.cursor()

    # Tampilkan daftar buku untuk referensi pengguna
    cursor.execute("SELECT id, judul FROM Buku")
    buku_result = cursor.fetchall()
    print(Style.BRIGHT+"Daftar Buku:")
    table_buku = PrettyTable(["ID", "Judul"])
    for row in buku_result:
        table_buku.add_row(row)
    print(table_buku.get_string())

    buku_id = input("Masukkan ID buku: ")
    tanggal_pinjam = input("Masukkan tanggal pinjam (YYYY-MM-DD): ")
    tanggal_kembali = input("Masukkan tanggal kembali (YYYY-MM-DD): ")

    # Cek apakah ID buku ada di database
    if buku_id.strip() == "":
        print(Fore.RED + "ID buku tidak boleh kosong!" + Style.RESET_ALL)
    else:
        cursor.execute("SELECT COUNT(*) FROM Buku WHERE id = %s", (buku_id,))
        count = cursor.fetchone()[0]
        if count == 0:
            print(Fore.RED + "\n[ ID buku tidak ditemukan! ]" + Style.RESET_ALL)
        else:
            # Query untuk menambahkan data peminjaman baru
            sql = "INSERT INTO Peminjaman (buku_id, anggota_id, tanggal_pinjam, tanggal_kembali) VALUES (%s, %s, %s, %s)"
            val = (buku_id, anggota_id, tanggal_pinjam, tanggal_kembali)
            cursor.execute(sql, val)
            connection.commit()
            print(Fore.GREEN + "\n[ Peminjaman berhasil ditambahkan! ]" + Style.RESET_ALL)

    cursor.close()
    connection.close()
    time.sleep(2)
    clear_screen()

def show_buku():
    # Fungsi untuk menampilkan daftar buku
    clear_screen()
    connection = create_connection()
    cursor = connection.cursor()
    
    # Query untuk mengambil data buku
    cursor.execute("""
        SELECT Buku.id, Buku.judul, Buku.pengarang, Buku.tahun_terbit, Kategori.nama as kategori
        FROM Buku
        JOIN Kategori ON Buku.kategori_id = Kategori.id
    """)
    result = cursor.fetchall()
    
    # Menampilkan data buku dalam tabel
    table = PrettyTable(["ID", "Judul", "Pengarang", "Tahun Terbit", "Kategori"])
    for row in result:
        table.add_row(row)
    print(table)
    cursor.close()
    connection.close()
    input(Fore.YELLOW + "Tekan Enter untuk kembali ke menu utama..." + Style.RESET_ALL)
    clear_screen()

def show_anggota():
    # Fungsi untuk menampilkan daftar anggota
    clear_screen()
    connection = create_connection()
    cursor = connection.cursor()
    
    # Query untuk mengambil data anggota
    cursor.execute("SELECT * FROM Anggota")
    result = cursor.fetchall()
    
    # Menampilkan data anggota dalam tabel
    table = PrettyTable(["ID", "Nama", "Alamat", "Tanggal Lahir", "Email"])
    for row in result:
        table.add_row(row)
    print(table)
    cursor.close()
    connection.close()
    input(Fore.YELLOW + "Tekan Enter untuk kembali ke menu utama..." + Style.RESET_ALL)
    clear_screen()

def show_peminjaman(anggota_id=None):
    # Fungsi untuk menampilkan daftar peminjaman
    clear_screen()
    connection = create_connection()
    cursor = connection.cursor()
    
    # Query untuk mengambil data peminjaman
    if anggota_id:
        cursor.execute("""
            SELECT Peminjaman.id, Buku.judul, Anggota.nama, Peminjaman.tanggal_pinjam, Peminjaman.tanggal_kembali
            FROM Peminjaman
            JOIN Buku ON Peminjaman.buku_id = Buku.id
            JOIN Anggota ON Peminjaman.anggota_id = Anggota.id
            WHERE Peminjaman.anggota_id = %s
        """, (anggota_id,))
    else:
        cursor.execute("""
            SELECT Peminjaman.id, Buku.judul, Anggota.nama, Peminjaman.tanggal_pinjam, Peminjaman.tanggal_kembali
            FROM Peminjaman
            JOIN Buku ON Peminjaman.buku_id = Buku.id
            JOIN Anggota ON Peminjaman.anggota_id = Anggota.id
        """)
    result = cursor.fetchall()
    
    # Menampilkan data peminjaman dalam tabel
    table = PrettyTable(["ID", "Buku", "Anggota", "Tanggal Pinjam", "Tanggal Kembali"])
    for row in result:
        table.add_row(row)
    print(table)
    cursor.close()
    connection.close()
    input(Fore.YELLOW + "Tekan Enter untuk kembali ke menu utama..." + Style.RESET_ALL)
    clear_screen()

def delete_peminjaman():
    # Fungsi untuk menghapus data peminjaman
    clear_screen()
    connection = create_connection()
    cursor = connection.cursor()

    # Tampilkan daftar peminjaman untuk referensi pengguna
    cursor.execute("""
        SELECT Peminjaman.id, Buku.judul, Anggota.nama, Peminjaman.tanggal_pinjam, Peminjaman.tanggal_kembali
        FROM Peminjaman
        JOIN Buku ON Peminjaman.buku_id = Buku.id
        JOIN Anggota ON Peminjaman.anggota_id = Anggota.id
    """)
    peminjaman_result = cursor.fetchall()
    print(Style.BRIGHT+"Daftar Peminjaman:")
    table_peminjaman = PrettyTable(["ID", "Buku", "Anggota", "Tanggal Pinjam", "Tanggal Kembali"])
    for row in peminjaman_result:
        table_peminjaman.add_row(row)
    print(table_peminjaman.get_string())

    print("")
    peminjaman_id = input("Masukkan ID peminjaman yang ingin dihapus: ")

    # Cek apakah ID peminjaman ada di database
    cursor.execute("SELECT COUNT(*) FROM Peminjaman WHERE id = %s", (peminjaman_id,))
    count = cursor.fetchone()[0]
    if count == 0:
        print(Fore.RED + "\n[ ID peminjaman tidak ditemukan! ]" + Style.RESET_ALL)
    else:
        # Query untuk menghapus data peminjaman
        sql = "DELETE FROM Peminjaman WHERE id = %s"
        cursor.execute(sql, (peminjaman_id,))
        connection.commit()
        print(Fore.GREEN + "\n[ Peminjaman berhasil dihapus! ]" + Style.RESET_ALL)

    cursor.close()
    connection.close()
    time.sleep(2)
    clear_screen()

def delete_buku():
    # Fungsi untuk menghapus data buku
    clear_screen()
    connection = create_connection()
    cursor = connection.cursor()

    # Tampilkan daftar buku untuk referensi pengguna
    cursor.execute("SELECT id, judul FROM Buku")
    buku_result = cursor.fetchall()
    print(Style.BRIGHT+"Daftar Buku:")
    table_buku = PrettyTable(["ID", "Judul"])
    for row in buku_result:
        table_buku.add_row(row)
    print(table_buku.get_string())

    print("")
    buku_id = input("Masukkan ID buku yang ingin dihapus: ")

    # Cek apakah ID buku ada di database
    cursor.execute("SELECT COUNT(*) FROM Buku WHERE id = %s", (buku_id,))
    count = cursor.fetchone()[0]
    if count == 0:
        print(Fore.RED + "\n[ ID buku tidak ditemukan! ]" + Style.RESET_ALL)
    else:
        # Hapus data peminjaman terkait buku
        cursor.execute("DELETE FROM Peminjaman WHERE buku_id = %s", (buku_id,))
        # Query untuk menghapus data buku
        cursor.execute("DELETE FROM Buku WHERE id = %s", (buku_id,))
        connection.commit()
        print(Fore.GREEN + "\n[ Buku berhasil dihapus! ]" + Style.RESET_ALL)
    
    cursor.close()
    connection.close()
    time.sleep(2)
    clear_screen()

def delete_anggota():
    # Fungsi untuk menghapus data anggota
    clear_screen()
    connection = create_connection()
    cursor = connection.cursor()

    # Tampilkan daftar anggota untuk referensi pengguna
    cursor.execute("SELECT id, nama FROM Anggota")
    anggota_result = cursor.fetchall()
    print(Style.BRIGHT+"Daftar Anggota:")
    table_anggota = PrettyTable(["ID", "Nama"])
    for row in anggota_result:
        table_anggota.add_row(row)
    print(table_anggota.get_string())

    print("")
    anggota_id = input("Masukkan ID anggota yang ingin dihapus: ")

    # Cek apakah ID anggota ada di database
    cursor.execute("SELECT COUNT(*) FROM Anggota WHERE id = %s", (anggota_id,))
    count = cursor.fetchone()[0]
    if count == 0:
        print(Fore.RED + "\n[ ID anggota tidak ditemukan! ]" + Style.RESET_ALL)
    else:
        # Hapus data di tabel Users yang berelasi dengan anggota
        cursor.execute("DELETE FROM Users WHERE anggota_id = %s", (anggota_id,))
        # Hapus data peminjaman terkait anggota
        cursor.execute("DELETE FROM Peminjaman WHERE anggota_id = %s", (anggota_id,))
        # Query untuk menghapus data anggota
        cursor.execute("DELETE FROM Anggota WHERE id = %s", (anggota_id,))
        connection.commit()
        print(Fore.GREEN + "\n[ Anggota berhasil dihapus! ]" + Style.RESET_ALL)
    
    cursor.close()
    connection.close()
    time.sleep(2)
    clear_screen()

def show_buku_sorted(order_by):
    # Fungsi untuk menampilkan daftar buku dengan urutan tertentu
    clear_screen()
    connection = create_connection()
    cursor = connection.cursor()
    
    # Tentukan urutan berdasarkan parameter order_by
    if order_by == "judul":
        cursor.execute("""
            SELECT Buku.id, Buku.judul, Buku.pengarang, Buku.tahun_terbit, Kategori.nama as kategori
            FROM Buku
            JOIN Kategori ON Buku.kategori_id = Kategori.id
            ORDER BY Buku.judul
        """)
    elif order_by == "tahun_terbit":
        cursor.execute("""
            SELECT Buku.id, Buku.judul, Buku.pengarang, Buku.tahun_terbit, Kategori.nama as kategori
            FROM Buku
            JOIN Kategori ON Buku.kategori_id = Kategori.id
            ORDER BY Buku.tahun_terbit
        """)
    
    result = cursor.fetchall()
    
    # Menampilkan data buku dalam tabel
    table = PrettyTable(["ID", "Judul", "Pengarang", "Tahun Terbit", "Kategori"])
    for row in result:
        table.add_row(row)
    print(table)
    cursor.close()
    connection.close()
    input(Fore.YELLOW + "Tekan Enter untuk kembali ke menu utama..." + Style.RESET_ALL)
    clear_screen()

def search_buku():
    # Fungsi untuk mencari buku berdasarkan kata kunci judul
    clear_screen()
    keyword = input("Masukkan kata kunci untuk mencari buku: ")
    connection = create_connection()
    cursor = connection.cursor()
    
    # Query untuk mencari data buku berdasarkan kata kunci
    cursor.execute("""
        SELECT Buku.id, Buku.judul, Buku.pengarang, Buku.tahun_terbit, Kategori.nama as kategori
        FROM Buku
        JOIN Kategori ON Buku.kategori_id = Kategori.id
        WHERE Buku.judul LIKE %s
    """, ("%"+keyword+"%",))
    
    result = cursor.fetchall()
    
    # Menampilkan data buku dalam tabel
    table = PrettyTable(["ID", "Judul", "Pengarang", "Tahun Terbit", "Kategori"])
    for row in result:
        table.add_row(row)
    print(table)
    cursor.close()
    connection.close()
    input(Fore.YELLOW + "Tekan Enter untuk kembali ke menu utama..." + Style.RESET_ALL)
    clear_screen()

def update_anggota():
    # Fungsi untuk memperbarui data anggota
    clear_screen()
    connection = create_connection()
    cursor = connection.cursor()

    # Tampilkan daftar anggota untuk referensi pengguna
    cursor.execute("SELECT id, nama, alamat, tanggal_lahir, email FROM Anggota")
    anggota_result = cursor.fetchall()
    print(Style.BRIGHT+"Daftar Anggota:")
    table_anggota = PrettyTable(["ID", "Nama", "Alamat", "Tanggal Lahir", "Email"])
    for row in anggota_result:
        table_anggota.add_row(row)
    print(table_anggota.get_string())

    print("")
    anggota_id = input("Masukkan ID anggota yang ingin diperbarui: ")

    # Cek apakah ID anggota ada di database
    cursor.execute("SELECT COUNT(*) FROM Anggota WHERE id = %s", (anggota_id,))
    count = cursor.fetchone()[0]
    if count == 0:
        print(Fore.RED + "\n[ ID anggota tidak ditemukan! ]" + Style.RESET_ALL)
    else:
        nama = input("Masukkan nama baru: ")
        alamat = input("Masukkan alamat baru: ")
        tanggal_lahir = input("Masukkan tanggal lahir baru (YYYY-MM-DD): ")
        email = input("Masukkan email baru: ")

        # Query untuk memperbarui data anggota
        sql = """
        UPDATE Anggota
        SET nama = %s, alamat = %s, tanggal_lahir = %s, email = %s
        WHERE id = %s
        """
        val = (nama, alamat, tanggal_lahir, email, anggota_id)
        cursor.execute(sql, val)
        connection.commit()
        print(Fore.GREEN + "\n[ Anggota berhasil diperbarui! ]" + Style.RESET_ALL)
    
    cursor.close()
    connection.close()
    time.sleep(2)
    clear_screen()

def update_buku():
    # Fungsi untuk memperbarui data buku
    clear_screen()
    connection = create_connection()
    cursor = connection.cursor()

    # Tampilkan daftar buku untuk referensi pengguna
    cursor.execute("SELECT id, judul, pengarang, tahun_terbit, kategori_id FROM Buku")
    buku_result = cursor.fetchall()
    print(Style.BRIGHT+"Daftar Buku:")
    table_buku = PrettyTable(["ID", "Judul", "Pengarang", "Tahun Terbit", "Kategori ID"])
    for row in buku_result:
        table_buku.add_row(row)
    print(table_buku.get_string())

    buku_id = input("Masukkan ID buku yang ingin diperbarui: ")

    # Cek apakah ID buku ada di database
    cursor.execute("SELECT COUNT(*) FROM Buku WHERE id = %s", (buku_id,))
    count = cursor.fetchone()[0]
    if count == 0:
        print(Fore.RED + "ID buku tidak ditemukan!" + Style.RESET_ALL)
    else:
        judul = input("Masukkan judul buku baru: ")
        pengarang = input("Masukkan pengarang baru: ")
        tahun_terbit = input("Masukkan tahun terbit baru: ")

        # Tampilkan daftar kategori untuk referensi pengguna
        cursor.execute("SELECT id, nama FROM Kategori")
        kategori_result = cursor.fetchall()
        print(Style.BRIGHT+"Daftar Kategori:")
        table_kategori = PrettyTable(["ID", "Nama"])
        for row in kategori_result:
            table_kategori.add_row(row)
        print(table_kategori.get_string())

        print("")
        kategori_id = input("Masukkan ID kategori baru: ")

        # Cek apakah ID kategori ada di database
        cursor.execute("SELECT COUNT(*) FROM Kategori WHERE id = %s", (kategori_id,))
        count = cursor.fetchone()[0]
        if count == 0:
            print(Fore.RED + "\n[ ID kategori tidak ditemukan! ]" + Style.RESET_ALL)
        else:
            # Query untuk memperbarui data buku
            sql = """
            UPDATE Buku
            SET judul = %s, pengarang = %s, tahun_terbit = %s, kategori_id = %s
            WHERE id = %s
            """
            val = (judul, pengarang, tahun_terbit, kategori_id, buku_id)
            cursor.execute(sql, val)
            connection.commit()
            print(Fore.GREEN + "\n[ Buku berhasil diperbarui! ]" + Style.RESET_ALL)
    
    cursor.close()
    connection.close()
    time.sleep(2)
    clear_screen()

def admin_menu(nama):
    # Menu untuk admin
    while True:
        clear_screen()
        print(Style.BRIGHT,Fore.BLUE+"Selamat Datang Admin,"+Style.RESET_ALL+Style.BRIGHT)
        print("➤"+Fore.GREEN+nama+Style.RESET_ALL,Style.BRIGHT)
        print("===========================================")
        print("| "+Fore.RED+"\t\tMenu Buku:\t\t"+Style.RESET_ALL+Style.BRIGHT+"  |")
        print("===========================================")
        print(" [1] Tambah Kategori Buku")
        print(" [2] Tambah Buku")
        print(" [3] Lihat Buku")
        print(" [4] Hapus Buku")
        print(" [5] Update Buku")
        print(" [6] Cari Buku")
        print(" [7] Lihat Buku Terurut Berdasarkan Judul")
        print(" [8] Lihat Buku Terurut Berdasarkan Tahun Terbit")
        print("===========================================")
        print("| "+Fore.RED+"\t\tMenu Anggota:\t\t"+Style.RESET_ALL+Style.BRIGHT+"  |")
        print("===========================================")
        print(" [9] Daftar Anggota")
        print(" [10] Lihat Anggota")
        print(" [11] Hapus Anggota")
        print(" [12] Update Anggota")
        print(" [13] Lihat Peminjaman")
        print(" [14] Hapus Peminjaman")
        print(" [0] Keluar")
        print("===========================================")
        choice = input("\nPilih menu\n-> ")

        if choice == '1':
            add_kategori()
        elif choice == '2':
            add_buku()
        elif choice == '3':
            show_buku()
        elif choice == '4':
            delete_buku()
        elif choice == '5':
            update_buku()
        elif choice == '6':
            search_buku()
        elif choice == '7':
            show_buku_sorted("judul")
        elif choice == '8':
            show_buku_sorted("tahun_terbit")
        elif choice == '9':
            add_anggota()
        elif choice == '10':
            show_anggota()
        elif choice == '11':
            delete_anggota()
        elif choice == '12':
            update_anggota()
        elif choice == '13':
            show_peminjaman()
        elif choice == '14':
            delete_peminjaman()
        elif choice == '0':
            print(Fore.YELLOW + "\n[ Keluar dari program. ]" + Style.RESET_ALL)
            time.sleep(2)
            clear_screen()
            break
        else:
            print(Fore.RED + "\n[ Pilihan tidak valid, coba lagi. ]" + Style.RESET_ALL)
            time.sleep(2)
            clear_screen()

def anggota_menu(anggota_id, nama):
    # Menu untuk anggota
    while True:
        clear_screen()
        print(Style.BRIGHT,Fore.BLUE+"Selamat Datang!,"+Style.RESET_ALL+Style.BRIGHT)
        print("➤"+Fore.GREEN+nama+Style.RESET_ALL,Style.BRIGHT)
        print("============================================")
        print("|\t\t\t\t\t   |")
        print("| Menu:\t\t\t\t\t   |")
        print("| [1] Pinjam Buku\t\t\t   |")
        print("| [2] Lihat Buku\t\t\t   |")
        print("| [3] Cari Buku\t\t\t\t   |")
        print("| [4] Lihat Buku Terurut Berdasarkan Judul |")
        print("| [5] Lihat Buku Terurut Berdasarkan Tahun |")
        print("| [6] Lihat Peminjaman\t\t\t   |")
        print("| [7] Keluar\t\t\t\t   |")
        print("============================================")
        choice = input("\nPilih menu\n-> ")

        if choice == '1':
            add_peminjaman(anggota_id, nama)
        elif choice == '2':
            show_buku()
        elif choice == '3':
            search_buku()
        elif choice == '4':
            show_buku_sorted("judul")
        elif choice == '5':
            show_buku_sorted("tahun_terbit")
        elif choice == '6':
            show_peminjaman(anggota_id)
        elif choice == '7':
            print(Fore.YELLOW + "\n[ Keluar dari program. ]" + Style.RESET_ALL)
            time.sleep(2)
            clear_screen()
            break
        else:
            print(Fore.RED + "\n[ Pilihan tidak valid, coba lagi. ]" + Style.RESET_ALL)
            time.sleep(2)
            clear_screen()

def menu():
    # Menu utama
    while True:
        clear_screen()
        print(Style.BRIGHT+"\n===========================================")
        print(Style.BRIGHT+"|\t* * *   " + Fore.CYAN + "Menu Utama" + Style.RESET_ALL, Style.BRIGHT + "* * *\t  |" )
        print(Style.BRIGHT+"===========================================")
        print("|    Selamat datang di Perpsutakaan-CLI   |")
        print("|\t\t\t\t\t  |")
        print("| Menu:\t\t\t\t\t  |")
        print("| [1] Login\t\t\t\t  |")
        print("| [2] Register\t\t\t\t  |")
        print("| [3] Keluar\t\t\t\t  |")
        print("===========================================")
        choice = input("\nPilih menu\n-> ")

        if choice == '1':
            anggota_id, role, nama = login()
            if anggota_id:
                if role == 'admin':
                    admin_menu(nama)
                elif role == 'anggota':
                    anggota_menu(anggota_id, nama)
        elif choice == '2':
            register()
        elif choice == '3':
            print(Fore.YELLOW + "\n[ Keluar dari program. ]" + Style.RESET_ALL)
            time.sleep(2)
            clear_screen()
            break
        else:
            print(Fore.RED + "\n[ Pilihan tidak valid, coba lagi. ]" + Style.RESET_ALL)
            time.sleep(2)
            clear_screen()

if __name__ == "__main__":
    menu()
