import json
import csv
import sys


def convert_to_csv(json_data, file_name):
    """
    Extracts JSON data from a file and saves it in a CSV Format
    :param json_data: data from the opened json file
    :param file_name: name of the opened json file
    """
    fields = [["Procedure Code", "ProcedureCode", "Code"],
              ["Procedure Code Type", "Code Type", "AltCodes"],
              ["Procedure Name", "ProcedureName", "Description"],
              ["Gross Charge", "Charge"],
              ["Insurance Payer Name", "InsuranceRates", "Max"],
              ["Insurance Rate", "InsuranceRates", "Cash Price"]]
    try:
        data = json.load(json_data)
    except json.decoder.JSONDecodeError:
        print("The file entered must be a valid JSON file")
        return
    output_file = file_name[:-5] + ".csv"
    with open(output_file, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(field[0] for field in fields)  # Writes the headers for the CSV
        if 'StandardCharges' in data:  # The CentinelaHospital file uses a StandardCharges key
            # to group together rows of data, while the AdventHealth file simply lists them
            StandardCharges = data['StandardCharges']['CDM']
        else:
            StandardCharges = data[0]
        for Procedure in StandardCharges:  # Loops through rows of data in the JSON file
            current_line = []
            for field in fields:  # Loops through the fields list above to look for keys in the JSON data
                for subfield in field:
                    if subfield in Procedure:
                        if subfield == "AltCodes":
                            line = list(Procedure[subfield].keys())
                            CodeType = line[0]
                            for i in range(1, len(line)):
                                CodeType += "/" + line[i]
                            current_line.append(CodeType)
                        elif subfield == "InsuranceRates":
                            for Insurance, Rate in Procedure[subfield].items():
                                current_line.append(Insurance)
                                current_line.append(Rate)
                                writer.writerow(current_line)
                                current_line.remove(Insurance)
                                current_line.remove(Rate)
                        elif subfield == "Max":  # If the insurances aren't categorized in a
                            # subdirectory, the Max key is used as the starting index since it always
                            # precedes the list of insurances
                            startpoint = list(Procedure.keys()).index("Max")
                            Insurances = list(Procedure.items())[startpoint+1:]
                            for Insurance in Insurances:
                                current_line.append(Insurance[0])
                                current_line.append(Insurance[1])
                                writer.writerow(current_line)
                                current_line.remove(Insurance[0])
                                current_line.remove(Insurance[1])
                        else:
                            current_line.append(Procedure[subfield])
        print("Created file "+output_file)


if __name__ == '__main__':
    for i in range(1,len(sys.argv)):
        convert_to_csv(open(sys.argv[i]), sys.argv[i])
