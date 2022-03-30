from random import choices,gauss,choice,randint,random,shuffle
from Block import Block
from Character import Character
from Organization  import Organization
from pprint import pprint as print
import math

def _readshitsheet(name,rows):
    with open("races.TSV","r") as file:
        l = file.read().split("\n")
    i=0
    races={}
    while True:
        f = lambda x:x.split("\t")[1:]
        t = lambda x:x.split("\t")[0]
        races[f(l[i])[0]] = {}
        for a in range(rows-1):
            races[f(l[i])[0]][t(l[i+1+a])]=f(l[i+1+a])
        i+=rows
        if i+rows>len(l):
            break
    return races
races =_readshitsheet("races.TSV",6)
with open("physical_traits", "r") as file:
    phyl = file.read().split("\n")
with open("personality_traits", "r") as file:
    perl = choice(file.read().split(","))

with open("appearance_traits", "r") as file:
    appl = choice(file.read().split(","))

with open("employment", "r") as file:
    empl = file.read().split("\n")

with open("unofficial_employment", "r") as file:
    uempl = file.read().split("\n")

with open("cyborg_traits","r") as file:
    ctraits1, ctraits2, ctraits3 = [x.split(",") for x in file.read().split("\n")]

with open("mutant_traits","r") as file:
    mtraits1, mtraits2, mtraits3 = [x.split(",") for x in file.read().split("\n")]

with open("mutant_abilities","r") as file:
        mabilities = file.read().split(",")



def _firstname(ethnicity):
    return "bob"


def _lastname(ethnicity):
    return "hope"


def _charactername(ethnicity):
    return _firstname(ethnicity),_lastname(ethnicity)


def _blockname(city=None,**_):
    with open("blockpre") as file:
        pre = file.read().split(",")
    with open("blocksuff") as file:
        suff = file.read().split(",")

    return choice(pre).capitalize()+" "+choice(suff).capitalize()


def _cyborgtrait(**kwargs):

    p=randint(1,10)
    T=[]



    if p<=6:
        T.append(choice(ctraits1))
    elif p<9:
        T.append(choice(ctraits2))
        if random()>.75:
            kwargs.update(_cyborgtrait(**kwargs))
    else:
        T.append(choice(ctraits3))
        if random()>.5:
            kwargs.update(_cyborgtrait(**kwargs))

    T=[_command(i,kwargs) for i in T]
    kwargs["traits"]=T

    return kwargs


def _mutanttrait(**kwargs):

    p=randint(1,10)
    T=[]



    if p<=8:
        n= random()

        if n<=.6:
            T.append(choice(mtraits1))
        elif n<=.9:
            T.append(choice(mtraits2))
        else:
            T.append((choice(mtraits3)))

    if p>6:
        T.append(choice(mabilities))

    T=[_command(i,kwargs) for i in T]
    kwargs["traits"]=T

    return kwargs


def _gangname():
    if random() > .3:
        with open("gang_pre", "r") as file:
            pre = choice(file.read().split(",")).capitalize()
        with open("gang_post", "r") as file:
            post = choice(file.read().split(",")).capitalize()
        if random() > .5:
            pre = "The " + pre
        n = pre + " " + post
    else:
        with open("gang_post", "r") as file:
            n = choice(file.read().split(",")).capitalize()
        if random() > .5:
            n = "The " + n
    return n


def _command(line,kwargs):

    try:
        a = line.split("@")
        line = a[0]
        command=a[1]
        if len(a)>2:
            line= "".join([line,*("@"+i for i in a[2:])])
        if "WHEIGHT" in command:
            command=command.replace("WHEIGHT","")
            num = float(command[1:])
            if command[0]=="+":
                kwargs["weight"]+=num*1.2
                kwargs["height"]+=num
            elif command[0]=="*":
                kwargs["weight"] *= num*1.2
                kwargs["height"] *= num
            else:
                kwargs["weight"] -= num*1.2
                kwargs["height"] -= num
        else:
            if "*" in command:
                key,num=command.split("*")
                num=float(num)
                kwargs[key.lower()]*=num
            elif "+" in command:
                key,num=command.split("+")
                num=float(num)
                kwargs[key.lower()]+=num
            else:
                key,num=command.split("-")
                num=float(num)
                kwargs[key.lower()]-=num
    except IndexError:
        pass
    try:
        a = line.split("%")
        start, command = a[:2]
        if len(a) > 2:
            end = "".join(a[2:])
        else:
            end = ""

        if command=="BODYPARTS":
            l=["Arms","Legs","Hands","Feet"]
        elif command=="BODYPART":
            l= ["Arm","Leg","Hand","Foot"]
            l = ["%LR% "+i for i in l]
        elif command == "LR":
            l= ["Left","Right"]
        else:
            l=["POOPOO"]
        line = start+choice(l)+end

    except ValueError:
        pass

    if "@" in line or "%" in line:
        line=_command(line,kwargs)


    return line


def _population(**kwargs):

    b=kwargs["block"]

    agepops=[]

    popn=b.population
    n=popn/10

    for i in range(10):
        agepops.append(n*gauss(1+(i/20),.2)+ (agepops[-1]*0.1 if len(agepops)!=0 else 0))

    d=popn/sum(agepops)

    agepops = [int(i*d) for i in agepops]


    agepops[randint(0,9)]+=popn-sum(agepops)
    sf=0
    pop=[[]]
    for GEN in range(10):
        cur=[]
        n=agepops.pop(0)
        sf+=n
        for _ in range(n):
            kwargs["app"].progress = (sf+_)/popn, f"{GEN + 1}. generation ({_+1}/{n}) TOTAL {sf}/{popn}"

            c = character(gen_age=len(agepops)*10+5,gen_age_dev=len(agepops)+5,block=b,floor=randint(1,b.floors))
            cur.append(c)
        pop[-1]+=cur

        if len(agepops)==0:
            break

        gay_girls=[]
        knave_girls=[]

        kwargs["app"].progress = (
                                         sf + len(
                                     cur)) / popn, f"{GEN + 1}. generation children ({len(cur) + 1}/{n}) TOTAL {sf}/{popn}"

        for girl in cur:
            if girl.gender=="female":
                gay_girls.append(girl)
            else:
                knave_girls.append(girl)
        br=int(min(1,max(0,gauss(.8,.2))))
        shuffle(gay_girls)
        shuffle(knave_girls)
        cur=[]


        for floor in range(b.floors):
            prospects =list(filter(lambda a:floor-1<a.floor<floor+1,knave_girls))
            weights = list(map(lambda a:max(1,abs(a.age-len(agepops)*10+5) - abs(22-a.bmi)+a.status*2),knave_girls))
            for lass in filter(lambda a:a.floor==floor,gay_girls[:agepops[0]*br]):

                lad=choices(prospects,weights)[0]
                c=child([lass,lad],gen_age=len(agepops)*10+5,gen_age_dev=len(agepops)+5,block=b,floor=min(b.floors,max(0,gauss(floor,2))))
                cur.append(c)
        pop.append(cur)
        sf+=len(cur)
        agepops[0]-=len(cur)

    p=[]
    for l in pop:
        p+=l

    b.people=p


def _finishup(b):
    a=["5D1520",
       "48A9A6",
       "CB793A",
       "F19A3E",
       "F9C80E",
       "F25757",
       "F0BCD4",
       "357DED",
       "F06543"
       ]

    cd={}

    for gang in b.crime_organizations:
        r=randint(0,len(a)-1)
        gang.color=a.pop(r)
        gang.coloredname=f"[color={gang.color}]{gang.name}[/color]"
        cd[gang.name]=gang

    for c in b.people:
        if c.crime_affiliation!="None":
            cd[c.crime_affiliation].members.append(c)

    for i in cd:
        print(i+" " +str(len(cd[i].members))+" "+ str(cd[i].power))



def child(p,**kwargs):

    d={}
    weights=[60,20,15,10,5,5,5,5,5]



    hdev = gauss(1, 0.05)
    phdev=(sum(i._hdev for i in p)+2)/4
    hdev*=phdev
    status=(sum(i.status for i in p)+2)/3

    d["parents"]=p
    d["ethnicity"] = choice(p).ethnicity
    d["gender"] = choice(["male","female"])
    d["name"] = [_firstname(d["ethnicity"]), choice(p).name[1]]

    d["height"] = int(races[d["ethnicity"]]["height"][0]) * hdev
    d["height"] += 5 if d["gender"] == "male" else 0
    d["_hdev"] = hdev

    d["weight"] = int(races[d["ethnicity"]]["weight"][0]) * hdev * 1.1 * gauss(1, 0.15)
    d["weight"] += 5 if d["gender"] == "male" else -5

    d["age"]=max(p[0].age-13,int(gauss(kwargs["gen_age"],kwargs["gen_age_dev"])))

    if d["age"]<=16:
        c=(d["age"]+16)/36
        d["weight"]*=c
        d["height"]*=c
    if 60>d["age"]>=20:
        status+=1
        d["weight"]+=abs(d["age"]-40)/2
    elif d["age"]>70:
        status+=max(0,-1+(random()*3))

    d["hair"]= choices([i.hair for i in p]+races[d["ethnicity"]]["hair"],
                                weights[:2+len(races[d["ethnicity"]]["hair"])])[0]
    d["eye"]= choices([i.eye for i in p]+races[d["ethnicity"]]["eye"],
                                weights[:2+len(races[d["ethnicity"]]["eye"])])[0]
    d["skin"]=choices([i.skin for i in p]+races[d["ethnicity"]]["skin"],
                                weights[:2+len(races[d["ethnicity"]]["skin"])])[0]
    mc=0
    for i in p:
        if i.classification == "mutant":
            mc+=15
        else:
            mc-=1
    d["classification"] = choices(["human","cyborg","mutant"],[70,25,5])[0]

    if d["classification"] == "mutant":
        status-=1
        mdev=gauss(1,.25)
        d["weight"]*=mdev
        d["height"]*=mdev
        if d["weight"]<30:
            d["weight"]+=randint(1,30)
        d.update(_mutanttrait(**d))
    if d["classification"] == "cyborg":
        d.update(_cyborgtrait(**d))


    bmi= (d["weight"]/d["height"]/d["height"])*10000
    d["bmi"]=bmi
    if bmi<18:
        phy=choice(phyl[0].split(","))
    elif bmi<26:
        phy=choice(phyl[1].split(","))
    elif bmi<30:
        phy=choice(phyl[2].split(","))
    elif bmi<35:
        phy=choice(phyl[3].split(","))
    else:
        phy = choice(phyl[4].split(","))
    per=choice(perl)
    app=choice(appl)
    per,phy,app=(_command(i,d) for i in (per,phy,app))
    if "traits" in d:
        d["traits"]+=[per,phy,app]
    else:
        d["traits"]= [per,phy,app]

    if "employment" not in kwargs:
        if "block" in kwargs:
            p = kwargs["block"].unemployment
        else:
            p = 50
        if d["classification"]=="mutant":
            p+=30
        if d["age"]<16:
            emp="None"
            d["crime_affiliation"]="None"

        elif randint(1,100)>p:
            d["crime_affiliation"]="None"

            if random()>.75:
                emp=choice(empl[1].split(","))
                status+=1
            else:
                emp=choice(empl[0].split(","))
        else:
            if randint(1,20)>kwargs["block"].crime_rate:

                if random()>.75:
                    emp=choice(empl[1].split(","))
                    status+=1

                else:
                    emp=choice(empl[0].split(","))
                emp="None ("+emp+")"
            else:
                emp="None"

            if "crime_affiliation" not in kwargs:
                if "block" not in kwargs:
                    d["crime_affiliation"]=choices(["Local","Mafia","Yakuza","Russian Mob","Triad"],[60,10,10,10,10])[0]
                else:
                    d["crime_affiliation"]= choices([i.name for i in kwargs["block"].crime_organizations],
                                                    [i.power for i in kwargs["block"].crime_organizations])[0]

                if d["crime_affiliation"]=="local":

                    d["crime_affiliation"]+=" ("+_gangname()+")"



        d["employment"]=emp.capitalize()

    if "status" not in kwargs:

        status=max(0,gauss(status,2))




    c=Character()
    c.__dict__.update(d)
    c.status=status
    return c


def character(**kwargs):
    hdev = gauss(1, 0.05)
    weights=[60,20,15,10,5,5,5]
    d={}
    status=2

    d["parents"]=Character,Character

    if "ethnicity" not in kwargs:
        d["ethnicity"] = choice(list(races))
    if "gender" not in kwargs:
        d["gender"] = choice(["male","female"])
    if "name" not in kwargs:
        d["name"]= _charactername(d["ethnicity"])
    if "height" not in kwargs:
        d["height"]= int(races[d["ethnicity"]]["height"][0]) * hdev
        d["height"] += 5 if d["gender"] == "male" else 0
        d["_hdev"] =hdev
    if "weight" not in kwargs:
        d["weight"]= int(races[d["ethnicity"]]["weight"][0]) * hdev*1.1 * gauss(1, 0.15)
        d["weight"]+=5 if d["gender"]=="male" else -5

    if "age" not in kwargs:
        if "gen_age" in kwargs:
            mu=kwargs["gen_age"]
            sigma=kwargs["gen_age_dev"]
        else:
            mu=40
            sigma=25
        d["age"]=max(5,int(gauss(mu,sigma)))

    if d["age"]<=16:
        c=(d["age"]+16)/36
        d["weight"]*=c
        d["height"]*=c
    if 60>d["age"]>=20:
        status+=1
        d["weight"]+=abs(d["age"]-40)/2
    elif d["age"]>70:
        status+=max(0,-1+(random()*3))
    if "hair" not in kwargs:
        d["hair"]= choices(races[d["ethnicity"]]["hair"],
                                weights[:len(races[d["ethnicity"]]["hair"])])[0]
    if "eye" not in kwargs:
        d["eye"]= choices(races[d["ethnicity"]]["eye"], weights[:len(races[d["ethnicity"]]["eye"])])[0]
    if "skin" not in kwargs:
        d["skin"]=choices(races[d["ethnicity"]]["skin"], weights[:len(races[d["ethnicity"]]["skin"])])[0]


    if "classification" not in kwargs:
        d["classification"] = choices(["human","cyborg","mutant"],[70,25,5])[0]

        if d["classification"] == "mutant":
            status-=1
            mdev=gauss(1,.25)
            d["weight"]*=mdev
            d["height"]*=mdev

            if d["weight"]<30:
                d["weight"]+=randint(1,30)

            d.update(_mutanttrait(**d))


        if d["classification"] == "cyborg":
            d.update(_cyborgtrait(**d))

    if "traits" not in kwargs:

        bmi= (d["weight"]/d["height"]/d["height"])*10000
        d["bmi"]=bmi
        if bmi<18:
            phy=choice(phyl[0].split(","))
        elif bmi<26:
            phy=choice(phyl[1].split(","))
        elif bmi<30:
            phy=choice(phyl[2].split(","))
        elif bmi<35:
            phy=choice(phyl[3].split(","))
        else:
            phy = choice(phyl[4].split(","))

        per = choice(perl)
        app = choice(perl)

        per,phy,app=(_command(i,d) for i in (per,phy,app))

        if "traits" in d:
            d["traits"]+=[per,phy,app]
        else:
            d["traits"]= [per,phy,app]

    if "employment" not in kwargs:
        if "block" in kwargs:
            p = kwargs["block"].unemployment
        else:
            p = 50
        if d["classification"]=="mutant":
            p+=30
        if d["age"]<16:
            emp="None"
            d["crime_affiliation"]="None"

        elif randint(1,100)>p:
            d["crime_affiliation"]="None"

            if random()>.75:
                emp=choice(empl[1].split(","))
                status+=1
            else:
                emp=choice(empl[0].split(","))
        else:
            if randint(1,20)>kwargs["block"].crime_rate:

                if random()>.75:
                    emp=choice(uempl[1].split(","))
                    status+=1

                else:
                    emp=choice(uempl[0].split(","))
                emp="None ("+emp+")"
            else:
                emp="None"

            if "crime_affiliation" not in kwargs:
                if "block" not in kwargs:
                    d["crime_affiliation"]=choices(["Local","Mafia","Yakuza","Russian Mob","Triad"],[60,10,10,10,10])[0]
                else:
                    d["crime_affiliation"]= choices([i.name for i in kwargs["block"].crime_organizations],
                                                    [i.power for i in kwargs["block"].crime_organizations])[0]
                if d["crime_affiliation"]=="local":

                    d["crime_affiliation"]+=" ("+_gangname()+")"



        d["employment"]=emp.capitalize()

    if "status" not in kwargs:

        status=max(0,gauss(status,2))




    c=Character()
    c.__dict__.update(d)
    c.status=status
    print(c.__dict__)
    input()
    return c


def block(**kwargs):

    b=Block()


    kwargs["app"].progress = 0, "started"
    d={}

    if "name" not in kwargs:
        d["name"]= _blockname(**kwargs)

    if "unemployment" not in kwargs:
        d["unemployment"]=min(100,max(0,gauss(60,30)))

    if "crime_rate" not in kwargs:

        d["crime_rate"] = gauss(5*(d["unemployment"]/100),3)**2


    if "crime_organizations" not in kwargs:
        n=0
        orgl=["Mafia","Russian Mob","Yakuza","Triad"]+[_gangname() for i in range(6)]
        organizations=[]
        weights = []
        while n<100 and len(orgl)!=0:
            p=min(max(gauss(10,4),gauss(40*(1-n/100),10)),100-n)
            if p<5:
                weights[-1]+=p
                n+=p
                continue
            organizations.append(orgl.pop(randint(0,len(orgl)-1)))
            weights.append(p)
            n+=p
        d["crime_organizations"]=[Organization(name=n, power=w,block=b) for n,w in zip(organizations,weights)]

    if "floors" not in kwargs:
        d["floors"]=int(gauss(20,5))*10

    if "population" not in kwargs:
        d["population"]=int(gauss(d["floors"]*375,1000))

    if "shape" not in kwargs:
        s=[]
        n=1
        for i in range(d["floors"]//40):
            a=max(0,gauss(1,.3))
            if a<n:
                n=a
            s.append(n)


        d["shape"]=list(reversed(s))

    b.__dict__.update(d)
    kwargs["app"].progress = 0, "Block done. Populating"
    kwargs["block"]=b


    _population(**kwargs)

    _finishup(b)

    return b


if __name__=="__main":
    block()