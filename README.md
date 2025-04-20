# Musical Instrument Retailer - Used Gear Scraper

This is a Python-based web scraper that collects product listings from a popular musical instrument retailer's website. It allows users to interactively select a product category and the number of pages to scrape, then outputs detailed product information to a CSV file.

## Features

- Category selection (e.g., Guitars, Drums, Keyboards, etc.)
- User-defined number of pages to scrape
- Extracts the following fields:
  - **Product Name**
  - **Product Price**
  - **Store Location**
  - **Condition**
  - **Product Image URL**
- Saves results as a `.csv` file in the `output` folder

## Requirements

Install required libraries with:

```bash
pip install -r requirements.txt
```

requirements.txt includes:
  - **requests**
  - **beautifulsoup4**
  - **lxml**
  - **pandas**
  - **fake-useragent**

## How to Use

  - **Clone or download this repository.**
  - **Choose a category by entering the corresponding letter.**
  - **Enter how many pages you want to scrape.**
  - **After scraping, the data will be saved in the output/ directory as a timestamped .csv file.**

## Output Example
A sample row in the output CSV:


|       Title       |       Price       |       Store       |     Condition     |              Image             |
|-------------------|-------------------|-------------------|-------------------|--------------------------------|
| Used Fender Strat	|       $599	      |    Portland, OR   |	      Great       |          /image/...jpg         |


## Notes
Be respectful with your scraping. The script includes randomized delays to avoid hammering the site with requests.
This scraper is intended for educational and personal use.