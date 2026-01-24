import random

from faker import Faker

from data.constants import ALL_COUNTRIES, ALL_COUNTRY_LOCALES

def address_generator(excluded=None):
    if excluded:
        available = list(filter(lambda x: x not in excluded, ALL_COUNTRIES))
        country = random.choice(available)
    else:
        country = random.choice(ALL_COUNTRIES)
    locale = ALL_COUNTRY_LOCALES[country]

    fake_data = Faker(locale)

    full_name = fake_data.name()

    st = fake_data.street_name()
    ab = fake_data.random_int(min=1, max=1000)
    street_address = f"{ab} {st}"

    ph = fake_data.phone_number().replace(' ', '').replace('(', '').replace(')', '').replace('+', '').replace(
        '.', '').replace('-', '').replace('x', '')
    if len(ph) > 10:
        mobile_number = int(ph[:10])
    else:
        mobile_number = int(ph)

    zip_code = str(fake_data.postcode().replace('-', ''))
    if len(zip_code) > 8:
        final_zip = zip_code[:8]
    else:
        final_zip = zip_code

    city = fake_data.city()

    return {
        'full_name': full_name,
        'street_address': street_address,
        'mobile_num': mobile_number,
        'zip_code': final_zip,
        'country': country,
        'city': city,

    }

def address_generator_raw():
    country = random.choice(ALL_COUNTRIES)
    locale = ALL_COUNTRY_LOCALES[country]

    fake_data = Faker(locale)

    full_name = fake_data.name()

    st = fake_data.street_name()
    ab = fake_data.random_int(min=1, max=1000)
    street_address = f"{ab} {st}"

    ph = fake_data.phone_number().replace(' ', '').replace('(', '').replace(')', '').replace('+', '').replace(
        '.', '').replace('-', '').replace('x', '')
    if len(ph) > 10:
        mobile_number = int(ph[:10])
    else:
        mobile_number = int(ph)

    zip_code = str(fake_data.postcode().replace('-', ''))
    if len(zip_code) > 8:
        final_zip = zip_code[:8]
    else:
        final_zip = zip_code

    city = fake_data.city()

    if country == 'USA':
        state = fake_data.state()
    else:
        state = None

    return {'fullName': full_name,
            'streetAddress': street_address,
            'mobileNum': mobile_number,
            'zipCode': final_zip,
            'country': country,
            'city': city,
            'state': state
    }

