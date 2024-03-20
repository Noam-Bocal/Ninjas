import sqlite3
import hashlib
import requests

# ANSI colors
GREEN = "\033[92m"
BLUE = "\033[94m"
RED = "\033[91m"
YELLOW = "\033[93m"
END = "\033[0m"

API_KEY = "591a3472a74237dbb42bee4e85cc8e4d8afd96003a1a1463726695c3b9fed462"  # My account API key
URL = "https://www.virustotal.com/vtapi/v2/file/report"  # ViruslTotal API


def menu():
    print("\n" + BLUE + "Welcome to cyber bot!" + END)
    print(BLUE + "Commands I know:" + END)
    print("1. " + BLUE + "Search for attacks in database:" + END)
    print("   For example: \"Search for attacks with ransomware\"")
    print("\n2. " + BLUE + "VIRUSTOTAL check" + END)
    print("   For example: \"Check the C:\\file\"")
    print("\n3. " + BLUE + "EXIT" + END)

    # Added try and except block because of ctrl+C.
    try:
        command = input("So what can I help you with?\n")
    except KeyboardInterrupt:
        print(BLUE + "BYE :)" + END)
        exit()
    handle_command(command.lower())


def handle_command(command):
    if "search" in command:
        what_to_search = command.split()[4]
        res = search_inDB(what_to_search)
        if res != "":
            print("\n" + BLUE + "Search results:" + END + "\n")
            for row in res:
                print_attack(row)
        else:
            print(YELLOW + "No results found." + END)

    elif "check" in command:
        what_to_check = command[command.index("the") + 4:]
        res = check_virustotal(what_to_check)
        if res != 0 and res != 1:
            print(YELLOW + "The signature is recognized as malicious by VirusTotal." + END)
            print(YELLOW + f"Detection Rate: {res:.2f}%" + END)
        elif res == 1:
            return  # Error in the hash calculating or api
        else:
            print(GREEN + "The signature is not recognized as malicious by VirusTotal." + END)

    elif "exit" in command:
        print(BLUE + "BYE :)" + END)
        exit()

    else:
        print(RED + "Unknown command" + END)


def search_inDB(search):
    # Create a connection to the database
    conn = sqlite3.connect(
        "C:\\Users\\user\\Desktop\\נועם לימודים\\rephael\\ninjas\\sql database handle\\attacks_data.db")
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM attacks WHERE Description LIKE '%{search}%' OR Name LIKE '%{search}%'")
    # Fetch all the matching rows
    rows = cursor.fetchall()
    conn.close()
    return rows


def check_virustotal(file_path):
    file_hash = calculate_file_hash(file_path)
    if file_hash is None:
        return 1
    # Set the parameters for the query
    params = {"apikey": API_KEY, "resource": file_hash}

    try:
        # Send the query to VirusTotal
        response = requests.get(URL, params=params)
        response.raise_for_status()  # Raise an exception for non-2xx status codes

        detection_rate = 0
        # Check the response status code
        if response.status_code == 200:
            json_response = response.json()
            # Check the detection rate
            if json_response["response_code"] != 0:
                positive_engines = json_response["positives"]
                total_engines = json_response["total"]
                detection_rate = positive_engines / total_engines * 100

        return detection_rate

    except requests.RequestException:
        print(RED + "Error occurred while communicating with VirusTotal." + END)
        return 1


def calculate_file_hash(file_path):
    try:
        # make a hash object
        h = hashlib.sha1()

        with open(file_path, "rb") as file:
            chunk = 0
            while chunk != b'':
                # read only 1024 bytes at a time
                chunk = file.read(1024)
                h.update(chunk)
        return h.hexdigest()
    except FileNotFoundError:
        print(RED + "File not found." + END)
        return None


def print_attack(attack):
    # Format and display the attack information
    name = attack[0]
    description = attack[1]
    id = attack[2]
    x_mitre_platform = attack[3]
    x_mitre_detection = attack[4]
    phase_name = attack[5]

    print(GREEN + "Name:" + END, name)
    print(GREEN + "ID:" + END, id)
    print(GREEN + "Platform:" + END, x_mitre_platform)
    print(GREEN + "Phase Name:" + END, phase_name)
    print(GREEN + "Description:" + END, description)
    print(GREEN + "Detection:" + END, x_mitre_detection)
    print(GREEN + "---------------------" + END)


if __name__ == "__main__":
    while True:
        menu()
