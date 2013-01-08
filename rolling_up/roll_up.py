# ** District level roll-up file + conversion to shapefile. **

'''

* To extract any other subset of data,
see google refine project "mif_raw" for original data
(that already has dist / states matched with state_name_prep_geocoding.py).

* This code hinges on there only being one MFI of the same name per district.

* Script Preparation Notes: 
	* Make sure data is sorted by state, district, then mfi.
	* Make sure row_counter is set to appropriate length of csv file.
	
'''

## Importing modules:

import csv
from string import *
from shapely.geometry import Point, mapping
from fiona import collection


## Variables Needed:


### Keeping track of district and state names
district_name = ""
state_name = ""


### To count the number of mfi's and number of mfis with line_item values:
mfi_name = ""
numb_mfi = 0
numb_out = 0
numb_port = 0
numb_delinq = 0


### To track the current loan portfolios, outstanding loans and delinquency for averaging
out_loans_total =  0.0
out_loans_avg = 0.0
loan_port_avg = 0.0
delinquent_avg = 0.0
str_out_loans_total = ""
str_out_loans_avg = ""
str_loan_port_avg = ""
str_delinquent_avg = ""


### To keep I/O files straight:
input_file = "../raw_data/states/mfi_raw_states_6_30.csv"
output_file = "../state_lvl/quarters/6_30_state_lvl.csv"

### To keep track of the rows we are on relative to the total rows:
row_counter = 0
row_total = 386

### Final output for new csv at the district level that will be converted to a point shapefile
##### (Headers initialized here.)
rolled_up = [["districts", "states", "number_of_mfis", "out_loans_total", "str_out_loans_total", "out_loans_avg", "str_out_loans_avg", "loan_port_avg", "str_loan_port_avg", "delinquent_avg", "str_delinquent_avg"]]


## Begin collecting aggregated data:

with open(input_file, "r") as mfi:
	dict_reader = csv.DictReader(mfi)

	for row in dict_reader:
		
		# Keeping track of what row we're on:
		row_counter += 1

		# Initializing relevant conditional factors:
		if row_counter == 1:
		
			district_name = row["districts"]
			mfi_name = row["mfi"]
		
		# End case: See normal cases for more detailed notes
		if row_counter == row_total:
			
			# Grabbing last line_item_value value:
			if row["element_id"] == "outstand_loan":
				out_loans_total = out_loans_total + float(row["line_item_value"])
				numb_out += 1
			if row["element_id"] == "loan_port":
				loan_port_avg = loan_port_avg + float(row["line_item_value"])
				numb_port += 1
			if row["element_id"] == "delinquent":
				delinquent_avg = delinquent_avg + float(row["line_item_value"])
				numb_delinq += 1
				
			# Have total outstanding loans already, just need to create string variable
			str_out_loans_total = str(out_loans_total)
			
			# Calculating averages:
			if numb_out != 0:
				out_loans_avg = out_loans_total / float(numb_out)
				str_out_loans_avg = str(out_loans_avg)
			
			else:
				out_loans_avg = 0.0
				str_out_loans_avg = "No Data"
			
			if numb_port != 0:
				loan_port_avg = loan_port_avg / float(numb_port)
				str_loan_port_avg = str(loan_port_avg)
			
			else:
				loan_port_avg = 0.0
				str_loan_port_avg = "No Data"
			
			if numb_delinq != 0:
				delinquent_avg = delinquent_avg / float(numb_delinq)
				str_delinquent_avg = str(delinquent_avg)
			
			else:
				delinquent_avg = 0.0
				str_delinquent_avg = "No Data"

			# The last row will need to be counted, if it's a singular line or not.		
			numb_mfi += 1

			district_name = row["districts"]
			state_name = row["states"]

			rolled_up.append([district_name, state_name, numb_mfi, out_loans_total, str_out_loans_total, out_loans_avg, str_out_loans_avg, loan_port_avg, str_loan_port_avg, delinquent_avg, str_delinquent_avg])
			break
		
		# If we are within the same district, we'll need to add up the relevant information:
		if row["districts"] == district_name:
		
			if row["element_id"] == "outstand_loan":
				out_loans_total = out_loans_total + float(row["line_item_value"])
				numb_out += 1
			if row["element_id"] == "loan_port":
				loan_port_avg = loan_port_avg + float(row["line_item_value"])
				numb_port += 1
			if row["element_id"] == "delinquent":
				delinquent_avg = delinquent_avg + float(row["line_item_value"])
				numb_delinq += 1
				
			# Counting number of MFIs per district
			if row["mfi"] != mfi_name:
				mfi_name = row["mfi"]
				numb_mfi += 1
			
			district_name = row["districts"]
			state_name = row["states"]
			
			
		else:
			
			# Need to count the last MFI of the district before doing calculations.
			numb_mfi += 1
			
			# Have total outstanding loans already, just need to create string variable
			str_out_loans_total = str(out_loans_total)
			
			# Calculating averages of outstanding loans, loan portfolio and delinquency.
			if numb_out != 0:
				out_loans_avg = out_loans_total / float(numb_out)
				str_out_loans_avg = str(out_loans_avg)
			
			else:
				out_loans_avg = 0.0
				str_out_loans_avg = "No Data"
			
			if numb_port != 0:
				loan_port_avg = loan_port_avg / float(numb_port)
				str_loan_port_avg = str(loan_port_avg)
			
			else:
				loan_port_avg = 0.0
				str_loan_port_avg = "No Data"
			
			if numb_delinq != 0:
				delinquent_avg = delinquent_avg / float(numb_delinq)
				str_delinquent_avg = str(delinquent_avg)
			
			else:
				delinquent_avg = 0.0
				str_delinquent_avg = "No Data"
			
			# Appending results to district level
			rolled_up.append([district_name, state_name, numb_mfi, out_loans_total, str_out_loans_total, out_loans_avg, str_out_loans_avg, loan_port_avg, str_loan_port_avg, delinquent_avg, str_delinquent_avg])	
			
			# Resetting and adding in newest line_item_value
			out_loans_total = 0.0
			out_loans_avg = 0.0
			loan_port_avg = 0.0
			delinquent_avg = 0.0
			numb_out = 0
			numb_port = 0
			numb_delinq = 0
			str_out_loans_total = ""
			str_out_loans_avg = ""
			str_loan_port_avg = ""
			str_delinquent_avg = ""
			numb_mfi = 0
			mfi_name = row["mfi"]
			district_name = row["districts"]
			state_name = row["states"]
			
			if row["element_id"] == "outstand_loan":
				out_loans_total = float(row["line_item_value"])
				numb_out += 1
			if row["element_id"] == "loan_port":
				loan_port_avg = float(row["line_item_value"])
				numb_port += 1
			if row["element_id"] == "delinquent":
				delinquent_avg = float(row["line_item_value"])
				numb_delinq += 1



## Writing results to new .csv file:

with open(output_file, "w") as output:

	writing_output = csv.writer(output)
	writing_output.writerows(rolled_up)

print "Done."


'''

WORK ON THIS CODE LATER FOR MORE GENERAL CASES - NOT NECESSARY FOR NOW


## Now we need to convert this mfi_district_lvl.csv file to a shapefile for easy manual editing in QGIS / publication on TileMill.

schema = { 'geometry': 'Point', 'properties': { 'districts': 'str', 'states': 'str', 'number_of_mfis': 'int', 'line_item_average': 'float' } }

with collection("mfi_district_lvl.shp", "w", "ESRI Shapefile", schema) as output:
    
    with open('mfi_district_lvl.csv', 'rb') as f:
        reader = csv.DictReader(f)
        for row in reader:
            point = Point(float(row['lon']), float(row['lat']))
            output.write({
                'properties': {
                    'districts': row['districts'],
                    'states': row['states'],
                    'number_of_mfis': row['number_of_mfis'],
                    'line_item_average': row['line_item_average']
                },
                'geometry': mapping(point)
            })

'''




