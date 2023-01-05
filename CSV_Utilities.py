import csv
import HashMap
import Package


class CSV_Utilities:

    @staticmethod
    # This method is used to open and read csv files. Returns a list of the contents from the csv file. This process
    # runs in 0(n) time. Because the reader must read through every row individually and add them to a list.
    def csv_to_list(csv_path):
        with open(csv_path, encoding='utf-8-sig') as csvfile:
            CSVPackage = csv.reader(csvfile, delimiter= ";")
            CSVPackage = list(CSVPackage)
        return CSVPackage
