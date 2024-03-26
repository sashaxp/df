
import wb.adv
import pandas as pd

def main():


    # Call fetch_and_process_data from getRkList.py
    data_table = wb.adv.getRkList()

    # Set display options to show all rows and columns
    # pd.set_option('display.max_rows', None)
    # pd.set_option('display.max_columns', None)

    # Print the data_table from getRkList.py
    print(data_table)

if __name__ == "__main__":
    main()
