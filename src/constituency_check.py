import bs4 as bs
import urllib.request as request
import sys
import re
import pandas as pd 

USAGE = "Usage: python3 constituency_check.py <postcode>"

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
    
    if seat_pred_table == None:
        print("Electoral Calculus could not be reached, you have either exceeded the number of calls for today or the service is down. Try again later")
        return
    
    seat_pred_headings = seat_pred_table.find_all("th")
    
    seat_pred_rows = seat_pred_table.find_all("tr")
    
    seat_pred_dataframe = transform_table_to_dataframe(seat_pred_headings, seat_pred_rows)
    
    seat_summary_rows = site_soup.find("table", attrs={"class":"seatsummary"}).find_all("tr")
    
    seat_title = site_soup.find("h1", attrs={"id":"title"}).text
    
    party_winner_prediction = site_soup.find("div", attrs={"class":"pills uppercase"}).text
    
    print("Welcome to Constituency Checker. Please see below for your seat details\n")
    
    print("%s\n" % seat_title)
    
    for seat_summary_row in seat_summary_rows:
        seat_summary_data = seat_summary_row.find_all('td')
        
        for data in seat_summary_data:
            print("%s " % data.text, end="")
            
        print()
    
    print("\n%s\n" % seat_pred_dataframe.to_string(index=False))
    
    print(party_winner_prediction)
    
def transform_table_to_dataframe(headings, html_table_rows, begin=1, end=-1) -> pd.DataFrame:
    res = []
    
    for table_row in html_table_rows[begin:end]:
        data = table_row.find_all("td")
        
        row = [tr.text.strip() for tr in data if tr.text.strip()]
        
        res.append(row)
    
    return pd.DataFrame(res, columns=[heading.text for heading in headings])
    
def get_soup(postcode: str) -> bs.BeautifulSoup:
    source = request.urlopen(URL + postcode).read()
    
    return bs.BeautifulSoup(source, "lxml")
        
if __name__ == "__main__":
    main()  