# C:\\Users\\jtuttle\\Documents\\GIM_New_Patient_Appts\\CRG1040 - Appts_GIM_56_2038282587443456905.csv

from patient_handler import PatientHandler
from simple_salesforce import Salesforce
from secret import *
import json


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


def main():
    csv_path = input('Enter full CSV Path:\n')
    sf = connectToSF()
    p = PatientHandler()
    appointments = p.run_CSV(open(csv_path, newline='\n'))
    appointments = p.dedupe(appointments)
    print('{0} unique appointments found'.format(str(len(appointments))))

    print(json.dumps(appointments, indent=4))

    """ Variable access example: 
            print(appt['ApptID'])
            print(appt['Patient']['firstName'])
            print(appt['Patient']['appointment']['duration'])  """


if __name__ == '__main__':
    main()
