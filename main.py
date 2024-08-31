import requests, json 
import pandas as pd
import numpy as np

with open('settings.json') as f:
    settings = json.load(f)

headers = {
    "Authorization": "Bearer " + settings["token"],
    "Content-Type": "application/json",
    "Notion-Version": "2022-02-22"
}

def readEntireDatabase(databaseID, headers):
    url = f"https://api.notion.com/v1/databases/{databaseID}/query"
    page_size = 100 
    payload = {"page_size": page_size}
    
    response = requests.request('POST', url, json=payload, headers=headers)
    data = response.json()
    results = data["results"]
    
    while data["has_more"]:
        payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
        response = requests.request("POST", url, json=payload, headers=headers)
        data = response.json()
        results.extend(data["results"])
    
    return results


if __name__ == "__main__":
    data = readEntireDatabase(settings["databaseID"], headers)
    properties = data[0]['properties'].keys()  #properties list
    print(f'|Downloaded {len(data)} positions|')
    #print('Selected features example:')
    creation_times, edition_times, names, statuses, tags, dates, content = [], [], [], [], [], [], []
    for page in data:
        creation_times.append(page['created_time'])   
        edition_times.append(page['last_edited_time']) 

        if not page['in_trash']:
            #print(page)
            try:
                names.append(page['properties']['Name']['title'][0]['plain_text']) 
            except:
                names.append('')
                
            try:
                content.append(page['properties']['Name']['title'][1]['text']['content'])
            except:
                content.append('')
            
            try:
                statuses.append(page['properties']['Status']['select']['name']) 
            except:
                statuses.append('')

            try:
                tags.append(page['properties']['Tags']['multi_select'])
            except:
                tags.append('')
            
            try:
                dates.append(page['properties']['Date']['date'])
            except:
                dates.append('')
                

    db = pd.DataFrame({'CREATION_TIME' : creation_times, 'EDITION_TIME' : edition_times, 
                        'NAME' : names, 'STATUS' : statuses, 'TAG' : tags, 'DATE' : dates, 'CONTENT' : content})
    db.to_csv('data.csv')