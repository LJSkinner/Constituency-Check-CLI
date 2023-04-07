import bs4 
import requests
import sys
import re

USAGE = 'Usage: python3 constiuency_check.py <postcode>'

POSTCODE_REGEX = '^[A-Z]{1,2}[0-9][A-Z0-9]?[0-9][A-Z]{2}$'

def main():
    if len(sys.argv) < 2:
        print('Postcode not provided. Please provide a postcode\n%s' % USAGE)
    elif re.match(POSTCODE_REGEX, sys.argv[1]) == None:
        print("You did not provide a valid UK Postcode. Example: FK20JA (do not include a space)\n%s" % USAGE)
    else:
        scrape_seat_details(sys.argv[1])

def scrape_seat_details(postcode: str):
    pass
        
if __name__ == '__main__':
    main()  