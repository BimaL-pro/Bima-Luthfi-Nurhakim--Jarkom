# Modul 11 DHCP

**Nama:** Gusti Rifan  
**NIM:** 103072400150  
**Kelas:** IF-04-05  
**Mata Kuliah:** Jaringan Komputer


---

##
Tujuan Praktikum 
1. Mahasiswa dapat menginvestigasi cara kerja protokol DHCP menggunakan Wireshark.

---

### DHCP

Dynamic Host Configuration Protocol (DHCP) adalah 
protokol jaringan yang digunakan untuk memberikan konfigurasi jaringan secara otomatis kepada perangkat yang terhubung ke jaringan. 
Konfigurasi tersebut meliputi IP Address, subnet mask, gateway, dan DNS server sehingga pengguna tidak perlu mengatur IP secara manual.

### Kelebihan DHCP
- Proses pemberian IP address menjadi otomatis dan lebih cepat
- Memudahkan administrator jaringan dalam mengelola alamat IP
- Menghindari terjadinya konflik penggunaan IP address yang sama
- Mengurangi risiko kesalahan konfigurasi IP address yang tidak valid
- Efisien digunakan pada jaringan dengan banyak perangkat

### Kekurangan DHCP
- Perangkat lebih sulit untuk dilacak karena IP address dapat berubah secara otomatis
- Membutuhkan konfigurasi tambahan pada server DHCP
- Jika server DHCP mengalami gangguan, perangkat klien tidak dapat memperoleh IP address
- Keamanan jaringan dapat berkurang apabila konfigurasi DHCP tidak dikelola dengan baik

### Proses DORA
DORA merupakan tahapan komunikasi antara client dan server DHCP untuk memperoleh IP address secara otomatis. DORA terdiri dari Discover, Offer, Request, dan Acknowledgement (ACK).

Langkah-langkah

1. Download dan ekstrak file http://gaia.cs.umass.edu/wireshark-labs/wireshark-traces.zip
2. Buka file DHCP menggunakan Wireshark
3. Gunakan filter dhcp untuk menampilkan paket DHCP saja

![DORA](../assets/image/M11/DORA.png)


Tahapan Dora

1. Discover

Pada baris satu, dapat dilihat client mengirimkan pesan DHCP Discover untuk mencari server DHCP yang tersedia pada jaringan. 
IP source masih 0.0.0.0 karena perangkat belum memiliki IP address. 
Paket dikirim secara broadcast agar dapat diterima oleh seluruh server DHCP dalam jaringan.

2. Offer

Pada baris kedua server DHCP yang menerima pesan Discover akan mengirimkan DHCP Offer. 
Pesan ini berisi penawaran IP address beserta konfigurasi jaringan lain yang dapat digunakan oleh client.

3. Request

Pada baris ketiga client memilih salah satu penawaran dari server DHCP, 
kemudian mengirimkan DHCP Request sebagai tanda bahwa client menerima IP address yang ditawarkan.

4. Acknowledgement (ACK)

Pada baris keempat server DHCP mengirimkan DHCP ACK untuk mengonfirmasi bahwa IP address telah resmi diberikan kepada client. 
Tahap ini merupakan proses finalisasi sehingga client dapat mulai menggunakan jaringan.