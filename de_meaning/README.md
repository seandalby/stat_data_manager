# "De"-meaning Function

This script defines a function, "demeaning", that centers variables (columns of data) in a .csv file by sub-groups defined by a "group\_var" variable and returns a new .csv file with these variables demeaned. (To center a variable means to subtract the mean of that variable from every row of that variable.) The "group\_var" variable is a column of data that sub-divides the dataset into smaller groups. 

To illustrate this concept more concretely, let's look at an example below of what a group\_var could look like, paired with a hypothetical variable:

|Group Var|Variable 1|
|:-------:|:--------:|
|1|5|
|1|4|
|1|5|
|1|7|
|2|10|
|2|1|
|3|2|
|3|2|
|3|4|
|3|5|
|3|6|
|4|9|
|4|4|
|4|5|

So, for this hypothetical dataset, there are four sub-groupings. Now, below is the output of the above dataset after running it through the script:

|Group Var|Variable 1|
|:-------:|:--------:|
|1|0.25|
|1|-0.75|
|1|0.25|
|1|1.75|
|2|4.5|
|2|-4.5|
|3|-1.8|
|3|-1.8|
|3|0.2|
|3|1.2|
|3|2.2|
|4|3.0|
|4|-2.0|
|4|-1.0|

For each row, the mean of each sub-group to which the row belongs has been subtracted from the row's Variable 1 value. The Group Var remains unchanged. 

## Parameters and Assumptions

The function takes four variables:

* A row\_total variable for the length of your dataset (enter as integer)
* A path for the file you want to read in (enter enclosed in "")
* A path for the file you want to create as your output (enter enclosed in "")
* A "group\_var" that labels the "grouping" column in your dataset (enter enclosed in "")

Note the following assumptions the script makes:

* This script can take any number of (strictly numerical) variables, although currently it will "demean" everything other than the group\_var. So don't put in a file with variables you don't want to objectify. 
* The function assumes that the data are ordered by the group\_var variable
* This script is written for Mac OS users. For Windows users, you'll have to put in a 'rb' or 'wb' into the "with" statements to open the files properly.

## Issues:

* Currently, there is a bit of a memory problem, as the script won't work on files approximately 250 MB or bigger. Probably some noob coding error on my part, but I'm not sure how to improve it for now. For those who want to try, the code creates a massive dictionary for storing results temporarily, and I feel that this is the source of the memory overload. 
* I haven't put a lot of thought into other use-case scenarios so far, as this script derives from a specific task in a work project that isn't open to the public. Some data is stored in the function, however, if you want to access it for other purposes. For example, a dictionary called "group_averages" has keys for each grouping and values that are themselves dictionaries. These sub-dictionaries have keys that are each variable (column header) and their group mean. 

I welcome any and all feedback about any parts of the code. 

