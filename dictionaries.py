district_dict = {"Металлургический": "Metallurgicheskiy-rayon",
                 "Калининский": "Kalininskiy-rayon",
                 "Курчатовский": "Kurchatovskiy-rayon",
                 "Ленинский": "Leninskiy-rayon",
                 "Советский": "Sovetskiy-rayon",
                 "Тракторозаводский": "Traktorozavodskiy-rayon",
                 "Центральный": "Centralnyi-rayon"}

rooms_dict = {1: "odnokomnatnye",
              2: "dvuhkomnatnye",
              3: "trehkomnatnye",
              4: "chetyrehkomnatnye",
              5: "mnogokomnatnye"}


def get_key_by_value(dictionary: {}, find_value):
    for key, value in dictionary.items():
        if value == find_value:
            return key


def validate_district(district: str) -> bool:
    if not district_dict.keys().__contains__(district.lower().strip()):
        return False

    return True
