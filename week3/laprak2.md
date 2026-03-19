# Laporan praktikun 2 - 12, Maret 2026
Nama        : Bima Luthfi Nurhakim  
Nim         : 103072400030  
Kelas       : IF-04-05  
Mata Kuliah : Jaringan Komputer  
  
  
## Tujuan Laprak:
- Modul 3: Mahasiswa dapat menginvestigasi cara kerja protokol HTTP menggunakan Wireshark.  
  
## Langkah-langkah Modul 3
1. Buka Wireshark.
![Buka Wireshark](../assets/image/week3-00.png)

2. Pada bagian capture pilih **WIFI**, setelah itu wireshark otomatis berjalan.
![Pilih capture](../assets/image/week3-01.png)

### LINK 1 Basic HTTP GET/response interaction
3. Lalu buka browser dan tempelkan link ini, http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file1.html.
![Link - 1](../assets/image/week3-02.png)

4. Buka wireshark kembali dan ketik "http"(tanpa tanda kutip) di pencarian dan klik enter. Cari baris yang length info-nya berteks **200 ok (text/html)**, lalu kita bisa melihat hypertext dan Line-based text datanya.
![Link - 1](../assets/image/week3-03.png)
![Link - 1](../assets/image/week3-04.png)

### LINK 2 HTTP CONDITIONAL GET/response interaction
5. Lalu buka browser kembali dan tempelkan link ini, http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file2.html.
![Link - 2](../assets/image/week3-05.png)

6. Buka wireshark kembali dan ketik "http"(tanpa tanda kutip) di pencarian dan klik enter. Cari baris yang length info-nya berteks **200 ok (text/html)**, lalu kita bisa melihat hypertext dan Line-based text datanya.
![Link - 2](../assets/image/week3-06.png)

### LINK 3 etrieving Long Documents
7. Lalu buka browser kembali dan tempelkan link ini, http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file3.html.
![Link - 3](../assets/image/week3-07.png)

8. Buka wireshark kembali dan ketik "http"(tanpa tanda kutip) di pencarian dan klik enter. Cari baris yang length info-nya berteks **200 ok (text/html)**, lalu kita bisa melihat hypertext dan Line-based text datanya.
![Link - 3](../assets/image/week3-08.png)
![Link - 3](../assets/image/week3-09.png)
![Link - 3](../assets/image/week3-10.png)

### LINK 4 HTML Documents dengan Embedded Objects
9. Lalu buka browser kembali dan tempelkan link ini, http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file4.html.
![Link - 3](../assets/image/week3-11.png)

10. Buka wireshark kembali dan ketik "http"(tanpa tanda kutip) di pencarian dan klik enter. Cari baris yang length info-nya berteks **200 ok (text/html)**, lalu kita bisa melihat hypertext dan Line-based text datanya.
![Link - 4](../assets/image/week3-12.png)

### LINK 5 HTTP Authentication
11. Lalu buka browser kembali dan tempelkan link ini, http://gaia.cs.umass.edu/wireshark-labs/protected_pages/HTTP-wireshark-file5.html. Disini ada dua skenario yaitu berhasil masuk atau gagal masuk(username dan password salah, username salah, dan password salah). Pertama coba skenario yang gagal masuk. Kita masukkan username dan password salah, lalu klik sign in.
![Link - 5](../assets/image/week3-13.png)

12. setelah kita klik sing in, kita diminta memasukkan username dan passowrd lagi. Jadi hasil dari skenario username dan passowrd salah adalah diminta memasukkan username dan passowrd dengan benar.
![Link - 5](../assets/image/week3-14.png)

13. Buka wireshark kembali dan ketik "http"(tanpa tanda kutip) di pencarian dan klik enter. Cari baris yang length info-nya berteks **200 ok (text/html)**, lalu kita bisa melihat hypertext dan Line-based text datanya.
![Link - 5](../assets/image/week3-15.png)

14. Kita coba skenario berhasil masuk dengan **username:** wireshark-students dan **password:** network, kita klik sign in.
![Link - 5](../assets/image/week3-16.png)

15. Kita berhasil masuk.
![Link - 5](../assets/image/week3-17.png)

16. Buka wireshark kembali dan ketik "http"(tanpa tanda kutip) di pencarian dan klik enter. Cari baris yang length info-nya berteks **200 ok (text/html)**, lalu kita bisa melihat hypertext dan Line-based text datanya.
![Link - 5](../assets/image/week3-18.png)

17. Setelah selesai, klik ikon kotak merah di pojok kiri atas untuk memberhnetikan wireshark.
![Link - 5](../assets/image/week3-19.png)

18. Lalu kelluar dengan klik tanda X di pojok kanan atas.
![Link - 5](../assets/image/week3-20.png)

19. Lalu pilih **Out without Saving**
![Link - 5](../assets/image/week3-21.png)