from xml.sax import parseString
from bs4 import BeautifulSoup
import re
import os
import csv
import unittest


def get_listings_from_search_results(html_file):
    """
    Write a function that creates a BeautifulSoup object on html_file. Parse
    through the object and return a list of tuples containing:
     a string of the title of the listing,
     an int of the cost to rent for one night,
     and a string of the listing id number
    in the format given below. Make sure to turn costs into ints.

    The listing id is found in the url of a listing. For example, for
        https://www.airbnb.com/rooms/1944564
    the listing id is 1944564.
.

    [
        ('Title of Listing 1', 'Cost 1', 'Listing ID 1'),  # format
        ('Loft in Mission District', 210, '1944564'),  # example
    ]
    """
    base_path = os.path.abspath(os.path.dirname(__file__))
    fullpath = os.path.join(base_path, html_file)
    file = open(fullpath, 'r')
    f = file.read()
    file.close()
    soup = BeautifulSoup(f, 'html.parser')

 
    return_list = []

    #from each div, get the div with the name and save the name to tuple, get the price and save the price to tuple, and get id and save id to tuple
    #class of interest for the titles is div class_ t1jojoys dir dir-ltr(for the actual name)

    
    #name list
    name_list = []
    #get name div list
    name_div = soup.find_all("div", class_ = "t1jojoys dir dir-ltr")
    #get actual name element
    for name in name_div:
        name_list.append(name.text)
    
    #get the price
    price_list = []
    #get price div
    price_div = soup.find_all("span", class_ = "_tyxjp1")
    #get the actual price
    for price in price_div:
        price_list.append(int(price.text.strip('$')))

    #get the id
    id_list = []
    for id in name_div:
        id_list.append(id.get("id").strip("title_"))
    
    #make list of tuples
    for index in range(len(name_list)):
        return_list.append((name_list[index], price_list[index], id_list[index]))


    return return_list
        
        








def get_listing_information(listing_id):
    """
    Write a function to return relevant information in a tuple from an Airbnb listing id.
    NOTE: Use the static files in the html_files folder, do NOT send requests to the actual website.
    Information we're interested in:
        string - Policy number: either a string of the policy number, "Pending", or "Exempt"
            This field can be found in the section about the host.
            Note that this is a text field the lister enters, this could be a policy number, or the word
            "pending" or "exempt" or many others. Look at the raw data, decide how to categorize them into
            the three categories.
        string - Place type: either "Entire Room", "Private Room", or "Shared Room"
            Note that this data field is not explicitly given from this page. Use the
            following to categorize the data into these three fields.
                "Private Room": the listing subtitle has the word "private" in it
                "Shared Room": the listing subtitle has the word "shared" in it
                "Entire Room": the listing subtitle has neither the word "private" nor "shared" in it
        int - Number of bedrooms
.
    (
        policy number,
        place type,
        number of bedrooms
    )
    """
    #first access the html file for given listing
    base_path = os.path.abspath(os.path.dirname(__file__))
    fullpath = os.path.join(base_path, "html_files/listing_" + listing_id + ".html")
    file = open(fullpath, 'r')
    f = file.read()
    file.close()
    soup = BeautifulSoup(f, 'html.parser')

    #then use soup to find policy number
    policy_list = []
    policy_div = soup.find_all("li", class_ = "f19phm7j dir dir-ltr")
    for div in policy_div:
        texts = div.find("span", class_ = "ll4r2nl dir dir-ltr")
        policy_list.append(texts.text)
    
    policy_add = ""

    pending_word = "pending"
    pending_caps = "Pending"
    exempt_word = "OSTR"
    if pending_word in policy_list[0] or pending_caps in policy_list[0]:
        policy_add = "Pending"
    elif exempt_word in policy_list[0]:
        policy_add = "Exempt"
    else:
        policy_add = policy_list[0]

    #get the place type 
    place_type = ""
    soup_text = soup.find('h2', class_ = '_14i3z6h').text
    
    #categorize
    priv_string = "Private"
    shared_string = "Shared"
    if priv_string in soup_text:
        place_type = "Private Room"
    elif shared_string in soup_text:
        place_type = "Shared Room"
    else:
        place_type = "Entire Room"


    #get the int of number of bedrooms
    return_bedroom = 0
    bedroom_soup = soup.find_all("li", class_ = "l7n4lsf dir dir-ltr")
    for bedroom_text in bedroom_soup:
        bedroomtxt = bedroom_text.text
        regex = r'([0-9]) bedroom'
        bedroom_num = re.findall(regex, bedroomtxt)
        
        if len(bedroom_num) > 0:
            return_bedroom = int(bedroom_num[0])

    #make return tuple
    return_tuple = (policy_add, place_type, return_bedroom)

    return return_tuple



def get_detailed_listing_database(html_file):
    """
    Write a function that calls the above two functions in order to return
    the complete listing information using the functions youve created.
    This function takes in a variable representing the location of the search results html file.
    The return value should be in this format:


    [
        (Listing Title 1,Cost 1,Listing ID 1,Policy Number 1,Place Type 1,Number of Bedrooms 1),
        (Listing Title 2,Cost 2,Listing ID 2,Policy Number 2,Place Type 2,Number of Bedrooms 2),
        ...
    ]
    """
    #get the list of listing id (list of tuples)
    first_list = get_listings_from_search_results(html_file)
    
    return_list = []
    #get each id and input to the second function and then attach t
    for element in first_list:
        input_list_id = element[2]
        second_tuple = get_listing_information(input_list_id)
        return_tuple = element + second_tuple
        return_list.append(return_tuple)

    
    return return_list
    

    


def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_detailed_listing_database()), sorts the tuples in
    ascending order by cost, writes the data to a csv file, and saves it
    to the passed filename. The first row of the csv should contain
    "Listing Title", "Cost", "Listing ID", "Policy Number", "Place Type", "Number of Bedrooms",
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Listing Title,Cost,Listing ID,Policy Number,Place Type,Number of Bedrooms
    title1,cost1,id1,policy_number1,place_type1,num_bedrooms1
    title2,cost2,id2,policy_number2,place_type2,num_bedrooms2
    title3,cost3,id3,policy_number3,place_type3,num_bedrooms3
    ...

    In order of least cost to most cost.

    This function should not return anything.
    """
    writer_file = open(filename, 'w')
    writer = csv.writer(writer_file)
    # write headers
    writer.writerow(["Listing Title", "Cost", "Listing ID", "Policy Number", "Place Type", "Number of Bedrooms"])

    #sort the tuples
    sorted_list = sorted(data, key = lambda t:t[1])

    #write sorted to the file
    for line in sorted_list:
        writer.writerow(line)

    #close file
    writer_file.close()
    


def check_policy_numbers(data):
    """
    Write a function that takes in a list of tuples called data, (i.e. the one that is returned by
    get_detailed_listing_database()), and parses through the policy number of each, validating the
    policy number matches the policy number format. Ignore any pending or exempt listings.
    Return the listing numbers with respective policy numbers that do not match the correct format.
        Policy numbers are a reference to the business license San Francisco requires to operate a
        short-term rental. These come in two forms, where # is a number from [0-9]:
            20##-00####STR
            STR-000####
    .
    Return value should look like this:
    [
        listing id 1,
        listing id 2,
        ...
    ]

    """
    regex1 = r'20[0-9][0-9]-00[0-9]{4}STR'
    regex2 = r'STR-000[0-9]{4}'
    
    return_list = []
    # at index of 3
    for place in data:
        policy_num = place[3]
        
        #check for pending and exempt

        if policy_num == "Pending" or policy_num == "Exempt":
            continue
        else:
            result1 = re.findall(regex1, policy_num)
            result2 = re.findall(regex2, policy_num)
            
            #match or no?
            if len(result1) == 0 and len(result2) == 0:
                return_list.append(place[2])
        
    return return_list        


def extra_credit(listing_id):
    """
    There are few exceptions to the requirement of listers obtaining licenses
    before listing their property for short term leases. One specific exception
    is if the lister rents the room for less than 90 days of a year.

    Write a function that takes in a listing id, scrapes the 'reviews' page
    of the listing id for the months and years of each review (you can find two examples
    in the html_files folder), and counts the number of reviews the apartment had each year.
    If for any year, the number of reviews is greater than 90 (assuming very generously that
    every reviewer only stayed for one day), return False, indicating the lister has
    gone over their 90 day limit, else return True, indicating the lister has
    never gone over their limit.
    """
    pass


class TestCases(unittest.TestCase):

    def test_get_listings_from_search_results(self):
        # call get_listings_from_search_results("html_files/mission_district_search_results.html")
        # and save to a local variable
        listings = get_listings_from_search_results("html_files/mission_district_search_results.html")
        # check that the number of listings extracted is correct (20 listings)
        self.assertEqual(len(listings), 20)
        # check that the variable you saved after calling the function is a list
        self.assertEqual(type(listings), list)
        # check that each item in the list is a tuple
        self.assertEqual(type(listings[0]), tuple)
        # check that the first title, cost, and listing id tuple is correct (open the search results html and find it)
        self.assertEqual(listings[0], ('Loft in Mission District', 210, '1944564'))
        # check that the last title is correct (open the search results html and find it)
        self.assertEqual(listings[19][0], "Guest suite in Mission District")


    def test_get_listing_information(self):
        html_list = ["1623609",
                     "1944564",
                     "1550913",
                     "4616596",
                     "6600081"]
        # call get_listing_information for i in html_list:
        listing_informations = [get_listing_information(id) for id in html_list]
        # check that the number of listing information is correct (5)
        self.assertEqual(len(listing_informations), 5)
        for listing_information in listing_informations:
            # check that each item in the list is a tuple
            self.assertEqual(type(listing_information), tuple)
            # check that each tuple has 3 elements
            self.assertEqual(len(listing_information), 3)
            # check that the first two elements in the tuple are string
            self.assertEqual(type(listing_information[0]), str)
            self.assertEqual(type(listing_information[1]), str)
            # check that the third element in the tuple is an int
            self.assertEqual(type(listing_information[2]), int)
        # check that the first listing in the html_list has policy number 'STR-0001541'
        self.assertEqual(listing_informations[0][0], 'STR-0001541')
        # check that the last listing in the html_list is a "Private Room"
        self.assertEqual(listing_informations[4][1], "Private Room")
        # check that the third listing has one bedroom
        self.assertEqual(listing_informations[2][2], 1)


    def test_get_detailed_listing_database(self):
        # call get_detailed_listing_database on "html_files/mission_district_search_results.html"
        # and save it to a variable
        detailed_database = get_detailed_listing_database("html_files/mission_district_search_results.html")
        # check that we have the right number of listings (20)
        self.assertEqual(len(detailed_database), 20)
        for item in detailed_database:
            # assert each item in the list of listings is a tuple
            self.assertEqual(type(item), tuple)
            # check that each tuple has a length of 6
            self.assertEqual(len(item), 6)
        # check that the first tuple is made up of the following:
        # 'Loft in Mission District', 210, '1944564', '2022-004088STR', 'Entire Room', 1
        self.assertEqual(detailed_database[0], ('Loft in Mission District', 210, '1944564', '2022-004088STR', 'Entire Room', 1))
        # check that the last tuple is made up of the following:
        # 'Guest suite in Mission District', 238, '32871760', 'STR-0004707', 'Entire Room', 1
        self.assertEqual(detailed_database[19], ('Guest suite in Mission District', 238, '32871760', 'STR-0004707', 'Entire Room', 1))
        

    def test_write_csv(self):
        # call get_detailed_listing_database on "html_files/mission_district_search_results.html"
        # and save the result to a variable
        detailed_database = get_detailed_listing_database("html_files/mission_district_search_results.html")
        # call write csv on the variable you saved
        write_csv(detailed_database, "test.csv")
        # read in the csv that you wrote
        csv_lines = []
        with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test.csv'), 'r') as f:
            csv_reader = csv.reader(f)
            for i in csv_reader:
                csv_lines.append(i)
        # check that there are 21 lines in the csv
        self.assertEqual(len(csv_lines), 21)
        # check that the header row is correct
        self.assertEqual(csv_lines[0], ["Listing Title", "Cost", "Listing ID", "Policy Number", "Place Type", "Number of Bedrooms"])
        # check that the next row is Private room in Mission District,82,51027324,Pending,Private Room,1
        self.assertEqual(csv_lines[1], ["Private room in Mission District","82","51027324","Pending","Private Room","1"])
        # check that the last row is Apartment in Mission District,399,28668414,Pending,Entire Room,2
        self.assertEqual(csv_lines[20], ["Apartment in Mission District","399","28668414","Pending","Entire Room","2"])
        

    def test_check_policy_numbers(self):
        # call get_detailed_listing_database on "html_files/mission_district_search_results.html"
        # and save the result to a variable
        detailed_database = get_detailed_listing_database("html_files/mission_district_search_results.html")
        # call check_policy_numbers on the variable created above and save the result as a variable
        invalid_listings = check_policy_numbers(detailed_database)
        # check that the return value is a list
        self.assertEqual(type(invalid_listings), list)
        # check that there is exactly one element in the string
        self.assertEqual(len(invalid_listings), 1)
        # check that the element in the list is a string
        self.assertEqual(type(invalid_listings[0]), str)
        # check that the first element in the list is '16204265'
        self.assertEqual(invalid_listings[0], '16204265')
        


if __name__ == '__main__':
    database = get_detailed_listing_database("html_files/mission_district_search_results.html")
    write_csv(database, "airbnb_dataset.csv")
    check_policy_numbers(database)
    unittest.main(verbosity=2)
