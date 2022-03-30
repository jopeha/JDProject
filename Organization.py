


class Organization:

    name=""

    leader=""#CHARACTER
    block=""#BLOCK
    power=0

    def __init__(self,*,name,power,block):
        self.name=name
        self.power=power
        self.block=block
        self.members = []
    @property
    def realpower(self):
        return len(self.members)/self.block.population