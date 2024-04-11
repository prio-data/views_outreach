# Codebook Generator

## Overview

The Codebook Generator is designed to generate Markdown codebooks from JSON data. It can fetch data from either an API or a local file, convert it to Markdown format, and save the Markdown codebook to a specified directory.

## Prerequisites
- Access to ViEWS Dropbox

## Configuration

Before running the script [codebook_generator_json_to_md.py](codebook_generator__json_to_md.py), you need to configure the [codebook_generator__config.py](codebook_generator__config.py) file.

### Configurable Variables

1. `outcome_type`: Specify the type of outcome data ("forecasts" or "predictors"), i.e., what data is the codebook documenting?
2. `fetch_type`: Specify the method to fetch the codebook data ("api" or "file").
3. `run`: Specify the run value for the API endpoint. Also used in the naming of the final file.


## How to run this script
After making necessary changes to [codebook_generator__config.py](codebook_generator__config.py), run the script by clicking on the Run button in the top right of your IDE, or executing the following in Terminal:

```bash
python codebook_generator__json_to_md.py
```
