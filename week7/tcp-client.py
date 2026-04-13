# SOCKRT = penjumlahan, pengurangan, perkalian, pembagian
from socket import * # import all

serverName = "localhost"
serverPort = 12000

# AF_INET = ipv4 | SOCK_STREAM = TCP
clientSocket = socket(AF_INET, SOCK_STREAM)

# hubungan | connect
clientSocket.connect(
    (serverName, serverPort)
)

print("[SYSTEM] Masukkan pesan")

running = True
while running:

    # input
    message = input("> ")

    # mengirim ke server
    # endcode = abcdef = 101010101010101001011
    clientSocket.send(message.encode())

    # kalau user ketik "exit, Exit, EXIT" = socket ditutup
    if message.lower() == "exit":
        print("[SYSTEM] keluar dari program")
        running = False
        break

    # menerima pesan dari server
    # abc = 10101010101
    modifiedMessage = clientSocket.recv(2048)

    print("[SERVER] pesan: ", modifiedMessage.decode())

# menutup socket yg tidak dipakai
clientSocket.close()
print("[SYSTEM] socket ditutup")