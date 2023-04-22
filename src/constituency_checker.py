import bs4 as bs
import urllib.request as request
import sys
import re
import pandas as pd 
import os

POSTCODE_USAGE = "Postcode Usage: python3 constituency_check.py <postcode>"

NAME_USAGE = "Seat Name Usage: python3 constituency_check.py -n <name> (If the seat contains spaces wrap it in quotes like \"this\")"

POSTCODE_REGEX = "^[A-Z]{1,2}[0-9][A-Z0-9]?[0-9][A-Z]{2}$"

# The postcode URL is used when searching via postcode input
POSTCODE_URL = "https://www.electoralcalculus.co.uk/fcgi-bin/seatdetails.py?postcode="

# The seat name URL is used when searching via seat name input
SEAT_NAME_URL = "https://www.electoralcalculus.co.uk/fcgi-bin/seatdetails.py?seat="

# The seat list URL is used when searching via seat name input, this retrieves the list of all current seats
SEAT_LIST_URL = "https://www.electoralcalculus.co.uk/orderedseats.html"

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
        handle_name_search(sys.argv[2])
    else:
        handle_postcode_search(sys.argv[1])
       
def handle_name_search(seat_name: str):
    seat_name = seat_name.lower().strip()
    
    seat_list_soup = get_seat_list_soup()
    
    seat_list_anchors = seat_list_soup.find("table", attrs={"class":"small ccllccrrrrrrrrcc"}).find_all("a")
    
    if seat_list_anchors == None:
        print("The seat list could not be retrieved, please try again later")
        
        return
    
    seat_list = []
    
    for seat_list_anchor in seat_list_anchors:
        seat_list.append(seat_list_anchor.text)
          
    while True:
      if seat_name == "exit":
          print("Thanks for using Constituency Checker, goodbye")
          
          break
      
      filtered_seat_list = [name for name in seat_list if seat_name in str.lower(name)]
      
      for i, filtered_seat in enumerate(filtered_seat_list):
          print(i + 1, ":", filtered_seat)
    
      if len(filtered_seat_list) == 0:
          clear_console()
          
          print("No results found, try again")
          
          seat_name = input("Enter the seat name (Type exit to quit): ").lower().strip()
          
          continue
      
      try:
          user_seat_choice = int(input("Please enter your choice using one of the numbers above (0 to go back): "))
      except ValueError:
          clear_console()
          
          print("Please make sure that you enter a number")
          
          continue
      
      if user_seat_choice < 0 or user_seat_choice > len(filtered_seat_list):
          clear_console()
          
          print("Please make sure the number you entered is one of the seats or 0 to go back.")
          
          continue
      elif user_seat_choice == 0:
          clear_console()
          
          seat_name = input("Enter the seat name (Type exit to quit): ").lower().strip()
          
          continue
      else:
          # Add %20 to account for spaces in the seat name
          selected_seat = str.replace(filtered_seat_list[user_seat_choice - 1], " ", "%20")
          
          soup = get_seat_soup_from_name(selected_seat)
          
          process_seat_details(soup)
          
      return
          
def handle_postcode_search(postcode: str):
    soup = get_seat_soup_from_postcode(postcode)
    
    process_seat_details(soup)

def process_seat_details(site_soup: bs.BeautifulSoup):
    clear_console()
    
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

def get_seat_soup_from_name(seat_name: str) -> bs.BeautifulSoup:
    source = request.urlopen(SEAT_NAME_URL + seat_name).read()
    
    return bs.BeautifulSoup(source, "lxml")

def get_seat_list_soup() -> bs.BeautifulSoup:
    source = request.urlopen(SEAT_LIST_URL).read()
    
    return bs.BeautifulSoup(source, "lxml")

def clear_console():
    os.system("cls" if os.name == "nt" else "clear")
  
if __name__ == "__main__":
    main()  