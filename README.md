# Constituency Check

Constituency Check is a command line utility written in Python that allows users to input a UK postcode and retrieve details about their constituencies corresponding MP's seat, the parties chances of winning, and other related information from the Electoral Calculus website. 

The data used in this project is provided by the [Electoral Calculus website](https://www.electoralcalculus.co.uk/newseatlookup.html), using their seat explorer tool. I am very grateful to the Electoral Calculus team for providing this website and data. 

Note: They do have an upper limit for the number of calls you can make to their service per day, so you may encounter an error if you're making a lot of calls in a day. Additionally, due to the nature of web scraping, this could break at any point should their website change. I also may private this repo at any time at the request of the authors.

## Usage & Installation
First clone the repo and install the requirements using pip. This assumes you have Python and Pip installed on your machine. If not, please be sure to get both of them before continuing.
```bash
git clone https://github.com/LJSkinner/Constituency-Check-CLI.git
cd Constituency-Check-CLI/
pip3 install -r requirements.txt
```

Currently this checker supports searching by postcode. Once you've installed the requirements, you will want to run the **constituency_check.py** through python. This is located in the **src** folder but you can move this to anywhere you wish.

An example of running this is as follows:
```bash
python3 constituency_check.py FK30JA
```

If you provided a valid postcode, you should see something like this:
```
Welcome to Constituency Checker. Please see below for your seat details

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
Usage: python3 constituency_check.py <postcode>
```

## Legal

This project is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and non-infringement. In no event shall the authors be liable for any claim, damages, or other liability, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the software or the use or other dealings in the software.

In non legal speak, be sensible with this util. Please don't spam or overload their site with requests. I am not responsible for anything you do with this that is unethical. 

If the authors over at Electoral Calculus have any concerns about the use or distribution of this software, please contact the project owner Luke Skinner at hyperconix@pm.me.

## License

This project is licensed under the terms of the MIT license. See the [LICENSE.md](LICENSE.md) file for details.
