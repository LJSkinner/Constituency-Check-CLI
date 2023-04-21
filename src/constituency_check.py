import bs4 as bs
import urllib.request as request
import sys
import re
import pandas as pd 

POSTCODE_USAGE = "Postcode Usage: python3 constituency_check.py <postcode>"

NAME_USAGE = "Seat Name Usage: python3 constituency_check.py -n <name> (If the seat contains spaces wrap it in quotes like \"this\")"

POSTCODE_REGEX = "^[A-Z]{1,2}[0-9][A-Z0-9]?[0-9][A-Z]{2}$"

POSTCODE_URL = "https://www.electoralcalculus.co.uk/fcgi-bin/seatdetails.py?postcode="

DEFAULT_NUM_ARGS = 3

def main():
    if len(sys.argv) > DEFAULT_NUM_ARGS:
        print("You entered incorrent inputs, please review the usages\n")
        
        print(POSTCODE_USAGE)
        
        print(NAME_USAGE)
        
        return
    
    if len(sys.argv) < 2:
        print("Postcode not provided. Please provide a postcode\n%s" % POSTCODE_USAGE)
        
        return
    elif re.match(POSTCODE_REGEX, sys.argv[1]) == None and sys.argv[1] != "-n":
        print("You did not provide a valid UK Postcode. Example: FK20JA (do not include a space)\n%s" % POSTCODE_USAGE)
        
        return
    elif sys.argv[1] == "-n" and len(sys.argv) < 3:
        print("You did not provide a valid input for the seat name. Example: Falkirk\n%s" % NAME_USAGE)
        
        return
   
    if sys.argv[1] == "-n":
        print("do name check stuff")
    else:
       handle_postcode_search()
       
def handle_name_search():
    pass
    
def handle_postcode_search():
    soup = get_seat_soup_from_postcode(sys.argv[1])
    
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
    
def get_seat_soup_from_postcode(postcode: str) -> bs.BeautifulSoup:
    source = request.urlopen(POSTCODE_URL + postcode).read()
    
    return bs.BeautifulSoup(source, "lxml")
        
if __name__ == "__main__":
    main()  