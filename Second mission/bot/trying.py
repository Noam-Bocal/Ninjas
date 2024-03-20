import requests
import hashlib

# Set your API key
api_key = '591a3472a74237dbb42bee4e85cc8e4d8afd96003a1a1463726695c3b9fed462'

# Define the URL for the VirusTotal API
url = 'https://www.virustotal.com/vtapi/v2/file/report'

def calculate_file_hash(file_path):
    # Create a hash object using the desired algorithm (e.g., SHA-256)
    hash_object = hashlib.sha256()

    # Open the file in binary mode
    with open(file_path, 'rb') as file:
        # Read the file in chunks to efficiently handle large files
        for chunk in iter(lambda: file.read(4096), b''):
            # Update the hash object with the current chunk
            hash_object.update(chunk)

    # Get the hexadecimal representation of the hash value
    file_hash = hash_object.hexdigest()

    return file_hash

def check_malicious_signature(file_hash):
    # Set the parameters for the query
    params = {'apikey': api_key, 'resource': file_hash}

    # Send the query to VirusTotal
    response = requests.get(url, params=params)

    # Check the response status code
    if response.status_code == 200:
        # Request was successful
        json_response = response.json()
        
        # Check if the file has been previously analyzed
        if json_response['response_code'] == 0:
            print('The file has not been previously analyzed by VirusTotal.')
        else:
            # Check the detection rate
            positive_engines = json_response['positives']
            total_engines = json_response['total']
            detection_rate = positive_engines / total_engines * 100
            
            if detection_rate > 0:
                print('The signature is recognized as malicious by VirusTotal.')
                print(f'Detection Rate: {detection_rate:.2f}%')
            else:
                print('The signature is not recognized as malicious by VirusTotal.')

    else:
        # Request failed
        print('Query failed with status code:', response.status_code)

# Specify the path to your file
file_path = R'C:\Users\user\Downloads\DEMO-20230528T150428Z-001.zip'

# Calculate the hash of the file
file_hash = calculate_file_hash(file_path)

# Check if the signature is recognized as malicious by VirusTotal
check_malicious_signature(file_hash)

