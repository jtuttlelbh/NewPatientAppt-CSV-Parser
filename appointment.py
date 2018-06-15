from datetime import datetime, timedelta


class Appointment(object):
    def __init__(self, **kwargs):
        self.provider = kwargs.pop('Provider')
        self.type = kwargs.pop('Type')
        self.location = kwargs.pop('Location')
        self.start = kwargs.pop('StartTime')
        self.end = kwargs.pop('EndTime')
        self.duration = self.getDuration(self.start, self.end)

    def getDuration(self, start_time, end_time):
        fmt = '%I:%M %p'
        tdelta = datetime.strptime(
            end_time, fmt) - datetime.strptime(start_time, fmt)
        duration = str(tdelta).split(':')[1]
        return duration
