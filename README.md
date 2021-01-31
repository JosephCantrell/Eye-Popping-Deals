# Amazon Associates promo code web scraper
This program was designed and created for a technical interview for Eye Popping Deals

## Setup

To run this bot, you must install the requirements
```bash
pip install -r requirements.txt
```

Enter your username, password and modify the timeout value if needed in the `config.py` file

```
url : Predetermined

infiniteScrollTimeout = 60

username = # Enter your Amazon Associates username / email here
password = # Enter your Amazon Associates password here

```
__NOTE: AFTER EDITING CONFIG.PY, DO NOT COMMIT THE FILE__

## Execute

To execute the bot, run the following in your terminal

```
python3 scrape.py

OR

scrape.py
```

## Functions

### Run Function

```
run(self, url)
```

**Description**  
The run starts the program after init. The run funciton writes data headers, logs in, clicks the 
'upcoming' checkbox and starts the scrolling function

**Parameters**  
self : self
url : The Url that the bot will first visit
 
### Login Function

```
login(self)
```

**Description**  
Assumes that the webpage is on the Login screen due to the redirect and inserts the `config.py` username
and password into the webpage and hits enter

**Parameters**  
self : self

### Scroll Function

```
scroll(self)
```

**Description**
The scroll function will check the current page source with the previous page source and 
determine if it needs to scroll to the bottom or not to allow for more promo codes to be 
loaded due to the infinite scrolling system. After scrolling to the bottom, it calls 
find_promo.

**Parameters**  
self : self

### Find Promo Function

```
find_promo(self, start_length)
```

**Description**  
The find promo function takes an input of starting length, which it uses to determine what
elements to save. This function is what allows the bot to save data as well as search through the 
promos at the same time.

**Parameters**  
self : self
start_length : This determines what elements will be saved to the `data.csv` file

### Manipulate String Function

```
manipulate_string(self, string)
```

**Description**  
This function will manipulate the given string and return a string with just the data we needed

** Parameters**
self : self
string : string for manipulation

**Returns**  
returnString : The manipulated string that the bot needs

## Running

The bot will begin by attempting to visit the URL listed in the config file.
The bot then gets redirected to the login screen where it will  automatically log the user in.
After this it sleeps for 10 seconds, checks the upcoming checkbox and begins scrolling
Scrolling will continue until the bot finds the bottom of the infinite scrolling element. While
scrolling, the bot saves every 10 items (how many load per scroll refresh) to the `data.csv` file.

### Scrolling

Scrolling works by comparing the source code of the current and previous page every 1 second
If the code determines that the previous and current source code are different, it scrolls down 
and resets a timer. Once this timer hits the infiniteScrollTimeout listed in the Config.py file,
the program moves onto getting the individual codes from the webpage.

### Code finding

We can determine all of the codes listed while scrolling is occuring. The bot searches for specific
elements that contains the information that we need. We then manipulate this information into 
what we are looking for such as company name, discount code, discount amount, etc.

### Data Saving
After the bot finds the data and manipulates it, the bot then saves the data to a `data.csv` file
inside of the Code Finding loop, allowing us to keep all data in the event of the code
prematurely exiting.

Example

```csv
Company Name,Discount Percentage,End Date,Promo Code,Link

VR EMPIRE,10.0%,3/3,109CCMQB,https://www.amazon.com/promocode/*Removed for Github*

VR EMPIRE,10.0%,3/3,10Y5NAAY,https://www.amazon.com/promocode/*Removed for Github*

VR EMPIRE,10.0%,3/3,107UNQZ8,https://www.amazon.com/promocode/*Removed for Github*
```

## Results
After around 4 hours of autonomous use and slow internet, which I eventually was disconnected from,
the bot stored 1097KB of data, or 14270 Data Points, which included company name, discount percentages,
end date, discount code and product link

## Contact Information
Joseph D Cantrell
JosephCantrell@josephdcantrell.com
