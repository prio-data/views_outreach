from pathlib import Path

#CHANGE:
outcome_type = "predictors" # "predictors" or "fatalities"
fetch_type = "api"  # "api" or "file"
run = "fatalities002_2024_02_t01" 
save_path = Path.home() / "ViEWS Dropbox" / "ViEWS" / "Codebooks" / "PDFs"

#DON'T CHANGE
# Logic to set the value of run based on outcome_type
if outcome_type == "predictors":
    run = "predictors_fatalities002_0000_00"
else:
    run = run #what you defined above

