def run_scraper(PROVINCE="mazowieckie", ORGANIZATION="bemowo", CATEGORY="B", HEADLESS=True, EXAM_TYPE=True):
    
    from urllib3 import poolmanager
    from requests.adapters import HTTPAdapter
    from http.cookiejar import MozillaCookieJar
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from datetime import datetime
    import os
    from dotenv import load_dotenv

    load_dotenv()

    def normalize_date(exam_date, exam_time):
        """
        Given date and time from info-car.pl returns timestamp in datetime format
        """
        cur_date = datetime.now()
        exam_day, exam_month = [int(x) for x in exam_date.split('.')]
        exam_hour, exam_minute = [int(x) for x in exam_time.split(':')]
        year = cur_date.year if (exam_month > cur_date.month or (exam_month == cur_date.month and exam_day >= cur_date.day)) else cur_date.year + 1
        exam_datetime = datetime(year, exam_month, exam_day, exam_hour, exam_minute)
        return exam_datetime

    # DEFINE URLS
    base_url = "https://info-car.pl"
    login_url = f"{base_url}/oauth2/login"

    # LOGIN CREDS, LOADED FROM .ENV
    credentials = {
        "username": os.getenv("INFO_CAR_EMAIL"),
        "password": os.getenv("INFO_CAR_PASSWORD"),
    }

    chrome_driver_path = "/home/maciek/Desktop/prawko/chromedriver-linux64/chromedriver"  # Update this path

    options = Options()
    if (HEADLESS):
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")

    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    # RUN THE WEBSITE WITH SELENIUM
    driver.get(login_url)

    wait = WebDriverWait(driver, 10)  # SPECIFY A MAXIMUM WAIT TIME FOR THE DRIVER

    # LOGIN

    cur_xpath = "/html/body/div/section/main/form/div[2]/div[1]/input"
    cur_input = wait.until(EC.element_to_be_clickable((By.XPATH, cur_xpath)))
    cur_input.send_keys(credentials['username'])

    cur_xpath = "/html/body/div/section/main/form/div[4]/div[1]/input"
    cur_input = wait.until(EC.element_to_be_clickable((By.XPATH, cur_xpath)))
    cur_input.send_keys(credentials['password'])

    cur_xpath = "/html/body/div/section/main/form/button"
    cur_button = wait.until(EC.element_to_be_clickable((By.XPATH, cur_xpath)))
    cur_button.click()

    # SWITCH TO EXAM WEBISTE

    exam_url = f"{base_url}/new/prawo-jazdy/sprawdz-wolny-termin"
    driver.get(exam_url)

    # ACCEPT COOKIES 

    wait = WebDriverWait(driver, 10)  # Timeout after 10 seconds
    cur_xpath = "/html/body/div[2]/div/div[2]/div[2]/div/div[2]"
    accept_cookies = wait.until(EC.element_to_be_clickable((By.XPATH, cur_xpath)))
    accept_cookies.click()

    # CHOOSE TO SIGN UP BY PKK (CRASHES SOMETIMES - TIMEOUT ON XPATH SEARCH, PROBABLY ISSUE ON THE WEBSITE'S SITE) ##################################################
    gui_PKK = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-layout/app-check-exam-availability/div/main/app-exam-availability-exam-center-step/div/section/label[1]/div')))
    
    gui_PKK.click()

    # PROVINCE

    gui_province = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-layout/app-check-exam-availability/div/main/app-exam-availability-exam-center-step/div/section[2]/div/form/div[1]/app-selectable-input/div/div[1]/si-internal-text-input/input')))
    
    gui_province.send_keys(PROVINCE)

    li_element = wait.until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/app-layout/app-check-exam-availability/div/main/app-exam-availability-exam-center-step/div/section[2]/div/form/div[1]/app-selectable-input/div/div[1]/si-internal-result-list/div/ul/li"))  # Locate by ID
    )
    
    driver.execute_script("arguments[0].click();", li_element)


    # ORGANIZATION

    gui_organization = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-layout/app-check-exam-availability/div/main/app-exam-availability-exam-center-step/div/section[2]/div/form/div[2]/app-selectable-input/div/div[1]/si-internal-text-input/input')))
    
    gui_organization.send_keys(ORGANIZATION)

    li_element = wait.until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/app-layout/app-check-exam-availability/div/main/app-exam-availability-exam-center-step/div/section[2]/div/form/div[2]/app-selectable-input/div/div[1]/si-internal-result-list/div/ul/li"))  # Locate by ID
    )

    driver.execute_script("arguments[0].click();", li_element)

    # CATEGORY

    gui_category = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-layout/app-check-exam-availability/div/main/app-exam-availability-exam-center-step/div/section[2]/div/form/div[3]/app-selectable-input/div/div[1]/si-internal-text-input/input')))
    
    gui_category.send_keys(CATEGORY)

    li_element = wait.until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/app-layout/app-check-exam-availability/div/main/app-exam-availability-exam-center-step/div/section[2]/div/form/div[3]/app-selectable-input/div/div[1]/si-internal-result-list/div/ul/li[1]"))  # Locate by ID
    )

    driver.execute_script("arguments[0].click();", li_element)
            
    # LOAD EXAMS

    load_button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-layout/app-check-exam-availability/div/main/app-exam-availability-exam-center-step/div/section[2]/div/ic-ghost-button/button')))
    driver.execute_script("arguments[0].click();", load_button)

    # CHOOSE TYPE

    if (EXAM_TYPE):
        practical_exam_button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-layout/app-check-exam-availability/div/main/app-exam-availability-calendar-step/app-word-exam-calendar/div/form/div[1]/div[2]')))
        practical_exam_button.click()
    else:
        theoretical_exam_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/app-layout/app-check-exam-availability/div/main/app-exam-availability-calendar-step/app-word-exam-calendar/div/form/div[1]/div[1]")))
        theoretical_exam_button.click()


    # DATE EXTRACTION

    try:
        date_element = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-layout/app-check-exam-availability/div/main/app-exam-availability-calendar-step/app-word-exam-calendar/section/exam-days-accordion/div/div[1]/div[1]/button/h5')))
        exam_weekday, exam_date = date_element.get_attribute("innerHTML").split(' ')
    except:
        # RETURN ERROR
        return {'error': 'error on date extraction'}
    
    time_element = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-layout/app-check-exam-availability/div/main/app-exam-availability-calendar-step/app-word-exam-calendar/section/exam-days-accordion/div/div[1]/div[2]/div/div/div[2]/div[1]/p[2]/span')))
    exam_time = time_element.get_attribute("innerHTML")

    exam_datetime = normalize_date(exam_date, exam_time)

    driver.quit()
    # RETURN THE NEXT AVAILABLE EXAM DATE
    return {'exam_datetime': exam_datetime, 'error': None}