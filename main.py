import csv
from simple_salesforce import Salesforce
from datetime import datetime, timedelta
from validate_email import validate_email
from secret import *


def run_CSV(ed):
    with ed as ed_file:
        with open('patient_file.csv', 'w', newline='') as patient_file:
            with open('appt_file.csv', 'w', newline='') as appt_file:
                patient_writer = csv.writer(
                    patient_file, delimiter=',', quotechar='"')
                appt_writer = csv.writer(
                    appt_file, delimiter=',', quotechar='"')
                ed_reader = csv.reader(ed_file, delimiter=',', quotechar='"')
                
                header_row = True
                record_count = 0

                for row in ed_reader:
                    if not row[0] and not row[1]:
                        print("%i records written to csv" % record_count)
                        return
                    elif header_row:
                        patient_writer.writerow(['Name', 'Email'])
                        appt_writer.writerow(
                            ['Start Time', 'End Time', 'Duration', 'Location', 'Appointment Type'])
                        headers = list(row)
                        i_name = headers.index('Person Name- Full')
                        i_email = headers.index('Person E-mail')
                        i_start = headers.index(
                            'Appointment Start Date & Time')
                        i_end = headers.index(
                            'Appointment End Date & Time')
                        i_location = headers.index(
                            'Appt Location- Nurs Unt (Scheduled)')
                        i_type = headers.index('Appointment Type- Short')
                        header_row = False
                    else:
                        duration = get_duration(
                            row[i_start], row[i_end])
                        start_time = get_start_time(
                            row[i_start])
                        end_time = get_end_time(row[i_end])

                        patient_writer.writerow(
                            [row[i_name], row[i_email]])
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
            print("Connection to Salesforce successful\n")
    except:
        raise Exception('Connection to Salesforce failed')


def get_duration(start_datestring, end_datestring):
    start = start_datestring.split(' ')
    end = end_datestring.split(' ')
    start_time = start[1]
    end_time = end[1]

    fmt = '%H:%M:%S'
    tdelta = datetime.strptime(
        end_time, fmt) - datetime.strptime(start_time, fmt)
    duration = str(tdelta).split(':')[1]
    return duration


def get_start_time(start_datestring):
    start = start_datestring.split(' ')
    start_time = start[1]
    return start_time


def get_end_time(end_datestring):
    end = end_datestring.split(' ')
    end_time = end[1]
    return end_time


def main():
    # connect_to_sf()
    run_CSV(open(input('Enter full CSV Path:\n'), newline='\n'))


if __name__ == '__main__':
    main()
