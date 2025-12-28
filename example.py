"""
Example script demonstrating the web scraping template usage.

This example shows:
1. How to initialize the scraper
2. How to use the login function
3. How to extract data with BeautifulSoup
4. How to process data with numpy
5. How to use timing utilities
"""

from scraper import WebScraper
import numpy as np


def example_without_login():
    """
    Example: Scraping a public website without authentication.
    """
    print("\n" + "=" * 60)
    print("Example: Scraping without Login")
    print("=" * 60)
    
    # Use context manager for automatic cleanup
    with WebScraper(headless=True, window_size="1920,1080") as scraper:
        # Scrape the page
        soup = scraper.scrape_page("https://example.com")
        
        # Extract title
        titles = scraper.extract_data(soup, "h1")
        if titles:
            print(f"\nPage Title: {titles[0]}")
        
        # Extract all paragraph texts
        paragraphs = scraper.extract_data(soup, "p")
        print(f"Number of paragraphs: {len(paragraphs)}")
        
        # Extract links
        links = scraper.extract_data(soup, "a", attribute="href")
        print(f"Number of links: {len(links)}")
        
        # Process data with numpy
        if paragraphs:
            # Convert to numpy array
            data_array = scraper.process_data_with_numpy(paragraphs)
            
            # Calculate some statistics
            lengths = np.array([len(p) for p in paragraphs])
            print(f"\nParagraph length statistics:")
            print(f"  Mean: {np.mean(lengths):.2f}")
            print(f"  Std: {np.std(lengths):.2f}")
            print(f"  Max: {np.max(lengths)}")
            print(f"  Min: {np.min(lengths)}")
        
        # Wait before next action
        scraper.wait_random(1, 2)


def example_with_login():
    """
    Example: Scraping a website that requires login.
    
    Note: This is a template. Replace with actual website details.
    """
    print("\n" + "=" * 60)
    print("Example: Scraping with Login (Template)")
    print("=" * 60)
    print("\nThis example demonstrates the login workflow.")
    print("Replace the URL and credentials with your actual website.\n")
    
    # Initialize scraper (set headless=False to see the browser)
    scraper = WebScraper(headless=True)
    scraper.start()
    
    # Example login configuration
    # Replace these with your actual website details:
    LOGIN_URL = "https://example.com/login"
    USERNAME = "your_username"
    PASSWORD = "your_password"
    
    # Login to the website
    # Customize the field names and selectors based on your target website
    print("Attempting to log in...")
    login_success = scraper.login(
        url=LOGIN_URL,
        username=USERNAME,
        password=PASSWORD,
        username_field="username",          # HTML name attribute of username field
        password_field="password",          # HTML name attribute of password field
        submit_button="//button[@type='submit']",  # XPath to submit button
        success_indicator="//div[@class='dashboard']"  # XPath to element shown after login
    )
    
    if login_success:
        print("✓ Login successful!")
        
        # Now scrape protected pages using the authenticated session
        protected_url = "https://example.com/protected-page"
        soup = scraper.scrape_page(protected_url)
        
        # Extract data from the protected page
        data = scraper.extract_data(soup, "div.content")
        
        print(f"\nExtracted {len(data)} items from protected page")
        
        # Process multiple pages
        for page_num in range(1, 4):
            print(f"\nProcessing page {page_num}...")
            url = f"https://example.com/data?page={page_num}"
            soup = scraper.scrape_page(url)
            
            # Extract data
            items = scraper.extract_data(soup, "div.item")
            print(f"Found {len(items)} items on page {page_num}")
            
            # Wait between requests to be polite
            scraper.wait_random(2, 4)
    else:
        print("✗ Login failed!")
    
    # Clean up
    scraper.close()


def example_advanced_extraction():
    """
    Example: Advanced data extraction and numpy processing.
    """
    print("\n" + "=" * 60)
    print("Example: Advanced Data Extraction")
    print("=" * 60)
    
    with WebScraper(headless=True) as scraper:
        soup = scraper.scrape_page("https://example.com")
        
        # Extract different types of data
        all_text = scraper.extract_data(soup, "body")
        headings = scraper.extract_data(soup, "h1, h2, h3")
        links = scraper.extract_data(soup, "a", attribute="href")
        
        print(f"\nExtraction results:")
        print(f"  Headings: {len(headings)}")
        print(f"  Links: {len(links)}")
        
        # Use numpy for data analysis
        if links:
            # Filter and analyze links
            links_array = np.array(links)
            
            # Count internal vs external links (example)
            internal = np.sum(['http' not in link for link in links])
            external = len(links) - internal
            
            print(f"\nLink analysis:")
            print(f"  Internal links: {internal}")
            print(f"  External links: {external}")
        
        # Demonstrate timing with multiple operations
        import time
        start_time = time.time()
        
        # Simulate multiple operations
        for i in range(3):
            scraper.wait_random(0.5, 1.0)
        
        elapsed_time = time.time() - start_time
        print(f"\nTotal operation time: {elapsed_time:.2f} seconds")


def main():
    """
    Run all examples.
    """
    print("\n" + "=" * 60)
    print("SELENIUM WEB SCRAPING TEMPLATE - EXAMPLES")
    print("=" * 60)
    
    # Run example 1: Basic scraping
    try:
        example_without_login()
    except Exception as e:
        print(f"Example 1 error: {e}")
    
    # Run example 2: Advanced extraction
    try:
        example_advanced_extraction()
    except Exception as e:
        print(f"Example 2 error: {e}")
    
    # Note: Login example is commented out by default
    # Uncomment and configure it with your actual website details
    # example_with_login()
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
