## Demeaning test code

### For your dataset, you'll have to:

#           (1) Set the row_total variable appropriately
#           (2) Name the "group_var" column appropriately (surround in "")
#           (3) Make sure in_file and out_file names are typed in correctly (surrounded by "")
#           (4) Make sure there aren't any additional columns we want to leave un-demeaned
#           (5) For Windows users, you'll have to put in a 'rb' or 'wb' into the "with" statements to open the files properly
#           (6) Make sure the in_file is sorted by the group_var
#           (7)


import csv

def demeaning(row_total, in_file, out_file, group_var):

    # To keep track of which group_var we are in:
    group_track = 1

    # Dictionaries for summs and lists
    summs ={}
    counters = {}

    # To count which row we are in:
    row_counter = 1

    # To calculate and store averages of each column in a block of rows belonging to one group_var group
    averages = {}

    # To collect averages of groups once we've finished a block of rows belonging to group_var one group:
    group_averages = {}

    # Dict of demeaned results for each row of final demeaned data:
    demeaned = {}

    # List storing dictionaries mapping columns of data:
    final_demeaned_data = []


    with open(in_file, 'r') as data:

        # Creating reader file from data:
        Reader = csv.DictReader(data)

        # Going through each row in reader object:
        for row in Reader:

            # Checking to make sure we are in correct group:
            if row[group_var] == str(group_track) and row_counter != row_total:

                # For each column in our row, we need to
                    # (1) Skip the column if it is the grouping column itself or if its value is missing
                    # (2) For each other column, we need to add its value to a dictionary and count how many values we've added so far
                for col in row.keys():

                    if col == group_var or row[col] == "":
                        pass
                        
                    else:
                        summs[col] = summs.get(col, 0) + float(row[col])
                        counters[col] = counters.get(col, 0) + 1
                        

            # We have gone through entire row and added float  values of columns to their respective column names in dictionary
            # We now need to compute averages once we've reached the next group:
            elif row[group_var] == str(group_track + 1):
                for col in summs.keys():

                    # NOTE: If all values were missing, we should have nothing in the summs dictionary for the column name.
                    averages[col] = summs[col] / float(counters[col])

                # Creating new dictionary of the format {group_#: {variable_name: average for variable for this group}} 
                group_averages["group_" + str(group_track)] = averages

                
                # Resetting variables for new group_var and increasing group_track count:
                summs = {}
                counters = {}
                averages = {}
                group_track = group_track + 1


                # Still need to add values of each column for this new row that beings the next group:
                for col in row.keys():

                    if col == group_var or row[col] == "":
                        pass
                        
                    else:
                        summs[col] = summs.get(col, 0) + float(row[col])
                        counters[col] = counters.get(col, 0) + 1

                # It's possible at this point that the final row is the only instance of the last cell_brith group:
                if row_counter == row_total:
                    for col in summs.keys():

                        # NOTE: In this case, there is only one instance of the group_var, so the averages will just be the values of the columns themselves.
                        averages[col] = summs[col] / float(counters[col])

                    # Creating new dictionary of the format {group_#: {variable_name: average for variable for this group}} 
                    group_averages["group_" + str(group_track)] = averages

            # If we've reached the end of the file, we need to add the last group onto the end:
            elif row_counter == row_total:
                
                # Still need to add values of each column for this new row that beings the next group:
                for col in row.keys():

                    if col == group_var or row[col] == "":
                        pass
                        
                    else:
                        summs[col] = summs.get(col, 0) + float(row[col])
                        counters[col] = counters.get(col, 0) + 1

                for col in summs.keys():

                    # NOTE: If all values were missing, we should have nothing in the summs dictionary for the column name.
                    averages[col] = summs[col] / float(counters[col])

                # Creating new dictionary of the format {group_track_number: {averages dictionary} } 
                group_averages["group_" + str(group_track)] = averages


            # If none of these conditions hold, we don't have a properly sorted csv file.
            else:
                print "Rows not sorted properly. Re-sort and re-run."
                break

            # This is end of outermost 'for' loop and we need to count which row we are on to end properly
            row_counter = row_counter + 1

        # Resetting group_track position and data position for going through data again:
        group_track = 1
        data.seek(0)

        # Going through data one more time to subtract means of each group
        # Storing these results in a list of dictionaries where each dictionary is a row in our demeaned dataset
        for row in Reader:

            # Skipping header row:
            if row[group_var] == group_var:
                pass

            else:

                # Going through current group:
                if row[group_var] == str(group_track):

                    for col in row.keys():
                        
                        # For each variable column, we are leaving the blank values and the group_var column alone
                        if col == group_var or row[col] == "":
                            demeaned[col] = row[col]

                        # Otherwise, we'll subtract the mean
                        else:
                            demeaned[col] = float(row[col]) - group_averages["group_"+str(group_track)][col]


                else:

                    for col in row.keys():

                        # For each variable column, we are leaving the blank values and the group_var column alone                    
                        if col == group_var or row[col] == "":
                            demeaned[col] = row[col]
                            
                        # Otherwise, we'll subtract the mean
                        else:

                            demeaned[col] = float(row[col]) - group_averages["group_"+str(group_track + 1)][col]


                    # Increasing group_track since we are through the previous group now        
                    group_track = group_track + 1
                    

                # Adding demeaned row into final_demeaned_data list
                final_demeaned_data.append(demeaned.copy())

                
    ## Need to write these results to a new file:

    data_out = open(out_file, 'w')
    dw = csv.DictWriter(data_out, fieldnames=Reader.fieldnames)
    dw.writerow(dict((fn,fn) for fn in Reader.fieldnames))

    for rows in final_demeaned_data:
        dw.writerow(rows)

    data_out.close()

            
