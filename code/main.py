import usosapi
import usosprzedmioty
import generujplan
import textwrap
import datetime
import json
import random
import Facebook as facebook
import schedule
import time



tokeny = []
with open("src/tokeny.txt") as token_plik:
    for line in token_plik:
        tokeny.append(line)

usosapi_base_url = 'https://apps.usos.pw.edu.pl/'
LONG_LIVED_ACCESS_TOKEN = tokeny[0]
usosapi_key_consumer = tokeny[1]
usosapi_key_secret = tokeny[2]
usosConnection = usosapi.USOSAPIConnection(usosapi_base_url, usosapi_key_consumer, usosapi_key_secret)

def laduj_plik(lista, filename):
    with open(filename, "r") as lista_f:
        for line in lista_f:
            lista.append(line[:-1])
    lista_f.close()


def zapisz_plik(lista, filename):
    with open(filename, "w") as plik_f:
        for elem in lista:
            plik_f.write(elem + "\n")
    plik_f.close()


def obj_dict(obj):
    return obj.__dict__


def zaladuj_przedmiot(uid, term="2018Z", start="2018-10-04"):
    tmp = usosConnection.get("services/courses/course", course_id=uid,
                             fields="name|ects_credits_simplified")
    przed = usosprzedmioty.UsosPrzedmiot(uid, tmp["name"]["pl"],
                                         usosConnection.get("services/tt/course_edition", course_id=uid,
                                                            term_id=term,
                                                            start=start),
                                         tmp["ects_credits_simplified"])
    return przed


def serializuj_przedmioty(przeddict, filename):
    with open(filename, 'w') as przed_f:
        json.dump(przeddict, przed_f, default=obj_dict)
        przed_f.close()


def deserializuj_przedmioty(filename):
    with open(filename, "r") as przed_f:
        przeddict = json.load(przed_f)
        for klucz in przeddict.keys():
            przeddict[klucz] = usosprzedmioty.UsosPrzedmiot(**przeddict[klucz])
    return przeddict


def czy_koliduje(lista, dur, new_start, day):
    new_end = new_start + (15+dur)/60
    for unit in lista:
        if day == unit.day:
            old_start = unit.start
            old_end = unit.start + (15+unit.dur)/60
            if old_start <= new_start and old_end >= new_end:
                return True
            if old_start >= new_start and old_end <= new_end:
                return True
            if old_start > new_start and float(old_start) < new_end:
                return True
            if old_start < new_start and old_end > float(new_start):
                return True
    return False


def wybierz_przedmioty(dict, ects_min=28):
    ects_cur = 0
    id_wybranych = []
    while ects_cur < ects_min:
        rtmp = random.randint(0, len(list(dict.keys())) - 1)
        # while czy_koliduje(dict, rtmp, id_wybranych):
        #     rtmp += 1
        #     if rtmp in dict:
        #         rtmp += 1
        #     if rtmp >= len(dict):
        #         rtmp = 0
        tmpstr = list(dict.keys())[rtmp]
        while tmpstr in id_wybranych:
            rtmp += 1
            if rtmp >= len(list(dict.keys())):
                rtmp = 0
            tmpstr = list(dict.keys())[rtmp]
        id_wybranych.append(tmpstr)
        ects_cur += dict[tmpstr].ects

    return [dict.get(key) for key in id_wybranych], ects_cur


def zaplanuj_zajecie(przed, unit, unitname, start, day):
    return usosprzedmioty.PrzedmiotWPlanie(textwrap.fill(przed.name + " - " + unitname, width=17), start,
                                           unit[unitname], day)


def zaplanuj_zajecia(wybrane):
    plan = []
    for przed in wybrane:
        for unitname in list(przed.units.keys()):
            day = random.randint(1, 5)
            hour = random.randint(8, 18)
            while czy_koliduje(plan, przed.units[unitname], hour, day):
                day = random.randint(1, 5)
                hour = random.randint(8, 18)
            plan.append(zaplanuj_zajecie(przed, przed.units, unitname, hour, day))

    return plan


def policz_okienka(plan):
    tabela = [[0]*13 for i in range(5)]
    h_okienek = 0
    for unit in plan:
        start = unit.start
        day_id = unit.day - 1
        dur = int((unit.dur+15)/60)
        for i in range(0, dur):
            tabela[day_id][start+i-8] = 1
    for day in tabela:
        i = 0
        j = 12
        while i < 12 and day[i] != 1:
            i += 1
        while j > i and day[j] != 1:
            j -= 1
        for k in range(i, j):
            h_okienek += 1-day[k]

    return h_okienek


def zapostuj_na_fb(sem="let"):
    wybrane_przed, ects_tot = wybierz_przedmioty(deserializuj_przedmioty("src/przed_" + sem + ".txt"))
    print(ects_tot)
    plan = zaplanuj_zajecia(wybrane_przed)
    generujplan.zapisz_plan(plan)
    okienka = policz_okienka(plan)
    graph = facebook.GraphAPI(LONG_LIVED_ACCESS_TOKEN)
    oknk = []
    rekord = ""
    print(oknk)
    laduj_plik(oknk, "src/okienka.txt")
    if int(oknk[0]) > okienka:
        oknk[0] = str(okienka)
        zapisz_plik(oknk, "src/okienka.txt")
        rekord = "\nNowy rekord okienek!"
    if int(oknk[1]) < okienka:
        oknk[1] = str(okienka)
        zapisz_plik(oknk, "src/okienka.txt")
        rekord = "\nNowy rekord okienek!"

    graph.put_photo(image=open('plan.png', 'rb'), message="Oto twój nowy plan! \n \n "
                                                         "W sumie ECTS: " + str(ects_tot) +
                                                         "\nGodzin okienek: " + str(okienka) +
                                                         "\nRekordowe min okienek: " + str(oknk[0]) +
                                                         "\nRekordowe max okienek: " + str(oknk[1]) +
                                                         rekord)
    print(str(datetime.datetime.now()) + "\nWrzucono post na bota, czas okienek: " + str(okienka))


random.seed(datetime.datetime.now())
# zapostuj_na_fb("zim")

# tutaj ustalane jest, o jakich godzinach ma miec miejsce planposting - godziny sa nieco
# inne niz na samej stronie, poniewaz bylo to potem kalibrowane na rpi

schedule.every().day.at("11:00").do(lambda: zapostuj_na_fb("zim"))
schedule.every().day.at("16:40").do(lambda: zapostuj_na_fb("zim"))
schedule.every().day.at("19:00").do(lambda: zapostuj_na_fb("let"))

while True:
    # Checks whether a scheduled task
    # is pending to run or not
    schedule.run_pending()
    time.sleep(1)