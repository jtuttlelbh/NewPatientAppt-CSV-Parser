import json
from simple_salesforce import Salesforce


class Patient(object):
    def __init__(self, **kwargs):
        self.FirstName          = str(kwargs.pop('FirstName')).title()
        self.HC4__MiddleName__c = str(kwargs.pop('MiddleName')).title()
        self.LastName           = str(kwargs.pop('LastName')).title()
        self.Email              = str(kwargs.pop('Email')).lower()
        self.street             = str(kwargs.pop('Street')).title()
        self.city               = str(kwargs.pop('City')).title()
        self.state              = str(kwargs.pop('State')).upper()
        self.validEmail         = kwargs.pop('ValidEmail')
        self.Appointment        = kwargs.pop('Appointment')
        self.LeadSource         = kwargs.pop('LeadSource')
        self.sf                 = kwargs.pop('sf_instance')
        self.postalcode         = kwargs.pop('PostalCode')

    def insert(self):
        payload = self.__dict__
        sf = payload.pop('sf')
        payload.pop('Appointment')
        if not payload['validEmail']:
            payload.pop('Email')  # remove field with no data
        payload.pop('validEmail')
        # perform insert operation, return id to be used in appointment record

        response = sf.Lead.create(payload)
        """ 
        print('Patient Payload: ' + json.dumps(payload, indent=4))
        print('Patient SF Response: ' + json.dumps(response, indent=4)) 
        """
        self.setSFID(response['id'])
        print("Inserted: {0} (Patient)".format(self.LastName))
        return response

    def setSFID(self, the_id):
        self.sfid = the_id
