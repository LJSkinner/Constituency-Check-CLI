import bs4 as bs
import urllib.request as request
import sys
import re

USAGE = "Usage: python3 constiuency_check.py <postcode>"

POSTCODE_REGEX = "^[A-Z]{1,2}[0-9][A-Z0-9]?[0-9][A-Z]{2}$"

URL = "https://www.electoralcalculus.co.uk/fcgi-bin/seatdetails.py?postcode="

def main():
    if len(sys.argv) < 2:
        print("Postcode not provided. Please provide a postcode\n%s" % USAGE)
    elif re.match(POSTCODE_REGEX, sys.argv[1]) == None:
        print("You did not provide a valid UK Postcode. Example: FK20JA (do not include a space)\n%s" % USAGE)
    else:
        soup = get_soup(sys.argv[1])
        
        process_seat_details(soup)

def process_seat_details(site_soup: bs.BeautifulSoup):
    seat_pred_table = site_soup.find("table", attrs={"class":"seatpred"})
    
    seat_pred_headings = seat_pred_table.find_all("th")
    
    seat_pred_rows = seat_pred_table.find_all("tr")
    
    for heading in seat_pred_headings:
        print(heading.text + " ", end="")
        
    print()
    
    for row in seat_pred_rows[1::]:
        row_data = row.find_all('td')
        
        for data in row_data:
            print(data.text + " ", end="")
        print()

def get_soup(postcode: str) -> bs.BeautifulSoup:
    source = request.urlopen(URL + postcode).read()
    
    return bs.BeautifulSoup(source, "lxml")
        
if __name__ == "__main__":
    main()  