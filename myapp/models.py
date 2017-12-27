# -*- coding: utf8 -*-

from myapp.app import db 

class Medicine(db.Document):
    medicine_id = db.IntField(required=False, default=0)
    generic_name = db.StringField(max_length=200, required=True)
    brand_name = db.StringField(max_length=200, required=True)
    measurement_unit = db.StringField(max_length=200, required=True)
    form = db.StringField(max_length=200, required=True)

    def serialize(self):
        return {
            "_id" : str(self.mongo_id),
            "id" : str(self.medicine_id),
            "generic_name" : self.generic_name,
            "brand_name" : self.brand_name,
            "measurement_unit" : self.measurement_unit,
            "form" : self.form
        } 

DOSAGE = [ 1, 2, 3 ]
DURATIONS = [ '1 day', '5 days', 'month 1' ]

class Preference(db.Document):
    dosage = db.ListField( db.IntField(), required=True, default=list() )
    duration = db.ListField( db.StringField(max_length=200), required=True, default=list() )
    top_duration = db.ListField( db.StringField(max_length=200), required=True, default=list() )
    top_dosage = db.ListField( db.StringField(max_length=200), required=True, default=list() )
    medicine = db.DocumentField( Medicine )

    def serialize(self):
        return {
            "_id" : str(self.mongo_id),
            "dosage" : self.top_dosage,
            "duration" : self.top_duration,
            "medicine" : self.medicine.serialize()
        } 

class Doctor(db.Document):
    doctor_id = db.IntField(required=False, default=0)
    name = db.StringField(max_length=200, required=True)
    preferences = db.ListField( db.DocumentField(Preference), db_field='Preferences', default=list())

    def serialize(self):
        return {
            "_id" : str(self.mongo_id),
            "id" : str(self.doctor_id),
            "name" : self.name,
            "preferences" : [ pref.serialize() for pref in self.preferences ]
        }
