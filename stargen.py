import random


def dice(n, sides):
    die = 0
    roll = 0
    while die < n:
        roll = roll + random.randint(1, sides)
        die += 1
    return roll


def pseudo_hex(num):
    num = int(num)
    code = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q",
            "E", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    num = code[num]
    return num


def reverse_hex(hex):
    hex = str(hex)
    code = {"0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "A": 10,
            "B": 11, "C": 12, "D": 13, "E": 14, "F": 15, "G": 16, "H": 17, "J": 18, "K": 19, "L": 20}
    return int(code[hex])


def random_line(filename):
    with open(filename, "r") as line_list:
        line = random.choice(line_list.readlines())
        line = line.strip()
    return line


def list_stringer(input_list):
    output_list = []
    for item in input_list:
        output_list.append(str(item))
    return ' '.join(output_list)


class World:
    def __init__(self, xylocation):
        self.location = [xylocation[0], xylocation[1]]
        self.location_string = ""
        if self.location[1] != 10:
            self.location_string = f"0{self.location[1]}0{self.location[0]}"
        elif self.location[1] == 10:
            self.location_string = f"0{self.location[0]}10"
        else:
            self.location_string = f"0{self.location[1]}0{self.location[0]}"

    def generate_world(self):
        self.name = random_line("data/worlds.txt")
        if dice(2, 6) <= 9:
            self.gas_giant = "G"
        else:
            self.gas_giant = " "
        starport_table = {2: "A", 3: "A", 4: "A", 5: "B", 6: "B",
                          7: "C", 8: "C", 9: "D", 10: "E", 11: "E", 12: "X"}
        self.starport = starport_table[dice(2, 6)]
        self.size = dice(2, 6)-2
        self.atmosphere = dice(2, 6) - 7 + self.size
        if self.atmosphere < 0:
            self.atmosphere = 0
        if self.size == 0:
            self.atmosphere = 0
        else:
            pass
        self.hydrographics = dice(2, 6) - 7 + self.atmosphere
        if self.size == 0:
            self.hydrographics = 0
        elif self.size in (0, 1) or self.size >= 10:
            self.hydrographics -= 4
        else:
            pass
        if self.hydrographics < 0:
            self.hydrographics = 0
        elif self.hydrographics > 10:
            self.hydrographics = 10
        else:
            pass
        self.population = dice(2, 6) - 2
        if self.population < 0:
            self.population = 0
        self.government = dice(2, 6) - 7 + self.population
        if self.government < 0:
            self.governmanent = 0
        if self.government > 15:
            self.government = 15
        self.law = dice(2, 6) - 7 + self.government
        if self.law < 0:
            self.law = 0
        else:
            pass
        self.tech_gen()
        self.base_gen()
        self.trade_gen()
        self.uwp_string = self.starport + pseudo_hex(str(self.size)) + pseudo_hex(str(self.atmosphere)) + pseudo_hex(str(self.hydrographics)) + pseudo_hex(
            str(self.population)) + pseudo_hex(str(self.government)) + pseudo_hex(str(self.law)) + "-" + pseudo_hex(str(self.tech))

    def tech_gen(self):
        starport_tech = {"A": 6, "B": 4, "C": 2, "D": 0, "E": 0, "X": -4}
        self.tech = dice(1, 6) + starport_tech[self.starport]
        if self.size in (0, 1):
            self.tech += 2
        elif self.size in (2, 3, 4):
            self.tech += 1
        if self.atmosphere in range(0, 4) or self.atmosphere >= 10:
            self.tech += 1
        if self.hydrographics == 9:
            self.tech += 1
        elif self.hydrographics == 10:
            self.tech += 2
        if self.population in range(1, 6):
            self.tech += 1
        elif self.population == 9:
            self.tech += 2
        elif self.population >= 10:
            self.tech += 4
        if self.government in (0, 5):
            self.tech += 1
        elif self.government == 13:
            self.tech -= 2

    def base_gen(self):
        starport_effect = {"X": 0, "E": 0, "D": 0, "C": -1, "B": -2, "A": -3}
        scout_roll = dice(2, 6) + starport_effect[self.starport]
        scout = False
        if scout_roll >= 7:
            scout = True
        else:
            scout = False
        if self.starport in ("X", "E"):
            scout = False
        naval = False
        if self.starport in ("A", "B"):
            naval_roll = dice(2, 6)
            if naval_roll >= 8:
                naval = True
            else:
                naval = False
        else:
            naval = False
        if not scout and not naval:
            self.base = ""
        elif scout and not naval:
            self.base = "S"
        elif naval and not scout:
            self.base = "N"
        elif naval and scout:
            self.base = "A"

    def trade_gen(self):
        self.trade_codes = []
        if self.atmosphere in range(4, 10) and self.hydrographics in range(4, 9) and self.population in range(5, 8):
            self.trade_codes.append("Ag")
        if self.atmosphere <= 3 and self.hydrographics <= 3 and self.population >= 6:
            self.trade_codes.append("Na")
        if self.atmosphere in (0, 1, 2, 4, 7, 9) and self.population >= 9:
            self.trade_codes.append("In")
        if self.population <= 6:
            self.trade_codes.append("Ni")
        if self.government in range(4, 10) and self.atmosphere in (6, 8):
            self.trade_codes.append("Ri")
        if self.atmosphere in range(2, 6) and self.hydrographics <= 3:
            self.trade_codes.append("Po")
        if self.hydrographics >= 10:
            self.trade_codes.append("Wa")
        if self.hydrographics == 0:
            self.trade_codes.append("De")
        if self.atmosphere == 0:
            self.trade_codes.append("Va")
        if self.size == 0:
            self.trade_codes.append("As")
        if self.atmosphere in (0, 1) and self.hydrographics >= 1:
            self.trade_codes.append("Ic")
        self.trade_string = list_stringer(self.trade_codes)
