# link to task: https://adventofcode.com/2015/day/11

import re

from string import ascii_lowercase as alc


class LowercaseNumber:
    def __init__(self, value: list):
        self.value = value

    @classmethod
    def from_string(cls, string: str):
        assert len(string) > 0
        assert string.islower()
        assert re.search(r'([0-9])+', string) is None
        return cls(value=[c for c in string[::-1]])

    def next(self):
        place = 0
        carry = True
        while carry:
            if carry:
                if place >= len(self.value):
                    self.value.append('a')
                    carry = False
                elif self.value[place] == 'z':
                    self.value[place] = 'a'
                    carry = True
                else:
                    cur_alphabet_id = alc.index(self.value[place])
                    self.value[place] = alc[cur_alphabet_id + 1]
                    carry = False
            place += 1

    def is_valid_password(self) -> bool:
        string = str(self)

        # Rule 1
        len_straight = 3
        found_valid_straight = False
        for i in range(len(alc) - len_straight + 1):
            target = f"{alc[i]}{alc[i+1]}{alc[i+2]}"
            if re.search(target, string) is not None:
                found_valid_straight = True
                break
        if not found_valid_straight:
            return False

        # Rule 2
        forbidden_letters = ['i', 'o', 'l']
        for fl in forbidden_letters:
            if fl in string:
                return False

        # Rule 3
        pair_count = 0
        for c in alc:
            pair = f"{c}{c}"
            if re.search(pair, string) is not None:
                pair_count += 1
            if pair_count > 1:
                return True

        return False

    def __str__(self):
        return "".join(self.value[::-1])


with open("input/2015.11.in", "r") as f:
    passwd_old = f.readline()


current_password = LowercaseNumber.from_string(passwd_old)
while not current_password.is_valid_password():
    current_password.next()
print(f"New password on first expiry: {current_password}")
current_password.next()
while not current_password.is_valid_password():
    current_password.next()
print(f"New password on second expiry: {current_password}")
