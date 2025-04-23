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

#url = 'https://www.imdb.com/search/title/?year=2024&title_type=feature&'
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
    
    #Wait for the page to load
    # WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.CLASS_NAME, "ipc-metadata-list"))
    # )
    
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
            # Extract movie name
            #name_element = movie.find_element(By.CSS_SELECTOR, "h3").text
        name_element = movie.find_element(By.CSS_SELECTOR, "h3").text.split('. ', 1)[1]
            # print("Name element HTML:", name_element.get_attribute('outerHTML'))
            # name = name_element.text
            # print(f"Extracted name: {name}")
            #print(name_element)  
        try:
            #imdb_rating = movie.find_elements(By.CSS_SELECTOR, "span.ipc-rating-star--rating")
              rating_element = movie.find_element(By.CSS_SELECTOR, "span.ipc-rating-star--imdb")
              rating_text = rating_element.get_attribute("aria-label")
              if rating_text:
                 imdb_rating = rating_text.split(":")[1].strip().split()[0]
            # print(f"Found {len(imdb_rating)} imdb_rating")
            # for j, elem in enumerate(imdb_rating, 1):
            #     print(f"imdb_rating {j}: {elem.text}")
            #print(imdb_rating)
        except (NoSuchElementException, IndexError, ValueError, AttributeError):
               #imdb_rating = None
               continue
               
        try:
            #vote_count = movie.find_elements(By.CSS_SELECTOR, "span.ipc-rating-star--voteCount").text
            #vote_count = movie.find_element(By.CSS_SELECTOR, "span.ipc-rating-star--voteCount").text.strip('()')
            #vote_count = movie.find_element(By.CSS_SELECTOR, "span.ipc-rating-star--voteCount").text.strip('()').replace("K", "000")
             vote_count = movie.find_element(By.CSS_SELECTOR, "span.ipc-rating-star--voteCount").text.replace('(', '').replace(')', '')
            # print(f"Found {len(vote_count)} vote_count")
            # for j, elem in enumerate(vote_count, 1):
            #     print(f"vote_count {j}: {elem.text}")
            #print(vote_count)
        except NoSuchElementException:
               #vote_count = None
               continue

            # time_duration = movie.find_elements(By.CSS_SELECTOR, "span.sc-5179a348-7.idrYgr.dli-title-metadata-item")
        try:
            # # Print the first 2 duration items
            # for i, duration in enumerate(time_duration[:2], 1):
            #     if i==2:
            #       print(f"Duration {i}: {duration.text.strip()}")
            #       break
             time_duration = movie.find_elements(By.CSS_SELECTOR, "span.sc-5179a348-7.idrYgr.dli-title-metadata-item")[1].text.strip()
            #print("time:", time_duration)
            # print(f"Found {len(time_duration)} time_duration")
            # for j, elem in enumerate(time_duration, 1):
            #     print(f"time_duration {j}: {elem.text}")
        except (NoSuchElementException, IndexError):
               #time_duration = None
               continue
        movies_data.append({
                    "Name": name_element,
                    "Rating": imdb_rating,
                    "Votes": vote_count,
                    "Duration": time_duration,
                    "Genre": genre.capitalize()
                })
            

            
            
            # Extract metadata (genre, duration, etc.)
            #metadata_elements = movie.find_elements(By.CSS_SELECTOR, ".ipc-metadata-list-summary-item__li")
            # metadata_elements = movie.find_elements(By.CSS_SELECTOR, ".ipc-inline-list__item")
            # print(f"Found {len(metadata_elements)} metadata elements")
            # for j, elem in enumerate(metadata_elements, 1):
            #     print(f"Metadata element {j}: {elem.text}")
            
            # Extract rating and votes
            # rating_element = movie.find_element(By.CSS_SELECTOR, "span.ipc-rating-star--imdb")
            # print("Rating element HTML:", rating_element.get_attribute('outerHTML'))
    #         rating = rating_element.text if rating_element else "N/A"
            
    #         votes_element = movie.find_element(By.CSS_SELECTOR, "[aria-label='IMDb rating'] + span")
    #         votes = votes_element.text if votes_element else "N/A"
            
    #         # Process metadata to extract genre and duration
    #         genres = []
    #         duration = "N/A"
            
    #         for item in metadata:
    #             text = item.text
    #             if "h" in text or "m" in text:  # Assuming duration contains h or m
    #                 duration = text
    #             else:
    #                 genres.extend([g.strip() for g in text.split(",")])
            
    #         movies_data.append({
    #             "Movie Name": name,
    #             "Genre": genres,
    #             "Ratings": rating,
    #             "Voting Counts": votes,
    #             "Duration": duration
    #         })
        
            
        # except Exception as e:
        #     print(f"Error processing a movie: {e}")
        #     continue
    #top_movies = sorted(movies_data, key=lambda x: x["Rating"], reverse=True)
    #print(top_movies)

    # print("\nTop 10 Highest Rated Movies:")
    # print("-" * 60)
    # print(f"{'No.':<4}{'Movie Name':<40}{'Rating':<8}{'Votes':<12}{'Duration':<10}")
    # print("-" * 60)
    # for i, movie in enumerate(top_movies, 1):
    #     print(f"{i:<4}{movie['Name'][:37]:<40}{movie['Rating']:<8}{movie['Votes']:<12}{movie['Duration']:<10}")
 
    df = pd.DataFrame(movies_data)
    df.to_csv(f'csv_files/movies_2024_{genre}.csv', index=False)
    print(f"Saved {len(movies_data)} {genre} movies to movies_2024_{genre}.csv")
    
    # return movies_data
    return movies_data

# Scrape movies for each genre
for genre in genres:
    print(f"\n{'='*50}")
    print(f"Scraping {genre} movies...")
    print(f"{'='*50}")
    scrape_imdb_movies_by_genre(genre)
    time.sleep(2)  # Brief pause between genres

driver.quit()
#movies_data = scrape_imdb_movies(url)

# Find all movie blocks
# movie_blocks = driver.find_elements(By.CSS_SELECTOR, "div.lister-item.mode-advanced")


# driver = webdriver.Chrome(path)

# driver.get(website)

