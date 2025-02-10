import os
import requests
import pandas as pd
import numpy as np


# Functions for downloading multiple datasets from the VIEWS API

def generate_API_datestamps(start_year, start_month, end_year, end_month) -> list:
    """This function takes start and end dates as arguments and creates a list of the year-months between them. 
    Each item in the list is returned as YYYY_MM, matching the datestamp format used in datasets in the VIEWS API.
    The output can be used for, e.g., loop functions to download a series of datasets from the VIEWS API. e.g. for the 'download_multiple_forecasts_from_api' function.

    Args:
        start_year: Listed as YYYY
        start_month: Listed as MM
        end_year: Listed as YYYY
        end_month: Listed as MM
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
        return []


def download_multiple_forecasts_from_api(models, periods, versions, loas, save_path):    
    """Function to download multiple datasets from the VIEWS API. The function loops through and downloads (as csv) all combinations of models, versions, and levels of analysis that are available for the specified time period. It makes note of combinations that do not exist but keeps running until all combinations have been explored.

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
                        
                        print(f"Fetching data for {model}_{period}_{version}_{loa}...")

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


# Function to fetch specific datasets from the VIEWS API (forecasts or predictors)

def fetch_data_from_api(api_call, csv, save_path, filename='VIEWS_data'):
    """Function to fetch and/or download single datasets from the VIEWS API. Results can be downloaded as a csv file (optional). Returns a pandas dataframe. 
    Args:
        api_call (str): API call to fetch data from the VIEWS API, without the csv flag. Consult the VIEWS API wiki for available datasets, filters, and correct specification. Without filters, the call should be provided in the format 'https://api.viewsforecasting.org/{dataset}/{loa}', where forecast datasets take the form of '{model}_{datestamp}_{version}', e.g. 'https://api.viewsforecasting.org/fatalities002_2024_08_t01/cm'. Predictor datasets, in turn, take the form of 'predictors_{model}_{datestamp}/{loa}', e.g. 'predictors_fatalities002_0000_00/cm', where '0000_00' refers to the rolling dataset that is updated monthly. In static datasets for archived models, '0000_00' is replaced by 'YYYY_MM', corresponding to the EndOfHistory in that dataset. 

        csv (bool): If True, the function will save the final dataframe to a csv file. 

        save_path (str): The path to your preferred save folder, starting after 'root/home/'.
    
        filename (str): The preferred name of the downloaded file. If no other value is passed, 'VIEWS_data' is used as the default name.

    Returns:
        df: Pandas dataframe with the fetched data.

    Dependencies:
    import os
    import requests
    import pandas as pd 
    """

    try:
        # Print status
        print(f"Fetching data for {api_call}...")
        
        # Fetch data
        r = requests.get(api_call)
        
        if r.status_code == 404 or r.status_code == 422:
            print(f"Dataset {dataset} does not exist ({r.status_code}). Try again.")
            return  # Skip to the next dataset

        if r.status_code != 200:
            print(f"Failed to fetch data: Status code {r.status_code}. Try again")
            return  # Skip to the next dataset

        page_data = r.json()

        if 'data' not in page_data:
            print(f"'data' key not found in the response for {api_call}. Response keys: {page_data.keys()}")
            return  # Skip to the next dataset

        master_list = page_data['data']
        
        while page_data.get('next_page', ''):
            r = requests.get(page_data['next_page'])
            if r.status_code == 404:
                print(f"Next page for {dataset} does not exist (404 error). Skipping pagination.")
                break  # Break the loop and stop pagination
            if r.status_code != 200:
                print(f"Failed to fetch the next page for {api_call}. Status code {r.status_code}")
                break
            page_data = r.json()
            if 'data' not in page_data:
                print(f"'data' key not found in a paginated response for {api_call}.")
                break
            master_list += page_data['data']
        
        # Create dataframe
        df = pd.DataFrame(master_list)
        df.rename(columns={'name':'country'},inplace=True)
        
        # Save data to csv, or return df
        if csv:
            # Create filename
            file_name = f'{filename}.csv'
            
            # Create path
            home = os.path.expanduser("~")
            PATH = os.path.join(home, save_path, file_name)
        
            df.to_csv(PATH, index=False)
            print(f"Data for {api_call} saved as csv to {PATH}.")
        
        print(f"Data for {api_call} saved to df.")
        return df

    except requests.exceptions.RequestException as e:
        print(f"Request failed for {api_call}: {e}")
        return  # Skip to the next dataset

    except Exception as e:
        print(f"An error occurred while processing {api_call}: {e}")
        return  # Skip to the next dataset
    

# Functions for creating watchlists

def forecasts_from_cm_to_cy(forecasts, year, csv, save_path):
    """Takes a dataframe with country-month forecasts from the VIEWS API and aggregates it to country-year. Options available to filter out results for a single indicator and/or year. Creates a csv file with the results (optional) and returns a pandas dataframe. 
    
    Args:
        forecasts (df): The forecast dataframe to use, fetched from the VIEWS API. The 'fetch_data_from_api()' function can be used to retrieve the data. 
        
        csv (bool): If True, the function will create a csv file with the results. 

        save_path (str): The path to your preferred save folder, starting after 'root/home/'.

    Returns:
        df: Dataframe with country-year forecasts, aggregated from country-month forecasts.

    Dependencies:
    import os
    import requests
    import pandas as pd 
    from utils import functions as f # functions from the views_outreach/utils folder
    """

    columns_to_keep=['country_id', 'country', 'month_id', 'year', 'month', 'main_mean']
    raw_forecasts = forecasts[columns_to_keep].copy()

    # Create dataframe with forecasts aggregated by country-year 
    forecasts_by_cy = raw_forecasts.groupby(['country_id', 'country', 'year'], as_index=False)['main_mean'].sum().sort_values(by=['main_mean'], ascending=False)

    # If specific year is selected, filter out and store forecasts for that year only. Set file name accordingly.

    if year == "": 
        print('No year was specified. Results have been grouped by year and saved to df, displayed here:')
        print(forecasts_by_cy)
        if csv:
            file_name = 'forecasts_by_country-year'
            save_path = os.path.join(save_path, file_name)
            forecasts_by_cy.to_csv(f'{save_path}.csv')
            print(f"{file_name} saved as csv to {save_folder}.")
        return forecasts_by_cy
    else: # if a year was specified
        filtered_forecasts_by_cy = forecasts_by_cy[forecasts_by_cy['year'].astype(str) == year]
        print(f'The data has been filtered for {year} and saved to df. Here is the result:')
        print(filtered_forecasts_by_cy)
        if csv:
            file_name = f'forecasts_by_country-year_{year}'
            save_path = os.path.join(save_path, file_name)
            filtered_forecasts_by_cy.to_csv(f'{save_path}.csv')
            print(f"{file_name} saved as csv to {save_path}.")
        return filtered_forecasts_by_cy
        

def get_sum_of_actuals_last_12months_by_c(predictor_df, feature, csv, save_path):
    """_summary_

    Args:
        predictor_dataset (df): Dataframe with predictor data fetched from the VIEWS API. Use the 'fetch_data_from_api()' function to retrieve the data in the correct format.
        
        feature (str): Column name for the feature to sum from the predictor_dataset. 
       
        csv (bool): If True, the function will save the final dataframe to a csv file.
        
        save_path (str): The path to your preferred save folder, starting after 'root/home/'.

    Returns:
        df: Pandas dataframe with the sum of actuals (for the chosen feature) for the last 12 months, grouped by country.
    """

    # Get last 12 month ids from predictor dataset
    last_12_month_ids = predictor_df['month_id'].drop_duplicates().nlargest(12)

    # Filter the actuals dataframe based on the last 12 unique month_id values
    actuals_last_12months = predictor_df[predictor_df['month_id'].isin(last_12_month_ids)][['country_id', 'month_id', 'country', 'year', 'month', feature]]

    # Sum the actuals for the last 12 months, grouping data by country, rename result column to understandable name
    sum_actuals_last_12months_by_c = actuals_last_12months.groupby(['country_id', 'country'], as_index=False)[feature].sum().rename(columns={feature:'actuals_last_12months'})

    if csv:
        file_name = 'sum_actuals_last_12months.csv'
        save_path = os.path.join(save_path, file_name)
        sum_actuals_last_12months_by_c.to_csv(f'{save_path}.csv')
        print(f"{file_name} saved to {save_path}.")

    return sum_actuals_last_12months_by_c


def filter_forecasts_by_criteria(forecasts_df, qualifying_countries_df, criteria_label, csv, save_path):
    """Takes a forecast dataframe retrieved from the VIEWS API and filters out results that meet a preset criteria. The criteria for filtering are based on the 'qualifying_countries' dataframe, which should contain a column with (only) the countries that meet the criteria, and other colum(s) with data representing the criteria itself (e.g. actuals). The two dataframes will be merged into one based on the 'country_id' column. Returns a pandas dataframe with the forecasts for the qualifying countries, for all categories of violence. 
        
    Args:
        forecasts: The forecast dataframe to use, fetched from the VIEWS API. Use the 'fetch_forecasts_from_api()' and, if relevant, the 'forecasts_from_cm_to_cy()' functions to retrieve the data in the correct format.

        qualifying_countries_df: A pandas dataframe with the countries that meet the criteria. The dataframe should contain a column with the country_ids, country names (named 'country') and other column(s) with data representing the criteria itself (e.g. actuals). The two dataframes will be merged on the 'country_id' columns. To ensure correct column names, use data produced by the functions 'fetch_forecasts_from_api()', 'fetch_cy_forecasts()', and fetch_features_from_api() to create your critera. 

        criteria_label (str): A label for the criteria used to filter the forecasts. This will be used in the filename if the results are saved as a csv file.
        
        csv (bool): If True, the function will create a csv file with the results. 

        save_path (str): The path to your preferred save folder, starting after 'root/home/'.

    Returns:    
        df: A pandas dataframe with the forecasts for the qualifying countries, for all categories of violence. The dataframe is sorted by highest predicted fatalities in descending order.

    Dependencies:
    import os
    import requests
    import pandas as pd 
    from utils import functions as f # functions from the views_outreach/utils folder
    """

    # Filter our forecast for qualifying countries 
    filtered_forecasts = forecasts_df[forecasts_df['country_id'].isin(qualifying_countries_df['country_id'])][['country_id', 'country', 'year', 'main_mean']]

    # Merge the two dataframes to store forecasts as well as data for the inclusion criteria
    merged_dfs = pd.merge(filtered_forecasts, qualifying_countries_df, on=['country_id', 'country'], how='left').sort_values(by=['main_mean'], ascending=False)

    if csv == True:
            file_name = f'forecasts_by_criteria_{criteria_label}'
            save_path = os.path.join(save_path, file_name)
            merged_dfs.to_csv(f'{save_path}.csv')
            print(f"Forecasts that meet selected criteria saved as csv to {save_path}.")
    return merged_dfs


def watchlist_relative_change_in_fatalities_by_intensity(forecasts_by_cy, sum_actuals_last_12months_by_c, category, csv, save_folder):
    """Takes a country-year forecast dataframe and a country-month actuals dataframe fetched from the VIEWS API, and calculates the predicted change in state-based fatalities for each country-year as compared to the sum of sb fatalities per country over the last 12 months. The function produces a set of csv files for (1) the full dataset with all categories, and (2) results filtered by each predicted intensity of violence in the given country-year. It returns a pandas dataframe with the results for all categories of violence.
    
    Args:
        cy_forecasts (df): Country-year forecasts dataframe, preferably produced by the 'fetch_cy_forecasts()' function to ensure correct column names. The country name column must be called "country".

        actuals_last_12_months_by_cy (df): Actuals dataframe with the sum of fatalities over the past 12 months per country, preferably produced by the 'get_sum_of_actuals_for_last_12months()' function to ensure correct column names. The country name column must be called "country".

        category: (str): Filter the results by predicted intensity of violence in the given year. Choose between: 'low' (less than 25 BRDs), 'medium' (25-99 BRDs), 'high' (100-999), 'war' (1000+). If you leave this empty, the function will return results for all categories as one dataframe. 

        csv (bool): If True, the function will save the selected data to a csv file. Else, it will only return a pandas dataframe.

        save_folder (str): The path to your preferred save folder, starting after 'root/home/'.
    
    Returns:
        df: A pandas dataframe with the predicted change in fatalities for each country-year as compared to the sum of fatalities per country over the last 12 months, for all categories of predicted conflict intensity. The dataframe is sorted by the percent change in descending order.

    Dependencies:
    import os
    import requests
    import pandas as pd 
    import numpy as np
    """

    # Merge actuals_last_12months with country-year forecasts
    prep_for_predicted_change = pd.merge(forecasts_by_cy, sum_actuals_last_12months_by_c, on=['country_id', 'country'], how='left')
    prep_for_predicted_change = prep_for_predicted_change.sort_values(by=['main_mean'], ascending=False)


   # Create a new column with the percent change from actuals_last_12_months to each country-year forecast
    prep_for_predicted_change['predicted_change_in_percent'] = ((prep_for_predicted_change['main_mean'] - prep_for_predicted_change['actuals_last_12months']) / prep_for_predicted_change['actuals_last_12months']) * 100

    # Replace inf values with NaN, sort by % change
    predicted_change = prep_for_predicted_change.replace([np.inf, -np.inf], np.nan)
    sorted_predicted_change = predicted_change.sort_values(by=['predicted_change_in_percent'], ascending=False)
    print('Data for the predicted change in fatalities has been created and stored to df. Here is the result:')
    print(sorted_predicted_change)

    # Add column for the predicted intensity of violence
    sorted_predicted_change['predicted_violence_category'] = sorted_predicted_change['main_mean'].apply(
    lambda x: 'low' if x < 25 
        else 'medium' if 25 <= x < 100 
        else 'high' if 100 <= x < 1000 
        else 'war' if x >= 1000 
        else 'unknown'  # Optional else case if needed
    )

    # Get the unique categories
    unique_categories = sorted_predicted_change['predicted_violence_category'].unique()

    # If no category has been selected, loop through data for each unique category, save them as csv files (optional), and return df with the combined results
    if category == "":
        for category in unique_categories:
            category_df = sorted_predicted_change[sorted_predicted_change['predicted_violence_category'] == category].sort_values(by=['predicted_change_in_percent'], ascending=False)
            if csv:
                file_name_cat = f'cy_forecasts_predictedchange_{category}_intensity'
                save_path = os.path.join(save_folder, file_name_cat)
                category_df.to_csv(f'{save_path}.csv')
                print(f'Saved {file_name_cat} as csv to {save_path}.')
        if csv:
            file_name_full = f'cy_forecasts_predictedchange_all_intensities'
            save_path = os.path.join(save_folder, file_name_full)
            sorted_predicted_change.to_csv(f'{save_path}.csv')
            print(f'Saved {file_name_full} as csv to {save_path}.')
        return sorted_predicted_change
    
    if category != "": # If a category has been selected, return the data for that category only
        category_df = sorted_predicted_change[sorted_predicted_change['predicted_violence_category'] == category].sort_values(by=['predicted_change_in_percent'], ascending=False)
        if csv:
            file_name_cat = f'cy_forecasts_predictedchange_{category}_intensity'
            save_path = os.path.join(save_folder, file_name_cat)
            category_df.to_csv(f'{save_path}.csv')
            print(f'Saved {file_name_cat} as csv to {save_path}.')
        return category_df


def watchlist_relative_change_in_fatalities_by_classification(forecasts_by_cy, sum_actuals_last_12months_by_c, csv, save_folder):
    """Takes a country-year forecast dataframe and a country-month actuals dataframe fetched from the VIEWS API, and calculates the predicted change in fatalities for each country-year as compared to the sum of fatalities per country over the last 12 months. Assigns a category to each prediction based on whether or not 25 or more BRDs have been predicted for that country-year. The function produces a csv file for each category, a csv file for all categories, and then returns a pandas dataframe with the all-categories result.
    
    Args:
        cy_forecasts (df): Country-year forecasts dataframe, preferably produced by the 'fetch_cy_forecasts()' function to ensure correct column names. The country name column must be called "country".

        actuals_last_12_months_by_cy (df): Actuals dataframe with the sum of fatalities over the past 12 months per country, preferably produced by the 'get_sum_of_actuals_for_last_12months()' function to ensure correct column names. The country name column must be called "country".

        csv (bool): If True, the function will save the selected data to a csv file. Else, it will only return a pandas dataframe.

        save_folder (str): The path to your preferred save folder, starting after 'root/home/'.
    
    Returns:
        df: A pandas dataframe with the predicted change in fatalities for each country-year as compared to the sum of fatalities per country over the last 12 months. The dataframe is sorted by the percent change in descending order.

    Dependencies:
    import os
    import requests
    import pandas as pd 
    import numpy as np
    """

    # Merge actuals_last_12months with country-year forecasts
    prep_for_predicted_change = pd.merge(forecasts_by_cy, sum_actuals_last_12months_by_c, on=['country_id', 'country'], how='left')
    prep_for_predicted_change = prep_for_predicted_change.sort_values(by=['main_mean'], ascending=False)


   # Create a new column with the percent change from actuals_last_12_months to each country-year forecast
    prep_for_predicted_change['predicted_change_in_percent'] = ((prep_for_predicted_change['main_mean'] - prep_for_predicted_change['actuals_last_12months']) / prep_for_predicted_change['actuals_last_12months']) * 100

    # Replace inf values with NaN, sort by % change
    predicted_change = prep_for_predicted_change.replace([np.inf, -np.inf], np.nan)
    sorted_predicted_change = predicted_change.sort_values(by=['predicted_change_in_percent'], ascending=False)
    print('Data for the predicted change in fatalities has been created and stored to df. Here is the result:')
    print(sorted_predicted_change)

    # Add column for the predicted intensity of violence
    sorted_predicted_change['predicted_violence_category'] = sorted_predicted_change['main_mean'].apply(
    lambda x: 'conflict' if x >= 25 
        else 'no-conflict' 
    )

    # Get the unique categories
    unique_categories = sorted_predicted_change['predicted_violence_category'].unique()

    # Loop through data for each unique category, save them as csv files (optional), and return df with the combined results
    for category in unique_categories:
        category_df = sorted_predicted_change[sorted_predicted_change['predicted_violence_category'] == category].sort_values(by=['predicted_change_in_percent'], ascending=False)
        if csv:
            file_name_cat = f'cy_forecasts_predictedchange_{category}'
            save_path = os.path.join(save_folder, file_name_cat)
            category_df.to_csv(f'{save_path}.csv')
            print(f'Saved {file_name_cat} as csv to {save_path}.')
    if csv:
        file_name_full = f'cy_forecasts_predictedchange_binary_classification'
        save_path = os.path.join(save_folder, file_name_full)
        sorted_predicted_change.to_csv(f'{save_path}.csv')
        print(f'Saved {file_name_full} as csv to {save_path}.')
    return sorted_predicted_change


if __name__ == "__main__":
    fetch_data_from_api(api_call='https://api.viewsforecasting.org/fatalities001_2022_12_t01/pgm', csv=True, save_path='Desktop/')