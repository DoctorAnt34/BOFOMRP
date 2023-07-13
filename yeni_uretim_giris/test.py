import db_module as db
import serialization as s

uretim_bag = s.json_load_dict('uretim_bag')
db.uretim_giris('BU230012')

for i in uretim_bag['BU230012']:
    db.bag_giris(i)