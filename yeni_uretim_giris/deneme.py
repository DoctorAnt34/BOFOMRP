import bofo_uretim_giris as bofo


a = bofo.bofoVeri('2430',1000,'LM5')
a.uretim_start()

a.sarf_add('NORMAL',2,'19',5000,'1566',20,10)
bofo.bofoVeri.commit()