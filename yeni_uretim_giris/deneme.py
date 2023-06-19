import bofo_uretim_giris as bofo


a = bofo.bofoVeri.uretim_cast('BU230001')

a.sarf_add('NORMAL',2,'19',5000,'1566',20,10)
bofo.bofoVeri.commit()