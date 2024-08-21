import os
import requests
import pandas as pd 

def generate_yearmonth_datestamps(start_year, start_month, end_year, end_month) -> list:
    """This function takes start and end dates as arguments and creates a list of the year-months between them. 
    Each item in the list is returned as YYYY_MM, matching the datestamp format used in datasets in the VIEWS API.
    The output can be used for, e.g., loop functions to download a series of datasets from the VIEWS API.
    """
    
    try:
        # Validate input
        if not (1 <= start_month <= 12 and 1 <= end_month <= 12):
            raise ValueError("Month must be between 1 and 12.")
    
        if (start_year > end_year) or (start_year == end_year and start_month > end_month):
            raise ValueError("End date must be after or equal to the start date.")
    
        # Generate and print the forecast period
        period_list = []
        current_year = start_year
        current_month = start_month

        while (current_year < end_year) or (current_year == end_year and current_month <= end_month):
            # Format month with leading zero if needed
            formatted_month = f"{current_month:02}"
            period_list.append(f"{current_year}_{formatted_month}")
            
            # Move to the next month
            if current_month == 12:
                current_month = 1
                current_year += 1
            else:
                current_month += 1

        return period_list
    
    except ValueError as e:
        print(f"Invalid input: {e}")

    if __name__ == "__main__":
        generate_yearmonth_datestamps(start_year, start_month, end_year, end_month)
    

def download_dataset_from_api(models, periods, versions, loas, save_path):    
    """Function to download a set of datasets from the VIEWS API. The function loops through and downloads (as csv) all combinations of models, versions, and levels of analysis that are available for the specified time period. It makes note of combinations that do not exist but keeps running until all combinations have been explored.

    Args:
        models (list): Models to include, e.g. "['fatalities001', 'fatalities002']".  
        periods (list): Data releases (YYYY_MM) to include for the chosen models, e.g. "['2024_01', '2024_02'". To auto-generate this list from a start and end date, you may use the generate_yearmonth_datestamps() function.
        versions (list): Versions or 'tries' for a given dataset, e.g. "['t01', 't02']" The default value for any dataset is 't01'. It is incremented by 1 for every additional version of the same dataset that is released (corrections).
        loas (list): Levels of analysis to include, e.g. "['cm', 'pgm']"
        save_path (str): The path to your preferred save folder, starting after the root/home folder.

    Dependencies:
    import os
    import requests
    import pandas as pd 
    """

    for model in models:
        for period in periods:
            for version in versions:
                for loa in loas:
                    try:
                        dataset = f"{model}_{period}_{version}"
                        views_url = f"https://api.viewsforecasting.org/{dataset}/{loa}"
                        file_name = f"{dataset}_{loa}.csv"  # Create a unique filename
                        PATH = os.path.join(save_path, file_name)
                        
                        r = requests.get(views_url)
                        
                        if r.status_code == 404:
                            print(f"Dataset {dataset} does not exist (404 error). Skipping.")
                            continue  # Skip to the next dataset

                        if r.status_code == 422:
                            print(f"Dataset {dataset} does not exist (422 error). Skipping.")
                            continue  # Skip to the next dataset

                        if r.status_code != 200:
                            print(f"Failed to fetch data for model {model}, period {period}, version {version}, loa {loa}: Status code {r.status_code}")
                            continue  # Skip to the next dataset
    
                        page_data = r.json()
    
                        if 'data' not in page_data:
                            print(f"'data' key not found in the response for model {model}, period {period}, version {version}, loa {loa}. Response keys: {page_data.keys()}")
                            continue  # Skip to the next dataset
    
                        master_list = page_data['data']
                        
                        while page_data.get('next_page', ''):
                            r = requests.get(page_data['next_page'])
                            if r.status_code == 404:
                                print(f"Next page for {dataset} does not exist (404 error). Skipping pagination.")
                                break  # Break the loop and stop pagination
                            if r.status_code != 200:
                                print(f"Failed to fetch the next page for model {model}, period {period}, version {version}, loa {loa}. Status code {r.status_code}")
                                break
                            page_data = r.json()
                            if 'data' not in page_data:
                                print(f"'data' key not found in a paginated response for model {model}, period {period}, version {version}, loa {loa}.")
                                break
                            master_list += page_data['data']
                            
                        df = pd.DataFrame(master_list)
                        os.makedirs(os.path.dirname(PATH), exist_ok=True)  # Ensure the directory exists
                        df.to_csv(PATH, index=False)
                        print(f"Data for model {model}, period {period}, version {version}, loa {loa} saved to {PATH}.")
    
                    except requests.exceptions.RequestException as e:
                        print(f"Request failed for model {model}, period {period}, version {version}, loa {loa}: {e}")
                        continue  # Skip to the next dataset

                    except Exception as e:
                        print(f"An error occurred while processing model {model}, period {period}, version {version}, loa {loa}: {e}")
                        continue  # Skip to the next dataset

    if __name__ == "__main__":
        download_dataset_from_api(models, periods, versions, loas, save_path)
