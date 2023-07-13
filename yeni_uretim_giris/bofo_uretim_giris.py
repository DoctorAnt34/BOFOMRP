"""
TODO Üretimden Bağ çıkardıkça verilen sarf malzemelerden düşünsün yeterli yoksa uyarı versin.
TODO Üretim kodunu kalite notu gerekli mi?
TODO dict ile aynı class attr ları olsun dicten daha rahat castlenir.(sonra düşünülebilir.)
TODO Hesaplamalar eklenecek.(veritabanından veri çekilip mi yapılsın?)
TODO jsonlar db ye işlenecek.(veriler şu an için onay ile veri tabanına işlenecek.Aktif üretimler ile bitmiş üretimler aynı tabloda olacak.)
TODO ayrı bir bag classı yapılıp sonuçlar ordan catslenip işlene bilir.
TODO Stok için ayrı class.
TODO Hata Çeşitlerinin kodlanması ve stok olarak çekilebilmesi.
TODO Cari tanımlamaları.
"""

import serialization as s
from datetime import datetime





DESEN = s.json_load_dict('desen')
KALIP = s.json_load_list('kalip')
uretim = s.json_load_dict('uretim')
aktif_uretim = s.json_load_dict('aktif_uretim')
bag = s.json_load_list('bag')
bag_veri = s.json_load_dict('bag_veri')
uretim_bag=s.json_load_dict('uretim_bag')
receteler = s.json_load_dict('receteler')
isi = s.json_load_dict('isi')


MAKINELER = ['LM2','LM4','LM5','LM6']
FILM_TIPI = ['19','30','VARAK','MAT']
HAMMADDE_TIPLERI = ['1566','5250','5049W','5049B']
TEMP_URETIM = {
    "desen": "",
    "makine": "",
    "hedeflenen_uretim_miktari": 0,
    "uretilen_saglam_urun": 0,
    "uretilen_hasarli_urun": 0,
    "top_sayisi": 0,
    "bicak_tipi_gereken": "",
    "bicak_tipi_verilen": "",
    "bicak_miktari_gereken": 0,
    "bicak_miktari_verilen": 0,
    "film_tipi_gereken": "",
    "film_tipi_verilen": "",
    "film_miktari_gereken": 0,
    "film_miktari_verilen": 0,
    "film_miktari_artan": 0,
    "hammadde_tipi_gereken": "",
    "hammadde_tipi_verilen": "",
    "hammadde_miktari_gereken": 0,
    "hammadde_miktari_verilen": 0,
    "hammadde_miktari_artan": 0,
    "rulo_miktari_gereken": 0,
    "rulo_miktari_verilen": 0,
    "rulo_miktari_artan": 0,
    "kalip_no_gereken": "",
    "kalip_no_verilen": "",
    "fire_tekne": 0,
    "fire_artik": 0,
}

TEMP_BAG = {
    "uretim_kodu": "",
    "desen": "",
    "metre": 0,
    "parti": "",
    'lot': "",
    "kalite": "",
}

TEMP_ISI = {
    "time": 0,
    "Bicak Sol" : 0,
    "Bicak Orta" : 0,
    "Bicak Sag" : 0,
    "Tekne" : 0,
    "Kazan" : 0,
    "Hava Giris" : 0,
    "Hava Cikis" : 0,
    "Oda" : 0
}

class bofoVeri():
    def __init__(self,desen,hedef_uretim,makine,uretim_kodu = None,uretim_aktif=1) -> None:
        if uretim_kodu == None:
            self.uretim_kodu = self.uretim_kod_gen()
        else:
            self.uretim_kodu = uretim_kodu

        self.desen = str(desen)
        #Desenin gerçekten olup olmadığı.
        if self.desen not in DESEN:
            desen = self.desen
            del self
            return print(f'{desen} nolu bir desen yoktur.')
        # Reçetenin olup olmadığı
        if self.desen not in receteler:
            desen = self.desen
            del self
            return print(f'{self.desen} için bir reçete yoktur.')
        
        self.makine = makine
        #Makine doğru girildi mi?
        if self.makine not in MAKINELER:
            makine = self.makine
            del self
            return print(f'{makine} isimli bir makine yoktur.')

        self.hedef_uretim = hedef_uretim
        self.recete = receteler[self.desen]
        self.saglam_uretim = 0
        self.hatali_uretim = 0
        self.top_sayisi = 0
        self.bicak_tipi = self.recete['bicak_tipi']
        self.bicak_tipi_verilen = ''
        self.bicak_miktari_gereken = round(self.recete['bicak_miktari']*self.hedef_uretim)
        self.bicak_miktari_verilen = 0
        self.film_tipi = self.recete['film_tipi']
        self.film_tipi_verilen = ''
        self.film_miktari_gereken = self.recete['film_miktari']*self.hedef_uretim
        self.film_miktari_verilen = 0
        self.film_miktari_artan = 0
        self.hammadde_tipi_gereken = self.recete['hammadde_tipi']
        self.hammadde_tipi_verilen = ''
        self.hammadde_miktari_gereken = self.recete['hammadde_miktari']*self.hedef_uretim
        self.hammadde_miktari_verilen = 0
        self.hammadde_miktari_artan = 0
        self.rulo_miktari_gereken = self.recete['rulo_miktari']*self.hedef_uretim
        self.rulo_miktari_verilen = 0
        self.rulo_miktari_artan = 0
        self.kalip_no_gereken = self.recete['kalip_no']
        self.kalip_no_verilen = 0
        self.fire_tekne = 0
        self.fire_artik = 0

    def uretim_start(self):
        global aktif_uretim

        #Üretim kodunun kullanılmış olup olmadığı   
        if self.uretim_kodu in uretim or self.uretim_kodu in aktif_uretim:
            uretim_kodu = self.uretim_kodu
            del self
            return print(f'{uretim_kodu} lu bir üretim zaten var. ')

        #Makine Aktif üretimde zaten varmı?
        if self.makine in aktif_uretim:
            makine = self.makine
            del self
            return print(f'{makine} isimli makine zaten üreitmde kullanıyor..')

        veriler = list(vars(self).values())
        del veriler[0],veriler[3]
        uretim_verileri = dict(TEMP_URETIM)
        k = 0
        for i in list(uretim_verileri.keys()):
            uretim_verileri[i] = veriler[k]
            k += 1
        aktif_uretim[self.uretim_kodu] = uretim_verileri

    def sarf_add(self,bicak_tipi = '', bicak_miktar = 0, film_tipi = '', film_miktar = 0, hammadde_tipi = '', hammadde_miktar = 0, rulo_miktar = 0):
        global uretim
        global aktif_uretim
        global uretim_bag

        self.bicak_miktari_verilen += bicak_miktar
        self.film_miktari_verilen += film_miktar
        self.hammadde_miktari_verilen += hammadde_miktar
        self.rulo_miktari_verilen += rulo_miktar
        
        self.bicak_tipi_verilen = bicak_tipi
        if self.bicak_tipi_verilen == "": self.bicak_tipi_verilen = self.recete['bicak_tipi'] 
        self.film_tipi_verilen = film_tipi
        if self.film_tipi_verilen == "": self.film_tipi_verilen = self.recete['film_tipi']
        self.hammadde_tipi_verilen = hammadde_tipi
        if self.hammadde_tipi_verilen == "": self.hammadde_tipi_verilen = self.recete['hammadde_tipi']

        if self.uretim_kodu not in aktif_uretim:return print('Üretim aktif değil.')

        uretim_veriler = aktif_uretim[self.uretim_kodu]
        uretim_veriler['bicak_tipi_verilen'] = self.bicak_tipi_verilen
        uretim_veriler['bicak_miktari_verilen'] = self.bicak_miktari_verilen
        uretim_veriler['film_tipi_verilen'] = self.film_tipi_verilen
        uretim_veriler['film_miktari_verilen'] = self.film_miktari_verilen
        uretim_veriler['hammadde_tipi_verilen'] = self.hammadde_tipi_verilen
        uretim_veriler['hammadde_miktari_verilen'] = self.hammadde_miktari_verilen
        uretim_veriler['rulo_miktari_verilen'] = self.rulo_miktari_verilen
        uretim_veriler['kalip_no_verilen'] = self.desen[:4]
        aktif_uretim[self.uretim_kodu] = uretim_veriler
        uretim_bag[self.uretim_kodu] = []

    def bag_add(self, bag_kodu = None, metre = 200, kalite = 'SAGLAM'):
        global aktif_uretim
        global bag
        global bag_veri
        global uretim_bag

        if bag_kodu in bag:return print(f'{bag_kodu} nolu bir bağ kod zaten mevcut.')
        if bag_kodu == None:bag_kodu = self.bag_kod_gen()
        bag_veriler = dict(TEMP_BAG)
        bag_veriler['uretim_kodu'] = self.uretim_kodu
        bag_veriler['desen'] = self.desen
        bag_veriler['metre'] = metre
        bag_veriler['kalite'] = kalite
        bag_veriler['parti'] = datetime.today().strftime('%y%m%d')
        uretim_veriler = aktif_uretim[self.uretim_kodu]
        self.top_sayisi += 1
        uretim_veriler['top_sayisi'] = self.top_sayisi

        if uretim_veriler['top_sayisi'] < 10:
            bag_veriler['lot'] = self.makine[-1:] + "00" + str(uretim_veriler['top_sayisi'])
        else:
            bag_veriler['lot'] = self.makine[-1:] + "0" + str(uretim_veriler['top_sayisi'])

        if kalite == 'SAGLAM':
            self.saglam_uretim += metre
            uretim_veriler['uretilen_saglam_urun'] =self.saglam_uretim
        else:
            self.hatali_uretim += metre
            uretim_veriler['uretilen_hasarli_urun'] = self.hatali_uretim

        for i in isi[self.makine]:
            bag_veriler[i] = isi[self.makine][i]
        
        del isi[self.makine]
        
        bag_veri[bag_kodu] = bag_veriler
        
        aktif_uretim[self.uretim_kodu] = uretim_veriler
        bag.append(bag_kodu)
        uretim_bag[self.uretim_kodu].append(bag_kodu)


    def isi_veri(self,time, bic_sol, bic_orta, bic_sag, tekne, kazan, hava_gir, hava_cik, oda):
        global isi
        global aktif_uretim

        if self.uretim_kodu not in aktif_uretim: return "Üretim aktif değil."
        
        isi_veriler = dict(TEMP_ISI)

        isi_veriler['time'] = time
        isi_veriler['Bicak Sol'] = bic_sol
        isi_veriler['Bicak Orta'] = bic_orta
        isi_veriler['Bicak Sag'] = bic_sag
        isi_veriler['Tekne'] = tekne
        isi_veriler['Kazan'] = kazan
        isi_veriler['Hava Giris'] = hava_gir
        isi_veriler['Hava Cikis'] = hava_cik        
        isi_veriler['Oda'] = oda

        if self.makine not in isi: 
            isi[self.makine] = {}
            isi[self.makine][1] = isi_veriler
        else:
            isi[self.makine][len(list(isi[self.makine].keys()))+1] = isi_veriler
        return 'Başarı ile eklendi.'
        


            


    def uretim_end(self,film_artan,hammadde_artan,rulo_artan,fire_tekne,fire_artık):
        global aktif_uretim
        global uretim
        self.film_miktari_artan = film_artan
        self.hammadde_miktari_artan = hammadde_artan
        self.rulo_miktari_artan = rulo_artan
        self.fire_tekne = fire_tekne
        self.fire_artik = fire_artık
        if self.uretim_kodu not in aktif_uretim:return print('Üretim aktif değil.')
        uretim_veriler = aktif_uretim[self.uretim_kodu]
        uretim_veriler['film_miktari_artan'] = self.film_miktari_artan
        uretim_veriler['hammadde_miktari_artan'] = self.hammadde_miktari_artan
        uretim_veriler['rulo_miktari_artan'] = self.rulo_miktari_artan
        uretim_veriler['fire_tekne'] = self.fire_tekne
        uretim_veriler['fire_artik'] = self.fire_artik
        uretim[self.uretim_kodu] = uretim_veriler
        del aktif_uretim[self.uretim_kodu]


    #Reçete oluşturmak için fonskiyon desen ismi gramajı ve hammadde tipi girilmek zorunda.
    #film tipi girilmez ise 19 mic ,biçak tipi girilmez ise gramaja göre hesaplanır.
    #hammadde tipide gramaja göre ayarlabilir??
    @staticmethod
    def recete_const(desen, gramaj:float, hammadde_tipi, film_tipi = '19', bicak_tipi = None):
        # Bıçak tipi belirtilmez ise gramaja göre bıçak belirlenir.
        # Yuvarlak bıçak için belirtilmesi lazım!
        hammadde_tipi = str(hammadde_tipi)
        desen = str(desen)
        film_tipi = str(film_tipi)
        # Seçilen hammaddenin gerçeten olup olmadığı
        if hammadde_tipi not in HAMMADDE_TIPLERI:return print(f'{hammadde_tipi} var olmayan bir hammadde tipi')
        # Seçilen desenin gerçeten olup olmadığı.
        if desen not in DESEN:return print(f'{desen} mevcut bir desen seçimi değildir.')
        # Film tipinin geçte olup olmadığı.
        if film_tipi not in FILM_TIPI:return print(f'{film_tipi} geçerli bir film tipi değildir.')
        # Kalıbın gerçekte olup olmadığı.
        if desen[-4:] not in KALIP:return print(f'{desen[-4:]} gerçerli bir kalıp değildir.')
        # Seçilen desenin zaten bir reçetesi olup olmadığı.
        if desen not in receteler:
            yeni_recete_values = {}
            yeni_recete_values['hammadde_tipi'] = hammadde_tipi
            yeni_recete_values['hammadde_miktari'] =round((((gramaj-0.26)*160)/1000),7)
            yeni_recete_values['rulo_miktari'] = 0.005
            # Bıçak tipi belirtilmemiş ise gramaja göre bıçak atanması.
            if bicak_tipi == None:
                if gramaj < 0.32:
                    yeni_recete_values['bicak_tipi'] = 'SUPER INCE'
                elif gramaj >= 0.32 and gramaj < 0.36:
                    yeni_recete_values['bicak_tipi'] = 'NORMAL INCE'
                elif gramaj >= 0.36:
                    yeni_recete_values['bicak_tipi'] = 'KALIN'
            else:
                yeni_recete_values['bicak_tipi'] = bicak_tipi
            yeni_recete_values['bicak_miktari'] = 0.0005
            yeni_recete_values['film_tipi'] = film_tipi
            yeni_recete_values['film_miktari'] = 1
            yeni_recete_values['kalip_no'] = desen[-4:]
            receteler[desen] = yeni_recete_values
            print('Reçete başarı ile eklendi')    
        else:
            print(f'{desen} nolu desen için reçete zaten tanımlı')


    #Üreteim kodu generasyonu. Rakamı en büyük kodtan devam eder ara değerlere bakmaz.
    #ilk iki rakam yıl otomatik olarak değişir.
    @staticmethod
    def uretim_kod_gen() -> str:
        this_year = datetime.today().strftime('%y')
        if len(list(uretim.keys())) == 0:
            list(uretim.keys()).append('BU'+this_year+'0001')
            return 'BU'+this_year+'0001'
        else:
            temp_value = list(uretim.keys())[(len(list(uretim.keys()))-1)]
            temp_value_2 = int(temp_value[-4:]) + 1
            if temp_value_2 < 10:
                list(uretim.keys()).append('BU' + this_year + '000' + str(temp_value_2))
                return 'BU' + this_year + '000' + str(temp_value_2)
            elif temp_value_2 < 100:
                list(uretim.keys()).append('BU' + this_year + '00' + str(temp_value_2))
                return 'BU' + this_year + '00' + str(temp_value_2)
            elif temp_value_2 < 1000:
                list(uretim.keys()).append('BU' + this_year + '0' + str(temp_value_2))
                return 'BU' + this_year + '0' + str(temp_value_2)
            elif temp_value_2 < 10000:
                list(uretim.keys()).append('BU' + this_year + str(temp_value_2))
                return 'BU' + this_year + str(temp_value_2)


    @staticmethod
    def bag_kod_gen():
        old_last = int(bag[len(bag)-1][-6:])
        new_last = old_last + 1

        if new_last < 10:
            new_last = "BP00000"+str(new_last)
        elif new_last < 100:
            new_last = "BP0000"+str(new_last)
        elif new_last < 1000:
            new_last = "BP000"+str(new_last)
        elif new_last < 10000:
            new_last = "BP00"+str(new_last)
        elif new_last < 100000:
            new_last = "BP0"+str(new_last)
        elif new_last < 1000000:
            new_last = "BP"+str(new_last)
        return new_last





    @staticmethod
    def uretim_cast(uretim_kodu):
        if uretim_kodu not in aktif_uretim:
            print(f'{uretim_kodu} nolu üretim aktif üretimde değil.')
            veriler = uretim[uretim_kodu]
        else:
            print(f'{uretim_kodu} nolu üretim aktif üretimde.')
            veriler = aktif_uretim[uretim_kodu]
        temp=bofoVeri(veriler['desen'],veriler['hedeflenen_uretim_miktari'],veriler['makine'],uretim_kodu)
        temp.saglam_uretim = veriler['uretilen_saglam_urun']
        temp.hatali_uretim = veriler['uretilen_hasarli_urun']
        temp.top_sayisi = veriler['top_sayisi']
        temp.bicak_miktari_verilen = veriler['bicak_miktari_verilen']
        temp.film_miktari_verilen = veriler['film_miktari_verilen']
        temp.film_miktari_artan = veriler['film_miktari_artan']
        temp.hammadde_miktari_verilen = veriler['hammadde_miktari_verilen']
        temp.hammadde_miktari_artan = veriler['hammadde_miktari_artan']
        temp.rulo_miktari_verilen = veriler['rulo_miktari_verilen']
        temp.rulo_miktari_artan = veriler['rulo_miktari_artan']
        temp.kalip_no_verilen = veriler['kalip_no_verilen']
        temp.fire_artik = veriler['fire_artik']
        temp.fire_tekne = veriler['fire_tekne']
        return temp

    @staticmethod
    def commit():
        s.json_save_dict('aktif_uretim',aktif_uretim)
        s.json_save_dict('uretim',uretim)
        s.json_save_dict('bag_veri',bag_veri)
        s.json_save_dict('desen',DESEN)
        s.json_save_dict('recetler',receteler)
        s.json_save_list('kalip',KALIP)
        s.json_save_list('bag',bag)
        s.json_save_dict('uretim_bag', uretim_bag)  
        s.json_save_dict('isi',isi)


    