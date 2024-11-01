# README

The data folder in this repository contains data output (a set of watchlists) from the create_watchlists script. The dates in the subfolder names indicate which model run the forecasts were produced with: the Sept-24 folder contains forecasts based on input data up to and including September 2024, and so forth. 

All datasets present predictions for **state-based armed conflict**.

## Datasets in the data folders:
All datasets contain - as a minimum - the following columns:

- *country_id:* The VIEWS ID for each country.
country: Name of the country
- *year:* the year that the data is filtered for (2025)
- *main_mean:* Country-year (cy) forecasts for 2025, i.e. the total number of predicted fatalities per country in 2025.
- *actuals_last_12_months:* Sum of fatalities over the past 12 months, per country
 
Watchlist 4-7 also contain the column *predicted_change_in_percent*, which lists the predicted change (%) in fatalities in 2025, as compared to the sum of recorded fatalities over the last 12 months. Moreover, each of the watchlists (4-7) contain an additional column with various categorizations, described under the respective sections below. 

### Watchlists 1-3:

Simple watchlists of the highest predicted fatalities in 2025:
- *forecasts_by_country-year_2025*: Highest predicted fatalities in 2025, all countries
- *forecasts_by_criteria_lessthan25ged*: Highest predicted fatalities in 2025, subset for countries that observed less than 25 BRDs over the last 12 months
- *forecasts_by_criteria_greq25ged*: Highest predicted fatalities in 2025, subset for countries that observed at least 25 BRDs over the last 12 months

### Watchlist 4

Highest predicted change in fatalities (in 2025, compared to sum of observed fatalities over the last 12 months), subset into separate files based on the predicted intensity of violence (low/medium/high/war):

The thresholds used are: 
- low: less than 25 BRDs in 2025
- medium: 25-99 BRDs
- high: 100-999 BRDs
- war: 1000+ BRDs

Datasets by predicted violence intensity:
- *cy_forecasts_predictedchange_low_intensity*
- *cy_forecasts_predictedchange_medium_intensity*
- *cy_forecasts_predictedchange_high_intensity*
- *cy_forecasts_predictedchange_war_intensity*
- *cy_forecasts_predictedchange_all_intensities* (combines all of the above)

### Watchlist 5

Variation of watchlist 4.

Highest predicted change in fatalities (in 2025, compared to sum of observed fatalities over the last 12 months), subset into separate files based on a binary classification of whether or not they are predicted to observe at least 25 BRDs:
- *cy_forecasts_predictedchange_conflict* (at least 25 predicted BRDs)
- *cy_forecasts_predictedchange_no-conflict* (less than 25 predicted BRDs)
- *cy_forecasts_predictedchange_binary_classification* (combined both of the above)

### Watchlist 6

Combination of watchlist 2 and 4.

For (only) countries that observed less than 25 BRDs over the past 12 months: Highest predicted change in fatalities (in 2025, compared to sum of observed fatalities over the last 12 months), incl. classification of whether or not they are predicted to observe at least 25 BRDs in 2025. 

- *cy_forecasts_predictedchange_lessthan25BRD* 

### Watchlist 7

Combination of watchlist 3 and 4.

For (only) countries that observed at least 25 BRDs over the past 12 months: Highest predicted change in fatalities (in 2025, compared to sum of observed fatalities over the last 12 months), incl. classification of whether or not they are predicted to observe at least 25 BRDs in 2025. 

- *cy_forecasts_predictedchange_morethan25BRD* 


