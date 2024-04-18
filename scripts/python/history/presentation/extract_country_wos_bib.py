import bibtexparser
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut


def get_country_from_addresses(address_list):
    """ Process a list of addresses to extract countries """
    geolocator = Nominatim(user_agent="geoapiExercises")
    countries = []

    for address in tqdm(address_list, desc="Geocoding addresses")::
        try:
            location = geolocator.geocode(address, timeout=10)  # Timeout set to 10 seconds
            if location:
                address_parts = location.address.split(',')
                country = address_parts[-1].strip()  # Country is typically the last component
                countries.append(country)
            else:
                countries.append("Country not found")
        except GeocoderTimedOut:
            countries.append("Timed out")
        except Exception as e:
            countries.append(f"Error occurred: {str(e)}")

    return countries




def extract_countries_from_bib_file(filename):
    with open(filename) as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)


    all_countries = set()
    for entry in bib_database.entries:
        if 'affiliation'  in entry:
            countries = get_country_from_addresses(entry['affiliation'])
            all_countries.update(countries)
        elif 'Affiliation'  in entry:
            countries = get_country_from_addresses(entry['affiliation'])
            all_countries.update(countries)

    return bib_database, all_countries

# Replace 'your_file.bib' with the path to your .bib file
droot = '../../../data/wos/'
filename = droot + 'wos_fMRI_2016-2024.bib'
bibd, countries = extract_countries_from_bib_file(filename)
print("Countries found:", countries)
