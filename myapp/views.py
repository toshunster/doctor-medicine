# -*- coding: utf8 -*-

from flask import render_template, request, redirect, url_for
from flask import jsonify

from myapp.app import app

# An absolute import gives us the Doctor, Preference, Medicine model
from myapp.models import Doctor, Preference, Medicine, DOSAGE, DURATIONS


@app.route('/')
def use_app():
    """Use our amazing app."""

    medicines = Medicine.query.all()
    doctors = Doctor.query.all()
    return render_template('index.html', medicines=medicines,
                                         doctors=doctors,
                                         DOSAGE=DOSAGE,
                                         DURATIONS=DURATIONS )

@app.route('/add/doctor/', methods=['POST'])
def add_doctor():
    """Adding doctor item"""

    doctor = Doctor( name=request.form['doctor_name'] )
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

    medicine = Medicine( generic_name=request.form['generic_name'],
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
            preference.duration = DURATIONS[duration]
            preference.dosage = DOSAGE[dosage]
            preference.save()
            doctor.save()
            break
    
    return redirect( url_for('use_app') )

@app.route('/get/medicine/?id=<string:medicine_id>')
def get_medicine_by_id( medicine_id ):
    return jsonify( Medicine.query.get( mongo_id=medicine_id ).serialize() )

@app.route('/get/doctor/?id=<string:doctor_id>')
def get_doctor_by_id( doctor_id ):
    return jsonify( Doctor.query.get( mongo_id=doctor_id ).serialize() )