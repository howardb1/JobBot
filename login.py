import time
import json
import os
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options 


# Load config file for location-specific resumes
with open('config.json') as f:
    CONFIG = json.load(f)

# Initialize Selenium WebDriver
def init_driver():
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    return driver

# Get resume path based on location
def get_resume_by_location(location):
    return CONFIG.get(location, CONFIG["default"])

# Log applied jobs
def log_job(title, company, location):
    with open("logs/applied_jobs.csv", mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([title, company, location, time.strftime("%Y-%m-%d %H:%M:%S")])

# Log in to LinkedIn
def linkedin_login(driver, email, password):
    driver.get("https://www.linkedin.com/login")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(email)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(5)

# Search jobs with keywords and location
def search_jobs(driver, title, location):
    driver.get("https://www.linkedin.com/jobs")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.jobs-search-box__text-input")))
    search_boxes = driver.find_elements(By.CSS_SELECTOR, "input.jobs-search-box__text-input")
    search_boxes[0].send_keys(title)
    search_boxes[3].clear()
    search_boxes[3].send_keys(location)
    driver.find_element(By.CSS_SELECTOR, "button.jobs-search-box__submit-button").click()
    time.sleep(5)

# Easy Apply to jobs
def easy_apply(driver, resume_path):
    job_cards = driver.find_elements(By.CLASS_NAME, "job-card-container")
    for job in job_cards:
        try:
            job.click()
            time.sleep(3)
            easy_apply_button = driver.find_element(By.CLASS_NAME, "jobs-apply-button")
            easy_apply_button.click()
            time.sleep(2)

            upload_input = driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
            upload_input.send_keys(os.path.abspath(resume_path))
            time.sleep(2)

            submit_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Submit application']")
            submit_button.click()
            time.sleep(2)

            # Log success
            title = driver.find_element(By.CLASS_NAME, "job-details-jobs-unified-top-card__job-title").text
            company = driver.find_element(By.CLASS_NAME, "job-details-jobs-unified-top-card__company-name").text
            location = driver.find_element(By.CLASS_NAME, "job-details-jobs-unified-top-card__bullet").text
            log_job(title, company, location)
        except Exception as e:
            print(f"[!] Skipped job due to error: {e}")
            continue

# Main
if __name__ == "__main__":
    EMAIL = "brianvhoward@outlook.com"
    PASSWORD = "Howard27$"
    TITLES = ["Data Analyst I", "Data Engineer I", "Junior Data Scientist", "SQL Developer I"]
    LOCATIONS = ["Boston", "New York"]

    driver = init_driver()
    linkedin_login(driver, EMAIL, PASSWORD)

    for location in LOCATIONS:
        resume = get_resume_by_location(location)
        for title in TITLES:
            search_jobs(driver, title, location)
            easy_apply(driver, resume)

    driver.quit()



            #Find and complete the form (if any fields exist)



