# Constituency Electoral Results Checker CLI

Constituency Electoral Results Checker is a command line utility written in Python that allows users to input a UK postcode and retrieve details about their constituencies corresponding MP's seat, the parties chances of winning, and other related information from the Electoral Calculus website. You can also search for a seat by name and make use of  similar functionality provided as the EC seat explorer. 

The data used in this project is provided by the [Electoral Calculus website](https://www.electoralcalculus.co.uk/newseatlookup.html), using their seat explorer tool. I am very grateful to the Electoral Calculus team for providing this website and data. 

**DISCLAIMER**: They do have an upper limit for the number of calls you can make to their service per day, so you may encounter an error if you're making a lot of calls in a day. Additionally, due to the nature of web scraping, this could break at any point should their website change. I also may private this repo at any time at the request of the authors.

## Usage & Installation
First clone the repo and install the requirements using pip. This assumes you have Python and Pip installed on your machine. If not, please be sure to get both of them before continuing.

**pip3** may just be **pip** depending on your OS.

```bash
git clone https://github.com/LJSkinner/Constituency-Electoral-Results-Checker-CLI.git
cd Constituency-Electoral-Results-Checker-CLI/
pip3 install -r requirements.txt
```

##### Searching by Seat or MP Name
When you run the program by default with no additional arguments you will start the search by name mode. The menu will allow you to search for constituencies by their seat name or MPs name. 

An example of running this is as follows:
```bash
python3 constituency_checker.py 
```

This will first ask us to search for a seat or MP name and then return a partial list of all the seats that contain the search term. So in this case we supplied **York** so we will get the two seats that contain **York** in them as shown below:
```
Enter the seat or MP name (Type exit to quit): York
1 : York Central (Rachael Maskell)
2 : York Outer (Luke Charters)
Please enter your choice using one of the numbers above (0 to go back): 
```
If we provided Rachael instead the first result would show up since it matches the name of the MP for that seat.

We can then select on of the seat options by using the numbers so let's go with **2** for **York Outer**. This will then display the constituency results as shown below:
```
MP at 2024: Luke Charters  (LAB) 
County/Area: North Yorkshire (Yorks/Humber) 
Electorate: 76,228 
Turnout: 67.0% 

 Party 2024Votes 2024Share PredVotes
   LAB    23,161     45.3%     37.0%
   CON    13,770     26.9%     24.7%
Reform     5,912     11.6%     21.1%
   LIB     5,496     10.8%     10.5%
 Green     2,212      4.3%      6.3%
   OTH       555      1.1%      0.3%

Prediction: LAB hold
All done? Type exit if you would like to exit, otherwise press enter to continue:
```



I recommend that you alias this command in some way if you plan to use it a lot, regardless of what option you are doing. For most Linux & Mac users that will be adding an entry to their .bashrc file, and for Windows users I recommend creating a .bat or .ps1 file and adding it to your path. I personally alias to "seatcheck" as it is easy to remember. 

##### Searching by Postcode
We can also search by postcode by suppling it as an additional argument when running constituency checker. This is meant to be used as a one off search that will bypass the user interface. Use this if you just want to see the results for your postcode quickly.

The postcode must not contain spaces and be a valid UK postcode. 

An example of running this is as follows (You may have to use "python" instead if you are on Windows):
```bash
python3 constituency_checker.py FK94LA
```

If you provided a valid postcode, you should see something like this:
```
Stirling and Strathallan: Seat Details

MP at 2024: Chris Kane  (LAB) 
County/Area: Central (Scotland) 
Electorate: 76,284 
Turnout: 65.3% 

 Party 2024Votes 2024Share PredVotes
   LAB    16,856     33.9%     20.2%
   SNP    15,462     31.1%     34.6%
   CON     9,469     19.0%     20.3%
Reform     3,145      6.3%     14.2%
   LIB     2,530      5.1%      4.4%
 Green     2,320      4.7%      6.1%
   OTH         0      0.0%      0.1%

Prediction: SNP gain from LAB

```
Otherwise you'll get the following output:
```
You did not provide a valid UK Postcode. Example: FK94LA (do not include a space)
Postcode Usage: python3 constituency_checker.py <postcode>
```

## Legal

This project is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and non-infringement. In no event shall the authors be liable for any claim, damages, or other liability, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the software or the use or other dealings in the software.

In non legal speak, be sensible with this util. Please don't spam or overload their site with requests. I am not responsible for anything you do with this that is unethical. 

If the authors over at Electoral Calculus have any concerns about the use or distribution of this software, please contact the project owner Luke Skinner at ljs.work@pm.me.

## License

This project is licensed under the terms of the MIT license. See the [LICENSE.md](LICENSE.md) file for details.
