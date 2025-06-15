import os

abspath = os.path.abspath(__file__)
dirname = os.path.dirname(abspath)
os.chdir(dirname)

import requests
import pandas as pd
import csv
import datetime
import pickle
from IPython.display import display # really for "if __name__ == '__main__'"

def request_df():

    ##############
    # Check .csv #
    ##############

    with open("update_csv.pickle", "rb") as file: # "rb" for "read bytes"
        update_csv = pickle.load(file) # load in the 'datetime.datetime.now()' object from last update

    next_time = update_csv + datetime.timedelta(days=7) # adding a time delta of 7 days (i.e., a week) from then on
    if (datetime.datetime.now() > next_time) == True: # looking to see if the time now HAS PAST a week from last update
        url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/periodictable/JSON"
        timeout = 10
        try: # try-except clause for the case of yes-internet or no-internet
            file = requests.get(url) # API call
            json_file = file.json()

            df = pd.DataFrame(columns=json_file["Table"]["Columns"]["Column"])
            for i in json_file["Table"]["Row"]:
                df.loc[len(df.index)] = i["Cell"]

            df.to_csv("new_csv.csv", index=False) # can't forget about turning off index

            with open("periodic_table.csv", "r") as t1, open("new_csv.csv", "r") as t2:
                file1 = t1.readlines()
                file2 = t2.readlines() # now we are comparing the lines of the .csv files

            with open("update.csv", "w") as outFile: # creating a new .csv containing all discrepancies 
                for i in file2:
                    if i not in file1:
                        outFile.write(i)
            
            try:
                update = pd.read_csv("update.csv") # this line IS TO BE RAN FIRST as to meet the except clause in the case there's no need to update
                os.remove("update.csv")
                os.remove("periodic_table.csv")
                os.rename("new_csv.csv", "periodic_table.csv")
                print("'UPDATE: periodic_table.csv' has successfully been updated.")

            except pd.errors.EmptyDataError: # if update.csv is empty (i.e., no discrepancies found), will return a pandas error
                os.remove("update.csv")
                os.remove("new_csv.csv")
                print("'UPDATE: periodic_table.csv' is up to date.")

            del file
            del json_file
            del file1
            del file2 # housekeeping

        except (requests.ConnectionError, requests.Timeout) as exception: # if local host has no internet connection
            print("Internet is off? Loading 'periodic_table.csv' as is locally.")
            df = pd.read_csv("periodic_table.csv") # load the file anyways

        os.remove("update_csv.pickle")
        with open("update_csv.pickle", "wb") as file: # "wb" for "write byte"
            pickle.dump(datetime.datetime.now(), file) # end of checking the .csv process involves making a new timestamp

        del url
        del timeout

    else: # now for the case if it HAS NOT been past a week since last update
        print("'periodic_table.csv' has been loaded successfully") # nothing happens

    ###########################
    # Return Pandas DataFrame #
    ###########################

    df = pd.read_csv("periodic_table.csv")

    del update_csv
    del next_time

    return df

if __name__ == "__main__":
    display(
        request_df()
    )

# https://www.geeksforgeeks.org/how-to-check-whether-users-internet-is-on-or-off-using-python/
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html
# https://stackoverflow.com/questions/38996033/python-compare-two-csv-files-and-print-out-differences
# https://www.w3schools.com/python/python_file_remove.asp
# https://www.geeksforgeeks.org/python-os-rename-method/
# https://stackoverflow.com/questions/4529815/saving-an-object-data-persistence
# https://stackoverflow.com/questions/67755157/how-to-get-a-date-a-week-from-now-on-in-python
# https://stackoverflow.com/questions/32517248/what-is-the-difference-between-python-functions-datetime-now-and-datetime-t