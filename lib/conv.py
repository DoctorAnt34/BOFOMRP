import uretim
import pandas as pd
from datetime import datetime

NOW_FILE = datetime.today().strftime('%d-%m-%y')


BAG_GEN_VERİ = [
    'Bicak',
    'Bicak Degisim',
    'Durum',
    'Gramaj',
    'Metre',
    'Parti'
]

BAG_HEADİNGS = [
    'Bağ Kodu',
    'Üretim Kodu',
    'Bıçak',
    'Bıçak Değişimi',
    'Durum',
    'Gramaj',
    'Metre',
    'Parti'
]
URETIM_HEADINGS = [
                   'Tarih', 
                   'Desen',
                   'Makine',
                   'Top',
                   'Bicak Sayisi',
                   'Film Tipi', 
                   'Fire Hammade', 
                   'Harcanan Film',
                   'Harcanan Malzeme',
                   'Kalip Durumu', 
                   'Toplam Hasarli Urun', 
                   'Toplam Saglam Urun'
                   ]

'''DAHA AÇIKLAYICI VE DÜZGÜN HALE GETİR!'''

def uretim_deneme(kod):
    if kod != [] :
        kod_p = kod[0]
        a = list(uretim.data.main_list[kod_p].keys())[-8:]
        b = list(uretim.data.main_list[kod_p].values())[-8:]
        c = []
        for i in range(len(a)):
            c.append([a[i],b[i]])
        del kod
        del kod_p
        return c
def bag_get(kod):
    kod_p = kod[0]
    key_dict = uretim.data.bag_uretim_list
    c = []
    for key,value in key_dict.items():
        if value == kod_p:
            c.append([key])
    del key_dict
    del kod
    del kod_p
    return c

def uretim_deneme_veri(kod):
    if kod != [] :
        kod_p = kod[0]
        a = list(uretim.data.main_list[kod_p].keys())[-12:]
        b = list(uretim.data.main_list[kod_p].values())[-12:]
        c = []
        for i in range(len(a)):
            c.append([a[i],b[i]])
        return c


#-------------Veriler Ekranı için tabloya veri çekme------------

#Değerlerin çekilmesi
def veriler_tablo_deger(uretim_kodu):
    if uretim_kodu !=[]:
        uretim_kodu = uretim_kodu[0]
        key_length = len(uretim.data.active_uretim[uretim_kodu].keys())
        db = uretim.data.active_uretim[uretim_kodu]

        if '0' in uretim.data.active_uretim[uretim_kodu]:
            data=[]
            for i in range(key_length-1):
                data_temp = []
                veri_key = list(db[str(i+1)].keys())
                data_temp = [i+1]
                for j in range (len(veri_key)):
                    data_temp.append(db[str(i+1)][veri_key[(j)]])
                data.append(data_temp)
                del data_temp
            return data

        else:
            data=[]
            for i in range(key_length):
                data_temp = []
                veri_key = list(db[str(i+1)].keys())
                data_temp = [i+1]
                for j in range (len(veri_key)):
                    data_temp.append(db[str(i+1)][veri_key[(j)]])
                data.append(data_temp)
                del data_temp

        return data            


def veriler_tablo_bas():
    return ['Veri No',
            'Bicak Sicakligi',
            'Bicak Sicaklik Ayari',
            'Kazan Sicakligi',
            'Kazan Yag Ayari',
            'Kazan Yag Donus', 
            'Oda Sicakligi Arka', 
            'Oda Sicakligi On', 
            'Olcum Alinan Metre', 
            'Olcum Alinan Zaman', 
            'Sarilmis Top Sicakligi', 
            'Sogutucu Silindir Sicakligi', 
            'Tekne Sicakligi', 
            'Tekne Sicaklik Ayari', 
            'Uretim Hizi'
            ]

#----------------Aktif Bağlara veri atma"""""""""""""""""""""

def bag_veri_tablo_data(uretim_kodu,bag_kodu):
    uretim_kodu = uretim_kodu[0]
    bag_kodu = bag_kodu[0][0]
    key_length = len(uretim.data.main_list[uretim_kodu][bag_kodu].keys())
    db = uretim.data.main_list[uretim_kodu][bag_kodu]
    data=[]
    for i in range(key_length-1):
        data_temp = []
        veri_key = list(db[str(i+1)].keys())
        data_temp = [i+1]
        for j in range (len(veri_key)):
            data_temp.append(db[str(i+1)][veri_key[(j)]])
        data.append(data_temp)
        del data_temp
    return data


def bag_std_veri_tablo_data(uretim_kodu,bag_kodu):
    uretim_kodu = uretim_kodu[0]
    bag_kodu = bag_kodu[0][0]
    db = uretim.data.main_list[uretim_kodu][bag_kodu]
    col1 = list(db['0'].keys())
    col2 = list(db['0'].values())
    data = []
    for i in range(len(col1)):
        data.append([col1[i],col2[i]])
    return data

#Bitmiş üretimlerin Listesini geri döndürüyor.
def fin_uretim():
    active_list = list(uretim.data.active_uretim.keys())
    gen_list = list(uretim.data.main_list.keys())
    fin_list = []
    for i in range(len(gen_list)):
        if gen_list[i] not in active_list:
            fin_list.append(gen_list[i])
    return fin_list



        
#Bitmiş bağların Listesini geri döndürüyor.
def fin_bag_kod() -> list:
    active_list = list(uretim.data.active_uretim.keys())
    fin_list = []
    for i in uretim.data.bag_uretim_list:
        if uretim.data.bag_uretim_list[i] not in active_list:
            fin_list.append(i)
    return fin_list


#Üretim verilerini 2d arraye çevirme.
def main_to_2d_uretim():
    fin_uretim_list = fin_uretim()
    data = []
    for i in fin_uretim_list:
        temp_data = [i]
        for j in URETIM_HEADINGS:
            temp_data.append(uretim.data.main_list[i][j])
        data.append(temp_data)
    return data

#Üretim bilgilerini excele kaydetme - raw string olarak parametre girilmesi lazım.
def uretim_excel(file_path : str):
    df = pd.DataFrame(main_to_2d_uretim())
    headings = ['Üretim Kodu']
    for i in URETIM_HEADINGS:
        headings.append(i)
    df.to_excel(f'{file_path}\{NOW_FILE}-Üretim.xlsx',header=headings, index=False)
    return 'Başarı ile kaydedildi.'


#Bütüm bağ kodlarını 2d arraye çevirme.

def main_to_2d_bag():
    data=[]
    for i in fin_uretim():
        for j in fin_bag_kod():
            if j in uretim.data.main_list[i]:
                temp_data = [j]
                temp_data.append(i)
                for k in BAG_GEN_VERİ:
                    temp_data.append(uretim.data.main_list[i][j]['0'][k])
                data.append(temp_data)
    return data

def bag_excel(file_path : str):
    df = pd.DataFrame(main_to_2d_bag())
    headings = BAG_HEADİNGS
    df.to_excel(f'{file_path}\{NOW_FILE}-Bağ.xlsx',header=headings, index=False)
    return 'Başarı ile kaydedildi.'



