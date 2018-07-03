import json
from datetime import datetime, timedelta


class Appointment(object):
    def __init__(self, sf_instance, **kwargs):
        self.apptid = kwargs.pop('ApptID')
        self.Refer_to_provider__c = kwargs.pop('Provider')
        self.HC4__Type__c = kwargs.pop('Type')
        self.HC4__HospitalName__c = kwargs.pop('Location')
        self.date = kwargs.pop('Date')
        self.start = kwargs.pop('Start')
        self.end = kwargs.pop('End')
        self.Status = "Open"
        self.Appointment_Date__c = self.formatDate(self.date)
        self.sf = sf_instance
        self.recordTypeId = self.getRecordTypeID()
        self.Appointment_Duration__c = self.getDuration(
            self.start, self.end)

    def getDuration(self, start_time, end_time):
        fmt = '%I:%M %p'
        tdelta = (datetime.strptime(end_time, fmt)
                  - datetime.strptime(start_time, fmt))
        # time will always be under 1 hour thus only one colon will be present
        duration = str(tdelta).split(':')[1]
        return duration

    def insert(self):
        payload = self.__dict__
        # don't insert these fields
        sf = payload.pop('sf')  # used for insert operation
        payload.pop('date')     # used for building appt date time
        payload.pop('start')    # used for building appt date time
        payload.pop('end')      # only start & duration needed in record
        payload.pop('apptid')   # used for dupe checking only
        #
        response = sf.HC4__Inquiry__c.create(payload)
        print("Inserted: {0} (Appt)".format(self.HC4__Patient__c))
        return response

    def formatDate(self, date):
        d = str(date)  # format as "mm/dd/yyyy"
        year = d[-4:]
        month = d[:2]
        day = d[3:5]
        # needs to be in format "yyyy-mm-dd"
        converted = '{0}-{1}-{2}'.format(year, month, day)
        return converted

    def setPatientID(self, the_id):
        self.HC4__Patient__c = the_id

    def getRecordTypeID(self):
        query = ("SELECT DeveloperName, Id FROM RecordType WHERE "
                 + "DeveloperName = 'GIM_New_Appts'")
        record_type = self.sf.query(query)
        record_type = record_type['records'][0]['Id']
        return record_type
