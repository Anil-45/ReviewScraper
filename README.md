# ReviewScraper
Scrape the product reviews and store them in a database.

## Table of Contents
* [General Info](#general-information)
* [Features](#features)
* [Screenshots](#screenshots)
* [Setup](#setup)
* [Usage](#usage)
* [Room for Improvement](#room-for-improvement)
* [Contact](#contact)
* [License](#license)


## General Information
- This project scrapes the reviews of the products from Flipkart and stores them in a database to avoid scraping for the same product at a later point in time.


## Features
- Provides user interface 
- Interactive graphical representation of ratings


## Screenshots
![Example screenshot](./screenshots/2.PNG)


## Setup
Clone this repo using
```sh
git clone https://github.com/Anil-45/ReviewScraper.git
```

Install the required modules using
```sh
pip install -r Requirements.txt
```


## Usage
To use SQL database, generate a config file using `generate_config.py`.

Open `generate_config.py` and edit host, username and password.
```sh
config_file.set(DATABASE, HOST, "127.0.0.1")
config_file.set(DATABASE, USERNAME, "root")
config_file.set(DATABASE, PASSWORD, "root")
```
Once you are done editing, run:
```bash
python generate_config.py
```
Alternatively, you can also edit `config.ini`. 

You can run the project without a database also, but the results for the products will always be scraped.

Run the app:

```bash
python app.py
```

Open [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

You can find all the logs in `.log` files

## Room for Improvement
- Add support for different databases.


## Contact
Created by [@Anil_Reddy](https://github.com/Anil-45/) 

## License
This project is available under the [MIT](https://github.com/Anil-45/ReviewScraper/blob/main/LICENSE).
