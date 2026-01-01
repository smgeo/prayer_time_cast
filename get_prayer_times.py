import requests
import json
from datetime import datetime, timedelta
import pandas as pd
from dotenv import load_dotenv
import os
#======== constants ==========
load_dotenv() # Load the environment variables from .env file

api_url = f'{os.getenv("HOME_ASSISTANT_URL")}/api/services/calendar/create_event'
headers = {
    'Authorization': f'Bearer { os.getenv("LONG_LIVE_TOKEN")}',
    'Content-Type': 'application/json'
}

def extract_prayer_times(mosque_link:str=os.getenv("MOSQUE_LINK")) -> pd.DataFrame:
    """function that extract the calendar from the mosque link and return a DataFrame

    Args:
        mosque_link (str): the link of the mosque page

    Returns:
        pd.Dataframe_: the DataFrame of the prayer times
    """
    # Faire la requête HTTP
    print("getting data from mawaqit mosquee page")
    response = requests.get(mosque_link)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.status_code}")
    # Extraire les données JSON de la réponse
    response =(response.text.split("confData =")[1].split(";")[0])
    data = json.loads(response)

    # Extraire le calendrier
    print("extracting and formatting data")
    calendar = data.get('calendar', [])
    # Préparer les données pour le DataFrame
    all_days = []
        # Parcourir chaque mois
    for month_idx, month in enumerate(calendar, 1):
        # Parcourir chaque jour
   
        for day_idx, times in month.items():
            if len(times) == 6:  # Vérifier qu'on a bien 5 temps de prière
                day_data = {
                    'month': month_idx if int(month_idx) > 9 else f'0{month_idx}',
                    'day': day_idx if int(day_idx) > 9 else f'0{day_idx}',
                    'Fajr': times[0],
                    'Duhr': times[2], 
                    'Asr': times[3],
                    'Maghreb': times[4],
                    'Isha': times[5]
                }
                all_days.append(day_data)
    
    # Créer le DataFrame
    print("data preparation")
    df = pd.DataFrame(all_days)
    the_year = datetime.now().year
    df['date'] = df.apply(lambda row: f'{the_year}-{row["month"]}-{row["day"]}', axis=1)
    df = df[['date', 'Fajr', 'Duhr', 'Asr', 'Maghreb', 'Isha']]
    prayers = df.columns[1:]
    for prayer in prayers:
        df[prayer] = df['date'].astype(str) + 'T' + df[prayer].astype(str)+":00"
    # Sauvegarder en Excel
    return df[prayers]

#===============================================================
#================== Import to Home Assistant ==================
#===============================================================

def import_to_home_assistant_calendar(df:pd.DataFrame):
    """function that load the prayer times to the home assistant calendar
    Args:
        df (pd.DataFrame): the input 5 times prayer dataframe
    """
    
    p_times = df.columns
    for i, item in df.iterrows():
        for col in p_times :
            print(item[col])
            event_data = {
                'entity_id': f'calendar.{os.getenv("CALENDAR_NAME")}', 
                'summary': f'{col} Time N: {i}',
                'description': f'Prayer Time of {col}',
                'start_date_time': item[col],
                'end_date_time': (datetime.strptime(item[col], '%Y-%m-%dT%H:%M:%S')+timedelta(minutes=3)).strftime('%Y-%m-%dT%H:%M:%S')
            }
            print(event_data)

            response = requests.post(api_url, headers=headers, data=json.dumps(event_data))
            print(response.status_code)
            if response.status_code == 201 or response.status_code == 200:
                print(i, 'Event created successfully')
            else:
                print(i, f'Failed to create event: {response.status_code}' , "error_code :" , response.status_code)
                print(response.text)


if __name__ == "__main__":
    import_to_home_assistant_calendar(extract_prayer_times())