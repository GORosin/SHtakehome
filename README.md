This program takes in JSON files from hospitals and writes data from these files into CSV format. The CSV contains six columns: Procedure Code, Procedure Code Type, Procedure Name, Gross Charge, Insurance Payer Name, and Insurance Rate. Corresponding data from the inputted JSON file is written into these columns. To use this program, put it in the same directory as your target JSON file(s), then run the program with the JSON file(s) as the parameter. It must include the .json extension to work.
i.e. > Python takehome.py 261150758_CentinelaHospitalMedicalCenter_standardcharges.json
Multiple JSON files may be converted consecutively by writing all of them as parameters.

Once a JSON is loaded, the program iterates through the json rows and appends specific data into a list. This data includes procedure name, code, code type, charge, insurance payer and rate. A separate list contains possible variations of those names and then looks for at least one of each in the JSON data. Once all six are found, the list is written into a row in the CSV.

One of the main challenges of this program is making it deal with two differently formatted JSON files. One possible solution is to simply have an if condition checking the file name, but that is cumbersome and not very modular to different files. Another way is to look for they key containing the main data: StandardCharges. If the file has this key, the program will look for it and unpack it's contents (after the sub-key CDM). If it doesn't find this key, it will use indices to find the content (as that is how the second file is formatted).

Planning, writing, testing, and documenting this program took about 3 hours. Some uncertainty about how to convert the Insurance Rates data in particular into CSV format was time consuming and the end solution was to create a new row for each insurance listed in a JSON object.

resources used:
https://www.w3schools.com/python/python_json.asp
https://docs.python.org/3/library/csv.html
https://realpython.com/iterate-through-dictionary-python/
