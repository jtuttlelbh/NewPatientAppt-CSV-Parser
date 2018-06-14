# TODO: duplicate patient checking

import csv
import json
from simple_salesforce import Salesforce
from datetime import datetime, timedelta
from validate_email import validate_email
from fieldMap import fieldMap
from secret import *

record_count = 0
unique_appointments = 0
valid_email_count = 0



def run_CSV(ed):
    with ed as ed_file:
        global record_count
        global valid_email_count
        global unique_appointments
        patient_appts = []
        header_row = True
        ed_reader = csv.reader(ed_file, delimiter=',', quotechar='"')

        for row in ed_reader:
            if not row[0] and not row[1]:
                print('\n%i records found' % record_count
                      + '\n%i valid emails found' % valid_email_count)
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
                header_row = False
            else:
                duration = getDuration(row[i_start], row[i_end])
                valid_email = validate_email(row[i_email])

                if valid_email:
                    valid_email_count += 1
                record_count += 1

                entry = {
                    'ApptID': row[i_appt_id],
                    'Patient': {
                        'FirstName': row[i_fname],
                        'MiddleName': row[i_mname],
                        'LastName': row[i_lname],
                        'Email': row[i_email],
                        'Valid Email': valid_email,
                        'Appointment': {
                            'Type': row[i_type],
                            'Location': row[i_location],
                            'StartTime': row[i_start],
                            'EndTime': row[i_end],
                            'Duration': duration
                        }
                    }
                }
                patient_appts.append(entry)

        appts_to_insert = dedupe(patient_appts)
        unique_appointments = len(appts_to_insert)
        print('\n%i unique appointments found' %unique_appointments)

        return appts_to_insert


def dedupe(the_list):
    unique_patients = []
    for each_dict in the_list:
        if each_dict['ApptID'] not in unique_patients:
                unique_patients.append(each_dict['ApptID'])
    return unique_patients


def connectToSF():
    try:
        sf = Salesforce(username=sandbox_username, domain='test',
                        password=sandbox_password, security_token=sandbox_token,
                        client_id='Jared~Python')
        if sf:
            print('Connection to Salesforce successful\n')
    except:
        raise Exception('Connection to Salesforce failed\n')


def getDuration(start_time, end_time):
    fmt = '%I:%M %p'
    tdelta = datetime.strptime(
        end_time, fmt) - datetime.strptime(start_time, fmt)
    duration = str(tdelta).split(':')[1]
    return duration


def main():
    # connectToSF()
    appointments = run_CSV(open(input('Enter full CSV Path:\n'), newline='\n'))
    print(json.dumps(appointments, indent=4))


if __name__ == '__main__':
    main()
