import re

regex = r"^(?!(0*1*)+011)(0*1*)+"

strings = [
    "",
    "0",
    "1",
    "00",
    "01",
    "10",
    "11",
    "000",
    "101",
    "111",
    "1001",
    "011",
    "0011",
    "0110",
    "1011",
    "00110",
    "01101"
]

for string in strings:
    if re.fullmatch(regex, string):
        print(f"Accepted: {string!r}")
    else:
        print(f"Rejected: {string!r}")