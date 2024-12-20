# Ankur Lighting Web Scraper

## Overview
This repository contains a Python-based web scraper designed to extract product information from the Ankur Lighting website. The scraper uses BeautifulSoup and Requests to fetch and parse HTML content, collecting detailed data on various lighting products across multiple categories. The extracted data is saved in a CSV file for further analysis or use.

## Features
- Scrapes product information from multiple categories, including chandeliers, table lamps, and wall lights.
- Supports pagination to ensure all pages in a category are processed.
- Extracts detailed product specifications such as dimensions, material, and power consumption.
- Includes retry logic to handle temporary network issues.
- Saves the scraped data in a structured CSV file for easy analysis.

## Prerequisites

### Python Libraries
Install the required libraries before running the scraper:

```bash
pip install requests beautifulsoup4 pandas
```

### System Requirements
- Python 3.7 or later
- Stable internet connection

## How It Works

1. **Category URL Generation**:
   The script generates URLs for all pages in a given product category using pagination logic.

2. **Data Fetching**:
   - The `make_request` function performs HTTP GET requests with retry logic to handle transient errors.
   - BeautifulSoup is used to parse the HTML content.

3. **Data Extraction**:
   - Product details such as title, price, and image URL are extracted using CSS selectors.
   - Additional specifications are fetched from product detail pages.

4. **Data Storage**:
   - All collected data is stored in a dictionary, which is converted into a Pandas DataFrame.
   - The final dataset is saved as a CSV file (`ankur_lighting_data.csv`).

## File Structure

- **main.py**: The primary script containing the scraping logic.
- **ankurL2.csv**: The output file containing the scraped data (generated after running the script).

## How to Use

1. Clone this repository:

   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the scraper:

   ```bash
   python main.py
   ```

4. View the results in the generated `ankur_lighting_data.csv` file.

## Data Fields

The output CSV file contains the following fields:

- `category`: The product category (e.g., chandeliers, table lamps).
- `title`: The product title.
- `price`: The product price.
- `img_url`: The URL of the product image.
- Additional fields may include detailed specifications such as dimensions, material, and power consumption.

## Error Handling
- Implements retry logic with exponential backoff for network issues.
- Skips products or pages that fail to load after retries.

## Contributing
Contributions to improve the scraper or extend its functionality are welcome. Feel free to submit a pull request or open an issue.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For questions or support, please contact:
- Email: [sandali.kishore08@gmail.com]
- GitHub: [sandaliikishore]

