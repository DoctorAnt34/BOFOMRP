#main_dict = {'BU230001':{'BP000101':{}, 'BP000102':{}, 'BP000103':{}, 'Total':{}, 'Geri Bildirim':{} } }
from datetime import datetime
import json
import os
from json.decoder import JSONDecodeError

NOW = datetime.today().strftime('%d/%m/%y')


class data():
    
    main_list = {}
    desen_list = []
    bag_uretim_list = {}
    makine_list = ['LM2','LM4','LM5','LM6']
    active_uretim = {}


def json_load():
    try:
        with open ('db\\active_uretim.json') as json_l:
            try:
                data.active_uretim = json.load(json_l)
            except JSONDecodeError:
                data.active_uretim = {}
    except OSError:
            with open('db\\active_uretim.json', 'w') as json_s:
                pass
            data.active_uretim = {}
    try:
        with open ('db\\main_list.json') as json_l:
            try:
                data.main_list = json.load(json_l)
            except JSONDecodeError:
                data.main_list = {}
    except OSError:
            with open('db\\main_list.json', 'w') as json_s:
                pass
            data.main_list = {}
    try:
        with open ('db\\desen_list.json') as json_l:
            try:
                data.desen_list = json.load(json_l)
            except JSONDecodeError:
                data.desen_list = []
    except OSError:
            with open('db\\desen_list.json', 'w') as json_s:
                pass
            data.desen_list = []
    try:
        with open ('db\\bag_uretim_list.json') as json_l:
            try:
                data.bag_uretim_list = json.load(json_l)
            except JSONDecodeError:
                data.bag_uretim_list = {}
    except OSError:
            with open('db\\bag_uretim_list.json', 'w') as json_s:
                pass
            data.bag_uretim_list = {}

        
def json_save():
    with open('db\\active_uretim.json', 'w') as json_s:
        json.dump(data.active_uretim, json_s, sort_keys = True, indent = 2)
    with open('db\\main_list.json', 'w') as json_s:
        json.dump(data.main_list, json_s, sort_keys = True, indent = 2)
    with open('db\\desen_list.json', 'w') as json_s:
        json.dump(data.desen_list, json_s, sort_keys = True, indent = 2)
    with open('db\\bag_uretim_list.json', 'w') as json_s:
        json.dump(data.bag_uretim_list, json_s, sort_keys = True, indent = 2)

def uretim_kod_gen() -> str:
    this_year = datetime.today().strftime('%y')
    if len(list(data.main_list.keys())) == 0:
        list(data.main_list.keys()).append('BU'+this_year+'0001')
        return 'BU'+this_year+'0001'
    else:
        temp_value = list(data.main_list.keys())[(len(list(data.main_list.keys()))-1)]
        temp_value_2 = int(temp_value[-4:]) + 1
        if temp_value_2 < 10:
            list(data.main_list.keys()).append('BU' + this_year + '000' + str(temp_value_2))
            return 'BU' + this_year + '000' + str(temp_value_2)
        elif temp_value_2 < 100:
            list(data.main_list.keys()).append('BU' + this_year + '00' + str(temp_value_2))
            return 'BU' + this_year + '00' + str(temp_value_2)
        elif temp_value_2 < 1000:
            list(data.main_list.keys()).append('BU' + this_year + '0' + str(temp_value_2))
            return 'BU' + this_year + '0' + str(temp_value_2)
        elif temp_value_2 < 10000:
            list(data.main_list.keys()).append('BU' + this_year + str(temp_value_2))
            return 'BU' + this_year + str(temp_value_2)


# Kullanımı sıkıntı ADMIN olarak kullanılması lazım
def uretim_kod_change(old_code, new_code):
    index = list(data.main_list.keys()).index(old_code)
    if new_code not in list(data.main_list.keys()):
        list(data.main_list.keys())[index] = new_code
    else:
        print('Yeni kod mevcut')
    del index


def uretim_start(desen : str,
                 makine : str,
                 kalıp_durumu : str,
                 film_tipi = '19 Mic',
                 tarih = NOW
                 ):
    if desen in data.desen_list:
        if makine in data.makine_list:
            temp_uretim_kod = uretim_kod_gen()
            temp_list = {
                        'Tarih' : tarih,
                        'Desen' : desen,
                        'Makine' : makine,
                        'Film Tipi' : film_tipi,
                        'Kalip Durumu' : kalıp_durumu,
                        'Top' : 0,
                        'Toplam Saglam Urun' : 0,
                        'Toplam Hasarli Urun' : 0,
                         }
            data.main_list[temp_uretim_kod] = temp_list
            data.active_uretim[temp_uretim_kod] = {'0' : 'Baslangic.'}
            return 'Başarı İle Üretim Eklendi'
        else:
            return 'Hatalı Makine girişi.'
    else:
        return 'Böyle bir desen kayıtlı değildir.'


def uretim_stop(uretim_kodu : str,
                film_metre : int,
                harc_ham : int,
                fire_ham : int,
                bicak_say = 0
                ):
    temp_dict = {'Harcanan Film' : film_metre,
                 'Harcanan Malzeme' : harc_ham,
                 'Fire Hammade' : fire_ham,
                 'Bicak Sayisi' : bicak_say,

                 }
    
    if str(uretim_kodu) in data.active_uretim:
        data.main_list[uretim_kodu].update(temp_dict)
        del data.active_uretim[uretim_kodu]
        return f'{uretim_kodu} başarı ile sonlandırılmıştır.'
    else:
        return 'Girdiğiniz üretim kodu aktif üretimlerden değildir.'

#Sadece aktif üretimler için.
def bag_kod_add(uretim_kodu : str,
                bag_kod : str,
                gramaj : int,
                bicak : str,
                metre = 200, 
                hata = 'Saglam', 
                bicak_deg = False
                ):

    if len(bag_kod) == 8:
        if bag_kod[:2] == 'BP':
            if uretim_kodu in data.active_uretim:
                if bag_kod not in data.main_list[uretim_kodu]:
                        if bag_kod not in data.bag_uretim_list:
                            temp_top = int(data.main_list[uretim_kodu]['Top']) + 1
                            data.main_list[uretim_kodu]['Top'] = temp_top
                            if temp_top < 10:
                                temp_top = str (temp_top)
                                temp_lot = data.main_list[uretim_kodu]['Makine'][-1] + '00' + temp_top
                            else:
                                temp_top = str (temp_top)
                                temp_lot = data.main_list[uretim_kodu]['Makine'][-1] + '0' + temp_top
                            
                            data.bag_uretim_list[bag_kod] = uretim_kodu
                            temp_dict = {bag_kod :{0 : {'Parti' : datetime.today().strftime('%y%m%d'),
                                                        'Lot' : temp_lot,
                                                        'Durum': hata,
                                                        'Metre' : metre,
                                                        'Gramaj' : gramaj,
                                                        'Bicak' : bicak,
                                                        'Bicak Degisim' : bicak_deg
                                                        }}}
                            data.main_list[uretim_kodu].update(temp_dict)
                            if hata == 'Saglam':
                                var_metre = data.main_list[uretim_kodu]['Toplam Saglam Urun']
                                data.main_list[uretim_kodu]['Toplam Saglam Urun'] = var_metre + metre
                            else:
                                var_metre = data.main_list[uretim_kodu]['Toplam Hasarli Urun']
                                data.main_list[uretim_kodu]['Toplam Hasarli Urun'] = var_metre + metre
                            return f'{uretim_kodu} nolu üretime {bag_kod} u eklendi.'
                        else:
                            return 'Bu bağ kodu başka bir üretimde tanımlı'
                else:
                    return'Bu bağ kodu bu üretimede zaten var'
            else:
                return 'Girdiğiniz Üretim kodu aktif üretimlerde bulunamadı.'
        else:
            return 'Bağ kodu yanlış bir formatta'
    elif len(bag_kod) < 8 :
        return 'Bağ kodu eksik girdiniz.'
    elif len(bag_kod) > 8 :
        return 'Bağ kodu fazla girdiniz.'

# Manuel bağ verisi ekleme 
def veri_add_bag(bag_kod : str,
                 time,
                 metre : int,
                 bic_temp_set : int,
                 bic_temp : int,
                 tek_temp_set : int,
                 tek_temp : int,
                 kazan_ayar : int,
                 kazan_don : int,
                 kazan_temp : int,
                 top_temp : int,
                 oda_on_temp : int,
                 oda_arka_temp : int,
                 hiz : int,
                 cool_temp : int                 
                 ):
    if bag_kod in data.bag_uretim_list:
        uretim_kod = data.bag_uretim_list[bag_kod]
        temp_veri_list = list(data.main_list[uretim_kod][bag_kod].keys())
        temp_veri_no = len(temp_veri_list)
        temp_dict = {str(temp_veri_no) :{'Olcum Alinan Zaman' : time, 
                        'Olcum Alinan Metre' : metre,
                        'Bicak Sicaklik Ayari' : bic_temp_set,
                        'Bicak Sicakligi' : bic_temp,
                        'Tekne Sicaklik Ayari' : tek_temp_set,
                        'Tekne Sicakligi' : tek_temp,
                        'Kazan Yag Ayari' : kazan_ayar,
                        'Kazan Yag Donus' : kazan_don,
                        'Kazan Sicakligi' : kazan_temp,
                        'Sarilmis Top Sicakligi' : top_temp,
                        'Oda Sicakligi On' : oda_on_temp,
                        'Oda Sicakligi Arka' : oda_arka_temp,
                        'Uretim Hizi' : hiz,
                        'Sogutucu Silindir Sicakligi' : cool_temp
                    }}
        data.main_list[uretim_kod][bag_kod].update(temp_dict)
        return f'Girdiğiniz veriler {bag_kod} a başarı ile eklendi'
    else:
        return f'Üretilmiş {bag_kod} nolu bir top yok.'

def veri_add(
        uretim_kodu : str,
        time,
        metre : int,
        bic_temp_set : int,
        bic_temp : int,
        tek_temp_set : int,
        tek_temp : int,
        kazan_ayar : int,
        kazan_don : int,
        kazan_temp : int,
        top_temp : int,
        oda_on_temp : int,
        oda_arka_temp : int,
        hiz : int,
        cool_temp : int                 
             ):
    if uretim_kodu in data.active_uretim:
        temp_veri_no = len(list(data.active_uretim[uretim_kodu].keys()))
        temp_dict = {
            str(temp_veri_no) : {
                                'Olcum Alinan Zaman' : time, 
                                'Olcum Alinan Metre' : metre,
                                'Bicak Sicaklik Ayari' : bic_temp_set,
                                'Bicak Sicakligi' : bic_temp,
                                'Tekne Sicaklik Ayari' : tek_temp_set,
                                'Tekne Sicakligi' : tek_temp,
                                'Kazan Yag Ayari' : kazan_ayar,
                                'Kazan Yag Donus' : kazan_don,
                                'Kazan Sicakligi' : kazan_temp,
                                'Sarilmis Top Sicakligi' : top_temp,
                                'Oda Sicakligi On' : oda_on_temp,
                                'Oda Sicakligi Arka' : oda_arka_temp,
                                'Uretim Hizi' : hiz,
                                'Sogutucu Silindir Sicakligi' : cool_temp
                                }
                    }
        data.active_uretim[uretim_kodu].update(temp_dict)
        return f'Veriler {uretim_kodu} nolu üretime eklendi.'
    else:
        return f'Aktif üretimlerde {uretim_kodu} nolu bir üretim yok.'

def auto_veri_add_bag (uretim_kodu : str, bag_kodu : str):
    if len(list(data.active_uretim[uretim_kodu].keys())) > 1:
        if '0' in list(data.active_uretim[uretim_kodu].keys()):
            if bag_kodu in data.main_list[uretim_kodu]:
                if '1' not in data.main_list[uretim_kodu][bag_kodu]:
                    del data.active_uretim[uretim_kodu]['0']
                    data.main_list[uretim_kodu][bag_kodu].update(data.active_uretim[uretim_kodu])
                    data.active_uretim[uretim_kodu] = {'0' : 'Baslangic.'}
                    return 'Veriler Başarı ile Eklendi.'
                else:
                    return 'Seçilen Bağ koduna zaten veri eklendi.'
            else:
                return 'Girilen üretimde girilen bağ kodu yoktur.'
        else:
            return 'Bu veri seti zaten bir bağ koduna eklendi.'
    else:
        return 'Veri datası yok.'





json_load()

json_save()




