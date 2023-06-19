import sqlite3 as sq
from sqlite3 import Error
from pathlib import Path
import serialization as s

road = Path('db/uretim.db')


uretim = s.json_load_dict('uretim')
aktif_uretim = s.json_load_dict('aktif_uretim')

con = sq.connect(road)
cur = con.cursor()

def uretim_giris(uretim_kodu):

        if uretim_kodu not in uretim and uretim_kodu not in aktif_uretim:
                return 'Bu üretim kodu bulunamadı.'
        
        if uretim_kodu in aktif_uretim:
                temp = aktif_uretim[uretim_kodu]
        else:
                temp = uretim[uretim_kodu]



        query = """INSERT INTO uretim
                (uretim_kodu,
                desen,
                makine,
                hedeflenen_uretim_miktari,
                uretilen_saglam_urun,
                uretilen_hasarli_urun,
                top_sayisi,
                bicak_tipi_gereken,
                bicak_tipi_verilen,
                bicak_miktari_gereken,
                bicak_miktari_verilen,
                film_tipi_gereken,
                film_tipi_verilen,
                film_miktari_gereken,
                film_miktari_verilen,
                film_miktari_artan,
                hammadde_tipi_gereken,
                hammadde_tipi_verilen,
                hammadde_miktari_gereken,
                hammadde_miktari_verilen,
                hammadde_miktari_artan,
                rulo_miktari_gereken,
                rulo_miktari_verilen,
                rulo_miktari_artan,
                kalip_no_gereken,
                kalip_no_verilen,
                fire_tekne,
                fire_artık,
                aktif_uretim
                )
                VALUES
                (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
        data = list()
        data.append(uretim_kodu)

        for i in list(temp.values()):
                data.append(i)

        if uretim_kodu in aktif_uretim:
                data.append(1)
        else:
                data.append(0)
        print(data)
        print(len(data))

        cur.execute(query,data)
        con.commit()

print(uretim_giris('BU230010'))