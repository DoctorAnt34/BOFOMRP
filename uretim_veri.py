import PySimpleGUI as sg
from datetime import datetime
import sys
sys.path.append('lib')

from lib import uretim
from lib import conv


sg.change_look_and_feel('DarkAmber')


#-------------Veri Ekleme Ekranı------------

layout_veri_ekle_col1 = sg.Column(
    [
        [
            sg.Frame('Veri Giriş Formu',[
                [
                    sg.Column(
                            [
                                [
                                    sg.Text('Üretim Kodu:', size =(18,1)), 
                                    sg.Input(key = '-VERİ-URETIM-KODU-', size =(10,1),do_not_clear=False),
                                    sg.Text('Hız:', size=(18,1)),
                                    sg.Input(key = '-HIZ-', size = (10,1),do_not_clear=False)],
                                [
                                    sg.Text('Ölçüm Alınan Saat:', size=(18,1)),
                                    sg.Input(key = '-VERİ-SAAT-', size = (10,1),do_not_clear=False),
                                    sg.Text('Ölçüm Alınan Metre:', size=(18,1)),
                                    sg.Input(key = '-VERİ-METRE-', size = (10,1),do_not_clear=False)
                                ],
                                [
                                    sg.Text('Bıçak Isı Ayarı:', size=(18,1)),
                                    sg.Input(key = '-BIC-SET-', size = (10,1),do_not_clear=False),
                                    sg.Text('Bıçak Isı Ölçümü:', size=(18,1)),
                                    sg.Input(key = '-BIC-TEMP-', size = (10,1),do_not_clear=False)
                                ],
                                [
                                    sg.Text('Tekne Isı Ayarı:', size=(18,1)),
                                    sg.Input(key = '-TEK-SET-', size = (10,1),do_not_clear=False),
                                    sg.Text('Tekne Isı Ölçümü:', size=(18,1)),
                                    sg.Input(key = '-TEK-TEMP-', size = (10,1),do_not_clear=False)
                                ],
                                [
                                    sg.Text('Kazan Ayarı:', size=(18,1)),
                                    sg.Input(key = '-KAZ-SET-', size = (10,1),do_not_clear=False),
                                    sg.Text('Top Isı Ölçümü:', size=(18,1)),
                                    sg.Input(key = '-TOP-TEMP-', size = (10,1),do_not_clear=False)
                                ],
                                [
                                    sg.Text('Kazan Dönüş:', size=(18,1)),
                                    sg.Input(key = '-KAZ-R-', size = (10,1),do_not_clear=False),
                                    sg.Text('Oda Ön Isı Ölçümü:', size=(18,1)),
                                    sg.Input(key = '-ON-TEMP-', size = (10,1),do_not_clear=False)
                                ],
                                [
                                    sg.Text('Kazan Ölçüm:', size=(18,1)),
                                    sg.Input(key = '-KAZ-TEMP-', size = (10,1),do_not_clear=False),
                                    sg.Text('Oda Arka Isı Ölçümü:', size=(18,1)),
                                    sg.Input(key = '-ARKA-TEMP-', size = (10,1),do_not_clear=False)
                                ],
                                [
                                    sg.Text('Soğutucu Silindir:', size=(18,1)),
                                    sg.Input(key = '-COOL-TEMP-', size = (10,1),do_not_clear=False)
                                ],
                                [
                                    sg.VPush()
                                ],
                                [
                                    sg.VPush()
                                ],
                                [
                                    sg.VPush()
                                ],
                                [
                                    sg.VPush()
                                ],
                                [
                                    sg.VPush()
                                ],
                                [
                                    sg.Button('Veri Ekle', key = '-VERİ-EKLE-'),
                                    sg.Push(),
                                    sg.Text('Girilecek veri detayları ->', auto_size_text=True),
                                    sg.Button('Detay')
                                ] 
                            
                            ],
                            size =(500,270)
                        )
                    ]
                ]
            )
        ]
    ]
)

veri_detay = '''
*** Bütün küsratlar nokta ile yazılmalıdır. ***
Üretim kodu : Aktif üretimlerden girilmesi gerekmekte.
Hız : Küsürat nokta ile yazılmalıdır.(3.5 gibi)
Ölçüm Alınan Saat : Örnek 10:30
Ölçüm Alınan Metre : Küsürat nokta ile yazılmalıdır.(10.23)
Bıçak Isı Ayarı : Makinenin Bıçak rezistans ayarı.
Bıçak Isı Ölçüm : Alet ile yapılan ısı ölçümü. Küsürat nokta ile.
Tekne Isı Ayarı : Makinenin Tekne rezistans ayarı.
Tekne Isı Ölçüm : Alet ile yapılan ısı ölçümü. Küsürat nokta ile.
Kazan Ayarı : Kazanın ayarlandığı hedef sıcaklık.
Kazan Dönüş : Kazanda gözüken yağ dönüş sıcaklığı.
Kazan Ölçüm : Yağ borusundan yapılan ölçüm.
Top Isı Ölçümü : Sarılmış ürün üstünden alınan ölçüm.
Oda Ön Isı Ölçümü : Odanın kalıp tarafındaki termostat değeri.
Oda Arka Isı Ölçümü : Odanın sarıcı tarafındaki termostat değeri.
Soğutucu Silindir : Soğutucu silindirden alının ölçüm.
'''

veri_bag_detay = '''
*** Bütün küsratlar nokta ile yazılmalıdır. ***
Bağ Kodu : Bağ kodu oluştuktan sonra bağ girilmeli.
Hız : Küsürat nokta ile yazılmalıdır.(3.5 gibi)
Ölçüm Alınan Saat : Örnek 10:30
Ölçüm Alınan Metre : Küsürat nokta ile yazılmalıdır.(10.23)
Bıçak Isı Ayarı : Makinenin Bıçak rezistans ayarı.
Bıçak Isı Ölçüm : Alet ile yapılan ısı ölçümü. Küsürat nokta ile.
Tekne Isı Ayarı : Makinenin Tekne rezistans ayarı.
Tekne Isı Ölçüm : Alet ile yapılan ısı ölçümü. Küsürat nokta ile.
Kazan Ayarı : Kazanın ayarlandığı hedef sıcaklık.
Kazan Dönüş : Kazanda gözüken yağ dönüş sıcaklığı.
Kazan Ölçüm : Yağ borusundan yapılan ölçüm.
Top Isı Ölçümü : Sarılmış ürün üstünden alınan ölçüm.
Oda Ön Isı Ölçümü : Odanın kalıp tarafındaki termostat değeri.
Oda Arka Isı Ölçümü : Odanın sarıcı tarafındaki termostat değeri.
Soğutucu Silindir : Soğutucu silindirden alının ölçüm.
'''
layout_veri_ekle_col2 =sg.Column(
        [
            [
            sg.Frame('Veri Giriş Bilgiler,',
                [
                    [
                        sg.Column(
                            [
                                [
                                    sg.Text('Aktif olan üretimlere veri \ngirişi yapılmak için kullanılır.', auto_size_text=True)
                                ],
                                [
                                    sg.Text('Her top için ayrı tutulur.\nTop çıktıktan sonra bağ kodu\noluşturularak o bağ koduna \nbağlanmalıdır.', auto_size_text=True)
                                ],
                                [
                                    sg.Text('Topun üretime gerçekleştirildiyse \nbağ kodu veri eklemeden \nveri eklenmelidir.', auto_size_text=True)
                                ],
                                [
                                    sg.Text('Bu menüden devam eden üretim \niçin veri girilip.\nTopun Üretiminin hemen \nardından bağ girişi yapılmadır.', auto_size_text=True)
                                ],
                            ],
                            size = (200,270)
                        )
                    ]
                ]
            )
        ]
    ]
)

layout_veri_ekle =[
                    [layout_veri_ekle_col1,layout_veri_ekle_col2],
                    [sg.Button('Geri')]

                ]
#-------------Bağ Kodu Ekleme Ekranı--------
layout_bag_add_col1=sg.Column(
    [
        [
            sg.Frame('Bağ Giriş Formu', [
                [
                    sg.Column(
                                [
                                    [
                                        sg.Text('Üretim Kodu:', size = (10,1)),
                                        sg.Input(key = '-BAG-URETİM-KOD-', size = (14,1),do_not_clear=False)
                                    ],
                                    [
                                        sg.Text('Bağ Kodu:', size = (10,1)),
                                        sg.Input(key = '-BAG-KOD-', size = (14,1),do_not_clear=False)
                                    ],
                                    [
                                        sg.Text('Gramaj:', size = (10,1)),
                                        sg.Input(key = '-GRAMAJ-', size = (14,1),do_not_clear=False)
                                    ],
                                    [
                                        sg.Text('Bıçak Tipi:', size = (10,1)),
                                        sg.Combo(['SUPER INCE','NORMAL INCE','KALIN','YUVARLAK'], key = '-BICAK-')
                                    ],
                                    [
                                        sg.Text('Metraj:', size = (10,1)),
                                        sg.Input(key = '-METRAJ-', size = (14,1),do_not_clear=False)
                                    ],
                                    [
                                        sg.Text('Top Durumu:', size = (10,1)),
                                        sg.Radio('Sağlam','-TOP-DURUM_'),
                                        sg.Radio('Hasarlı','-TOP-DURUM_')
                                    ],
                                    [
                                        sg.Text('Bıçak Değişti mi:', size = (10,1)),
                                        sg.Radio('Değişti ','-BICAK-DURUM-',),
                                        sg.Radio('Değişmedi','-BICAK-DURUM-')
                                    ],
                                    [
                                        sg.VPush()
                                    ],
                                    [
                                        sg.VPush()
                                    ],
                                    [
                                        sg.VPush()
                                    ],
                                    [
                                        sg.VPush()
                                    ],
                                    [
                                        sg.VPush()
                                    ],
                                    [
                                        sg.VPush()
                                    ],
                                    [
                                        sg.VPush()
                                    ],
                                    [
                                        sg.VPush()
                                    ],
                                    [
                                        sg.Button('Bağ Kodu Ekle', key = '-BAG-EKLE-')
                                    ]

                            ],
                            size= (300,270)
                        )
                    ]
                ]
            )
        ]
    ]
)

layout_bag_add_col2 =sg.Column(
    [
        [sg.Frame('Bilgiler',
            [
                [
                    sg.Column(
                                [
                                    [
                                        sg.Text('''Desen: Yapılacak desen girilecek.\nYeni yapılacak bir desen yada daha önce denenmemiş\nbir üretim ise desen olarak eklemesi yapılması gerekmekte.''', auto_size_text=True)
                                    ],
                                    [
                                        sg.Text('Makine: Üretim yapılacak makine seçilir.', auto_size_text=True)
                                    ],
                                    [
                                        sg.Text('''Film Tipi: Üretimde kullanılacak film tipi.\nBirşey girilmez ise 19 Micron film üretime atanır.''',auto_size_text=True)
                                    ],
        
                                ],
                                size = (400,270)
                        )
                    ]
                ]
            )
        ]
    ]
)

layout_bag_add = [
    [
        layout_bag_add_col1,layout_bag_add_col2
    ],
    [sg.Button('Geri')]
]

#-------------Direk Bağ Koda veri ekleme ekranı--------
layout_bag_veri_add_col1 = sg.Column(
    [
        [sg.Frame('Bağ Koda Veri Ekleme',
            [
                [
                    sg.Column(
                        [
                            [
                                sg.Text('Bağ Kodu:', size =(18,1)),
                                sg.Input(key = '-VERİ-BAG-KODU-', size =(10,1),do_not_clear=False),
                                sg.Text('Hız:', size=(18,1)),
                                sg.Input(key = '-HIZ-BAG-', size = (10,1),do_not_clear=False)
                            ],
                            [
                                sg.Text('Ölçüm Alınan Saat:', size=(18,1)),
                                sg.Input(key = '-VERİ-SAAT-BAG-', size = (10,1),do_not_clear=False),
                                sg.Text('Ölçüm Alınan Metre:', size=(18,1)),
                                sg.Input(key = '-VERİ-METRE-BAG-', size = (10,1),do_not_clear=False)
                            ],
                            [
                                sg.Text('Bıçak Isı Ayarı:', size=(18,1)),
                                sg.Input(key = '-BIC-SET-BAG-', size = (10,1),do_not_clear=False),
                                sg.Text('Bıçak Isı Ölçümü:', size=(18,1)),
                                sg.Input(key = '-BIC-TEMP-BAG-', size = (10,1),do_not_clear=False)
                            ],
                            [
                                sg.Text('Tekne Isı Ayarı:', size=(18,1)),
                                sg.Input(key = '-TEK-SET-BAG-', size = (10,1),do_not_clear=False),
                                sg.Text('Tekne Isı Ölçümü:', size=(18,1)),
                                sg.Input(key = '-TEK-TEMP-BAG-', size = (10,1),do_not_clear=False)
                            ],
                            [
                                sg.Text('Kazan Ayarı:', size=(18,1)),
                                sg.Input(key = '-KAZ-SET-BAG-', size = (10,1),do_not_clear=False),
                                sg.Text('Top Isı Ölçümü:', size=(18,1)),
                                sg.Input(key = '-TOP-TEMP-BAG-', size = (10,1),do_not_clear=False)
                            ],
                            [
                                sg.Text('Kazan Dönüş:', size=(18,1)),
                                sg.Input(key = '-KAZ-R-BAG-', size = (10,1),do_not_clear=False),
                                sg.Text('Oda Ön Isı Ölçümü:', size=(18,1)),
                                sg.Input(key = '-ON-TEMP-BAG-', size = (10,1),do_not_clear=False)
                            ],
                            [
                                sg.Text('Kazan Ölçüm:', size=(18,1)),
                                sg.Input(key = '-KAZ-TEMP-BAG-', size = (10,1),do_not_clear=False),
                                sg.Text('Oda Arka Isı Ölçümü:', size=(18,1)),
                                sg.Input(key = '-ARKA-TEMP-BAG-', size = (10,1),do_not_clear=False)
                            ],
                            [
                                sg.Text('Soğutucu Silindir:', size=(18,1)),
                                sg.Input(key = '-COOL-TEMP-BAG-', size = (10,1),do_not_clear=False)
                            ],
                            [
                                sg.VPush()
                            ],
                            [
                                sg.VPush()
                            ],
                            [
                                sg.VPush()
                            ],
                            [
                                sg.VPush()
                            ],
                            [
                                sg.VPush()
                            ],
                            [
                                sg.Button('Veri Ekle', key = '-VERİ-EKLE-BAG-'),
                                sg.Push(),
                                sg.Text('Girilecek veri detayları ->', auto_size_text=True),
                                sg.Button('Detay', key ='-BAG-DETAY-')
                            ] 
                            ],
                            size = (500,270)
                        )
                    ]
                ]
            )
        ]
    ]
)

layout_bag_veri_add_col2 =sg.Column(
    [
        [
            sg.Frame('Veri Giriş Bilgiler,',
                    [
                        [
                            sg.Column(
                            [
                                [
                                    sg.Text('Oluşturulmuş bağlara veri \ngirişi yapılmak için kullanılır.', auto_size_text=True)
                                ],
                                [
                                    sg.Text('Geriye dönük veri girişi için\nkullanıla bilir.\nÜretimi devam eden \ntop için kullanılmamamlı.', auto_size_text=True)
                                ],
                                [
                                    sg.Text('Topun üretime gerçekleştirildiyse \nbağ kodu veri eklemeden \nveri eklenmelidir.', auto_size_text=True)
                                ],
                            ],
                            size = (200,270)
                       )
                    ]
                ]
            )
        ]
    ]
)

layout_bag_veri_add = [
    [
        layout_bag_veri_add_col1,
        layout_bag_veri_add_col2
    ],
    [sg.Button('Geri')]
]
#-------------Üretim Bitirme Ekranı--------
layout_uretim_bitirme_col1 = sg.Column(
    [
        [sg.Frame('Üretim Bitirme Formu', 
            [
                [sg.Column(
                        [
                            [
                                sg.Text('Üretim Kodu', size = (22,1)),
                                sg.Input(key = '-URETİM-KOD-BIT-', size = (10,1), do_not_clear= False)
                            ],
                            [
                                sg.Text('Toplam Harcanan Film', size = (22,1)),
                                sg.Input(key = '-FILM-BIT-', size = (10,1), do_not_clear= False)
                            ],
                            [
                                sg.Text('Toplam Harcanan Hammadde', size = (22,1)),
                                sg.Input(key = '-MAL-BIT-', size = (10,1), do_not_clear= False)
                            ],
                            [
                                sg.Text('Toplam Fire Hammadde', size = (22,1)),
                                sg.Input(key = '-FIRE-BIT-', size = (10,1), do_not_clear= False)
                            ],
                            [
                                sg.Text('Toplam Harcanan Bıçak', size = (22,1)),
                                sg.Input(key = '-BIC-BIT-', size = (10,1), do_not_clear= False)
                            ],
                            [
                                sg.VPush()
                            ],
                            [
                                sg.VPush()
                            ],
                            [
                                sg.VPush()
                            ],
                            [
                                sg.VPush()
                            ],
                            [
                                sg.VPush()
                            ],
                            [
                                sg.VPush()
                            ],
                            [
                                sg.VPush()
                            ],
                            [
                                sg.VPush()
                            ],
                            [
                                sg.VPush()
                            ],
                            [
                                sg.VPush()
                            ],
                            [
                                sg.VPush()
                            ],
                            [
                                sg.VPush()
                            ],
                            [
                                sg.VPush()
                            ],
                            [
                                sg.VPush()
                            ],
                            [
                                sg.VPush()
                            ],
                            [
                                sg.VPush()
                            ],
                            [
                                sg.VPush()
                            ],
                            [
                                sg.VPush()
                            ],
                            [
                                sg.Button('Üretim Bitirme', key = '-URETİM-BİTİRME-')
                            ] 
                        ],
                        size = (300,270))                   
                    ]
                ]
            )
        ]
    ]
)

layout_uretim_bitirme_col2 =sg.Column(
    [
        [sg.Frame('Veri Giriş Bilgiler,',
            [
                [sg.Column(
                            [
                                [
                                    sg.Text('Üretimi sonlandırmak için kullanılır.', auto_size_text=True)
                                ],
                                [
                                    sg.Text('Üretim kodu : Sonlandırılacak üretim kodu yazılır. ', auto_size_text=True)
                                ],
                                [
                                    sg.Text('Toplam Harcanan Film : Gün sonunda makinadan okunan metraj \ngün başından çıkarılır. \nSonuçta bir üretim için harcanan film bulunur.', auto_size_text=True)
                                ],
                                [
                                    sg.Text('Toplam Harcanan Hammadde : Üretime verilen toplam\nhammaddeden gün sonu geri alınan hammadde çıkarılarak bulunur.', auto_size_text=True)
                                ],
                                [
                                    sg.Text('Toplam Fire Hammadde : Üretim sonunda çöpe giden hammadde \nmiktarı.', auto_size_text=True)
                                ],
                                [
                                    sg.Text('Toplam Harcanan Bıçak : Üretim için toplam harcanan \nbıçak miktarı.', auto_size_text=True)
                                ],
                            ],
                            size = (400,270)
                        )
                    ]
                ]
            )
        ]
    ]
)

layout_uretim_bitirme = [
    [
        layout_uretim_bitirme_col1,
        layout_uretim_bitirme_col2
    ],
    [sg.Button('Geri')]
]

#-------------Üretim Ekleme Ekranı----------
layout_uretim_ekle_col1=sg.Column(
    [
        [sg.Frame('Üretim Giriş Formu', 
            [
                [sg.Column(
                            [
                                [
                                    sg.Text('Desen:', size = (10,1)),
                                    sg.Input(key = '-DESEN-',size =(10,1),do_not_clear=False)
                                ],
                                [
                                    sg.Text('Makine:', size = (10,1)), sg.Radio('LM2','-MAKİNE-'),
                                    sg.Radio('LM4','-MAKİNE-')
                                ],
                                [
                                    sg.Text('',size = (10,1)),sg.Radio('LM5','-MAKİNE-'),
                                    sg.Radio('LM6','-MAKİNE-')
                                ],
                                [
                                    sg.Text('Kalıp Durumu:', size = (10,1)),
                                    sg.Combo(['YIKANDI','YIKANMADI','YENİ KALIP'],key = '-KALIP-DURUMU-')
                                ],
                                [
                                    sg.Text('Film Tipi:', size = (10,1), tooltip='Birşey Girilmez ise 19 Mic'),
                                    sg.Combo(['19 Mic', '30 Mic', 'MAT', 'VARAK'],key='-FİLM-TİPİ-')
                                ],
                                [
                                    sg.VPush()
                                ],
                                [
                                    sg.VPush()
                                ],
                                [
                                    sg.VPush()
                                ],
                                [
                                    sg.VPush()
                                ],
                                [
                                    sg.VPush()
                                ],
                                [
                                    sg.VPush()
                                ],
                                [
                                    sg.VPush()
                                ],
                                [
                                    sg.VPush()
                                ],
                                [
                                    sg.VPush()
                                ],
                                [
                                    sg.VPush()
                                ],
                                [
                                    sg.VPush()
                                ],
                                [
                                    sg.VPush()
                                ],
                                [
                                    sg.VPush()
                                ],
                                [
                                    sg.VPush()
                                ],
                                [
                                    sg.VPush()
                                ],
                                [
                                    sg.VPush()
                                ],
                                [
                                    sg.VPush()
                                ],
                                [
                                    sg.Button('Üretim Ekle', key = '-URETİM-EKLE-',enable_events=True)
                                ]
                            ],
                            size = (300,270)
                        )
                    ]
                ]
            )
        ]
    ]
)
layout_uretim_ekle_col2 =sg.Column(
    [
        [sg.Frame('Bilgiler',
            [
                [sg.Column(
                            [
                                    [
                                        sg.Text('''Desen: Yapılacak desen girilecek.\nYeni yapılacak bir desen yada daha önce denenmemiş\nbir üretim ise desen olarak eklemesi yapılması gerekmekte.''', auto_size_text=True)
                                    ],
                                    [
                                        sg.Text('Makine: Üretim yapılacak makine seçilir.', auto_size_text=True)
                                    ],
                                    [
                                        sg.Text('''Film Tipi: Üretimde kullanılacak film tipi.\nBirşey girilmez ise 19 Micron film üretime atanır.''',auto_size_text=True)
                                    ],
  
                            ],
                            size = (400,270)
                        )
                    ]
                ]
            )
        ]
    ]
)

layout_uretim_ekle = [
    [
        layout_uretim_ekle_col1,
        layout_uretim_ekle_col2
    ],
    [sg.Button('Geri')]
]


#------------Üretim Ekranı----------------
#Üretim ana ekran kolonlar

col_active_uretim = sg.Column(
    [
        [sg.Frame('Aktif Üretimler',
            [
                [sg.Column(
                            [
                                [
                                    sg.Push(),
                                    sg.Listbox(
                                        values = list(uretim.data.active_uretim.keys()),
                                        size = (11,13),
                                        key = '-URETIM-KODU-',
                                        enable_events=True,
                                        no_scrollbar=True
                                    ),
                                    sg.Push()
                                ],
                                [
                                    sg.Push(),
                                    sg.Button('Veriler'),
                                    sg.Push()
                                ]
                            ],
                            size = (100,270)
                        )
                    ]
                ],
                title_location=sg.TITLE_LOCATION_TOP
            )
        ]
    ]
)


col_selecet_uretim = sg.Column(
    [
        [sg.Frame('Üretim Verileri',
            [
                [sg.Column(
                            [
                                [
                                    sg.Push(),
                                    sg.Table(
                                        values=[],
                                        key = '-TABLE-',
                                        headings=['İsim','Değer'],
                                        justification = 'left',
                                        auto_size_columns = False,
                                        vertical_scroll_only=True,
                                        max_col_width= 50,
                                        def_col_width=26,
                                        num_rows= 13,
                                        hide_vertical_scroll=True
                                    ),
                                    sg.Push()
                                ],
                                [sg.Push(),
                                sg.Button('Veri Ekle'),
                                sg.Push()]
                            ],
                            size = (500,270)
                        )
                    ]
                ],
                title_location=sg.TITLE_LOCATION_TOP
            )
        ]
    ]
)

col_select_bag = sg.Column(
    [
        [sg.Frame('Bağ Kodlar',
            [
                [sg.Column(
                            [
                                [
                                    sg.Push(),
                                    sg.Listbox(
                                        values=[],
                                        size = (11,13),
                                        key = '-BAG-KODU-',
                                        enable_events=True,  
                                        no_scrollbar =True         
                                    ),
                                    sg.Push()
                                ],
                                [sg.Push(),
                                sg.Button('Veriler',key = '-BAG-VERİLER-'),
                                sg.Push()]
                            ],
                            size = (100,270)
                        )
                    ]
                ],
                title_location=sg.TITLE_LOCATION_TOP
            )
        ]
    ]
)

layout_main_uretim = [
    [
        col_active_uretim,
        col_selecet_uretim,
        col_select_bag
    ],
    [sg.Button('Geri')]
]
#--------------------tab grup-------------
uretim_veri_tab_group = [
    [
        sg.Image('bofologo.png',size=(100,48)),
        sg.Text('Bozkurt Baskı Üretim Takip Sistemi',size =(30,1),font=("Arial Black", 25),relief=sg.RELIEF_RIDGE,justification='center')
    ],
    [
        sg.TabGroup(
                    [
                        [
                            sg.Tab('Ana Üretim', layout_main_uretim),
                            sg.Tab('Üretim Ekleme', layout_uretim_ekle),
                            sg.Tab('Veri Girişi(Bağ Kodsuz)', layout_veri_ekle),
                            sg.Tab('Bağ Kodu Ekleme', layout_bag_add),
                            sg.Tab('Bağ Koduna Veri Ekleme', layout_bag_veri_add),
                            sg.Tab('Üretim Bitirme',layout_uretim_bitirme), 
                        ],
            ],
            tab_location = 'centertop',
            selected_title_color = 'Yellow',
        )
    ]
]

#----------------------Veriler Ekranı----------------------------
def veri_table(uretim_kodu,data):
    col_veri_active_uretim = sg.Column(
    [
        [sg.Frame('Aktif Üretimler',
            [
                [sg.Column(
                            [
                                    [
                                        sg.Listbox(
                                            list(uretim.data.active_uretim.keys()),
                                            size = (18,18),
                                            key = '-URETIM-KODU-VERİ-',
                                            enable_events=True,
                                            no_scrollbar=True
                                        )
                                    ]   
                                ],
                                size = (100,270)
                            )
                        ]
                    ],
                    title_location=sg.TITLE_LOCATION_TOP
                )
            ]
        ]
    )

    col_veri_table = sg.Column(
    [
        [sg.Frame(f'{uretim_kodu} Üretim Verileri',
            [
                [sg.Column(
                    [
                                    [
                                        sg.Table(
                                            values=[],
                                            key = '-TABLE-VERİ-',
                                            headings=conv.veriler_tablo_bas(),
                                            justification = 'center',
                                            auto_size_columns = False,
                                            vertical_scroll_only=True,
                                            max_col_width= 20,
                                            def_col_width=5, 
                                            col_widths=[5,10,14,11,11,12,13,12,14,14,14,17,10,10,8],
                                            num_rows= 15
                                        )
                                    ]
                                ],
                                size=(1630,270)
                            )
                        ]
                    ],
                    title_location=sg.TITLE_LOCATION_TOP
                )
            ]
        ]
    )

    layout_veriler = [
        [
            col_veri_table
        ],
    ]

    window_veri  = sg.Window('Girilmiş Veriler', layout_veriler,finalize=True)
    window_veri['-TABLE-VERİ-'].update(values = data )

    return window_veri

#----------------------Aktif Üretim Bağ verileri---------------------

def veri_bag_table(bag_kodu,data_veri, data_ana):
    col_ana_veri = sg.Column(
        [
            [sg.Frame(f'{bag_kodu} Genel Veriler',
                [
                    [sg.Column(
                        [
                                    [
                                        sg.Push(),
                                        sg.Table(
                                            values=[],
                                            key = '-BAG-ANA-',
                                            headings=['Veri Adı','Veri'],
                                            justification = 'center',
                                            auto_size_columns = False,
                                            vertical_scroll_only=True,
                                            max_col_width= 20,
                                            def_col_width=20, 
                                            num_rows= 15,
                                            hide_vertical_scroll=True
                                        ),
                                        sg.Push()
                                    ]
                                ],
                                size = (400,270)
                            )
                        ]
                    ],
                    title_location=sg.TITLE_LOCATION_TOP
                )
            ]
        ]
    )

    col_ure_veri = sg.Column(
        [
            [sg.Frame(f'{bag_kodu} Üretim Veriler',
                [
                    [sg.Column(
                        [
                                [
                                    sg.Push(),
                                    sg.Table(
                                        values=[],
                                        key = '-BAG-URE-',
                                        headings=conv.veriler_tablo_bas(),
                                        justification = 'center',
                                        auto_size_columns = False,
                                        vertical_scroll_only=True,
                                        max_col_width= 20,
                                        def_col_width=5, 
                                        col_widths=[5,10,14,11,11,12,13,12,14,14,14,17,10,10,8],
                                        num_rows= 15,
                                    ),
                                    sg.Push()
                                ]
                            ],
                            size = (1630,270)
                        )
                    ]
                ],
                title_location=sg.TITLE_LOCATION_TOP
                )
            ]
        ]
    )

    layout_bag_veri = [
        [
            col_ana_veri,
            col_ure_veri
        ]
    ]
    window_bag_veri = sg.Window('Bağ verileri', layout_bag_veri,finalize=True)      
    window_bag_veri['-BAG-URE-'].update(values = data_veri)
    window_bag_veri['-BAG-ANA-'].update(values = data_ana)

    return window_bag_veri


#--------------------Ana Menü--------------------------

main_menu_layout = [
    [
        sg.Image('bofologo.png',size=(100,48)),
        sg.Text('Bozkurt Baskı Üretim Takip Sistemi',size =(30,1),font=("Arial Black", 25),relief=sg.RELIEF_RIDGE,justification='center')
    ],
    [
        sg.Button(
                    'Üretim Veri Girişi',
                    key = '-URETİM-VERİ-GİRİSİ',
        ),
        sg.Button(
                    'Bitmiş Üretim Verileri',
                    key = '-BİTMİS-VERİ-'
        ),
        sg.Button(
                    'Veri Grafikleri',
                    key = '-VERİ-GRAFİK-'
        ),
        sg.Button(
                    'Depo Miktarları',
                    key = '-DEPO-MİK-'
        ),
        sg.Push(),
        sg.Button('Export'),
        sg.Button('Ayarlar')
    ]
]
layout_col1 =sg.Column(
    [
        [sg.Frame('Üretim Kodları',
            [
                [sg.Column(
                            [
                                [
                                    sg.Input(size = (10,1),key = '-VERİ-OKU-ÜRETİM-KODU-'),
                                    sg.Button('Ara', key ='-VERİ-OKU-ARA-URETİM-KOD-' ),
                                ],
                                [
                                    sg.Push(),
                                    sg.Listbox(
                                        values=conv.fin_uretim(),
                                        size = (11,13),
                                        key = '-VERİ-OKU-URETIM-KODU-LIST-',
                                        enable_events=True,
                                        no_scrollbar=False,
                                    ),
                                    sg.Push()                                       
                                ]
                            ]
                        )
                    ]
                ],
                title_location = sg.TITLE_LOCATION_TOP 
            )
        ]
    ]
)

layout_col2 =sg.Column(
    [
        [sg.Frame('Bağ Kodları',
            [
                [sg.Column(
                            [
                                [
                                    sg.Input(size = (10,1),key = '-VERİ-OKU-BAG-KOD-'),
                                    sg.Button('Ara', key ='-VERİ-OKU-ARA-BAG-KOD-' ),
                                ],
                                [
                                    sg.Push(),
                                    sg.Listbox(
                                        values = conv.fin_bag_kod(),
                                        size = (11,13),
                                        key = '-VERİ-OKU-BAG-KODU-',
                                        enable_events=True,
                                        no_scrollbar=False
                                    ),
                                    sg.Push()                                       
                                ]
                            ]
                        )
                    ]
                ],
                title_location = sg.TITLE_LOCATION_TOP 
            )
        ]
    ]
)
    
layout_col3 =sg.Column(
    [
        [sg.Frame('Genel Üretim Verileri',
            [
                [sg.Column(
                            [
                                [
                                    sg.Push(),
                                    sg.Table(
                                        values=[],
                                        key = '-VERİ-OKU-GENEL-TABLE-',
                                        headings=['İsim','Değer'],
                                        justification = 'center',
                                        auto_size_columns = False,
                                        vertical_scroll_only=True,
                                        max_col_width= 20,
                                        def_col_width=5, 
                                        col_widths=[16,12],
                                        num_rows = 12,
                                        hide_vertical_scroll=True
                                    ),
                                    sg.Push()                                       
                                ]
                            ],size = (282,230)
                        )
                    ]
                ],
                title_location = sg.TITLE_LOCATION_TOP
            )
        ]
    ]
)

layout_col4 =sg.Column(
    [
        [sg.Frame('Genel Bağ Verileri',
            [
                [sg.Column(
                            [
                                [
                                    sg.Push(),
                                    sg.Table(
                                        values=[],
                                        key = '-BAG-GENEL-VERİ-',
                                        headings=['Veri Adı','Veri'],
                                        justification = 'center',
                                        auto_size_columns = False,
                                        vertical_scroll_only=True,
                                        max_col_width= 20,
                                        def_col_width=5, 
                                        col_widths=[16,12],
                                        num_rows = 7,
                                        hide_vertical_scroll=True
                                    ),
                                    sg.Push()                                       
                                ]
                            ],size = (282,150)
                        )
                    ]
                ],
                title_location = sg.TITLE_LOCATION_TOP
            )
        ]
    ]
)

#------------------------Veri Ekranı-------------------
layout_veri = sg.Column(
    [
        [
            layout_col1,
            layout_col2,
        ],
        [
            sg.Text('Seçilmiş Üretim Kodu: ', key = '-VERİ-URETİM-KOD-TEXT-'),
        ],
        [
            sg.Text('Seçilmiş Bağ Kodu: ',key = '-VERİ-BAG-KOD-TEXT-'),
        ],
        [
            layout_col3,
        ],
        [
            layout_col4
        ],
        [
            sg.Button('Geri', key = 'GERİ-VERİ'),
            sg.Push(),
            sg.Button('Temizle')
        ]
    ]
)


layout_bag_veri_table = sg.Column(
    [
        [sg.Frame('Bağ Kod Verileri',
            [
                [sg.Column(
                    [
                                [
                                    sg.Push(),
                                    sg.Table(
                                        values=[],
                                        key = '-BAG-TABLE-VERİ-',
                                        headings=conv.veriler_tablo_bas(),
                                        justification = 'center',
                                        auto_size_columns = False,
                                        vertical_scroll_only=True,
                                        max_col_width= 20,
                                        def_col_width=5, 
                                        col_widths=[5,10,14,11,11,12,13,12,14,14,14,17,10,10,8],
                                        num_rows=48,
                                    ),
                                    sg.Push()
                                ],
                                [
                                    sg.VPush()
                                ]
                            ],expand_x=True,expand_y=True
                            
                        )
                    ]
                ],
                title_location=sg.TITLE_LOCATION_TOP,expand_x=True,expand_y =True
            )
        ]
    ]
)



layout_veri_ana = [
    [
        layout_veri,
        layout_bag_veri_table
    ]
]

#------------------Export Popup-------------------------

def export_popup():
    layout = [
        [
        sg.Text('Excel olarak çıktı almak istediğiniz veri tipini seçin.'),
        ],
        [
        sg.Button('Üretim Verileri'),sg.Button('Bağ Verileri'),sg.Push(),sg.Button('İptal')
        ]
        ]
    window_export = sg.Window('Export',layout,modal=True)

    while True:
        event, values = window_export.read()
        if event == sg.WIN_CLOSED or event == 'Exit' or event == 'İptal':
            break
        if event == 'Üretim Verileri':
            file_path = sg.popup_get_folder('Kaydedilecek yeri seçin.')
            if file_path is not None:
                test = conv.uretim_excel(file_path)
                sg.popup(test)

        if event == 'Bağ Verileri':
            file_path = sg.popup_get_folder('Kaydedilecek yeri seçin.')
            if file_path is not None:
                test = conv.bag_excel(file_path)
                sg.popup(test)
    window_export.close()


#------------------Ana layout----------------------------
main_layout = [
    [
        sg.Column(
                    main_menu_layout,
                    key = '-COL1',
                    visible = True              
         ),
        sg.Column(
                    uretim_veri_tab_group,
                    key = '-COL2',
                    visible = False
        ),
        sg.Column(
                    layout_veri_ana,
                    key = '-COL3',
                    visible = False                    
        )
        
    ]
]

location = sg.user_settings_get_entry('-location-', (None,None))

window = sg.Window('BOFO VERİ V0.01',main_layout , default_element_size = (40,1), grab_anywhere=False, enable_close_attempted_event=True,location=location)

def clear_input():
    for key in values:
        window[key]('')
    return None

uretim.json_load()
layout = 1
location = sg.user_settings_get_entry('-location-', (None,None))


while True:
    event, values = window.read()
    if event == sg.WIN_CLOSE_ATTEMPTED_EVENT or event == 'Exit':
        sg.user_settings_set_entry('-location-', window.current_location())
        break
    
    if event == '-URETİM-VERİ-GİRİSİ':
        window[f'-COL{layout}'].update(visible = False)
        layout = 2
        window[f'-COL{layout}'].update(visible = True)
    
    if event == '-BİTMİS-VERİ-':
        window[f'-COL{layout}'].update(visible = False)
        layout = 3
        window[f'-COL{layout}'].update(visible = True)
        window['-VERİ-OKU-URETIM-KODU-LIST-'].update(values = conv.fin_uretim())
        window['-VERİ-OKU-BAG-KODU-'].update(values = conv.fin_bag_kod())
    
    if event[:4] == 'Geri':
        window[f'-COL{layout}'].update(visible = False)
        layout = 1
        window[f'-COL{layout}'].update(visible = True)
        window['-URETIM-KODU-'].update(values = list(uretim.data.active_uretim.keys()))
        
    if event == 'GERİ-VERİ':
        window[f'-COL{layout}'].update(visible = False)
        layout = 1
        window[f'-COL{layout}'].update(visible = True)
        window['-URETIM-KODU-'].update(values = list(uretim.data.active_uretim.keys()))
        window['-VERİ-BAG-KOD-TEXT-'].update(f'Seçilmiş Bağ Kodu: ')
        window['-VERİ-URETİM-KOD-TEXT-'].update(f'Seçilmiş Üretim Kodu: ')

    if event == 'Veriler' :
        data = conv.veriler_tablo_deger(values['-URETIM-KODU-'])
        if values['-URETIM-KODU-'] != []: 
            veri_table(values['-URETIM-KODU-'][0],data)
        
    if event == '-URETIM-KODU-':
        window['-TABLE-'].update(values = conv.uretim_deneme(values['-URETIM-KODU-']))
        window['-BAG-KODU-'].update(values = conv.bag_get(values['-URETIM-KODU-']))
    if event == '-URETİM-EKLE-':
        if values[2] == True: makine ='LM2'
        if values[3] == True: makine ='LM4'
        if values[4] == True: makine ='LM5'
        if values[5] == True: makine ='LM6'
        test = uretim.uretim_start(values['-DESEN-'],makine,values['-KALIP-DURUMU-'],values['-FİLM-TİPİ-'])
        sg.popup(test)
        if test == 'Başarı İle Üretim Eklendi':
            uretim.json_save()
            window['-URETIM-KODU-'].update(values = list(uretim.data.active_uretim.keys()))
        del test
    if event == 'Detay':
        sg.popup(veri_detay)
    if event == '-VERİ-EKLE-':
        test = uretim.veri_add(values['-VERİ-URETIM-KODU-'],
                               values['-VERİ-SAAT-'],
                               int(values['-VERİ-METRE-']),
                               int(values['-BIC-SET-']),
                               float(values['-BIC-TEMP-']),
                               int(values['-TEK-SET-']),
                               float(values['-TEK-TEMP-']),
                               int(values['-KAZ-SET-']),
                               int(values['-KAZ-R-']),
                               float(values['-KAZ-TEMP-']),
                               float(values['-TOP-TEMP-']),
                               float(values['-ON-TEMP-']),
                               float(values['-ARKA-TEMP-']),
                               float(values['-HIZ-']),
                               float(values['-COOL-TEMP-']),
        )
        uretim_kodu = values['-VERİ-URETIM-KODU-']
        if test == f'Aktif üretimlerde {uretim_kodu} nolu bir üretim yok.':
            sg.popup(test)
           
        else:
            sg.popup(test)
            uretim.json_save()
            del test
            del uretim_kodu
    if event == '-BAG-EKLE-':
        if values[6] == True:saglam = 'Saglam'
        if values[7] == True:saglam = 'Hasarlı'
        test = uretim.bag_kod_add(values['-BAG-URETİM-KOD-'],
                           values['-BAG-KOD-'],
                           float(values['-GRAMAJ-']),
                           values['-BICAK-'],
                           int(values['-METRAJ-']),
                           saglam,
                           values[8]
                           )
        uretim_kodu = values['-BAG-URETİM-KOD-']
        bag_kod = values['-BAG-KOD-']
        if test == f'{uretim_kodu} nolu üretime {bag_kod} u eklendi.':
            sg.popup(test)
            uretim.json_save()
            del test
            del uretim_kodu
            del bag_kod
            uretim.json_load()
        else:
            sg.popup(test)
    if event == 'Veri Ekle':
        if values['-URETIM-KODU-'] and values['-BAG-KODU-'] !=[]:
            test = uretim.auto_veri_add_bag(values['-URETIM-KODU-'][0],values['-BAG-KODU-'][0][0])
            sg.popup(test)
            uretim.json_save()
            uretim.json_load()
    
    if event == '-BAG-VERİLER-':
        if values['-BAG-KODU-'] != []:
            data_ana = conv.bag_std_veri_tablo_data(values['-URETIM-KODU-'],values['-BAG-KODU-'])
            data_veri = conv.bag_veri_tablo_data(values['-URETIM-KODU-'],values['-BAG-KODU-'])
            veri_bag_table(values['-BAG-KODU-'][0][0],data_veri,data_ana)
    if event == '-VERİ-EKLE-BAG-':
        test = uretim.veri_add_bag(values['-VERİ-BAG-KODU-'],
                               values['-VERİ-SAAT-BAG-'],
                               int(values['-VERİ-METRE-BAG-']),
                               int(values['-BIC-SET-BAG-']),
                               float(values['-BIC-TEMP-BAG-']),
                               int(values['-TEK-SET-BAG-']),
                               float(values['-TEK-TEMP-BAG-']),
                               int(values['-KAZ-SET-BAG-']),
                               int(values['-KAZ-R-BAG-']),
                               float(values['-KAZ-TEMP-BAG-']),
                               float(values['-TOP-TEMP-BAG-']),
                               float(values['-ON-TEMP-BAG-']),
                               float(values['-ARKA-TEMP-BAG-']),
                               float(values['-HIZ-BAG-']),
                               float(values['-COOL-TEMP-BAG-']),
        )

        bag_kodu = values['-VERİ-BAG-KODU-']
        if test == f'Üretilmiş {bag_kodu} nolu bir top yok.':
            sg.popup(test)
        else:
            sg.popup(test)
            uretim.json_save()
            del test
            del bag_kodu
    if event == '-BAG-DETAY-':
        sg.popup(veri_bag_detay)
    
    if event == '-URETİM-BİTİRME-':
        test = uretim.uretim_stop(values['-URETİM-KOD-BIT-'],
                                  values['-FILM-BIT-'],
                                  values['-MAL-BIT-'],
                                  values['-FIRE-BIT-'],
                                  values['-BIC-BIT-'],
                                 )
        uretim_kodu = values['-URETİM-KOD-BIT-']
        if test == f'{uretim_kodu} başarı ile sonlandırılmıştır.':
            sg.popup(test)
            uretim.json_save()
            del test
            del uretim_kodu
            window['-URETIM-KODU-'].update(list(uretim.data.active_uretim.keys()))
        else:
            sg.popup(test)

    if event == '-VERİ-OKU-ARA-URETİM-KOD-':
        if values['-VERİ-OKU-ÜRETİM-KODU-'] not in uretim.data.active_uretim:
            if values['-VERİ-OKU-ÜRETİM-KODU-'] in uretim.data.main_list:
                temp_list = []
                temp_list.append(values['-VERİ-OKU-ÜRETİM-KODU-'])
                window['-VERİ-OKU-URETIM-KODU-LIST-'].update(temp_list)
                temp_bag_list = []
                for i in uretim.data.bag_uretim_list:
                    if uretim.data.bag_uretim_list[i] == values['-VERİ-OKU-ÜRETİM-KODU-']:
                        temp_bag_list.append(i)
                window['-VERİ-OKU-BAG-KODU-'].update(values = temp_bag_list)
                window['-VERİ-OKU-GENEL-TABLE-'].update(values = conv.uretim_deneme_veri(temp_list))
            else:
                window['-VERİ-OKU-URETIM-KODU-LIST-'].update(conv.fin_uretim())
                window['-VERİ-OKU-BAG-KODU-'].update(conv.fin_bag_kod())
                window['-VERİ-OKU-GENEL-TABLE-'].update([])
                sg.popup('Böyle bir üretim kodu yok.')
        else:
                window['-VERİ-OKU-URETIM-KODU-LIST-'].update(conv.fin_uretim())
                window['-VERİ-OKU-BAG-KODU-'].update(conv.fin_bag_kod())
                window['-VERİ-OKU-GENEL-TABLE-'].update([])
                sg.popup('Üretim kodu hala aktif üretimde.')
    if event == '-VERİ-OKU-URETIM-KODU-LIST-':
        temp_bag_list = []
        temp_list = []
        temp_list.append(values['-VERİ-OKU-URETIM-KODU-LIST-'][0])
        for i in uretim.data.bag_uretim_list:
            if uretim.data.bag_uretim_list[i] == values['-VERİ-OKU-URETIM-KODU-LIST-'][0]:
                temp_bag_list.append(i)
        window['-VERİ-OKU-BAG-KODU-'].update(values = temp_bag_list)
        window['-VERİ-OKU-GENEL-TABLE-'].update(values = conv.uretim_deneme_veri(temp_list))
        window['-VERİ-URETİM-KOD-TEXT-'].update(f'Seçilmiş Üretim Kodu: {temp_list[0]}')
        window['-VERİ-BAG-KOD-TEXT-'].update(f'Seçilmiş Bağ Kodu: ')
        window['-BAG-GENEL-VERİ-'].update(values = [])
        window['-BAG-TABLE-VERİ-'].update(values = [])
    if event == '-VERİ-OKU-ARA-BAG-KOD-':
        temp_list_b = conv.fin_bag_kod()
        if values['-VERİ-OKU-BAG-KOD-'] in temp_list_b:
            temp_bag_list = []
            temp_bag_list.append(values['-VERİ-OKU-BAG-KOD-'])
            temp_list = []
            temp_bag_list_2 = []
            temp_bag_list_2.append(temp_bag_list)
            temp_list.append(uretim.data.bag_uretim_list[values['-VERİ-OKU-BAG-KOD-']])
            window['-VERİ-OKU-BAG-KODU-'].update(values = temp_bag_list)
            window['-VERİ-OKU-URETIM-KODU-LIST-'].update(values = temp_list)
            window['-VERİ-OKU-GENEL-TABLE-'].update(values = conv.uretim_deneme_veri(temp_list))
            window['-BAG-TABLE-VERİ-'].update(values =conv.bag_veri_tablo_data(temp_list,temp_bag_list_2))
            window['-BAG-GENEL-VERİ-'].update(values = conv.bag_std_veri_tablo_data(temp_list,temp_bag_list_2))
        else:
            window['-VERİ-OKU-URETIM-KODU-LIST-'].update(conv.fin_uretim())
            window['-VERİ-OKU-BAG-KODU-'].update(conv.fin_bag_kod())
            window['-VERİ-OKU-GENEL-TABLE-'].update([])
            window['-BAG-TABLE-VERİ-'].update(values = [])
            window['-BAG-GENEL-VERİ-'].update(values =[])
            sg.popup('Böyle bir bağ kodu yok.')
    if event == '-VERİ-OKU-BAG-KODU-':
        if values['-VERİ-OKU-BAG-KODU-'] != []:
            temp_bag_list = []
            temp_bag_list.append(values['-VERİ-OKU-BAG-KODU-'][0])
            temp_bag_list_2 = []
            temp_bag_list_2.append(temp_bag_list)
            temp_list = []
            temp_list.append(uretim.data.bag_uretim_list[values['-VERİ-OKU-BAG-KODU-'][0]])
            #window['-VERİ-OKU-BAG-KODU-'].update(values = temp_bag_list)
            #window['-VERİ-OKU-URETIM-KODU-LIST-'].update(values = temp_list)
            window['-VERİ-OKU-GENEL-TABLE-'].update(values = conv.uretim_deneme_veri(temp_list))
            window['-BAG-TABLE-VERİ-'].update(values =conv.bag_veri_tablo_data(temp_list,temp_bag_list_2))
            window['-BAG-GENEL-VERİ-'].update(values = conv.bag_std_veri_tablo_data(temp_list,temp_bag_list_2))
            window['-VERİ-BAG-KOD-TEXT-'].update(f'Seçilmiş Bağ Kodu: {temp_bag_list[0]}')

    if event == 'Temizle':
        clear_input()
        window['-VERİ-OKU-URETIM-KODU-LIST-'].update(conv.fin_uretim())
        window['-VERİ-OKU-BAG-KODU-'].update(conv.fin_bag_kod())
        window['-VERİ-OKU-GENEL-TABLE-'].update([])
        window['-VERİ-BAG-KOD-TEXT-'].update(f'Seçilmiş Bağ Kodu: ')
        window['-VERİ-URETİM-KOD-TEXT-'].update(f'Seçilmiş Üretim Kodu: ')
    
    if event == 'Export':
        export_popup()



    window.refresh()

uretim.json_save()
window.close()