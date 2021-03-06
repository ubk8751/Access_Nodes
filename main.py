'''
By:     Samuel Jonsson
        Blekinge Tekniska Högskola
Date:   2021-04-02
Email:  ubk8751@gmail.com
'''

# Import the good stuff
import requests
import json

def get_data(unit_name):
    '''
    Description:
        A function for gettin information about a sensor, or all sensors connected 
        to the account

    Args:
        unit_name (string): the name of the sensor that we want information about. Leave blank for complete list.

    Return:
        Prints the name of the sensor(s). 
    '''

    # Get the authorisation file
    try:
        f = open("token.json")
        dct = json.load(f)
        f.close()
    
    # If there is an error in loading the authorisation file
    except:
        print("There was an error in loading the token file!")
    
    # Necessary link, don't touch
    url = "https://api.yggio-sandbox.sensative.net/api/iotnodes"
    
    # If we aren't looking for a specific sensor, get the complete list by creating the url
    if unit_name != "":
        lst_unit_name = list(unit_name)
        temp = ""
        for letter in lst_unit_name:
            if letter == " ":
                temp += "%20"
            else:
                temp += letter
        ending = "?name=" + temp
        url = "https://api.yggio-sandbox.sensative.net/api/iotnodes" + ending
    
    # Create the token
    token = "Bearer " + dct["token"]

    # Create header info
    header = {
            "Authorization": token
            }
    
    # Get the request object containing the info needed
    request = requests.get(url, headers=header)
    
    # Check if the request status is ok
    if request.status_code == 200:
        data = request.json()

        # In this case, print the name of all sensors, 
        # but this can be changed depending on what you want
        for i in range(len(data)):
            try:
                print(data[i]["name"] + ": " + str(data[i]["description"]) + "\n")
            except:
                print(data[i]["name"] + ": " + "No descrition\n")

def get_all_names():
    '''
    Description:
        A function for printing all the sensors connected to the user.

    Return:
        Prints the name of all the sensors connected to the account. 
    '''

    # Get the authorisation file
    try:
        f = open("token.json")
        dct = json.load(f)
        f.close()
    
    # If there is an error in loading the authorisation file
    except:
        print("There was an error in loading the token file!")
    
    # Necessary link, don't touch
    url = "https://api.yggio-sandbox.sensative.net/api/iotnodes"
    
    # Create the token
    token = "Bearer " + dct["token"]

    # Create header info
    header = {
            "Authorization": token
            }
    
    # Get the request object containing the info needed
    request = requests.get(url, headers=header)
    
    # Check if the request status is ok
    if request.status_code == 200:
        data = request.json()

        # In this case, print the name of all sensors, 
        # but this can be changed depending on what you want
        for i in range(len(data)):
            print(data[i]["name"])

def create_auth(u_name, p_word):
    '''
    Description:
        A function for creating the authentication information for the API.

    Args:
        u_name (string): username of the account
        p_word (string): password of the account

    Return:
        Creates a JSON file with the authentication information. 
    '''

    # Needed stuff, don't touch
    header = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    # Login info
    payload = {
        "username": u_name,
        "password": p_word
    }

    # Don't touch
    url = "https://api.yggio-sandbox.sensative.net/auth/local"
    
    # Get the authorisation token
    try:
        request = requests.post(url=url, data=json.dumps(payload), headers=header)
    except:
        print("Not a Json respose")
    print(request)
    
    # Check if the status is ok
    if request.status_code == 200:
        # Convert the request object to a json file
        r = request.json()

        r["username"] = u_name

        r["password"] = p_word

        try:
            # Dump the dictionary as a Json file named data.json
            with open("token.json", "w") as outfile: 
                json.dump(r, outfile)
            print("Token created")
    
        # If there is an error in the creation of the file
        except IOError:
            print("I/O error")

if __name__ == "__main__":
    '''unit_name is the name of the sensor, leave blank to print complete 
    list of sensors connected with the account. Only include one sensor at a time.'''
    
    unit_name = ""
    get_data(unit_name)
    
    '''u_name is the username and p_word is the password that will 
    be used for logging in'''
    
    # u_name = "test@test.com"
    # p_word = "test"
    # create_auth(u_name, p_word)

    '''Easy way to print all of the sensors connected to the user'''
    # get_all_names()