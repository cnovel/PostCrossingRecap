import pycountry
import json
import flag
from collections import Counter


def as_string(i: int) -> str:
    return "{:,}".format(i).replace(",", " ")


def country_alpha_to_str(alpha_2):
    return pycountry.countries.get(alpha_2=alpha_2).name.title() + " " + flag.flag(alpha_2)


class CardInfo:
    def __init__(self, data_card) -> None:
        self.id = data_card[0]
        self.other = data_card[1]
        self.country_code = data_card[3]
        self.posted = data_card[4]
        self.arrived = data_card[5]
        self.kilometers = data_card[6]
        self.days = data_card[7]

cards_sent = []
cards_received = []
with open('data/sent.json', 'r') as sent_file:
    sents = json.load(sent_file)
    for s in sents:
        cards_sent.append(CardInfo(s))
with open('data/received.json', 'r') as received_file:
    receiveds = json.load(received_file)
    for s in receiveds:
        cards_received.append(CardInfo(s))

from_number = len(cards_received)
from_quickest_days = 1000
from_quickest_country = ""
from_slowest_days = 0
from_slowest_country = ""
from_km_traveled = 0
c_best_countries = Counter()
for c in cards_received:
    from_km_traveled += c.kilometers
    c_best_countries[c.country_code] += 1
    if c.days < from_quickest_days:
        from_quickest_days = c.days
        from_quickest_country = country_alpha_to_str(c.country_code)
    if c.days > from_slowest_days:
        from_slowest_days = c.days
        from_slowest_country = country_alpha_to_str(c.country_code)
from_best_country = c_best_countries.most_common(1)[0][0]
from_best_country = country_alpha_to_str(from_best_country)


to_number = len(cards_sent)
to_max_km = 0
to_max_country = ""
to_min_km = 10000000
to_min_country = ""
c_best_countries = Counter()
to_km_traveled = 0
for c in cards_sent:
    to_km_traveled += c.kilometers
    c_best_countries[c.country_code] += 1
    if c.kilometers > to_max_km:
        to_max_km = c.kilometers
        to_max_country = country_alpha_to_str(c.country_code)
    if c.kilometers < to_min_km:
        to_min_km = c.kilometers
        to_min_country = country_alpha_to_str(c.country_code)
to_best_country = c_best_countries.most_common(1)[0][0]
to_best_country = country_alpha_to_str(to_best_country)

with open("template.html", 'r') as temp:
    html = temp.read()
html = html.replace("$$FROM_NUMBER$$", as_string(from_number))
html = html.replace("$$FROM_QUICKEST_DAYS$$", as_string(from_quickest_days))
html = html.replace("$$FROM_QUICKEST_COUNTRY$$", from_quickest_country)
html = html.replace("$$FROM_SLOWEST_DAYS$$", as_string(from_slowest_days))
html = html.replace("$$FROM_SLOWEST_COUNTRY$$", from_slowest_country)
html = html.replace("$$FROM_BEST_COUNTRY$$", from_best_country)
html = html.replace("$$FROM_KM_TRAVELED$$", as_string(from_km_traveled))

html = html.replace("$$TO_NUMBER$$", as_string(to_number))
html = html.replace("$$TO_MAX_KM$$", as_string(to_max_km))
html = html.replace("$$TO_MAX_COUNTRY$$", to_max_country)
html = html.replace("$$TO_MIN_KM$$", as_string(to_min_km))
html = html.replace("$$TO_MIN_COUNTRY$$", to_min_country)
html = html.replace("$$TO_BEST_COUNTRY$$", to_best_country)
html = html.replace("$$TO_KM_TRAVELED$$", as_string(to_km_traveled))

with open("recap.html", 'w') as recap:
    recap.write(html)
