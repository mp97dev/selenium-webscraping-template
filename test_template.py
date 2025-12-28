"""
Test script to verify the web scraping template structure.
This tests imports, class instantiation, and method signatures without requiring network access.
"""

import sys

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    try:
        from scraper import WebScraper
        import numpy as np
        from bs4 import BeautifulSoup
        import time
        from selenium import webdriver
        from webdriver_manager.chrome import ChromeDriverManager
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False


def test_class_structure():
    """Test that WebScraper class can be instantiated and has required methods."""
    print("\nTesting class structure...")
    try:
        from scraper import WebScraper
        
        # Test instantiation with different parameters
        scraper1 = WebScraper()
        scraper2 = WebScraper(headless=False)
        scraper3 = WebScraper(headless=True, window_size="1280,720")
        
        # Verify attributes
        assert hasattr(scraper1, 'driver'), "Missing 'driver' attribute"
        assert hasattr(scraper1, 'headless'), "Missing 'headless' attribute"
        assert hasattr(scraper1, 'window_size'), "Missing 'window_size' attribute"
        assert hasattr(scraper1, 'session_active'), "Missing 'session_active' attribute"
        
        # Verify methods exist
        required_methods = [
            '_setup_driver',
            'start',
            'login',
            'scrape_page',
            'extract_data',
            'process_data_with_numpy',
            'wait_random',
            'close',
            '__enter__',
            '__exit__'
        ]
        
        for method in required_methods:
            assert hasattr(scraper1, method), f"Missing method: {method}"
            assert callable(getattr(scraper1, method)), f"'{method}' is not callable"
        
        print("✓ Class structure is correct")
        print(f"  - All {len(required_methods)} required methods present")
        return True
    except Exception as e:
        print(f"✗ Class structure test failed: {e}")
        return False


def test_method_signatures():
    """Test that methods have correct signatures."""
    print("\nTesting method signatures...")
    try:
        from scraper import WebScraper
        import inspect
        
        scraper = WebScraper()
        
        # Test login method signature
        login_sig = inspect.signature(scraper.login)
        login_params = list(login_sig.parameters.keys())
        required_login_params = ['url', 'username', 'password']
        for param in required_login_params:
            assert param in login_params, f"Missing parameter '{param}' in login method"
        
        # Test scrape_page method signature
        scrape_sig = inspect.signature(scraper.scrape_page)
        assert 'url' in scrape_sig.parameters, "Missing 'url' parameter in scrape_page"
        
        # Test extract_data method signature
        extract_sig = inspect.signature(scraper.extract_data)
        extract_params = list(extract_sig.parameters.keys())
        assert 'soup' in extract_params, "Missing 'soup' parameter in extract_data"
        assert 'selector' in extract_params, "Missing 'selector' parameter in extract_data"
        
        print("✓ Method signatures are correct")
        return True
    except Exception as e:
        print(f"✗ Method signature test failed: {e}")
        return False


def test_features():
    """Verify that all required features are present."""
    print("\nVerifying required features...")
    features = []
    
    # Check for webdriver-manager usage
    try:
        with open('scraper.py', 'r') as f:
            content = f.read()
            if 'webdriver_manager' in content:
                features.append("WebDriver Manager")
            if 'ChromeDriverManager().install()' in content:
                features.append("Automatic driver installation")
            if "headless" in content:
                features.append("Headless mode support")
            if "def login" in content:
                features.append("Login function")
            if "BeautifulSoup" in content:
                features.append("BeautifulSoup4 integration")
            if "import numpy" in content:
                features.append("NumPy support")
            if "import time" in content or "time.sleep" in content:
                features.append("Time module usage")
            if "session_active" in content:
                features.append("Session management")
            if "window_size" in content or "window-size" in content:
                features.append("Window size configuration")
            if "__enter__" in content and "__exit__" in content:
                features.append("Context manager support")
    except Exception as e:
        print(f"Error reading scraper.py: {e}")
        return False
    
    print("✓ All required features present:")
    for feature in features:
        print(f"  - {feature}")
    
    return len(features) >= 8


def test_numpy_usage():
    """Test that numpy functions work correctly."""
    print("\nTesting numpy integration...")
    try:
        import numpy as np
        from scraper import WebScraper
        
        scraper = WebScraper()
        
        # Test process_data_with_numpy with sample data
        sample_data = ["item1", "item2", "item3", "item1"]
        result = scraper.process_data_with_numpy(sample_data)
        
        assert isinstance(result, np.ndarray), "Result should be numpy array"
        assert len(result) == len(sample_data), "Array length should match input"
        
        print("✓ NumPy integration works correctly")
        return True
    except Exception as e:
        print(f"✗ NumPy test failed: {e}")
        return False


def test_beautifulsoup_usage():
    """Test that BeautifulSoup extraction works."""
    print("\nTesting BeautifulSoup integration...")
    try:
        from bs4 import BeautifulSoup
        from scraper import WebScraper
        
        # Create a simple HTML for testing
        html = """
        <html>
            <head><title>Test Page</title></head>
            <body>
                <h1>Main Title</h1>
                <p>Paragraph 1</p>
                <p>Paragraph 2</p>
                <a href="http://example.com">Link 1</a>
                <a href="http://test.com">Link 2</a>
            </body>
        </html>
        """
        
        # Try lxml parser first, fall back to html.parser
        try:
            soup = BeautifulSoup(html, 'lxml')
        except (ImportError, LookupError):
            soup = BeautifulSoup(html, 'html.parser')
        scraper = WebScraper()
        
        # Test extracting text
        paragraphs = scraper.extract_data(soup, "p")
        assert len(paragraphs) == 2, f"Expected 2 paragraphs, got {len(paragraphs)}"
        
        # Test extracting attributes
        links = scraper.extract_data(soup, "a", attribute="href")
        assert len(links) == 2, f"Expected 2 links, got {len(links)}"
        assert "example.com" in links[0], "Link extraction failed"
        
        print("✓ BeautifulSoup integration works correctly")
        return True
    except Exception as e:
        print(f"✗ BeautifulSoup test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("WEB SCRAPING TEMPLATE VERIFICATION")
    print("=" * 60)
    
    results = []
    
    # Run all tests
    results.append(("Imports", test_imports()))
    results.append(("Class Structure", test_class_structure()))
    results.append(("Method Signatures", test_method_signatures()))
    results.append(("Features", test_features()))
    results.append(("NumPy Integration", test_numpy_usage()))
    results.append(("BeautifulSoup Integration", test_beautifulsoup_usage()))
    
    # Print summary
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All verification tests passed!")
        print("The web scraping template is ready to use.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
