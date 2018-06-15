from patient_handler import PatientHandler
from simple_salesforce import Salesforce
from secret import *


def connectToSF():
    try:
        sf = Salesforce(username=sandbox_username, domain='test',
                        password=sandbox_password, security_token=sandbox_token,
                        client_id='Jared~Python')
        if sf:
            print('Connection to Salesforce successful\n')
            return sf
    except:
        raise Exception('Connection to Salesforce failed\n')


def dedupe(appointments):
    unique_ids = []
    final_list = []
    for appt in appointments:
        if appt['ApptID'] not in unique_ids:
            unique_ids.append(appt['ApptID'])
            final_list.append(appt)
    return final_list


def main():
    # sf = connectToSF()
    p = PatientHandler()
    appointments = p.run_CSV(
        open(input('Enter full CSV Path:\n'), newline='\n'))
    appointments = dedupe(appointments)
    print('{0} unique appointments found'.format(str(len(appointments))))

if __name__ == '__main__':
    main()
