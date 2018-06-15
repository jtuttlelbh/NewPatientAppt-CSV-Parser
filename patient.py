class Patient(object):
    def __init__(self, **kwargs):
        self.firstName = str(kwargs.pop('FirstName')).title()
        self.middleName = str(kwargs.pop('MiddleName')).title()
        self.lastName = str(kwargs.pop('LastName')).title()
        self.email = kwargs.pop('Email')
        self.validEmail = kwargs.pop('ValidEmail')
        self.appointment = kwargs.pop('Appointment')
