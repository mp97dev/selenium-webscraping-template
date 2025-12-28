"""
Selenium Web Scraping Template
A template for web scraping using Selenium, BeautifulSoup4, numpy, and time.

Features:
- WebDriver Manager for automatic driver management
- Standard driver options (headless mode, window size, etc.)
- Login function to authenticate and maintain session
- BeautifulSoup4 integration for HTML parsing
- Example usage of numpy and time modules
"""

import time
from typing import Optional, Dict, List
import numpy as np

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup


class WebScraper:
    """
    A web scraping template class that handles authentication and data extraction.
    """
    
    def __init__(self, headless: bool = True, window_size: str = "1920,1080"):
        """
        Initialize the web scraper with Selenium WebDriver.
        
        Args:
            headless: Whether to run browser in headless mode (default: True)
            window_size: Browser window size as "width,height" (default: "1920,1080")
        """
        self.driver = None
        self.headless = headless
        self.window_size = window_size
        self.session_active = False
        
    def _setup_driver(self) -> webdriver.Chrome:
        """
        Set up Chrome WebDriver with standard options and WebDriver Manager.
        
        Returns:
            Configured Chrome WebDriver instance
        """
        # Configure Chrome options
        chrome_options = ChromeOptions()
        
        if self.headless:
            chrome_options.add_argument('--headless')
        
        chrome_options.add_argument(f'--window-size={self.window_size}')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Add user agent to avoid detection
        # Using a recent Chrome version for better compatibility
        chrome_options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        )
        
        # Use WebDriver Manager to automatically handle ChromeDriver installation
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        return driver
    
    def start(self) -> None:
        """
        Start the web scraper by initializing the WebDriver.
        """
        if self.driver is None:
            self.driver = self._setup_driver()
            print("WebDriver initialized successfully")
    
    def login(self, url: str, username: str, password: str, 
              username_field: str = "username", password_field: str = "password",
              submit_button: str = "//button[@type='submit']",
              success_indicator: Optional[str] = None) -> bool:
        """
        Log in to a website and maintain the session.
        
        Args:
            url: Login page URL
            username: Username for authentication
            password: Password for authentication
            username_field: ID or name of username input field (default: "username")
            password_field: ID or name of password input field (default: "password")
            submit_button: XPath of submit button (default: "//button[@type='submit']")
            success_indicator: XPath of element that indicates successful login (optional)
        
        Returns:
            True if login successful, False otherwise
        """
        if self.driver is None:
            self.start()
        
        try:
            print(f"Navigating to login page: {url}")
            self.driver.get(url)
            
            # Wait for page to load
            time.sleep(2)
            
            # Find and fill username field
            print("Filling in credentials...")
            username_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, username_field))
            )
            username_input.clear()
            username_input.send_keys(username)
            
            # Find and fill password field
            password_input = self.driver.find_element(By.NAME, password_field)
            password_input.clear()
            password_input.send_keys(password)
            
            # Click submit button
            print("Submitting login form...")
            submit_btn = self.driver.find_element(By.XPATH, submit_button)
            submit_btn.click()
            
            # Wait for navigation after login
            time.sleep(3)
            
            # Check if login was successful
            if success_indicator:
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, success_indicator))
                    )
                    print("Login successful!")
                    self.session_active = True
                    return True
                except TimeoutException:
                    print("Login failed: success indicator not found")
                    return False
            else:
                # If no success indicator provided, assume success if no error
                print("Login completed (no success indicator to verify)")
                self.session_active = True
                return True
                
        except Exception as e:
            print(f"Login failed with error: {str(e)}")
            return False
    
    def scrape_page(self, url: Optional[str] = None, 
                    wait_time: float = 2.0) -> BeautifulSoup:
        """
        Scrape a page and return BeautifulSoup object for parsing.
        
        Args:
            url: URL to scrape (if None, uses current page)
            wait_time: Time to wait for page to load in seconds (default: 2.0)
        
        Returns:
            BeautifulSoup object containing parsed HTML
        """
        if self.driver is None:
            self.start()
        
        if url:
            print(f"Navigating to: {url}")
            self.driver.get(url)
        
        # Wait for page to load
        time.sleep(wait_time)
        
        # Get page source and parse with BeautifulSoup
        # Using lxml parser for better performance; falls back to html.parser if unavailable
        page_source = self.driver.page_source
        try:
            soup = BeautifulSoup(page_source, 'lxml')
        except Exception:
            soup = BeautifulSoup(page_source, 'html.parser')
        
        return soup
    
    def extract_data(self, soup: BeautifulSoup, selector: str, 
                    attribute: Optional[str] = None) -> List[str]:
        """
        Extract data from parsed HTML using CSS selectors.
        
        Args:
            soup: BeautifulSoup object
            selector: CSS selector to find elements
            attribute: Attribute to extract (if None, extracts text)
        
        Returns:
            List of extracted data
        """
        elements = soup.select(selector)
        
        if attribute:
            data = [elem.get(attribute, '') for elem in elements]
        else:
            data = [elem.get_text(strip=True) for elem in elements]
        
        print(f"Extracted {len(data)} items using selector '{selector}'")
        return data
    
    def process_data_with_numpy(self, data: List[str]) -> np.ndarray:
        """
        Example function demonstrating numpy usage for data processing.
        
        Args:
            data: List of data to process
        
        Returns:
            Numpy array with processed data
        """
        # Convert to numpy array
        arr = np.array(data)
        
        # Example: Get unique values
        unique_values = np.unique(arr)
        print(f"Found {len(unique_values)} unique values out of {len(arr)} total items")
        
        return arr
    
    def wait_random(self, min_seconds: float = 1.0, max_seconds: float = 3.0) -> None:
        """
        Wait for a random amount of time to avoid detection.
        
        Args:
            min_seconds: Minimum wait time (default: 1.0)
            max_seconds: Maximum wait time (default: 3.0)
        """
        wait_time = np.random.uniform(min_seconds, max_seconds)
        print(f"Waiting for {wait_time:.2f} seconds...")
        time.sleep(wait_time)
    
    def close(self) -> None:
        """
        Close the WebDriver and clean up resources.
        """
        if self.driver:
            print("Closing WebDriver...")
            self.driver.quit()
            self.driver = None
            self.session_active = False
    
    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


def main():
    """
    Example usage of the WebScraper template.
    """
    # Example 1: Basic scraping without login
    print("=" * 50)
    print("Example 1: Basic Web Scraping")
    print("=" * 50)
    
    with WebScraper(headless=True) as scraper:
        # Scrape a page
        soup = scraper.scrape_page("https://example.com")
        
        # Extract some data (example: all paragraph text)
        paragraphs = scraper.extract_data(soup, "p")
        print(f"\nExtracted {len(paragraphs)} paragraphs")
        
        # Process data with numpy
        if paragraphs:
            arr = scraper.process_data_with_numpy(paragraphs)
            print(f"Data array shape: {arr.shape}")
        
        # Random wait
        scraper.wait_random(1, 2)
    
    # Example 2: Scraping with login (commented out - requires actual credentials)
    """
    print("\n" + "=" * 50)
    print("Example 2: Web Scraping with Login")
    print("=" * 50)
    
    scraper = WebScraper(headless=False)
    scraper.start()
    
    # Login to website
    login_success = scraper.login(
        url="https://example.com/login",
        username="your_username",
        password="your_password",
        username_field="username",
        password_field="password",
        success_indicator="//div[@id='dashboard']"  # Element present after successful login
    )
    
    if login_success:
        # Now you can scrape pages that require authentication
        soup = scraper.scrape_page("https://example.com/protected-page")
        
        # Extract and process data
        data = scraper.extract_data(soup, "div.content")
        
        # Do something with the data
        for item in data[:5]:  # Print first 5 items
            print(f"- {item}")
    
    scraper.close()
    """


if __name__ == "__main__":
    main()
