from socket import *

serverPort = 12000
serverSocket =  socket(AF_INET, SOCK_STREAM)

# sudah meng-bind server
serverSocket.bind(
    ('', serverPort)
)

# server siap menerima koneksi
serverSocket.listen(1)
print("[SYSTEM] server TCP siap digunakan")

running = True
while running:

    # menyetujui koneksi dari client
    connetionSocket, addr = serverSocket.accept()

    while True:
        # pesan yg diterima = 10101010
        message = connetionSocket.recv(2048).decode()
        if not message:
            break

        # cek apakah "exit"?
        if message.lower() == "exit":
            print("[SYSTEM] client ingin keluar")
            running = False
            break

        # memodifikasi menjadi capslock
        modifiedMessage = message.upper()
        print("[SERVER] diterima: ", modifiedMessage)

        # kirim ke client
        connetionSocket.send(
            modifiedMessage.encode()
        )

    connetionSocket.close()

serverSocket.close()