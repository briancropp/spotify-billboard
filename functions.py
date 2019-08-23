from requests.auth import HTTPBasicAuth # Import HTTPBasicAuth for encoding
from IPython.core.debugger import set_trace # Import set trace
import requests # Import requests
from lxml import etree # Import etree for parsing
import sqlalchemy as sa # Import sqlalchemy
import pandas as pd # Import pandas 
import json # Import json
import re # import regular expressions
import io # Import io
import lxml.html as lh # Import lxml.html for parsing html elements
import json # Import json
import numpy as np

def buildURL(protocol, location, resource):
    """ This function takes an input of a protocol, location, and year and puts these  items together to 
    format them. We return a formatted correctly url.
    
    Parameters: 
        protocol: Can be http or https
        location: The specific website you want to go to. 
        resource: any added parameters to get to the exact website needed. 
    
    Return Value: 
        The url 
    """
    
    if protocol is None: # If statement to see if protocol is None. 
        protocol = 'http' # If protocol is None, then we define the protocol as 'http'
    if protocol == 'http' or protocol == 'https': # If statement to see add '://' to protocol if input protocol = 'http' or 'https' 
        protocol = protocol+'://' # Define protocol
        
    template = '{}{}/{}' # Format template of final location with resource and protocol
         
    url = template.format(protocol, location, resource) # Final formatting of url
    return url # Return url

def HTTPGet(url, params, link):
    """ This function takes an input of a protocol, location, resource, pdict and extension as inputs. It puts this url 
    toether properly formated with the buildURL function above, performs a GET request. 
    
    Parameters: 
        url: the specific website someone wants to go to. 
        params: the specific parameters the person needs to make a url correct. 
        link: the website link that has been created. 
        
    Return Value: 
        The url, none, a json file, an xml object, an html root, or content as a string. 
    """
    resp = requests.get(url, params = params) # use the requests module to perform a GET 
    if resp.status_code != 200: # If function to test if the status of the GET is successful
        return None # Returns None value if GET request was not successful
    
    if link == "Y": # If statement to return link if link is Y
        return print(resp.url) # Return printed url response
    
    if "application/json" in resp.headers["Content-Type"]: # Tests if the return of the GET is a JSON object and returns it if true
        return resp.json() # Returns JSON file in python data structure format if content type is JSON
    
    if "application/xml" in resp.headers["Content-Type"] or 'text/xml' in resp.headers["Content-Type"]: # Tests if the return of the GET is a XML object and returns it if true
        xml = etree.fromstring(resp.content) # Defines content type as Element data structure
        return xml # Returns xml element object
    
    if "text/html" in resp.headers["Content-Type"]: # Tests if the return of the GET is a HTML object and returns it if true
        htmlroot = lh.fromstring(resp.content)
        return htmlroot # Returns the object
    
    else: # Returns the the resp as a string if not a JSON, HTML, or XML.
        return resp.text # Return content as string
    


def addcreds(dic, key):
    """This function taeks an input of a dictinary and keeps adding to the creds when need be.
    
    Parameters: 
        dic: the dictionary that will be adding into the creds each time. 
        key: The specific part you are adding to the creds. 
    
    Return Value: 
        None. 
    
    
    """
    with open("creds.json", "r+") as file: # Open json file
        creds = json.load(file) # Define creds as JSON file
        creds[key] = dic # Create new key with value as dic
        file.seek(0)  # rewind 
        json.dump(creds, file) # # Dump creds file
        file.truncate() # Turncate

def opencreds():
    """This function opens the creds file and reads it. 
    
    Parameters: 
        None. 
    
    Return Value: 
        Creds file. 
    """
    with open("creds.json", "r") as file: # Open json file
        creds = json.load(file) # Define creds as JSON file
        return creds # Return creds

def getToken():
    '''
   
       This function takes the specific protocol, location, resource and uses the refresh token to get a new token 
    
    
    Parameters: 
        None
        
    Return Value: 
        The token from spotify. 
    '''
    
    creds = opencreds() # Use opencreds to get creds
    protocol = 'https' # Define protocol
    location = 'accounts.spotify.com' # Define location
    resource = 'api/token' # Define resource
    url = buildURL(protocol, location, resource) # use the buildURL to define url
    auth = HTTPBasicAuth(creds['Spotify HTTPBasicAuth']['client_id'], creds['Spotify HTTPBasicAuth']['client_secret']) # Create auth with HTTPBasicAuth
    data = creds["Spotify Refresh"] # define data as creds["Spotify Refresh"] 
    resp = requests.post(url, auth=auth, data=data) # Post requests to get new refrshed token
    code = resp.json()["access_token"] # Parse token
    return code # Return token

def database_setup(user, password, database):
    """
    The following function takes an input of user, password and database. It takes the inputs and connects to MySQL
    database for further data exploration. Data management and heavy lifting dataframes is done by SQL in the form
    of SQLAlchemy. The output is the engine, connect, cstring of the database.
    
    Parameters: 
        user: the person who is using the database. 
        password: the specific password that the user has specified. 
        database: the specific area where the table is. 
        
    Return Value: 
        the engine, connect, and cstring of database
    """
    try: # Try function to close connection if open
        connection.close() # Close connection
        del engine # Delete engine
    except: # Except if connection is not open
        pass # Pass if connection is not open
    template = 'mysql+mysqlconnector://{}:{}@hadoop2.mathsci.denison.edu/{}' # Template of MySQL database link
    cstring = template.format(user, password, database) # Creates connection string with inputs and template
    engine = sa.create_engine(cstring) # Create engine from connection string
    connect = engine.connect() # Creates connect by connecting engine
    return engine, connect, cstring # Returns engine, connect, cstring of database