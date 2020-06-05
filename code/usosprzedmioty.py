import datetime


class UsosPrzedmiot:
    def __init__(self, id, name, units, ects):
        self.id = id
        self.name = name
        self.units = load_units(units)
        self.ects = ects

    def __str__(self) -> str:
        return "Id: " + str(self.id) + \
               "\nName: " + str(self.name) + \
               "\nUnits: " + str(self.units) + \
               "\nECTS: " + str(self.ects)


def load_units(units: list):
    units2 = {}
    for dict in units:
        units2[dict["name"]["pl"].split(' ', 1)[0]] = (datetime.datetime.strptime(dict["end_time"], '%Y-%m-%d %H:%M:%S')\
                                                      - datetime.datetime.strptime(dict["start_time"], '%Y-%m-%d %H:%M:%S')).seconds/60
    return units2


class PrzedmiotWPlanie:
    def __init__(self, name, start, dur, day):
        self.name = name
        self.start = start # should be full hour, int
        self.dur = dur
        self.day = day # 1 - Monday, 5 - Friday