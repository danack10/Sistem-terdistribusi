import xmlrpc.client
import os
import datetime

s = xmlrpc.client.ServerProxy('http://26.240.147.120:8008', allow_none=True)

def HomePage():
	while True:
		os.system("CLS")
		e = datetime.datetime.now()
		#untuk mengecek waktu urutan dan jika melebihi akan dihapus
		s.refreshUrutan()
		#UI Homepage
		print("==========> Bagian Homepage <========")
		print ("Today's date: ",e.strftime("%a, %d-%b-%Y"))
		print()
		print("=====================================")
		print("=========> Selamat Datang <==========")
		print("=====================================")
		print("======__________________________=====")
		print("=====|           Menu           |====")
		print("=====|  1. Pilih Klinik         |====")
		print("=====|  2. Lihat Data Medis     |====")
		print("=====|     Seluruh Klinik       |====")
		print("=====|  3. Cari Antrian         |====")
		print("=====|  0. Exit                 |====")
		print("=====|__________________________|====")
		print("=====================================")
		print("=====> Masukkan Pilihan Anda <=======")
		print("=====================================")
		# untuk menyimpan jawaban dari inputan user
		answer = input('=======> Pilihan Anda: ')

		# kondisi pilihan homepage
		if answer == '1':
			PilihKlinik()
		elif answer == '2':
			print()
			print("Berikut adalah data medis yang ada pada seluruh klinik yang kami miliki:")
			print(s.seeList())
			print()
			print("=====> Mohon ditunggu <=======")			
			input()
		elif answer == '3':
			cariAntrian()
			input()
		elif answer == '0':
		   	AreYouSure()
		   	os.system("CLS")
		   	break
		else:
			print()
			print("====> Masukkan Pilihan Anda dengan benar  <====")
			print("===============================================")
			print("=======> TEKAN ENTER UNTUK MELANJUTKAN <=======")
			print("===============================================")
			input()
			os.system("CLS")

#UI jika user ingin keluar dari homepage
def AreYouSure():
	print("=======================================================")
	print("Apakah kamu benar-benar ingin meninggalkan homepage ?")
	print(" 1. Ya")
	print(" 2. Tidak")
	print("=======================================================")
	#untuk menyimpan jawaban dari inputan user
	answer = input('=======> Pilihan Anda: ')

	# kondisi pilihan jika user ingin keluar dari Homepage
	if answer == '1':
		print()
		print("======================> Sekian Terima Kasih Dan Sampai Jumpa <======================")
		input()
	elif answer == '2':
		HomePage()

#UI untuk Pilih Klinik
def PilihKlinik():
	while True:
		os.system("CLS")
		e = datetime.datetime.now()
		global klinik
		print("========> Bagian Pilih Klinik <======")
		print ("Today's date: ",e.strftime("%a, %d-%b-%Y"))
		print()
		print("======__________________________=====")

		# untuk menampilkan pilihan klinik
		print("=====|  Silahkan Pilih Klinik   |====")
		print("=====|  1. Klinik Sukapura      |====")
		print("=====|  2. Klinik Sukabirus     |====")
		print("=====|  3. Klinik Telkom        |====")
		print("=====|  0. Exit                 |====")
		print("=====|__________________________|====")
		print("=====================================")
		print("=====> Masukkan Pilihan Anda <=======")
		print("=====================================")

		# untuk menyimpan jawaban dari inputan user
		answer = input('=======> Pilihan Anda: ')

		# kondisi untuk menentukan klinik sesuai dengan answer dari user
		if answer == '1':
			klinik = "Klinik Sukapura"
			DataMedis()
			break
		elif answer == '2':
		   	klinik = "Klinik Sukabirus"
		   	DataMedis()
		   	break
		elif answer == '3':
		   	klinik = "Klinik Telkom"
		   	DataMedis()
		   	break
		elif answer == '0':
			HomePage()
			break
		else:
			print()
			print("====> Masukkan Pilihan Anda dengan benar! <====")
			print("===============================================")
			print("=======> TEKAN ENTER UNTUK MELANJUTKAN <=======")
			print("===============================================")
			input()
			os.system("CLS")

#UI untuk pendaftaran Data Medis	
def DataMedis():
	os.system("CLS")
	global noRekam, nama, tanggalLahir
	print("==========> Bagian Data Medis <========")
	print("=======================================")
	print("=====> Masukkan Data diri Anda <=======")
	# untuk menyimpan jawaban data medis dari user
	noRekam = input("Nomor Rekam Medis : ")
	nama = input("Nama : ")
	tanggalLahir = input("Tanggal Lahir : ")

	# untuk menjalankan fungsi registrasi dari server
	hasil = s.registrasi(noRekam,nama,tanggalLahir,klinik)

	# menampilkan nomor antrian dan waktu tunggu
	print("Nomor Antrian :",hasil)
	print("===============================================")
	print("=======> TEKAN ENTER UNTUK MELANJUTKAN <=======")
	print("===============================================")
	input()

#UI untuk mencari antrian user
def cariAntrian():
	os.system("CLS")
	print("========> Bagian Cari Antrian  <=======")
	print("=======================================")
	print("=====> Masukkan Data diri Anda <=======")
    # nama klinik
	k = input("Nama Klinik : ")
    # no rekam medis
	nk = input("No Rekam Medis : ")
	tunggu,hasil = s.lihatAntrian(nk,k)

	#Jika data user tidak ada di antrian
	if hasil == False:
		print()
		print("==============================================================")
		print("=> Maaf data antrian anda tidak ditemukan di seluruh klinik <=")
		print("==============================================================")
	#Jika data user ada di antrian
	else:
		print()
		print("============================================")
		print("Nomor Antrian anda adalah ",hasil)
		print("Anda harus Menunggu ",tunggu," Antrian Lagi")
		print("============================================")

#MAIN
#____________________________
#clear cmd
os.system("CLS")
#menampilkan UI Homepage
HomePage()