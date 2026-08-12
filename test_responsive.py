from playwright.sync_api import sync_playwright

def test_responsive_and_cart():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        # Test Desktop
        page_desktop = browser.new_page()
        page_desktop.set_viewport_size({"width": 1280, "height": 800})
        page_desktop.goto("http://127.0.0.1:5000")
        assert "Productos" in page_desktop.title()
        print("Desktop view OK")

        # Test Mobile
        page_mobile = browser.new_page()
        page_mobile.set_viewport_size({"width": 375, "height": 667})
        page_mobile.goto("http://127.0.0.1:5000")
        print("Mobile view OK")
        
        # Test adding to cart
        page_desktop.click("text=Añadir al carrito")
        page_desktop.click("text=🛒 Ver Carrito")
        assert page_desktop.is_visible("#cartItems")
        print("Cart functionality OK")
        
        browser.close()

if __name__ == "__main__":
    print("Run the flask app first: python app.py")
    # test_responsive_and_cart() # Commented out to prevent errors if server isn't running
