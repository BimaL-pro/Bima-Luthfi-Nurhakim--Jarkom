# Modul 12 ICMP 

**Nama:** Gusti Rifan  
**NIM:** 103072400150  
**Kelas:** IF-04-05  
**Mata Kuliah:** Jaringan Komputer


---

##
Tujuan Praktikum
1. Mahasiswa dapat menginvestigasi cara kerja protokol ICMP menggunakan Wireshark
2. Mahasiswa dapat membuat program ICMP Pinger

---

### ICMP
Internet Control Message Protocol (ICMP) merupakan salah satu protokol pada jaringan komputer yang berfungsi untuk mengirimkan pesan kontrol, informasi status, serta notifikasi kesalahan dalam komunikasi berbasis Internet Protocol (IP). Protokol ini digunakan untuk membantu proses pemantauan dan diagnostik jaringan sehingga administrator dapat mengetahui kondisi konektivitas antar perangkat.

### Fungsi ICMP

1. Membantu proses diagnosis jaringan untuk memastikan komunikasi antar perangkat berjalan dengan baik.
2. Memeriksa ketersediaan host atau perangkat tujuan dalam suatu jaringan.
3. Menyampaikan informasi terkait kesalahan yang terjadi selama proses pengiriman data.

### Pemanfaatan ICMP

1. Menguji keterhubungan suatu host menggunakan utilitas seperti ping.
2. Menelusuri jalur yang dilalui paket data menuju tujuan menggunakan traceroute atau tracert.
3. Memberikan pesan kesalahan apabila terjadi kendala dalam proses komunikasi jaringan.

### Hubungan ICMP dengan IP

ICMP bekerja berdampingan dengan protokol IP. Saat sebuah paket IP dikirimkan, informasi ICMP dapat ditempatkan pada bagian payload untuk membawa pesan kontrol maupun informasi kesalahan. Dengan demikian, ICMP berperan sebagai protokol pendukung yang membantu IP dalam mengelola komunikasi jaringan secara lebih efektif.

### Struktur Paket ICMP

1. Type : menunjukkan jenis pesan ICMP
2. Code : memberikan detail tambahan dari jenis pesan ICMP
3. Checksum : digunakan untuk mengecek apakah paket mengalami error atau tidak
4. Identifier : penanda untuk membedakan paket ICMP
5. Sequence Number : menunjukkan urutan paket yang dikirim

### Analisis ICMP yang Dihasilkan Oleh Ping
1. Bukak wireshark dan pilih salah satu jaringan (Wifi), lalu aktifkan / capture
2. Buka CMD, kemudian ketikan perintah ping -n 10 www.ust.hk

![Pinging www.ust.hk](/assets/image/M12/Pinging%20www.ust.hk.png)

3. Stop capture pada wireshark
4. Lakukan filter ICMP
5. Pilih dan expand salah satu paket ICMP Echo Request
6. Pilih dan expand salah satu paket ICMP Echo Reply

Analisis

- Pesan ICMP 

![ICMP](/assets/image/M12/ICMP.png)

Perintah ping menghasilkan dua jenis pesan ICMP, yaitu Echo Request dan Echo Reply. Pada percobaan ini digunakan perintah ping -n 10, yang berarti sistem mengirimkan sepuluh permintaan ping ke host tujuan. Setiap permintaan akan menghasilkan satu paket Echo Request dan satu paket Echo Reply sebagai balasannya. Oleh karena itu, total paket ICMP yang terekam pada Wireshark adalah sebanyak dua puluh paket yang terdiri dari sepuluh request dan sepuluh reply.

- Format dan Isi Pesan ICMP
    1. ICMP Echo Request

    ![echoRequest](/assets/image/M12/echoRequest.png)

    - Perhatikan bahwa paket ICMP ini adalah Tipe 8 dan Kode 0 - yang disebut paket "echo request" ICMP. Perhatikan juga bahwa paket ICMP ini berisi checksum, identifier, dan sequence number.
    - Checksum = 0x4d4c [correct], menandakan checksum valid sehingga paket tidak mengalami kerusakan/error saat dikirim
    - Sequence Number = 15 (0x000f), menunjukkan bahwa paket ini merupakan urutan ping ke-15 yang dikirim

    2. ICMP Echo Reply

    ![echoReply](/assets/image/M12/echoReplay.png)

    Paket ICMP Echo Reply (Type 0) merupakan balasan dari ICMP Echo Request yang digunakan dalam proses ping. Paket memiliki checksum yang valid sehingga tidak terjadi kerusakan data selama transmisi. Identifier bernilai 1 dan sequence number 2719 digunakan untuk mencocokkan paket balasan dengan paket permintaan. Wireshark menunjukkan bahwa paket ini merupakan balasan terhadap frame 1967 dengan waktu respons (RTT) sebesar 84,264 ms, yang menandakan host tujuan berhasil dijangkau melalui jaringan.

### Analisis ICMP yang Dihasilkan Oleh Traceroute

1. Bukak wireshark dan pilih salah satu jaringan (Wifi), lalu aktifkan / capture
2. Buka CMD, kemudian ketikan perintah tracert www.ust.hk

![ICMPtracert](/assets/image/M12/ICMPtracert.png)

3. Stop capture pada wireshark
4. Lakukan filter ICMP
5. Pilih dan expand salah satu paket ICMP Echo Request
6. Pilih dan expand salah satu paket Time To Live (TTL)

Analisis :

- Pesan ICMP yang dihasilkan oleh program tracerout

![ICMPtraceroutWS](/assets/image/M12/ICMPtraceroutWS.png)

Proses traceroute menghasilkan beberapa jenis pesan ICMP untuk mengidentifikasi jalur yang dilewati paket menuju host tujuan. Pada hasil pengamatan, ditemukan dua jenis pesan utama, yaitu:

1. ICMP Echo Request : Paket ini digunakan untuk meminta respon dari host atau router yang dilewati
2. ICMP Time Exceeded (TTL Expired) : pesan yang dikirim oleh router ketika nilai TTL pada suatu paket habis sebelum paket mencapai tujuan

- Format dan Isi Pesan ICMP
    ICMP Echo Request:
    
    ![ICMPechoRequest](/assets/image/M12/ICMPechoRequest.png)

    ICMP Time Exceeded :

    ![ICMPttl](/assets/image/M12/ICMPttl.png)

Pesan ICMP Time Exceeded digunakan oleh traceroute untuk mengidentifikasi setiap router yang dilewati paket. Dengan memanfaatkan informasi tersebut, jalur komunikasi dari sumber menuju tujuan dapat diketahui secara bertahap.