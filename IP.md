# Modul 10 IP

**Nama:** Gusti Rifan  
**NIM:** 103072400150  
**Kelas:** IF-04-05  
**Mata Kuliah:** Jaringan Komputer


---

##
Tujuan Praktikum 
1. Mahasiswa dapat menginvestigasi cara kerja protokol IP menggunakan Wireshark 

---

### IP

IP Address adalah alamat unik yang digunakan untuk mengidentifikasi perangkat dalam jaringan, 
baik di internet maupun jaringan lokal. 
IP address berfungsi seperti “alamat rumah” supaya data bisa dikirim ke tujuan yang benar.

Jenis-jenis

IPv4 : menggunakan 32-bit (contoh: 192.168.1.1)
IPv6 : menggunakan 128-bit (contoh: 2001:db8::1)
Cara menghitung

IPv4 terdiri dari 4 oktet (masing-masing 8 bit) ex : 192.168.1.1

192 = 11000000
168 = 10101000
1 = 00000001
Subnetting digunakan untuk membagi jaringan menjadi Network ID (identitas jaringan) dan Host ID (identitas perangkat).

### Mengamati IP Address

- Buka CMD
- Ketik ipconfig

![ipconfig](../assets/image/M10/ipconfig.png)

Perangkat menggunakan alamat IP 192.168.0.16 yang termasuk dalam rentang alamat private kelas C. 
Subnet mask 255.255.255.0 (/24) membagi alamat IP menjadi 24 bit network dan 8 bit host. 
Berdasarkan konfigurasi tersebut, Network ID adalah 192.168.0.0 dan Broadcast Address adalah 192.168.0.255. 
Jumlah host yang dapat digunakan dalam jaringan ini adalah 254 perangkat. 
Default gateway berada pada jaringan yang sama, misalnya 192.168.0.1, 
yang berfungsi sebagai penghubung ke jaringan lain atau internet.

### Traceroute

Traceroute adalah teknik untuk mengetahui jalur yang dilewati paket data dari komputer kita menuju suatu tujuan (misalnya website).

Fungsi Traceroute

- Menampilkan router (hop) yang dilewati
- Mengetahui waktu tempuh tiap hop
- Mendeteksi gangguan jaringan

Mengamati Traceroute dari suatu Website

- Buka CMD
- Ketik tracert google.com

![tracert google.com](../assets/image/M10/tracert%20google.com.png)

Hasil traceroute menunjukkan paket data berhasil mencapai server Google dengan alamat IP 64.233.170.138. 
Hop 1 merupakan router lokal (192.168.0.1), sedangkan hop 2–4 masih berada dalam jaringan internal ISP. 
Mulai hop 5 paket memasuki jaringan publik internet, dan pada hop 8–13 telah melewati infrastruktur jaringan Google.

Beberapa hop, yaitu hop 6 dan hop 14–23, menampilkan "Request Timed Out" karena router tidak merespons paket traceroute, 
yang merupakan kondisi normal. Pada hop 24, paket berhasil mencapai tujuan akhir yaitu server Google. 
Waktu tempuh berkisar antara 1–44 ms, sehingga dapat disimpulkan bahwa koneksi jaringan dalam kondisi baik dan stabil.


### IMCP, MTU, TTL

IMCP adalah protokol yang digunakan untuk mengirim pesan kontrol dalam jaringan. ICMP digunakan untuk:

- Mengecek koneksi (ping)
- Mengirim pesan error
- Digunakan pada traceroute

MTU adalah ukuran maksimum paket data yang bisa dikirim dalam satu kali transmisi. 
Contoh: Ethernet -> 1500 byte. Jika paket lebih besar dari MTU akan terjadi fragmentasi.

TTL adalah batas jumlah hop (router) yang bisa dilewati paket. Setiap melewati router maka TTL berkurang 1. 
Jika TTL = 0 maka paket dibuang. TTL digunakan untuk mencegah looping jaringan.

### Fragmentasi

Fragmentasi adalah proses pemecahan paket data menjadi beberapa bagian yang lebih kecil karena ukuran paket melebihi MTU (Maximum Transmission Unit) jaringan. Fragmentasi terjadi ketika paket terlalu besar dan melewati jaringan dengan MTU lebih kecil.

Percobaan Fragmentasi

1. Jalankan Wireshark pilih interface Wifi yang aktif
2. Klik Start
2. Buka CMD
4. Ketik ping google.com -l 2000 (mengirim paket besar (2000 byte) yg melebihi MTU sehingga memicu fragmentasi)
5. Kembali ke Wireshark, gunakan filter ip.flags.mf == 1 || ip.frag_offset > 0

![Fragmentasi](../assets/image/M10/Fragmentasi.png)

Berdasarkan hasil capture menggunakan Wireshark, ditemukan paket dengan keterangan:

- Fragmented IP protocol (proto=ICMP) yang menunjukkan terjadinya fragmentasi
- Paket memiliki ukuran sebesar 1514 bytes, melebihi batas MTU (±1500 byte)
- Terdapat nilai Identification yang menandakan setiap fragment berasal dari satu paket yang sama
- Nilai Fragment Offset (off=0) menunjukkan urutan fragment pertama
- Ditemukan keterangan Reassembled in #203 yang menunjukkan bahwa fragment berhasil digabung kembali

Sehingga dapat disimpulkan bahwa paket ICMP yang dikirim mengalami fragmentasi karena ukurannya melebihi MTU jaringan.

### IPv6

IPv6 (Internet Protocol version 6) adalah versi terbaru dari IP yang digunakan untuk menggantikan IPv4. 
Ciri-ciri IPv6 adalah menggunakan 128-bit address dan ditulis dalam bentuk heksadesimal.

Analisis IPv6 di Wireshark:

- Membuka file ipv6_sample dengan wireshark
- Gunakan filter IPv6

![IPv6](../assets/image/M10/IPv6.png)

Berdasarkan hasil capture menggunakan Wireshark, ditemukan paket dengan protokol IPv6. Hal ini dibuktikan dengan adanya informasi:

- Internet Protocol Version 6 pada detail paket
- Alamat source: 2001:db8:1::10 dan Alamat destination: 2a00:1450:4009:80b::200e
- Alamat tersebut memiliki format heksadesimal dengan tanda titik dua (:) yang merupakan ciri khas IPv6.
- Next Header menunjukkan penggunaan TCP
- Paket dikirim ke port 443 (HTTPS) yang menandakan komunikasi web
- Ditemukan juga TCP Retransmission yang menunjukkan adanya pengiriman ulang paket

Sehingga dapat disimpulkan bahwa komunikasi jaringan menggunakan IPv6 berhasil diamati dan digunakan untuk akses layanan web.