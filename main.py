import csv
from simple_salesforce import Salesforce
from datetime import datetime, timedelta
from validate_email import validate_email
from fieldMap import fieldMap
from secret import *

record_count = 0
valid_email_count = 0


def run_CSV(ed):
    with ed as ed_file:
        with open('patient_file.csv', 'w', newline='') as patient_file:
            with open('appt_file.csv', 'w', newline='') as appt_file:
                global record_count
                global valid_email_count
                header_row = True

                patient_writer = csv.writer(
                    patient_file, delimiter=',', quotechar='"')
                appt_writer = csv.writer(
                    appt_file, delimiter=',', quotechar='"')
                ed_reader = csv.reader(ed_file, delimiter=',', quotechar='"')

                for row in ed_reader:
                    if not row[0] and not row[1]:
                        print('%i records written to csv' % record_count + '\n'
                              + '%i valid emails found' % valid_email_count + '\n'
                              + 'appt_file and patient_file ready for upload.\n')
                        return
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
                        patient_writer.writerow(
                            ['First Name', 'Middle Name', 'Last Name', 'Email', 'Valid Email'])
                        appt_writer.writerow(
                            ['Start Time', 'End Time', 'Duration', 'Location', 'Appointment Type'])
                        header_row = False
                    else:
                        duration = get_duration(
                            row[i_start], row[i_end])
                        start_time = row[i_start]
                        end_time = row[i_end]

                        valid_email = validate_email(row[i_email])
                        if valid_email:
                            valid_email_count += 1

                        patient_writer.writerow(
                            [row[i_fname], row[i_mname], row[i_lname], row[i_email], valid_email])
                        appt_writer.writerow(
                            [start_time, end_time, duration, row[i_location], row[i_type]])

                        record_count += 1
                return


def connect_to_sf():
    try:
        sf = Salesforce(username=sandbox_username, domain='test',
                        password=sandbox_password, security_token=sandbox_token,
                        client_id='Jared~Python')
        if sf:
            print('Connection to Salesforce successful\n')
    except:
        raise Exception('Connection to Salesforce failed\n')


def get_duration(start_time, end_time):
    fmt = '%I:%M %p'
    tdelta = datetime.strptime(
        end_time, fmt) - datetime.strptime(start_time, fmt)
    duration = str(tdelta).split(':')[1]
    return duration


def main():
    connect_to_sf()
    run_CSV(open(input('Enter full CSV Path:\n'), newline='\n'))


if __name__ == '__main__':
    main()
