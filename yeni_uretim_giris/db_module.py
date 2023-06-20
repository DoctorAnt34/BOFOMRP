
#TODO DB time tipi datetime olarak değişecek ve pk olacak.


import sqlite3 as sq
from sqlite3 import Error
from pathlib import Path
import serialization as s

road = Path('yeni_uretim_giris/db/uretim.db')


uretim = s.json_load_dict('uretim')
aktif_uretim = s.json_load_dict('aktif_uretim')
bag_veri = s.json_load_dict('bag_veri')

con = sq.connect(road)
cur = con.cursor()

def uretim_giris(uretim_kodu):

        query = "SELECT uretim_kodu FROM uretim"
        cur.execute(query)
        temp = cur.fetchall()
        list_uretim = []
        for i in temp:
                list_uretim.append(i[0])
        
        if uretim_kodu not in list_uretim:
     
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

                cur.execute(query,data)
                con.commit()
        else:
                if uretim_kodu not in uretim and uretim_kodu not in aktif_uretim:
                        return 'Bu üretim kodu bulunamadı.'
                
                if uretim_kodu in aktif_uretim:
                        temp = aktif_uretim[uretim_kodu]
                else:
                        temp = uretim[uretim_kodu]


                query = """
                UPDATE uretim
                SET
                desen = ?,
                makine = ?,
                hedeflenen_uretim_miktari = ?,
                uretilen_saglam_urun = ?,
                uretilen_hasarli_urun = ?,
                top_sayisi = ?,
                bicak_tipi_gereken = ?,
                bicak_tipi_verilen = ?,
                bicak_miktari_gereken = ?,
                bicak_miktari_verilen = ?,
                film_tipi_gereken = ?,
                film_tipi_verilen = ?,
                film_miktari_gereken = ?,
                film_miktari_verilen = ?,
                film_miktari_artan = ?,
                hammadde_tipi_gereken = ?,
                hammadde_tipi_verilen = ?,
                hammadde_miktari_gereken = ?,
                hammadde_miktari_verilen = ?,
                hammadde_miktari_artan = ?,
                rulo_miktari_gereken = ?,
                rulo_miktari_verilen = ?,
                rulo_miktari_artan = ?,
                kalip_no_gereken = ?,
                kalip_no_verilen = ?,
                fire_tekne = ?,
                fire_artık = ?,
                aktif_uretim = ?
                WHERE uretim_kodu = ?

                
                """
                
                data = list()

                for i in list(temp.values()):
                        data.append(i)

                if uretim_kodu in aktif_uretim:
                        data.append(1)
                else:
                        data.append(0)
                data.append(uretim_kodu)
                cur.execute(query,data)
                con.commit()


def bag_giris(bag_kodu):        

        query = "SELECT bag_kodu FROM bag_veri"
        cur.execute(query)
        temp = cur.fetchall()
        list_bag = []
        for i in temp:
                list_bag.append(i[0])
        
        if bag_kodu not in list_bag:
                if bag_kodu not in bag_veri:return 'Bağ kodu bulunamadı.'

                query = """
                INSERT INTO bag_veri
                (
                bag_kodu,
                uretim_kodu,
                desen,
                metre,
                parti,
                lot,
                kalite
                )
                values(?,?,?,?,?,?,?)

                """
                data = list()
                data.append(bag_kodu)
                temp = bag_veri[bag_kodu]
                j = 0
                for i in list(temp.values()):
                        data.append(i)
                        j +=1
                        if j >= 6: break
                cur.execute(query,data)
                con.commit()
        else:
                if bag_kodu not in bag_veri:return 'Bağ kodu bulunamadı.'
                query = """
                UPDATE bag_veri
                SET
                uretim_kodu = ?,
                desen = ?,
                metre = ?,
                parti = ?,
                lot = ?,
                kalite = ?
                WHERE bag_kodu = ?
                """

                data = list()
                temp = bag_veri[bag_kodu]
                j = 0
                for i in list(temp.values()):
                        data.append(i)
                        j +=1
                        if j >= 6: break
                
                data.append(bag_kodu)
                cur.execute(query,data)
                con.commit()

def isi_giris(bag_kodu):

        if len(list(bag_veri[bag_kodu].keys())) > 6:
                
                makine = bag_veri[bag_kodu]['lot'][:1]

                query = f"""
                SELECT No FROM isi_veri_LM{makine} WHERE bag_kodu = '{bag_kodu}'
                """
                cur.execute(query)
                temp = cur.fetchall()
                veri_list = list()
                for i in temp:
                        veri_list.append(i[0])
                

                j = 0
                for i in list(bag_veri[bag_kodu].values())[6:]:
                        data = list()
                        data.append(bag_kodu)
                        j += 1
                        data.append(j)
                        for k in list(i.values()):
                                data.append(k)
                        if data[1] not  in veri_list:
                                query = f"""
                                INSERT INTO isi_veri_LM{makine}
                                (
                                bag_kodu,
                                No,
                                time,
                                bic_sol,
                                bic_orta,
                                bic_sag,
                                tekne,
                                kazan,
                                hava_gir,
                                hava_cik,
                                oda
                                )
                                VALUES(?,?,?,?,?,?,?,?,?,?,?)
                                """
                                cur.execute(query,data)
                                con.commit()
                        else:
                                query = f"""
                                UPDATE isi_veri_LM{makine}
                                SET
                                time = ?,
                                bic_sol = ?,
                                bic_orta = ?,
                                bic_sag = ?,
                                tekne = ?,
                                kazan = ?,
                                hava_gir = ?,
                                hava_cik = ?,
                                oda = ?
                                WHERE bag_kodu = ? AND No = ?
                                """
                                data_ = data[2:]
                                data_.append(data[0])
                                data_.append(data[1])
                                cur.execute(query,data_)
                                con.commit()

        else:
                return f'{bag_kodu} nun ısı verileri yok.'

