from validate_email import validate_email
from fieldMap import fieldMap
from patient import Patient
from appointment import Appointment
import csv


class PatientHandler(object):
    def __init__(self, sf_instance):
        self.__record_count = 0
        self.__unique_appointments = 0
        self.__valid_email_count = 0
        self.__duplicate_count = 0
        self.sf = sf_instance

    def dedupe(self, appointments):
        unique_ids = []
        final_list = []
        for appt in appointments:
            if appt['ApptID'] not in unique_ids:
                unique_ids.append(appt['ApptID'])
                final_list.append(appt)

        print('{0} unique appointments found'.format(str(len(final_list))))
        return final_list

    def run_CSV(self, ed):
        with ed as ed_file:
            unique_appt_ids = []
            results = []
            header_row = True  # prepare to skip to data rows
            ed_reader = csv.reader(ed_file, delimiter=',', quotechar='"')

            for row in ed_reader:
                if not row[0] and not row[1]:  # blank or end of document
                    print("{0} records found".format(
                        self.__record_count))
                    print("{0} unique appointments found".format(
                        self.__unique_appointments))
                    print("{0} valid emails found".format(
                        self.__valid_email_count))
                    print("{0} duplicates found".format(
                        self.__duplicate_count))
                    break
                elif header_row:
                    headers = list(row)
                    i_fname = headers.index(fieldMap['FirstName'])
                    i_mname = headers.index(fieldMap['MiddleName'])
                    i_lname = headers.index(fieldMap['LastName'])
                    i_email = headers.index(fieldMap['Email'])
                    i_date = headers.index(fieldMap['Date'])
                    i_start = headers.index(fieldMap['Start'])
                    i_end = headers.index(fieldMap['End'])
                    i_location = headers.index(fieldMap['Location'])
                    i_type = headers.index(fieldMap['Type'])
                    i_appt_id = headers.index(fieldMap['ApptID'])
                    i_provider = headers.index(fieldMap['Provider'])
                    i_street = headers.index(fieldMap['Street'])
                    i_city = headers.index(fieldMap['City'])
                    i_state = headers.index(fieldMap['State'])
                    i_zip = headers.index(fieldMap['PostalCode'])
                    header_row = False
                else:
                    valid_email = validate_email(row[i_email])
                    self.__record_count += 1

                    if row[i_appt_id] in unique_appt_ids:
                        print('Duplicate ignored - Appt ID: ' + row[i_appt_id])
                        self.__duplicate_count += 1
                        pass
                    else:
                        unique_appt_ids.append(row[i_appt_id])

                        a = Appointment(ApptID=row[i_appt_id],
                                        Type=row[i_type],
                                        Location=row[i_location],
                                        Date=row[i_date],
                                        Start=row[i_start],
                                        End=row[i_end],
                                        Provider=row[i_provider],
                                        sf_instance=self.sf)

                        p = Patient(FirstName=row[i_fname],
                                    MiddleName=row[i_mname],
                                    LastName=row[i_lname],
                                    Email=row[i_email],
                                    Street=row[i_street],
                                    City=row[i_city],
                                    State=row[i_state],
                                    PostalCode=row[i_zip],
                                    ValidEmail=valid_email,
                                    LeadSource='Call Center',
                                    Appointment=a.__dict__,
                                    sf_instance=self.sf)

                        if valid_email:
                            self.__valid_email_count += 1
                        self.__unique_appointments += 1

                        p_response = p.insert()
                        a.setPatientID(p.sfid)
                        a_response = a.insert()

                        entry = {'Patient': p_response,
                                 'Appt': a_response}

                        results.append(entry)
            return results
