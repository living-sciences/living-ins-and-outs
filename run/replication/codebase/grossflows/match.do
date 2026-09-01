***Set the directory to the one containing the raw CPS files AND flows_67.dta.  
***The montly files must be extracted and named cpsbYYYYMM.raw.

version 7.0
set more 1
clear
set mem 50m
log using log_match, replace

**Exract the data from the raw CPS files
do match_extract
**Match consecutive monthly files when possible
do match_merge
**Create the flow data
do match_flows
**Seasonally adjust using ratio-to-moving-average
do match_sa

log close
