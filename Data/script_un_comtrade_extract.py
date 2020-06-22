"""
Reference material:
Key for URL get headings: https://comtrade.un.org/api/swagger/ui/index#!/Data/Data_GetData
Reporter explanation: https://comtrade.un.org/data/doc/api/#reporters
Reporter ids: https://comtrade.un.org/Data/cache/reporterAreas.json
"""


# Packages just in case
#=== Packages
import pandas as pd
import requests
import csv
import time

# Custom import test
def f_file_test():
    print("Funciton package loaded")

# Function to extract data from UN comtrade
def f_un_comtrade_data(p_r_country = ["854"],p_p_country = ["all","854"],p_freq = "A",p_ps_years = ["2010","2011"],p_extra = ""):

    """This function works on the principle of one reporting country per URL in order to avoid the 5 country limit imposed by the API.
    You can enter any number of countries in the list, but each will run separately and be separated by the duration of the call plus 1 second pause."""

    #============= URL GENERATION =============

    # base UN COMTRADE url
    base_url = "https://comtrade.un.org/api/get?"

    # URL settings
    url_comma = "%2C"
    url_add = "&"

    # API reporters
    reporting_country = "r=" # country numerical ID

    #=== Partner countries
    partner_country = "p=" # country numerical ID
    if len(p_p_country) == 1:
        partner_country = partner_country + p_p_country[0]
    else:
        # if more than one entry rotate through entries (except last) adding entry and comma
        for entry in p_p_country[:-1]:
            partner_country = partner_country + entry + url_comma

        # add last entry
        partner_country = partner_country + p_p_country[-1]

    #=== Frequency / years
    data_frequency = "freq=" # response can be A or M
    data_frequency = data_frequency + p_freq

    #=== Years / Months
    time_ps = "ps="

    if len(p_ps_years) == 1:
        time_ps = time_ps + p_ps_years[0]
    else:
        # if more than one entry rotate through entries (except last) adding entry and comma
        for entry in p_ps_years[:-1]:
            time_ps = time_ps + entry + url_comma

        # add last entry
        time_ps = time_ps + p_ps_years[-1]

    #=== prepare extra reporters
    url_extra = [partner_country,data_frequency,time_ps,p_extra]
    url_extra_string = ""

    for entry in url_extra:
        url_extra_string = url_extra_string + url_add + entry

    # list of URLs
    un_url_list = []

    for entry in p_r_country:
        temp_url = base_url + reporting_country + entry
        #print(temp_url) #for testing
        temp_url = temp_url + url_extra_string
        #print(temp_url) #for testing
        un_url_list.append(temp_url)

    #============= URL DOWNLOAD =============

    # list of dataframes
    df_un_list = []

    for index,un_url in enumerate(un_url_list):

        # Work report
        print(f"WORKING ON | Country {p_r_country[index]}| URL {un_url}")

        base_error = f"Country {p_r_country[index]}| URL {un_url} | not ok, data not processed further"

        try:
            un_data = requests.get(un_url)
            un_url_status = un_data.json()["validation"]["status"]["name"]

            # check data was ok
            if un_url_status == "Ok":
                # create dataframe
                df_un = pd.DataFrame(un_data.json()["dataset"])
                df_un_list.append(df_un)
            else:
                print(f"DATA CHECK | {base_error}")

        except:
            print(f"DL ATTEMPT | {base_error}")

        print("OBLIGATORY PAUSE")
        time.sleep(2)


    # all databases and urls
    return_objects = [df_un_list,un_url_list]

    return return_objects
