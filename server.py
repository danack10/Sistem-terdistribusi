from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from datetime import datetime,timedelta
import time
import os

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)
with SimpleXMLRPCServer(("127.0.0.1",8008), requestHandler=RequestHandler, allow_none=True) as server:
    server.register_introspection_functions()
    
    # untuk menyimpan data registrasi
    dataMedis = []   
    # untuk menyimpan jumlah berapa kali program dijalankan oleh client(iterasi ini digunakan untuk mengakses index sekarang dari array DataMedis)
    iterasi = 0
    
    # fungsi untuk melakukan registrasi
    def registrasi(noRekam,nama,tanggalLahir,klinik):
        # inisialiasi variabel global iterasi
        global iterasi

        # untuk menghandle jika datamedis kosong
        if len(dataMedis) == 0:
            iterasi = 0

        # untuk menyimpan data yang diinputkan user kedalam array dataMedis
        dataMedis.append([])
        dataMedis[iterasi].append(noRekam)
        dataMedis[iterasi].append(nama)
        dataMedis[iterasi].append(tanggalLahir)
        dataMedis[iterasi].append(klinik)
        # menentukan jam masuk praktek
        noAntrian = hitungAntrian(dataMedis,klinik)
        # kondisi jika antrian adalah antrian pertama
        if(noAntrian-1 == 0):   
            # memasukkan perkiraan waktu selesai dari user.
            dataMedis[iterasi].append((datetime.now() + timedelta(minutes = 1)).strftime("%H:%M:%S"))
        else:
            # untuk mengambil waktu selesai dari antrian sebelumnya
            waktuSelesai = datetime.strptime(datetime.now().date().strftime("%d%m%y")+" "+dataMedis[len(dataMedis)-2][4], "%d%m%y %H:%M:%S")
            
            #kondisi untuk meng-handle waktu selesai antrian terakhir yang kurang dari waktu sekarang
            if(waktuSelesai < datetime.now()):
                # jika waktu selesai antrian terakhir kurang dari waktu sekarang, maka akan diisi dengan waktu sekarang ditambahkan 1 menit
                dataMedis[iterasi].append((datetime.now() + timedelta(minutes = 1)).strftime("%H:%M:%S"))
            else:
                # jika tidak maka waktu selesai adalah waktu selesai dari antrian sebelumnya ditambah dengan 1 menit
                dataMedis[iterasi].append((waktuSelesai + timedelta(minutes = 1)).strftime("%H:%M:%S"))

        # untuk menghitung nomor antrian sesuai dengan klinik yang dipilih
        dataMedis[iterasi].append(noAntrian)

        # menambahkan jumlah iterasi
        iterasi += 1

        # kondisi untuk menghandle jika antrian adalah antrian yang pertama
        if noAntrian == 0:
            noAntrian += 1
        
        arr = noAntrian

        return arr

    # untuk menampilkan datamedis
    def seeList():
        return dataMedis

    # untuk menghitung antrian sesuai dengan klinik
    def hitungAntrian(arr,key):
        jumlah = 0
        for j in range(len(arr)):
            for k in range(len(arr[j])):
                if arr[j][k] == key:
                    jumlah += 1
        return jumlah

    # untuk melihat antrian berdasarkan klinik dan norekam medis
    def lihatAntrian(noRekam,klinik):
        global dataMedis
        k = 0
        for j in range(len(dataMedis)):
            # untuk mengecek klinik dan no rekam medis dari array
            if dataMedis[j][3] == klinik and dataMedis[j][0] == noRekam:
                return k,dataMedis[j][5]
            else:
                if dataMedis[j][3] == klinik:
                    k += 1
        return False,False

    #untuk menghapus antrian sesuai waktu
    def refreshUrutan():
        global dataMedis, iterasi
        if len(dataMedis) > 0:
            if dataMedis[0][4] < datetime.now().strftime("%H:%M:%S"):
                dataMedis.pop(0)
                iterasi -= 1
        return True

    # menginisialisasi fungsi agar dapat digunakan oleh client
    server.register_function(registrasi, 'registrasi')
    server.register_function(seeList, 'seeList')
    server.register_function(lihatAntrian, 'lihatAntrian')
    server.register_function(refreshUrutan, 'refreshUrutan')
    
    os.system("CLS")
    print("Serving.....")
    # menjalankan server selamanya
    
    server.serve_forever()

        

