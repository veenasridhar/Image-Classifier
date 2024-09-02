import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from selenium import webdriver
import time

#%%
# Define the list of food items
#food_items = ['sambar', 'rasam', 'curd rice', 'vatha kuzhambu', 'poha', 'biriyani', 'lassi', 'paneer butter masala', 'gobi manchurian']
food_items = ['Erling haaland']

# Specify the number of images you want to download per food item
num_images_per_item = 100

#%%
root_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
print(root_dir)

# Create the save directory if it doesn't exist
SAVE_DIR = os.path.join(root_dir, 'raw_data')
print(SAVE_DIR)

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

#%%
# Initialize Chrome WebDriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode (without GUI)
driver = webdriver.Chrome(options=chrome_options)

#%%
# Search and download images for each food item
for food_item in food_items:
    search_url = f"https://www.google.com/search?sca_esv=ab2746a6ddac7fed&sca_upv=1&q=erling+haaland+images&udm=2&fbs=AEQNm0Aa4sjWe7Rqy32pFwRj0UkWd8nbOJfsBGGB5IQQO6L3J_86uWOeqwdnV0yaSF-x2joQcoZ-0Q2Udkt2zEybT7HdNV1kobqvEwEVRYBCltlBtQd5-pPeakpVgpgEn2RgmgzeZo15rltNMrDtoZe63sl46hHJXZmfPBeZdqdwrtlSxkvce3I&sa=X&ved=2ahUKEwjJt--D35-IAxW50gIHHdQaIn0QtKgLegQIERAB&biw=1280&bih=598&dpr=1.5"

    driver.get(search_url)

    

    # Create a subdirectory for each food item
    item_save_dir = os.path.join(SAVE_DIR, food_item)
    if not os.path.exists(item_save_dir):
        os.makedirs(item_save_dir)

    # Download and save images
    image_count = 0
    while image_count < num_images_per_item:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        response = requests.get(search_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        # Download and save images from the current page
        for img in soup.find_all('img'):
            image_url = img.get('src')
            if image_url:
                # Convert relative URLs to absolute URLs
                if image_url.startswith('//'):
                    image_url = 'http:' + image_url
                elif not image_url.startswith(('http:', 'https:')):
                    continue  # Skip if the URL is not valid

            if image_url and image_url.startswith('http'):
                image_filename = "image"+str(image_count)+".jpg"  # Get the filename from the URL
                image_data = requests.get(image_url)
                if image_data.status_code == 200:
                    with open(os.path.join(item_save_dir, image_filename), 'wb') as f:
                        f.write(image_data.content)
                    image_count += 1
                    print(f'Downloaded: image : {image_filename} count : {image_count}')

        if image_count >= num_images_per_item:
            break


        # Scroll down to load more images
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Give time for images to load

# Close the WebDriver
driver.quit()

print('Image downloading completed.')
