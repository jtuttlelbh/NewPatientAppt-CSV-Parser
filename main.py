# TODO:
# 1. Error handling and reporting
# 2. More robust comments
# 3. Too many kwargs.pop()s?


from patient_handler import PatientHandler
from simple_salesforce import Salesforce
from secret import *
import json


def connectToSF():
    try:
        sf = Salesforce(username=sandbox_username,
                        password=sandbox_password,
                        security_token=sandbox_token,
                        domain='test',
                        client_id='PythonUploader')
        if sf:
            print('Connection to Salesforce successful\n')
            return sf
    except:
        raise Exception('Connection to Salesforce failed\n')


def main():
    csv_path = input('Enter full CSV Path:\n')
    sf = connectToSF()
    p = PatientHandler(sf)
    results = p.run_CSV(open(csv_path, newline='\n'))
    errors = collectErrors(results)
    print(json.dumps(errors, indent=4))


def collectErrors(results):  # clearly does nothing other than 
    errors = []              # print the data right now
    print(json.dumps(results, indent=4))
    return results


if __name__ == '__main__':
    main()
