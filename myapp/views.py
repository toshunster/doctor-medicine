# -*- coding: utf8 -*-

from flask import render_template, request, redirect, url_for
from flask import jsonify

from myapp.app import app

import json

# An absolute import gives us the Doctor, Preference, Medicine model
from myapp.models import Doctor, Preference, Medicine, DOSAGE, DURATIONS

import logging

logger = logging.getLogger(__name__)
logger.setLevel( logging.INFO )

# create a file handler
flask_log_name = 'flask.log'
handler = logging.FileHandler( flask_log_name )
handler.setLevel( logging.INFO )

# create a logging format
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s]: %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)


#logging.basicConfig(filename="test.log", level=logging.DEBUG)

@app.route('/')
def use_app():
    """Use our amazing app."""

    medicines = Medicine.query.all()
    doctors = Doctor.query.all()
    return render_template('index.html', medicines=medicines,
                                         doctors=doctors,
                                         DOSAGE=DOSAGE,
                                         DURATIONS=DURATIONS )

@app.route('/data', methods=['GET'])
def get_data():
    doctor_id = request.args.get('doctorid', None)
    medicine_id = request.args.get('medicineid', None)
    
    if doctor_id is not None:
        logger.info( "[GET] doctorid: {}".format( doctor_id ) )
        return jsonify( Doctor.query.filter( Doctor.doctor_id == int(doctor_id) ).first().serialize() )
    logger.info( "[GET] medicineid: {}".format( medicine_id ) )
    return jsonify( Medicine.query.filter( Medicine.medicine_id == int(medicine_id) ).first().serialize() )

@app.route('/model', methods=['POST'])
def post_medicine():
    doctor_id = int( request.args.get('doctorid', None) )
    medicine_id = int( request.args.get('medicineid', None) )
    json_data = json.loads( request.data )
    doctor = Doctor.query.filter(Doctor.doctor_id == doctor_id).first()
    duration = json_data['doctorSelection']['duration']
    dosage = int( json_data['doctorSelection']['dosage'] )
    logger.info( "[POST] doctorid: {}, medicineid: {}, dosage: {}, duration: {}".format( doctor_id, medicine_id, dosage, duration ) )

    for preference in doctor.preferences:
        if preference.medicine.medicine_id == medicine_id:
            print('i\'m wolf')
            preference.duration.append( duration )
            preference.dosage.append( dosage )
            preference.save()
            doctor.save()
            break
    return jsonify( Doctor.query.filter( Doctor.doctor_id == doctor_id ).first().serialize() )

@app.route('/log/get/', methods=['GET'])
def get_log():
    log_content = ''
    with open( flask_log_name, 'r' ) as input_log:
        log_content = input_log.read()
    return "<pre>{}</pre>".format( log_content )

@app.route('/add/doctor/', methods=['POST'])
def add_doctor():
    """Adding doctor item"""

    doctor = Doctor( doctor_id = int(request.form['doctor_id']),
                     name=request.form['doctor_name'] )
    doctor.save()
    medicines = Medicine.query.all()
    for medicine in medicines:
        preference = Preference(medicine=medicine)
        preference.save()
        doctor.preferences.append( preference )
        doctor.save()
    return redirect( url_for('use_app') )

@app.route('/add/medicine/', methods=['POST'])
def add_medicine():
    """Adding new medicine item"""

    medicine = Medicine( medicine_id = int(request.form['medicine_id']),
                         generic_name=request.form['generic_name'],
                         brand_name=request.form['brand_name'],
                         measurement_unit=request.form['measurement_unit'],
                         form=request.form['form'] )
    medicine.save()
    doctors = Doctor.query.all()
    for doctor in doctors:
        preference = Preference( medicine=medicine )
        preference.save()
        doctor.preferences.append( preference )
        doctor.save()
    return redirect( url_for('use_app') )

@app.route('/change/preference', methods=['POST'])
def change_preference():
    doctor_id = request.form['doctor']
    medicine_id = request.form['medicine']
    dosage = int( request.form['dosage'] )
    duration = int( request.form['duration'] )
    doctor = Doctor.query.get(mongo_id=doctor_id)
    for preference in doctor.preferences:
        if str(preference.medicine.mongo_id) == medicine_id:
            print('i\'m wolf')
            preference.duration.append( DURATIONS[duration] )
            preference.dosage.append( DOSAGE[dosage] )
            preference.save()
            doctor.save()
            break
    
    return redirect( url_for('use_app') )

@app.route('/get/medicine/?id=<string:medicine_id>')
def get_medicine_by_id( medicine_id ):
    #logging.info( "[GET] get_medicine_by_id" )
    return jsonify( Medicine.query.get( mongo_id=medicine_id ).serialize() )

@app.route('/get/doctor/?id=<string:doctor_id>')
def get_doctor_by_id( doctor_id ):
    #logging.info( "[GET] get_doctor_by_id" )
    return jsonify( Doctor.query.get( mongo_id=doctor_id ).serialize() )