from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException,ElementClickInterceptedException,NoSuchElementException
import time
import pandas as pd

genres = [
    "action", "adventure", "animation", "biography", "comedy",
    "crime", "documentary", "drama", "family", "fantasy",
    "film_noir", "history", "horror", "music", "musical",
    "mystery", "romance", "sci_fi", "sport", "thriller",
    "war", "western"
]

path = 'C:/Users/kiranRaj/Downloads/driver/chromedriver-win64/chromedriver.exe'

service = Service(executable_path=path)

# (Optional) Set up options
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

# Disable images and stylesheets for faster loading
options.add_experimental_option("prefs", {
    "profile.managed_default_content_settings.images": 2,
    "profile.managed_default_content_settings.stylesheet": 2
})

# Initialize driver with service and options
driver = webdriver.Chrome(service=service, options=options)
def scrape_imdb_movies_by_genre(genre):
    url = f'https://www.imdb.com/search/title/?year=2024&title_type=feature&genres={genre}'
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    load_attempts = 0
    max_load_attempts = 130  # Prevent infinite loops
    while load_attempts < max_load_attempts:
     try:
        # Find the span
        load_more_span = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'span.ipc-see-more__text'))
        )

        # Scroll into view
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", load_more_span)

        # Click using JavaScript
        driver.execute_script("arguments[0].click();", load_more_span)
        
        print("Clicked 'Load More'")
        time.sleep(2)  # Wait for new content to load

     except Exception as e:
        print("Done loading or error:", e)
        break
    
    #Scroll to load all movies (adjust based on page structure)
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    
    # Extract movie elements
    movie_elements = driver.find_elements(By.CSS_SELECTOR, ".ipc-metadata-list-summary-item")

    print(f"Found {len(movie_elements)} movie elements on the page")
    
    movies_data = []
    
    for movie in movie_elements:
        name_element = movie.find_element(By.CSS_SELECTOR, "h3").text.split('. ', 1)[1]

        try:
              rating_element = movie.find_element(By.CSS_SELECTOR, "span.ipc-rating-star--imdb")
              rating_text = rating_element.get_attribute("aria-label")
              if rating_text:
                 imdb_rating = rating_text.split(":")[1].strip().split()[0]
        except (NoSuchElementException, IndexError, ValueError, AttributeError):
               continue
               
        try:
            vote_count = movie.find_element(By.CSS_SELECTOR, "span.ipc-rating-star--voteCount").text.replace('(', '').replace(')', '')
        except NoSuchElementException:
               continue

        try:
             time_duration = movie.find_elements(By.CSS_SELECTOR, "span.sc-5179a348-7.idrYgr.dli-title-metadata-item")[1].text.strip()
        except (NoSuchElementException, IndexError):
               continue
        movies_data.append({
                    "Name": name_element,
                    "Rating": imdb_rating,
                    "Votes": vote_count,
                    "Duration": time_duration,
                    "Genre": genre.capitalize()
                })
            

    df = pd.DataFrame(movies_data)
    df.to_csv(f'csv_files/movies_2024_{genre}.csv', index=False)
    print(f"Saved {len(movies_data)} {genre} movies to movies_2024_{genre}.csv")
    
    return movies_data

# Scrape movies for each genre
for genre in genres:
    print(f"\n{'='*50}")
    print(f"Scraping {genre} movies...")
    print(f"{'='*50}")
    scrape_imdb_movies_by_genre(genre)
    time.sleep(2)  # Brief pause between genres

driver.quit()

