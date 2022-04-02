import re

required_fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]

def open_txt(filename: str):
    with open(filename) as f:
        lines = [dict()]
        for line in f:
            if line.rstrip() != "":
                kv_pairs = line.rstrip().split()
                for pair in kv_pairs:
                    k, v = tuple(pair.split(sep=":"))
                    lines[-1][k] = v
            else:
                lines.append(dict())
    return lines

def passport_validate(line: dict):
    for k in required_fields:
        if line.get(k) is None:
            return False
    return True

class Passport:
    def __init__(self, p: dict) -> None:
        self.byr = p["byr"]
        self.iyr = p["iyr"]
        self.eyr = p["eyr"]
        self.hgt = p["hgt"]
        self.hcl = p["hcl"]
        self.ecl = p["ecl"]
        self.pid = p["pid"]

    def valid(self) -> bool:
        try:
            byr = int(self.byr)
            if byr < 1920 or byr > 2002:
                return False

            iyr = int(self.iyr)
            if iyr < 2010 or iyr > 2020:
                return False

            eyr = int(self.eyr)
            if eyr < 2020 or eyr > 2030:
                return False

            hgt = int(self.hgt[:-2])
            if self.hgt[-2:] == "cm":
                if hgt < 150 or hgt > 193:
                    return False
            elif self.hgt[-2:] == "in":
                if hgt < 59 or hgt > 76:
                    return False

            hcl = self.hcl
            if hcl[0] != "#" or len(hcl) != 7 or re.search(r"[^0-9a-fA-F]", hcl[1:]):
                return False

            ecl_values = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
            if self.ecl not in ecl_values:
                return False

            pid = self.pid
            if len(pid) != 9 or re.search(r"[^0-9]", pid):
                return False
        except Exception:
            return False

        return True

if __name__ == "__main__":
    # lines = open_txt("test.txt")
    lines = open_txt("aoc04.txt")
    valid_count = 0
    passports = []
    for line in lines:
        if passport_validate(line):
            valid_count += 1
            passports.append(Passport(line))
    print("part 1: ", valid_count)

    valid_count = 0
    for passport in passports:
        if passport.valid():
            valid_count += 1
    print("part 2: ", valid_count)
