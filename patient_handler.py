from validate_email import validate_email
from fieldMap import fieldMap
from patient import Patient
from appointment import Appointment
import csv


class PatientHandler(object):
    def __init__(self):
        self.__record_count = 0
        self.__unique_appointments = 0
        self.__valid_email_count = 0

    @staticmethod
    def dedupe(appointments):
        unique_ids = []
        final_list = []
        for appt in appointments:
            if appt['ApptID'] not in unique_ids:
                unique_ids.append(appt['ApptID'])
                final_list.append(appt)
        return final_list

    def run_CSV(self, ed):
        with ed as ed_file:
            patient_appts = []
            header_row = True
            ed_reader = csv.reader(ed_file, delimiter=',', quotechar='"')

            for row in ed_reader:
                if not row[0] and not row[1]:
                    print('\n%i records found' % self.__record_count
                          + '\n%i valid emails found' % self.__valid_email_count)
                    break
                elif header_row:
                    headers = list(row)
                    i_fname = headers.index(fieldMap['FirstName'])
                    i_mname = headers.index(fieldMap['MiddleName'])
                    i_lname = headers.index(fieldMap['LastName'])
                    i_email = headers.index(fieldMap['Email'])
                    i_start = headers.index(fieldMap['StartTime'])
                    i_end = headers.index(fieldMap['EndTime'])
                    i_location = headers.index(fieldMap['Location'])
                    i_type = headers.index(fieldMap['Type'])
                    i_appt_id = headers.index(fieldMap['ApptID'])
                    i_provider = headers.index(fieldMap['Provider'])
                    header_row = False
                else:
                    valid_email = validate_email(row[i_email])

                    if valid_email:
                        self.__valid_email_count += 1
                    self.__record_count += 1

                    a = Appointment(Type=row[i_type],
                                    Location=row[i_location],
                                    StartTime=row[i_start],
                                    EndTime=row[i_end],
                                    Provider=row[i_provider])

                    p = Patient(FirstName=row[i_fname],
                                MiddleName=row[i_mname],
                                LastName=row[i_lname],
                                Email=row[i_email],
                                ValidEmail=valid_email,
                                Appointment=a.__dict__)

                    entry = {'ApptID': row[i_appt_id], 'Patient': p.__dict__}
                    patient_appts.append(entry)

            return patient_appts
