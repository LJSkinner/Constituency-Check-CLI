# Constituency Checker

Constituency Checker is a command line utility written in Python that allows users to input a UK postcode and retrieve details about their constituencies corresponding MP's seat, the parties chances of winning, and other related information from the Electoral Calculus website. You can also search for a seat by name and make use of  similar functionality provided as the EC seat explorer. 

The data used in this project is provided by the [Electoral Calculus website](https://www.electoralcalculus.co.uk/newseatlookup.html), using their seat explorer tool. I am very grateful to the Electoral Calculus team for providing this website and data. 

Note: They do have an upper limit for the number of calls you can make to their service per day, so you may encounter an error if you're making a lot of calls in a day. Additionally, due to the nature of web scraping, this could break at any point should their website change. I also may private this repo at any time at the request of the authors.

## Usage & Installation
First clone the repo and install the requirements using pip. This assumes you have Python and Pip installed on your machine. If not, please be sure to get both of them before continuing.

**pip3** may just be **pip** depending on your OS.

```bash
git clone https://github.com/LJSkinner/Constituency-Check-CLI.git
cd Constituency-Check-CLI/
pip3 install -r requirements.txt
```

##### Seaching by Postcode
Currently this checker supports searching by postcode. Once you've installed the requirements, you will want to run the **constituency_check.py** through python. This is located in the **src** folder but you can move this to anywhere you wish.

An example of running this is as follows (You may have to use "python" instead if you are on Windows):
```bash
python3 constituency_check.py FK30JA
```

If you provided a valid postcode, you should see something like this:
```
Linlithgow and East Falkirk: Seat Details

MP at 2019: Martyn Day  (SNP) 
County/Area: Edinburgh area (Scotland) 
Electorate: 87,044 
Turnout: 66.4% 

 Party 2019Votes 2019Share PredVotes
   SNP    25,551     44.2%     38.5%
   CON    14,285     24.7%     18.3%
   LAB    10,517     18.2%     29.9%
   LIB     4,393      7.6%      3.7%
Reform     1,257      2.2%      2.4%
 Green     1,184      2.0%      4.4%
   OTH       588      1.0%      2.8%

Prediction: SNP hold
```
Otherwise you'll get the following output:
```
You did not provide a valid UK Postcode. Example: FK20JA (do not include a space)
Postcode Usage: python3 constituency_checker.py <postcode>
```

##### Searching by Seat Name
If you would like to search by seat name you'll want to use the **-n** switch and then provide the name. Note that the first time you run this as a command you'll be passing it as an argument, so make sure if it has spaces to wrap them in quotes like **"North East"**. After the menu displays, if you choose to search for another seat, you don't need to do this from then on.

An example of running this is as follows:
```bash
python3 constituency_checker.py -n Falkirk
```

This will return a partial list of all the seats that contain the search term. So in this case we supplied **Falkirk** so we will get the two seats that contain **Falkirk** in them as shown below:
```
1 : Linlithgow and East Falkirk
2 : Falkirk
Please enter your choice using one of the numbers above (0 to go back):
```

From this point it works the same as the entering the postcode, we can go back with by entering 0 and then you'll be prompted to enter the seat name again. If you type exit then it will close or you can just terminate it from the shell.

I recommend that you alias this command in some way if you plan to use it a lot, regardless of what option you are doing. For most Linux & Mac users that will be adding an entry to their .bashrc file, and for Windows users I recommend creating a .bat or .ps1 file and adding it to your path. I personally alias to "seatcheck" as it is easy to remember. 

## Legal

This project is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and non-infringement. In no event shall the authors be liable for any claim, damages, or other liability, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the software or the use or other dealings in the software.

In non legal speak, be sensible with this util. Please don't spam or overload their site with requests. I am not responsible for anything you do with this that is unethical. 

If the authors over at Electoral Calculus have any concerns about the use or distribution of this software, please contact the project owner Luke Skinner at ljs.work@pm.me.

## License

This project is licensed under the terms of the MIT license. See the [LICENSE.md](LICENSE.md) file for details.
