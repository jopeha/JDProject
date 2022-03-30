filename= "employment"


with open(filename,"r") as file:
    a=file.read()

a=a.replace("\t",",")

with open(filename,"w") as file:
    file.write(a)