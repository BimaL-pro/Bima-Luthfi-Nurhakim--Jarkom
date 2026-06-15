import socket
import threading
import json
import struct
import hashlib
import os
import time
from turtle import mode

HOST = "10.218.8.109"
PORT = 12345
send_lock = threading.Lock()

def start_client():
    host = input("Host server : ").strip()
    if host == "":
        host = HOST

    port_input = input("Port server : ").strip()
    if port_input == "":
        port = PORT
    else:
        port = int(port_input)

    client_name = input("Masukkan nama client: ")
    password = input("Buat password client ini: ")
    password_hash = hash_password(password)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    send_packet(sock, {
        "action": "register",
        "name": client_name,
        "password_hash": password_hash
    })

    header, payload = recv_packet(sock)

    if not header or not header.get("success"):
        print("Gagal login:", header.get("message") if header else "Tidak ada respon")
        sock.close()
        return

    print(header.get("message"))

    thread = threading.Thread(target=receiver_loop, args=(sock, client_name))
    thread.daemon = True
    thread.start()

    while True:
        print()
        print("MENU")
        print("1. Unicast")
        print("2. Multicast")
        print("3. Broadcast")
        print("4. Lihat client online")
        print("5. Keluar")

        choice = input("Pilih menu: ")

        if choice == "1":
            thread_mode = choose_thread_mode()
            send_data(sock, client_name, "unicast", thread_mode)

        elif choice == "2":
            thread_mode = choose_thread_mode()
            send_data(sock, client_name, "multicast", thread_mode)

        elif choice == "3":
            thread_mode = choose_thread_mode()
            send_data(sock, client_name, "broadcast", thread_mode)

        elif choice == "4":
            send_packet(sock, {
                "action": "list_clients"
            })

        elif choice == "5":
            send_packet(sock, {
                "action": "exit"
            })
            sock.close()
            break

        else:
            print("Pilihan tidak valid")


def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def recv_exact(sock, size):
    data = b""
    while len(data) < size:
        part = sock.recv(size - len(data))
        if not part:
            return None
        data += part
    return data


def send_packet(sock, header, payload=b""):
    header["payload_size"] = len(payload)
    header_bytes = json.dumps(header).encode("utf-8")
    sock.sendall(struct.pack("!I", len(header_bytes)))
    sock.sendall(header_bytes)
    if payload:
        sock.sendall(payload)


def recv_packet(sock):
    header_len_bytes = recv_exact(sock, 4)
    if not header_len_bytes:
        return None, None

    header_len = struct.unpack("!I", header_len_bytes)[0]
    header_bytes = recv_exact(sock, header_len)

    if not header_bytes:
        return None, None

    header = json.loads(header_bytes.decode("utf-8"))
    payload_size = header.get("payload_size", 0)

    payload = b""
    if payload_size > 0:
        payload = recv_exact(sock, payload_size)
        if payload is None:
            return None, None

    return header, payload


def save_received_file(client_name, sender, filename, payload):
    folder = os.path.join("received_files", client_name)
    os.makedirs(folder, exist_ok=True)

    safe_filename = os.path.basename(filename)
    timestamp = str(int(time.time()))
    new_filename = sender + "_" + timestamp + "_" + safe_filename
    path = os.path.join(folder, new_filename)

    with open(path, "wb") as file:
        file.write(payload)

    return path


def choose_thread_mode():
    print()
    print("Pilih mode pengiriman:")
    print("1. Single Thread")
    print("2. Multi Thread")
    ch = input("Pilihan: ")
    return "multi" if ch == "2" else "single"


def receiver_loop(sock, client_name):
    while True:
        try:
            header, payload = recv_packet(sock)

            if not header:
                print("\nKoneksi ke server terputus")
                break

            action = header.get("action")

            if action == "status":
                print("\n[STATUS]", header.get("message"))

            elif action == "client_list":
                print("\nClient online:", header.get("clients", []))

            elif action == "receive":
                sender = header.get("sender")
                data_type = header.get("data_type")
                content_type = header.get("content_type")

                if data_type == "text":
                    message = payload.decode("utf-8")
                    print("\n[Pesan dari " + sender + "]")
                    print("Jenis:", content_type)
                    print(message)

                elif data_type == "file":
                    filename = header.get("filename", "file_diterima")
                    path = save_received_file(client_name, sender, filename, payload)
                    print("\n[File dari " + sender + "]")
                    print("Jenis:", content_type)
                    print("Disimpan di:", path)

        except Exception as e:
            print("\nReceiver error:", e)
            break


def choose_content():
    print()
    print("Jenis data:")
    print("1. 1-5 kata")
    print("2. 1 kalimat panjang")
    print("3. 1 paragraf")
    print("4. File dokumen txt/docx/pdf")
    print("5. Gambar jpg/png")
    print("6. Audio mp3")
    print("7. Video mp4")

    choice = input("Pilih jenis data: ")

    if choice == "1":
        text = input("Masukkan 1-5 kata: ")
        words = text.split()

        if len(words) > 5:
            print("Maksimal 5 kata")
            return None, None, None, None

        return "text", "kata", None, text.encode("utf-8")

    if choice == "2":
        text = input("Masukkan 1 kalimat panjang: ")
        return "text", "kalimat", None, text.encode("utf-8")

    if choice == "3":
        text = input("Masukkan 1 paragraf: ")
        return "text", "paragraf", None, text.encode("utf-8")

    if choice == "4":
        path = input("Masukkan path file dokumen: ")
        allowed = [".txt", ".docx", ".pdf"]
        content_type = "dokumen"

    elif choice == "5":
        path = input("Masukkan path gambar: ")
        allowed = [".jpg", ".jpeg", ".png"]
        content_type = "gambar"

    elif choice == "6":
        path = input("Masukkan path audio: ")
        allowed = [".mp3"]
        content_type = "audio"

    elif choice == "7":
        path = input("Masukkan path video: ")
        allowed = [".mp4"]
        content_type = "video"

    else:
        print("Pilihan tidak valid")
        return None, None, None, None

    if not os.path.exists(path):
        print("File tidak ditemukan")
        return None, None, None, None

    ext = os.path.splitext(path)[1].lower()

    if ext not in allowed:
        print("Ekstensi file tidak sesuai")
        return None, None, None, None

    with open(path, "rb") as file:
        payload = file.read()

    filename = os.path.basename(path)

    return "file", content_type, filename, payload


def send_data(sock, client_name, mode, thread_mode="single"):
    targets = []

    if mode == "unicast":
        target = input("Masukkan nama tujuan: ")
        targets = [target]

    elif mode == "multicast":
        raw_targets = input("Masukkan tujuan, pisahkan dengan koma. Contoh B,C: ")
        targets = [target.strip() for target in raw_targets.split(",") if target.strip()] 

    elif mode == "broadcast":
        targets = [] 

    password_hashes = {}
    if mode == "broadcast":
        password_hashes["__broadcast__"] = "" 
    else:
        raw_passwords = input("Masukkan password penerima :")
        passwords = [p.strip() for p in raw_passwords.split(",") if p.strip()]
        if len(passwords) == 1:
            for target in targets:
                password_hashes[target] = hash_password(passwords[0])
        elif len(passwords) == len(targets):
            for i in range(len(targets)):
                password_hashes[targets[i]] = hash_password(passwords[i])
        else:
            print("Jumlah password harus 1 atau sama dengan jumlah target")
            return False
    
    data_type, content_type, filename, payload = choose_content()
    if data_type is None:
        return False

    header = {
        "action": "send",
        "mode": mode,
        "sender": client_name,
        "targets": targets,
        "password_hashes": password_hashes,
        "data_type": data_type,
        "content_type": content_type,
        "filename": filename
    }
    header["thread_mode"] = thread_mode
    if thread_mode == "single":
        send_packet(sock, header, payload)
        return True
    if thread_mode == "multi":
        if mode in ("unicast", "multicast") and targets:
            threads = []
            def worker(hdr, pl):
                with send_lock:
                    try:
                        send_packet(sock, hdr, pl)
                    except Exception as e:
                        print("Send thread error:", e)

            for t in targets:
                h2 = dict(header)
                h2["targets"] = [t]
                th = threading.Thread(target=worker, args=(h2, payload))
                th.start()
                threads.append(th)

            for th in threads:
                th.join()

            return True
        else:
            send_packet(sock, header, payload)
            return True

    send_packet(sock, header, payload)
    return True

if __name__ == "__main__":
    start_client()