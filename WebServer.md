# Modul 9 WEB SERVER 

**Nama:** Gusti Rifan  
**NIM:** 103072400150  
**Kelas:** IF-04-05  
**Mata Kuliah:** Jaringan Komputer


---

##
Tujuan Praktikum 
1.	Mahasiswa bisa membuat program web server sederhana berbasis TCP socket programming 

---

### Web server
Web server merupakan komponen penting dalam sistem komunikasi berbasis internet. 
Web server berfungsi untuk menerima permintaan (request) dari klien, seperti browser, 
kemudian mengirimkan respons berupa halaman web atau data yang diminta. 
Proses komunikasi ini umumnya menggunakan protokol HTTP (HyperText Transfer Protocol) yang berjalan di atas TCP (Transmission Control Protocol).


- Membuat file serverweb.py
- code :

from socket import *
import sys

#membuat socket server (TCP)

serverSocket = socket(AF_INET, SOCK_STREAM)

#Prepare a server socket
serverPort = 6789
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

while True:
    # Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()

    try:
        # menerima request dari client
        message = connectionSocket.recv(1024).decode()
        print(message)

        # mengambil nama file
        filename = message.split()[1]

        # membuka file
        f = open(filename[1:])
        outputdata = f.read()

        # Send HTTP header
        connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
        connectionSocket.send("Content-Type: text/html\r\n".encode())
        connectionSocket.send("\r\n".encode())

        # kirim isi file
        for i in range(len(outputdata)):
            connectionSocket.send(outputdata[i].encode())

        connectionSocket.send("\r\n".encode())
        connectionSocket.close()

    except IOError:
        # kirim 404 jika file tidak ada
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n".encode())
        connectionSocket.send("Content-Type: text/html\r\n".encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.send("<html><body><h1>404 Not Found</h1></body></html>".encode())

        # tutup koneksi
        connectionSocket.close()

serverSocket.close()
sys.exit()

- Meembuat file HelloWorld.html

<html>
<head>
    <title>Test Server</title>
</head>
<body>
    <h1>Hello World!</h1>
    <p>Ini hasil server Python TCP</p>
</body>
</html>


- Buka terminal dan jalankan file code tersebut (py serverweb.py)
- Buka browser ketikan URL: http://localhost:6789/HelloWorld.html

![HelloWorld.html](../assets/image/M9/HelloWorld.html.png)

- Buka tab lain dan ketikan ERL: http://localhost:6789/salah.html

![salah.html](../assets/image/M9/salah.html.png)

server menampilkan "404 Not Found". Hal ini menunjukkan bahwa server berhasil menangani request valid dan error dengan benar.

Program dimulai dengan membuat socket TCP menggunakan library socket. 
Server kemudian diikat pada port tertentu dan masuk ke mode listening untuk menunggu koneksi dari klien. 
Ketika klien terhubung, server menerima request HTTP dan mengekstrak nama file yang diminta. 
Jika file tersedia, server mengirimkan response dengan status 200 OK beserta isi file HTML. 
Jika file tidak ditemukan, server mengirimkan response 404 Not Found. Program ini bersifat single-threaded, 
sehingga hanya dapat menangani satu permintaan dalam satu waktu.


### Latian Web Tambahan (Multithreaded Server)

- Membuat file server.py
Code :

from socket import *
import threading

def handle_client(connectionSocket):
    try:
        # menerima pesan user
        message = connectionSocket.recv(1024).decode() # decode = 10101010 = "message"

        # index.html, hello.html
        # message isinya = /GET /index.html HTTP/1.1
        message = message[4:15]
        print(message)
        # filename = message.split()[1]

        # membuka index.html serta menghilangkan "/"
        f = open(message[1:])

        # membaca file html
        outputData = f.read()

        # kirim respon
        connectionSocket.send(
            "HTTP/1.1 200 OK\r\n\r\n".encode()
        )

        # kirim data
        connectionSocket.sendall(outputData.encode())

        # tutup koneksi
        connectionSocket.close()
    
    except IOError:
        # kirim respon bila tidak ditemukan
        connectionSocket.send(
            "HTTP/1.1 404 Not Found\r\n\r\n".encode()
        )

        # kirim data
        connectionSocket.send(
            "<h1>404 Not Found</h1>".encode()
        )

        # tutup koneksinya
        connectionSocket.close()


serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', 6789))
serverSocket.listen(5) # dapat menerima sebanyak 5 client
print("[SYSTEM] server is running...")

while True:
    connectionSocket, addr =  serverSocket.accept()

    # membuat thread dan target threadnya, beseerta parameter
    thread = threading.Thread(
        target = handle_client,
        args = (connectionSocket,)
        )
    # menjalankan
    thread.start()


- Membuat file index.html :

<h1>sudah berhasil, asprak nya gacor tapi gusti lebih gacor</h1>

- Buka terminal dan jalankan file code tersebut (py server.py)
- Buka browser ketikan URL: http://localhost:6789/index.html

![index.html](../assets/image/M9/index.html.png)

Pada versi ini, server menggunakan multithreading untuk menangani beberapa klien secara bersamaan. 
Setiap koneksi yang masuk akan dibuatkan thread baru yang menjalankan fungsi handle_client(). 
Dengan pendekatan ini, server tidak perlu menunggu satu klien selesai sebelum melayani klien lain, 
sehingga meningkatkan efisiensi dan performa server.