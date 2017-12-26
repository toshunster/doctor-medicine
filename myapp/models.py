# -*- coding: utf8 -*-

from myapp.app import db 

class Medicine(db.Document):
    generic_name = db.StringField(max_length=200, required=True)
    brand_name = db.StringField(max_length=200, required=True)
    measurement_unit = db.StringField(max_length=200, required=True)
    form = db.StringField(max_length=200, required=True)

    def serialize(self):
        return {
            "_id" : str(self.mongo_id),
            "generic_name" : self.generic_name,
            "brand_name" : self.brand_name,
            "measurement_unit" : self.measurement_unit,
            "form" : self.form
        } 

DOSAGE = [ 1, 2, 3 ]
DURATIONS = [ '1 day', '5 days', 'month 1' ]

class Preference(db.Document):
    dosage = db.IntField(required=True, default=DOSAGE[0])
    duration = db.StringField(max_length=200, required=True, default=DURATIONS[0])
    medicine = db.DocumentField( Medicine )

    def serialize(self):
        return {
            "_id" : str(self.mongo_id),
            "dosage" : self.dosage,
            "duration" : self.duration,
            "medicine" : self.medicine.serialize()
        } 

class Doctor(db.Document):
    name = db.StringField(max_length=200, required=True)
    preferences = db.ListField( db.DocumentField(Preference), db_field='Preferences', default=list())

    def serialize(self):
        return {
            "_id" : str(self.mongo_id),
            "name" : self.name,
            "preferences" : [ pref.serialize() for pref in self.preferences ]
        } 
    

