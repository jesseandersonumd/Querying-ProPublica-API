import requests

with open("key.txt") as fh:
    api_key = fh.read()

headers = {"X-API-KEY": f"{api_key}"}

def get(session, chamber):
    '''
      Purpose: The purpose of this function is to get a list of all the members that we can work with later.

      Returns: List of all members.

    '''

    formatted = f"https://api.propublica.org/congress/v1/{str(session)}/{chamber}/members.json"
    data = requests.get(formatted, headers=headers).json()
    members_list = data["results"][0]["members"]
    return members_list

def set_list(session, party, chamber):
    '''
      Purpose: The purpose of this function is to create a list of tuple objects in the format (firstname_lastname, party_percentage) for the party passed in.
      
      Returns: A list of tuples. 

    '''

    new_session = get(session, chamber)
    new_list = []
    for element in range(len(new_session)):
      first_name = new_session[element]["first_name"]
      last_name = new_session[element]["last_name"]
      full_name = first_name + " " + last_name

      # I have to check if ["votes_with_party_pct"] actually has a value. I update party_check to True if there is a value.

      party_check = False
      try:
        party_unit = new_session[element]["votes_with_party_pct"]
      except:
        continue
      else:
        party_check = True
      
      if party_check and (new_session[element]["party"]==party):
        new_list.append((full_name,party_unit))
      elif (new_session[element]["party"]==party):
        new_list.append((full_name,"NA"))
    return new_list

def party_unity(party_list):
    '''
      Purpose: The purpose of this function is to iterate through each tuple in the list we passed in and add the corresponding party unity percentage, 
        found reliably at index 1 of the tuples, to the total under the condition that it's not == "NA". 
      
      Returns: The average of all the party unity percentages. 

    '''
    total = 0
    for tup in party_list:
        if(tup[1] != "NA"):
          total+=int(tup[1])
    return round(total/len(party_list),2)

def main(session, chamber):
    '''
      Purpose: The purpose of this function is to create lists of democrats and republicans using the function set_list().
        Further, it calculates the party unity percentages using party_unity() for both of the lists previously created. 
      
      Returns: A formatted list documenting the session #, the number of Democrats, the number of Republicans, the chamber (house or senate)
        as well as the party unity values for both. 

    '''
    # to obtain the list of democrats and republicans:
    democrats = set_list(session, "D", chamber)
    republicans = set_list(session, "R", chamber)

    # to obtain the party unity values for both democrats and republicans
    party_unity_democrats = party_unity(democrats)
    party_unity_republicans = party_unity(republicans)

    return f"For session {session}, there were {len(democrats)} Democrats and {len(republicans)} Republicans in the {chamber}. Party unity among these democrats was {party_unity_democrats} and party unity among republicans was {party_unity_republicans}."

if __name__ == "__main__":

    chamber = "senate" # Note - this can be changed to "house" and perform the exact same operations. 

    # This for loop goes through all of the possible sessions - 111 - 116. 
    for i in range(111,117):

        # We create a curr_session object here by executing the main() function for the session at i and the chamber ("house" or "senate")
        curr_session = main(i, chamber)
        print(curr_session)
        print("Here is the full list of Democrats with their appropriate party unity percentages:")
        democrats = set_list(i, "D", chamber)
        republicans = set_list(i, "R", chamber)
        for dem in democrats:
            print(dem)
        print()
        print("Here is the full list of Republicans with their appropriate party unity percentages:")
        for rep in republicans:
            print(rep)
        print("----------")