class Block:

    name = ""
    city = "MC-1"
    unemployment = 0
    floors = 0
    population = 0
    crime_rate = 0.0
    crime_organizations = []
    shape=[]
    _people=[]

    def __init__(self):
        pass

    @property
    def people(self):
        return self._people

    @people.setter
    def people(self,value):
        self.population=len(value)
        self._people=value

    def stats(self):

        d= {"name":self.name,
            "city":self.city,
            "population":str(self.population),
            "floors":str(self.floors),
            "unemployment": f"{self.unemployment:.0f}%",
            "crime rate": f"{self.crime_rate:.0f}",


        }

        a = "".join([k.upper()+": "+d[k]+"\n" for k in d])

        b = "\n".join(f"{o.coloredname}: {o.realpower*100:.0f}%({len(o.members)})" for o in self.crime_organizations)


        #r={"basic":a,
        #   "crime":}

        return a+b
class Floor:
    number=0
    control=""

