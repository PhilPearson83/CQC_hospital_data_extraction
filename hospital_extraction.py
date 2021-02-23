import requests
import pandas as pd
import os

# function to retreive hopsital from CQC using their API
def getHospitals():
    # retrieve a list of care homes in the South West
    url = 'https://api.cqc.org.uk/public/v1/locations?'
    params = {'localAuthority': ['Devon', 'Somerset', 'Torbay', 'Plymouth'], 'gacServiceTypeDescription': 'Acute services with overnight beds','partnerCode': 'DSFRS'} #'perPage': 4000
    req = requests.get(url, params=params)
    j = req.json()
    df = pd.DataFrame.from_dict(j.get('locations'))
    locationids = df['locationId'].tolist()
    dfs = []
    counter1 = 0
    for ids in locationids:
        counter1 += 1
        print(counter1)
        loc_details_url = f'https://api.cqc.org.uk/public/v1/locations/{ids}?partnerCode=DSFRS'
        req = requests.get(loc_details_url, timeout=(5, 27)) #time.sleep(0.5),
        j = req.json()
        dfs.append(j)
    dfz = pd.DataFrame(dfs)
    dfz.to_csv("cqc_hospitals.csv", index = False)
    print(dfz.head())
    print(dfz.info())
# check if csv file exist, if not generate new data
if os.path.exists('cqc_hospitals.csv') == False:
    getHospitals()
    print('***CQC hospital csv generated***')
print('***CQC hospital csv already exists***')