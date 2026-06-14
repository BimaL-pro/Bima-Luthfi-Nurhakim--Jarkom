from email import header
import socket
import threading
import json
import struct
from turtle import mode

HOST = "0.0.0.0"
PORT = 12345
VERIFY_PASSWORD = True

clients = {}
lock = threading.Lock()


def main_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print("Server multithread berjalan di", HOST, PORT)

    while True:
        client_sock, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_sock, addr))
        thread.daemon = True
        thread.start()


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


def send_status(sock, message):
    send_packet(sock, {
        "action": "status",
        "message": message
    })


def remove_client(name):
    with lock:
        if name in clients:
            try:
                clients[name]["socket"].close()
            except:
                pass
            del clients[name]
            print(name, "disconnect")


def get_targets(mode, sender, target_list):
    with lock:
        if mode == "unicast":
            return target_list

        if mode == "multicast":
            return target_list

        if mode == "broadcast":
            return [name for name in clients.keys() if name != sender]

    return []


def forward_message(header, payload):
    sender = header.get("sender")
    mode = header.get("mode")
    target_list = header.get("targets", [])
    password_hashes = header.get("password_hashes", {})

    targets = get_targets(mode, sender, target_list)

    delivered = []
    failed = []

    for target in targets:
        with lock:
            target_data = clients.get(target)

        if not target_data:
            failed.append(target)
            continue

        if VERIFY_PASSWORD and mode != "broadcast":
            target_password_hash = target_data.get("password_hash", "")
            sent_password_hash = password_hashes.get(target, "")

            if sent_password_hash != target_password_hash:
                failed.append(target + " password salah")
                continue

        new_header = dict(header)
        new_header["action"] = "receive"
        new_header.pop("password_hashes", None)

        try:
            send_packet(target_data["socket"], new_header, payload)
            delivered.append(target)
        except:
            failed.append(target)

    with lock:
        sender_data = clients.get(sender)

    if sender_data:
        try:
            send_packet(sender_data["socket"], {
                "action": "status",
                "message": "Terkirim ke: " + str(delivered) + " | Gagal: " + str(failed)
            })
        except:
            pass


def handle_client(sock, addr):
    name = None

    try:
        header, payload = recv_packet(sock)

        if not header or header.get("action") != "register":
            sock.close()
            return

        name = header.get("name")
        password_hash = header.get("password_hash", "")

        if not name:
            send_packet(sock, {
                "action": "register_result",
                "success": False,
                "message": "Nama tidak boleh kosong"
            })
            sock.close()
            return

        with lock:
            if name in clients:
                send_packet(sock, {
                    "action": "register_result",
                    "success": False,
                    "message": "Nama client sudah digunakan"
                })
                sock.close()
                return

            clients[name] = {
                "socket": sock,
                "address": addr,
                "password_hash": password_hash
            }

        send_packet(sock, {
            "action": "register_result",
            "success": True,
            "message": "Berhasil login sebagai " + name
        })

        print(name, "connect dari", addr)

        while True:
            header, payload = recv_packet(sock)

            if not header:
                break

            action = header.get("action")

            if action == "send":
                forward_message(header, payload)

            elif action == "list_clients":
                with lock:
                    names = list(clients.keys())

                send_packet(sock, {
                    "action": "client_list",
                    "clients": names
                })

            elif action == "exit":
                break

    except Exception as e:
        print("Error:", e)

    finally:
        if name:
            remove_client(name)
        else:
            try:
                sock.close()
            except:
                pass

if __name__ == "__main__":
    main_server()
    
