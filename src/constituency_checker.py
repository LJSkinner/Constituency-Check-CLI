import bs4 as bs
import urllib.request as request
import sys
import re
import pandas as pd 
import os

POSTCODE_USAGE = "Postcode Usage: python3 constituency_checker.py <postcode>"

POSTCODE_REGEX = "^[A-Z]{1,2}[0-9][A-Z0-9]?[0-9][A-Z]{2}$"

# The postcode URL is used when searching via postcode input
POSTCODE_URL = "https://www.electoralcalculus.co.uk/fcgi-bin/seatdetails.py?postcode="

# The seat name URL is used when searching via seat name input
SEAT_NAME_URL = "https://www.electoralcalculus.co.uk/fcgi-bin/seatdetails.py?seat="

# The seat list URL is used when searching via seat name input, this retrieves the list of all current seats
SEAT_LIST_URL = "https://www.electoralcalculus.co.uk/orderedseats.html"

DEFAULT_NUM_ARGS = 2

MIN_SEATS_TO_DISPLAY = 10

def main():
    if len(sys.argv) > DEFAULT_NUM_ARGS:
        print("You entered incorrent inputs, please review the usages\n")
        
        print(POSTCODE_USAGE)
        
        return
    
    if len(sys.argv) < 2:
        handle_name_search(); 
        
        return
    elif re.match(POSTCODE_REGEX, sys.argv[1]) == None:
        print("You did not provide a valid UK Postcode. Example: FK94LA (do not include a space)\n%s" % POSTCODE_USAGE)
        
        return
    else:
        handle_postcode_search(sys.argv[1])
       
def handle_name_search():
    seat_list_soup = get_seat_list_soup()
    
    seat_list_table = seat_list_soup.find("table", attrs={"class":"small ccllccrrrrrrrrcc"})
    
    seat_list_anchors = seat_list_table.find_all("a")
    
    # This section for getting the mp names is a bit messy due to the way the table is. (there's a definitely a better way to do this)
    
    # We start by getting rid of the headings that are stored in td 
    seat_list_rows = seat_list_table.find_all("td")[6:]
    
    mp_names = []
    
    # We insert the first name which is at index 3
    mp_names.insert(0, seat_list_rows[3].text)
    
    # We start at index 19 and then increment by 16, since that is the amount of spaces to get each name in that column
    for i in range(19, len(seat_list_rows), 16):
        mp_names.append(seat_list_rows[i].text)
    
    if seat_list_anchors == None or len(mp_names) == 0:
        print("The seat list could not be retrieved, please try again later")
        
        return
    
    if len(seat_list_anchors) != len(mp_names):
        print("Something has went wrong. The length of seats and mp names do not match")
    
    seat_list = []
    
    for i, seat_list_anchor in enumerate(seat_list_anchors):
        seat_list.append(f"{seat_list_anchor.text} ({mp_names[i]})")
          
    while True:    
      seat_name = input("Enter the seat or MP name (Type exit to quit): ").lower().strip()
    
      seat_name = seat_name.lower().strip()
      
      if seat_name == "exit":
          print("Thanks for using Constituency Checker, goodbye")
          
          break
    
      filtered_seat_list = [name for name in seat_list if seat_name in str.lower(name)][0:MIN_SEATS_TO_DISPLAY]
      
      for i, filtered_seat in enumerate(filtered_seat_list):
          print(i + 1, ":", filtered_seat)
    
      if len(filtered_seat_list) == 0:
          clear_console()
          
          print("No results found, try again")
          
          continue
      
      try:
          user_seat_choice = int(input("Please enter your choice using one of the numbers above (0 to go back): "))
      except ValueError:
          clear_console()
          
          print("Please make sure that you enter a number")
          
          continue
      
      if user_seat_choice < 0 or user_seat_choice > len(filtered_seat_list):
          clear_console()
          
          print("Please make sure the number you entered is one of the options or 0 to go back.")
          
          continue
      elif user_seat_choice == 0:
          clear_console()
          
          continue
      else:
          # Add %20 to account for spaces in the seat name. Also we only want the seat name for this, so drop MP name.
          selected_seat = str.replace(filtered_seat_list[user_seat_choice - 1], " ", "%20").split("%20(")[0]
          
          soup = get_seat_soup_from_name(selected_seat)
          
          process_seat_details(soup)
          
          user_continue_choice = input("All done? Type exit if you would like to exit, otherwise press enter to continue: ")
          
          if str.lower(user_continue_choice) == "exit":
              print("Thanks for using Constituency Checker, goodbye")
              
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