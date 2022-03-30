class Character:

    height = 1
    weight = 1
    hair = ""
    eye = ""
    skin = ""
    employed = True
    _status=0
    _statusname=""
    gender=""
    floor=0
    age=0

    def __init__(self):
        pass

    @property
    def status(self):
        return self._status
    @status.setter
    def status(self,value):
        self._status=value

        with open("status","r") as file:
            l = file.read().split(",")

        self._statusname=l[min(6,int(value))]
