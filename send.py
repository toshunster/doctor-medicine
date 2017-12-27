
import json
import requests

data = """{
            "_version": 1,
            "id": "1",
            "genericName": "ABCIXIMAB INJECTION 10MG IN 5ML",
            "brandName": "REOPRO",
            "measurementUnit": "None",
            "form": "Injectible",
            "doctorSelection": {
                "dosage": 100400,
                "duration": "Week 1"
            }
}"""
url = 'http://localhost:5000/model?doctorid=23&medicineid=0'

requests.post( url, headers={'Content-Type': 'application/json'}, data=data )

