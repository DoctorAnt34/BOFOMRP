"""
--Üreitme Kaydedilecek değerler--
    +Başlangıç+
        +Üretim kodu
        +Desen
        +Hedeflenen Üreitm miktarı
        +Reçete+(auto atanıcak)
            +Kalıp
            +Hammadde Miktarı ve tipi
            +Bıçak tipi
            +Film Tipi ve miktarı
            +Rulo miktarı
    +Üretim Başladıktan sonra-       
        +Girilen Hammaddeler-
            +Verilen Hammadde miktarı
            +Harcanan film miktarı
            +Kullanılan Bıçak Sayısı
            +Kalıp
            +Rulo
        +Üretilen Sağlam Ürün
        +Üretilen Hatalı Ürün
        +Top Sayısı-
            +Bağlar-
                +Parti
                +Lot
                +Miktar
                +Sağlam/hasarlı flag
    -Üreitm Sonu-
        -Çıkan Hammaddeler-
            -Geri alınan Hammadde
            -Kalan film miktarı            
        -Fire Hammadde(Tekne ve Artık)
"""
import serialization as s
from datetime import datetime
from collections import OrderedDict



DESEN = s.json_load_dict('desen')
KALIP = s.json_load_list('kalip')
URETIM = s.json_load_dict('uretim')
AKTIF_URETIM = s.json_load_dict('aktif_uretim')
BAG = s.json_load_list('bag')
BAG_VERI = s.json_load_dict('bag_veri')
receteler = s.json_load_dict('receteler')

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
    "bicak_miktari_gereken": 0,
    "bicak_miktari_verilen": 0,
    "film_tipi_gereken": "",
    "film_miktari_gereken": 0,
    "film_miktari_verilen": 0,
    "film_miktari_artan": 0,
    "hammadde_tipi_gereken": "",
    "hammadde_miktari_gereken": 0,
    "hammadde_miktari_verilen": 0,
    "hammadde_miktari_artan": 0,
    "rulo_miktari_gereken": 0,
    "rulo_miktari_verilen": 0,
    "rulo_miktari_artan": 0,
    "kalip_no_gereken": "",
    "kalip_no_verilen": "",
}    

TEMP_BAG = {
    "uretim_kodu": "",
    "desen": "",
    "metre": 0,
    "parti": "",
    'lot': "",
    "kalite": "",
}

class bofoVeri():

    def __init__(self,uretim_kodu= None):
        if uretim_kodu == None:
            self.uretim_kodu = self.uretim_kod_gen()
        else:
            self.uretim_kodu = uretim_kodu
        self.desen = None
        self.hedef_uretim = None
        self.makine = None
        self.recete = None
        self.saglam_uretim = None
        self.hatali_uretim = None
        self.top_sayisi = None
        self.bicak_tipi = None
        self.bicak_miktar_gereken = None
        self.bicak_miktar_verilen = None
        self.film_tipi = None
        self.fim_miktari_gereken = None
        self.film_miktari_verilen = None
        
    def uretim_start(self,desen,hedef_uretim,makine):  
        global DESEN
        global KALIP
        global URETIM
        global AKTIF_URETIM
        global BAG
        global BAG_VERI
        global receteler
              
        self.desen = str(desen)
        if self.desen not in receteler:return print(f'{self.desen} için bir reçete yoktur.')
        self.recete = receteler[self.desen]
        self.hedef_uretim = hedef_uretim
        self.makine = makine

        #Üretim kodunun kullanılmış olup olmadığı
        if self.uretim_kodu in URETIM or self.uretim_kodu in AKTIF_URETIM:
            uretim_kodu = self.uretim_kodu
            del self
            return print(f'{uretim_kodu} lu bir üretim zaten var. ')
        
        #Desenin gerçekten olup olmadığı.
        if self.desen not in DESEN:
            desen = self.desen
            del self
            return print(f'{desen} nolu bir desen yoktur.')
        # Makine ismi gerçek mi?
        #TODO Makine mevcut aktif üretimde varmı? eklenmeli.
        if self.makine not in MAKINELER:
            makine = self.makine
            del self
            return print(f'{makine} isimli bir makine yoktur.')
        
        uretim_veriler = dict(TEMP_URETIM)
        uretim_veriler['desen'] = self.desen
        uretim_veriler['makine'] = self.makine
        uretim_veriler['hedeflenen_uretim_miktari'] = self.hedef_uretim

        #Reçeteden gerekli sarf malzemelerin işlenmesi.Üretim miktarına göre değişecekler hesaplanıyor.
        for i,j in self.recete.items():
            if type(j) is int or type(j) is float:
                uretim_veriler[i+'_gereken'] = j*self.hedef_uretim
            else:
                uretim_veriler[i+'_gereken'] = j
        uretim_veriler['hammadde_miktari_gereken'] = round(uretim_veriler['hammadde_miktari_gereken'],2)
        # Bıçak miktarı birden düşük olmaması.
        if uretim_veriler['bicak_miktari_gereken'] < 1:uretim_veriler['bicak_miktar_gereken'] = 1
        AKTIF_URETIM[self.uretim_kodu] = uretim_veriler
        URETIM[self.uretim_kodu] = uretim_veriler

        
        print(f'{self.uretim_kodu} nolu üretim başarı ile eklendi.')

    # Aktif üretime sarf malzeme atmak için kullanılır.Aktif olmayan üretimde çalışmaz.
    def sarf_add(self,bicak_miktar = 0, film_miktar = 0, hammadde_miktar = 0, rulo_miktar = 0):
        global DESEN
        global KALIP
        global URETIM
        global AKTIF_URETIM
        global BAG
        global BAG_VERI
        global receteler
        self.bicak_miktar_verilen = bicak_miktar
        self.film_miktar_verilen = film_miktar
        if self.uretim_kodu not in AKTIF_URETIM:return print('Üretim aktif değil.')
        uretim_veriler = AKTIF_URETIM[self.uretim_kodu]
        uretim_veriler['bicak_miktari_verilen'] += self.bicak_miktar_verilen
        uretim_veriler['film_miktari_verilen'] += self.film_miktar_verilen
        uretim_veriler['hammadde_miktari_verilen'] += hammadde_miktar
        uretim_veriler['rulo_miktari_verilen'] += rulo_miktar
        uretim_veriler['kalip_no_verilen'] = self.desen[:4]
        AKTIF_URETIM[self.uretim_kodu] = uretim_veriler
        URETIM[self.uretim_kodu] = uretim_veriler
    
    def bag_add(self, bag = None, metre = 200, kalite = 'SAGLAM'):
        global DESEN
        global KALIP
        global URETIM
        global AKTIF_URETIM
        global BAG
        global BAG_VERI
        global receteler

        if bag in BAG:return print(f'{bag} nolu bir bağ kod zaten mevcut.')
        if bag == None:bag = self.bag_kod_gen()
        bag_veriler = dict(TEMP_BAG)
        bag_veriler['uretim_kodu'] = self.uretim_kodu
        bag_veriler['desen'] = self.desen
        bag_veriler['metre'] = metre
        bag_veriler['kalite'] = kalite
        bag_veriler['parti'] = datetime.today().strftime('%y%m%d')
        uretim_veriler = AKTIF_URETIM[self.uretim_kodu]
        uretim_veriler['top_sayisi'] += 1

        if uretim_veriler['top_sayisi'] < 10:
            bag_veriler['lot'] = self.makine[-1:] + "00" + str(uretim_veriler['top_sayisi'])
        else:
            bag_veriler['lot'] = self.makine[-1:] + "0" + str(uretim_veriler['top_sayisi'])

        if kalite == 'SAGLAM':
            uretim_veriler['uretilen_saglam_urun'] += metre 
        else:
            uretim_veriler['uretilen_hasarli_urun'] += metre 


        BAG_VERI[bag] = bag_veriler
        AKTIF_URETIM[self.uretim_kodu] = uretim_veriler
        URETIM[self.uretim_kodu] = uretim_veriler
        BAG.append(bag)


           
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
        if len(list(URETIM.keys())) == 0:
            list(URETIM.keys()).append('BU'+this_year+'0001')
            return 'BU'+this_year+'0001'
        else:
            temp_value = list(URETIM.keys())[(len(list(URETIM.keys()))-1)]
            temp_value_2 = int(temp_value[-4:]) + 1
            if temp_value_2 < 10:
                list(URETIM.keys()).append('BU' + this_year + '000' + str(temp_value_2))
                return 'BU' + this_year + '000' + str(temp_value_2)
            elif temp_value_2 < 100:
                list(URETIM.keys()).append('BU' + this_year + '00' + str(temp_value_2))
                return 'BU' + this_year + '00' + str(temp_value_2)
            elif temp_value_2 < 1000:
                list(URETIM.keys()).append('BU' + this_year + '0' + str(temp_value_2))
                return 'BU' + this_year + '0' + str(temp_value_2)
            elif temp_value_2 < 10000:
                list(URETIM.keys()).append('BU' + this_year + str(temp_value_2))
                return 'BU' + this_year + str(temp_value_2)
    

    @staticmethod
    def bag_kod_gen():
        old_last = int(BAG[len(BAG)-1][-6:])
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
    def aktif_uretim_cast(uretim_kodu):
        aktif_uretim = bofoVeri(uretim_kodu)
        aktif_uretim.desen = AKTIF_URETIM[uretim_kodu]['desen']
        aktif_uretim.hedef_uretim = AKTIF_URETIM[uretim_kodu]['hedeflenen_uretim_miktari']
        aktif_uretim.makine = AKTIF_URETIM[uretim_kodu]['makine']
        return aktif_uretim
    
    @staticmethod
    def sort_uretim_veri(uretim_kodu):
        unsorted_veriler = URETIM[uretim_kodu]
        sort_order = list(TEMP_URETIM.keys())
        uretim_veriler_ordered = dict()
        for key in sort_order:
            if key in unsorted_veriler: uretim_veriler_ordered[key] = unsorted_veriler[key]
        URETIM[uretim_kodu] = uretim_veriler_ordered
        if uretim_kodu in AKTIF_URETIM:
            AKTIF_URETIM[uretim_kodu] = uretim_veriler_ordered

    
    #Program açıldığında aktif üretimleri kontrol edip otomatik olarak castlama.            
    @staticmethod       
    def start_up() -> dict:
        temp_list = list(AKTIF_URETIM.keys())
        if temp_list  != []:
            aktif_üretimler = dict()
            for i in temp_list:
                aktif_üretimler[i] = bofoVeri.aktif_uretim_cast(i)
            return aktif_üretimler
        
    @staticmethod
    def commit():
        s.json_save_dict('aktif_uretim',AKTIF_URETIM)
        s.json_save_dict('uretim',URETIM)
        s.json_save_dict('bag_veri',BAG_VERI)
        s.json_save_dict('desen',DESEN)
        s.json_save_dict('recetler',receteler)
        s.json_save_list('kalip',KALIP)
        s.json_save_list('bag',BAG)

a=bofoVeri.aktif_uretim_cast('BU230001')
a.bag_add(kalite='HASARLI')
bofoVeri.commit()



