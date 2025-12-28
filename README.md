# Selenium Web Scraping Template

This is a Python template for web scraping using Selenium, BeautifulSoup4, numpy, and time. Stop writing the same boilerplate code every time you need to scrape a website!

## Features

- 🚀 **WebDriver Manager** - Automatic ChromeDriver installation and management
- 🔐 **Login Function** - Authenticate and maintain sessions for scraping protected pages
- 👻 **Headless Mode** - Run browser in headless mode or with GUI
- ⚙️ **Configurable Options** - Standard driver options (window size, user agent, etc.)
- 🍲 **BeautifulSoup4 Integration** - Easy HTML parsing and data extraction
- 📊 **NumPy Support** - Data processing and analysis capabilities
- ⏱️ **Smart Timing** - Random wait times to avoid detection
- 🔄 **Context Manager** - Automatic resource cleanup

## Installation

1. Clone this repository:
```bash
git clone https://github.com/mp97dev/selenium-webscraping-template.git
cd selenium-webscraping-template
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

### Basic Usage

```python
from scraper import WebScraper

# Use context manager for automatic cleanup
with WebScraper(headless=True) as scraper:
    # Scrape a page
    soup = scraper.scrape_page("https://example.com")
    
    # Extract data using CSS selectors
    titles = scraper.extract_data(soup, "h1")
    paragraphs = scraper.extract_data(soup, "p")
    
    # Process data with numpy
    data_array = scraper.process_data_with_numpy(paragraphs)
    
    # Wait randomly to avoid detection
    scraper.wait_random(1, 3)
```

### Scraping with Login

```python
from scraper import WebScraper

scraper = WebScraper(headless=False)
scraper.start()

# Login to website
success = scraper.login(
    url="https://example.com/login",
    username="your_username",
    password="your_password",
    username_field="username",
    password_field="password",
    success_indicator="//div[@id='dashboard']"
)

if success:
    # Scrape protected pages
    soup = scraper.scrape_page("https://example.com/protected")
    data = scraper.extract_data(soup, "div.content")

scraper.close()
```

## API Reference

### WebScraper Class

#### `__init__(headless=True, window_size="1920,1080")`
Initialize the web scraper.

**Parameters:**
- `headless` (bool): Run browser in headless mode (default: True)
- `window_size` (str): Browser window size as "width,height" (default: "1920,1080")

#### `start()`
Start the WebDriver.

#### `login(url, username, password, username_field="username", password_field="password", submit_button="//button[@type='submit']", success_indicator=None)`
Log in to a website and maintain the session.

**Parameters:**
- `url` (str): Login page URL
- `username` (str): Username for authentication
- `password` (str): Password for authentication
- `username_field` (str): Name of username input field
- `password_field` (str): Name of password input field
- `submit_button` (str): XPath of submit button
- `success_indicator` (str, optional): XPath of element indicating successful login

**Returns:** `bool` - True if login successful

#### `scrape_page(url=None, wait_time=2.0)`
Scrape a page and return BeautifulSoup object.

**Parameters:**
- `url` (str, optional): URL to scrape (if None, uses current page)
- `wait_time` (float): Time to wait for page load (default: 2.0)

**Returns:** `BeautifulSoup` - Parsed HTML

#### `extract_data(soup, selector, attribute=None)`
Extract data from parsed HTML using CSS selectors.

**Parameters:**
- `soup` (BeautifulSoup): BeautifulSoup object
- `selector` (str): CSS selector to find elements
- `attribute` (str, optional): Attribute to extract (if None, extracts text)

**Returns:** `List[str]` - Extracted data

#### `process_data_with_numpy(data)`
Process data using numpy.

**Parameters:**
- `data` (List[str]): List of data to process

**Returns:** `np.ndarray` - Numpy array with processed data

#### `wait_random(min_seconds=1.0, max_seconds=3.0)`
Wait for a random amount of time.

**Parameters:**
- `min_seconds` (float): Minimum wait time (default: 1.0)
- `max_seconds` (float): Maximum wait time (default: 3.0)

#### `close()`
Close the WebDriver and clean up resources.

## Examples

See `example.py` for more detailed usage examples:

```bash
python example.py
```

Or run the main scraper module:

```bash
python scraper.py
```

## Requirements

- Python 3.7+
- selenium >= 4.15.0
- beautifulsoup4 >= 4.12.0
- numpy >= 1.24.0
- webdriver-manager >= 4.0.0
- lxml >= 4.9.0

## License

This is a template repository - feel free to use it however you like!

## Contributing

This is a personal template, but feel free to fork and customize it for your needs.

## Tips

- Always use `wait_random()` between requests to avoid getting blocked
- Use CSS selectors with `extract_data()` for flexible element selection
- The login function maintains the session, so you can scrape multiple pages after authentication
- Set `headless=False` during development to see what the browser is doing
- Use the context manager (`with WebScraper() as scraper:`) for automatic cleanup

## Troubleshooting

**Issue: ChromeDriver not found**
- The template uses webdriver-manager which automatically downloads the correct driver
- Make sure you have Chrome/Chromium installed

**Issue: Login not working**
- Inspect the login page to find correct field names and button XPath
- Try setting `headless=False` to see what's happening
- Add a longer wait time or adjust the `success_indicator`

**Issue: Elements not found**
- Wait for page to load completely before extraction
- Use browser DevTools to verify CSS selectors
- Try increasing `wait_time` in `scrape_page()`
