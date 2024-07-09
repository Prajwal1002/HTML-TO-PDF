import os
import time
import pdfkit
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Paths to Chrome and chromedriver
chromedriver_path = 'C:/Users/Admin/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe'
chrome_binary_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe'

# URL of the HTML content you want to convert to PDF
url = 'https://trulygreensolutions.com/warranty/'

# Path where you want to save the PDF file
pdf_filename = 'Extended-Warranty.pdf'
pdf_path = os.path.join('C:/Users/Admin/Downloads', pdf_filename)

# Path to wkhtmltopdf executable
wkhtmltopdf_path = 'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'  # Change this to the actual path

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run Chrome in headless mode
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.binary_location = chrome_binary_path

# Set up Chrome service
service = Service(chromedriver_path)

# Create a new instance of the Chrome driver
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Open the web page
    driver.get(url)

    # Wait for the page to load completely (adjust sleep time as needed)
    time.sleep(5)

    # Extract specific HTML content based on CSS selectors using JavaScript
    css_selector = '#main'  # Replace with your specific CSS selector
    script = f'''
        var elements = document.querySelectorAll('{css_selector}');
        var html = '<html><head>' + document.head.innerHTML + '</head><body>';
        elements.forEach(function(element) {{
            html += element.outerHTML;
        }});
        html += '</body></html>';
        return html;
    '''
    extracted_html = driver.execute_script(script)

    # Check if HTML content is extracted
    if not extracted_html:
        raise ValueError("No HTML content extracted. Please check your CSS selectors and URL.")

    # Add a base tag to ensure resources are resolved correctly
    base_tag = f'<base href="{url}">'
    extracted_html = extracted_html.replace('<head>', f'<head>{base_tag}')

    # Write the extracted HTML content to a temporary HTML file
    temp_html_path = 'temp.html'
    with open(temp_html_path, 'w', encoding='utf-8') as file:
        file.write(extracted_html)

    # Check if the temporary HTML file exists
    if not os.path.exists(temp_html_path):
        raise FileNotFoundError("Temporary HTML file was not created successfully.")

    # Convert the temporary HTML file to PDF
    config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
    options = {'enable-local-file-access': ''}
    pdfkit.from_file(temp_html_path, pdf_path, configuration=config, options=options)

    print(f"PDF saved successfully at {pdf_path}")

finally:
    # Quit the driver
    driver.quit()

    # Clean up temporary files
    if os.path.exists(temp_html_path):
        os.remove(temp_html_path)
