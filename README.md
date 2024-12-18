# Amazon Best Sellers Scraper

## Description
This Python project uses Selenium to scrape the Amazon Best Sellers section for detailed product information. The scraper extracts information for the top 1500 products in selected categories and saves the data in JSON format.

## Features
- Authenticates with Amazon using user credentials.
- Filters products with discounts greater than 50%.
- Scrapes product details: name, price, discount, rating, images, and more.
- Saves structured data into a JSON file.

## Setup Instructions

### Prerequisites
1. Python 3.7 or higher
2. Chrome browser installed
3. ChromeDriver (ensure compatibility with your Chrome version)
4. Selenium library installed (`pip install selenium`)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/amazon-scraper.git
   cd amazon-scraper
