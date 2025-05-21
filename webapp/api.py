'''
    app.py
    Jeff Ondich, 25 April 2016
    Updated 5 November 2021

    Tiny Flask API to support a cats and dogs web application
    that doesn't use a database.
'''
import flask
import json

api = flask.Blueprint('api', __name__)

# Of course, your API will be extracting data from your postgresql database.
# To keep the structure of this tiny API crystal-clear, I'm just hard-coding data here.
types = ["BATTERY - SIMPLE ASSAULT", 
         "OTHER MISCELLANEOUS CRIME", 
         "VEHICLE - STOLEN", 
         "THEFT FROM MOTOR VEHICLE - PETTY ($950 & UNDER)", 
         "THEFT-GRAND ($950.01 & OVER)EXCPT,GUNS,FOWL,LIVESTK,PROD", 
         "ROBBERY", "VEHICLE, STOLEN - OTHER (MOTORIZED SCOOTERS, BIKES, ETC)", 
         "CHILD ANNOYING (17YRS & UNDER)", "VANDALISM - MISDEAMEANOR ($399 OR UNDER)", "ASSAULT WITH DEADLY WEAPON, AGGRAVATED ASSAULT", "VANDALISM - FELONY ($400 & OVER, ALL CHURCH VANDALISMS)", 
         "BURGLARY", "ARSON", "CRIMINAL THREATS - NO WEAPON DISPLAYED", "SEX,UNLAWFUL(INC MUTUAL CONSENT, PENETRATION W/ FRGN OBJ", "BURGLARY FROM VEHICLE", "VEHICLE - ATTEMPT STOLEN", "INDECENT EXPOSURE", "RAPE, FORCIBLE", "TRESPASSING", 
         "VIOLATION OF COURT ORDER", "CHILD NEGLECT (SEE 300 W.I.C.)", "THEFT OF IDENTITY", "THEFT PLAIN - PETTY ($950 & UNDER)", "EXTORTION", "ILLEGAL DUMPING", "THEFT FROM MOTOR VEHICLE - GRAND ($950.01 AND OVER)", 
         "BRANDISH WEAPON", "BATTERY WITH SEXUAL CONTACT", "CHILD PORNOGRAPHY", "ASSAULT WITH DEADLY WEAPON ON POLICE OFFICER", "THEFT FROM PERSON - ATTEMPT", "SHOPLIFTING - PETTY THEFT ($950 & UNDER)"]

areas = ["Topanga", "Northeast", "Harbor", "Newton", "Southwest", "Southeast", "West Valley", 
         "Mission", "Devonshire", "77th Street", 
         "Hollenbeck", "Wilshire", "Pacific", "West LA", 
         "Foothill", "Van Nuys", "Central", "Rampart", "N Hollywood", "Olympic"]

dates = ["2025-01", "2025-02", "2025-03"]


@api.route('/types/', strict_slashes=False)
def get_types():
    return json.dumps(types)

@api.route('/areas/')#, strict_slashes=False) 
def get_areas():
    return json.dumps(areas)

@api.route('/dates/')#, strict_slashes=False) 
def get_dates():
    return json.dumps(dates)

