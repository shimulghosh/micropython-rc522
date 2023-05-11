import time
import mfrc522
rdr = mfrc522.MFRC522(0, 2, 4, 5, 14)
while True:
	# Détecte la présence d'un badge
	(stat, tag_type) = rdr.request(rdr.REQIDL)
	print(stat)
	if stat == rdr.OK:
		(stat, raw_uid) = rdr.anticoll()
		if stat == rdr.OK:
			# Affichage du type de badge et de l'UID
			print("\nBadge détecté !")
			print(" - type : %03d" % tag_type)
			print(" - uid : %03d.%03d.%03d.%03d" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
			# Affichage des données en mémoire
			if rdr.select_tag(raw_uid) == rdr.OK:
				key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
				if rdr.auth(rdr.AUTHENT1A, 8, key, raw_uid) == rdr.OK:
					print(" - données : %s" % rdr.read(8))
					rdr.stop_crypto1()
				# Affichage en cas de problème
				else:
					print("Erreur de lecture")
			# Affichage en cas de problème
			else:
				print("Erreur badge")