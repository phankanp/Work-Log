import csv
import os.path
import re
import string
import sys
from csv import DictReader, DictWriter
from datetime import datetime

from entry import Entry

filename = "worklog.csv"


class Worklog:

    def __init__(self):
        self.main_menu()

    def main_menu(self):
        """Main program menu,
        prompts user for input
        """

        print("\nWork Logger Application")

        exists = os.path.isfile(filename)

        while True:
            print("\nOptions:\n")
            print("  1. Add a new entry")
            print("  2. Lookup a previous entry")
            print("  3. Quit\n")

            get_user_choice = input(
                "Please enter the number of your selection (1-3): ")

            print()

            if get_user_choice == "1":
                entry = Entry()
                self.add_entry(entry)
                print("Entry successfully added.")
                self.main_menu()
            elif get_user_choice == "2":
                if not exists:
                    print("There are currently 0 entries. Must add entries, before searching.")
                else:
                    self.lookup_entry()
            elif get_user_choice == "3":
                print("\nExiting Work Logger")
                exit()
            else:
                print("Invalid choice, please try again.")

    def add_entry(self, entry):
        """Adds entry to csv file"""

        exists = os.path.isfile(filename)

        with open(filename, 'a') as file:
            headers = ["Task Name", "Time Spent (mins)", "Notes", "Date"]
            csv_writer = DictWriter(file, fieldnames=headers)

            if not exists:
                csv_writer.writeheader()
            csv_writer.writerow({
                headers[0]: entry.name,
                headers[1]: entry.time,
                headers[2]: entry.notes,
                headers[3]: entry.date
            })

    def update_entries(self, entries):
        """Updates entries by overwirting csv,
        with a new file
        """

        with open(filename, 'w') as file:
            headers = ["Task Name", "Time Spent (mins)", "Notes", "Date"]
            csv_writer = DictWriter(file, fieldnames=headers)
            csv_writer.writeheader()
            for entry in entries:
                csv_writer.writerow({
                    headers[0]: entry.name,
                    headers[1]: entry.time,
                    headers[2]: entry.notes,
                    headers[3]: entry.date
                })

    def lookup_entry(self):
        """Provides search options for user, 
        promptes for input
        """

        search_options = {"1": "By date", "2": "By date range", "3": "By keyword", "4": "By time spent",
                          "5": "By pattern", "6": "Exit to main menu"}

        while True:
            print()

            for k, v in search_options.items():
                print(k + ". " + v)

            user_choice = input(
                "\nPlease enter the number of your preferred search option: ").lower().strip()

            if user_choice == '6':
                self.main_menu()
            elif user_choice == '1':
                self.find_by_date()
            elif user_choice == '2':
                self.find_by_date_range()
            elif user_choice == '3':
                self.find_by_keyword()
            elif user_choice == '4':
                self.find_by_time_spent()
            elif user_choice == '5':
                self.find_by_pattern()
            else:
                print("Invalid choice! Please try again. ")

    def get_dates_list(self, entries):
        """Returns list entry dates"""

        dates = []

        for entry in entries:
            dates.append(entry.date)
        return dates

    def get_csv_data(self):
        """Gets entries from csv file, 
        returns a list of entries
        """

        data_list = []

        with open(filename, 'r') as file:
            csv_reader = DictReader(file)
            for e in csv_reader:
                entry = Entry(**e)
                data_list.append(entry)
        return data_list

    def remove_duplicate_dates(self, dates):
        """Removes diplcates dates from list"""

        date_list = []

        for date in dates:
            if date not in date_list:
                date_list.append(date)
        return date_list

    def validate_user_date_choice(self, text="date"):
        """Checks, validates, and returns user's date choice"""

        date_choice = input(f"Enter a {text}(MM-DD-YYYY) to search by:  ")

        try:
            datetime.strptime(date_choice, "%m-%d-%Y")
            return date_choice
        except ValueError:
            input("\nInvalid entry, format of date must be MM-DD-YYYY\n")
            return self.validate_user_date_choice(text)

    def paging_options(self, index, entries):
        """Prints out available paging options"""

        options = {"P": "Previous Entry", "N": "Next Entry",
                   "E": "Edit Entry", "D": "Delete Entry", "M": "Main Menu"}

        if index == 0:
            del options["P"]

        if index == len(entries) - 1:
            del options["N"]

        for k, v in options.items():
            print(" " + k + ". " + v)

    def print_entry(self, index, entries):
        """Prints single entry"""

        print(f"\nEntry {index+1} of {len(entries)}:\n")

        print(" Task Name: {}\n".format(entries[index].name), "Time Spent (mins): {}\n".format(entries[index].time),
              "Notes: {}\n".format(entries[index].notes), "Date: {}\n".format(entries[index].date))

    def print_entries(self, entries):
        """Interates through entries,
        selecting appropriate entry to
        print
        """

        index = 0

        while True:
            self.print_entry(index, entries)

            # if len(entries) == 1:
            #  self.paging_options(index, entries)
            # self.main_menu()

            self.paging_options(index, entries)

            user_choice = input(
                "\nPlease select one of the paging options: ").lower().strip()

            if index == 0 and user_choice == 'n':
                index += 1
            elif 0 < index < len(entries) - 1 and user_choice == 'n':
                index += 1
            elif 0 < index <= len(entries) - 1 and user_choice == 'p':
                index -= 1
            elif user_choice == 'e':
                self.edit_entry(index, entries)
            elif user_choice == 'd':
                self.delete_entry(index, entries)
            elif user_choice == 'm':
                self.main_menu()
            else:
                input("\nInvalid choice, please try again :")

    def search_again(self):
        """Checks if user wants to
        perform anoth search
        """

        response = input(
            "\nWould you like to search for something else? (Yes or No): ")

        while response.lower().strip() != 'yes' or response.lower().strip() != 'no':

            if response.lower().strip() == 'yes':
                self.lookup_entry()
            elif response.lower().strip() == "no":
                self.main_menu()
            else:
                response = input("\nInvalid choice, please try again: ")

    def find_by_date(self):
        """Finds entries by date"""

        print("\nAvailable Dates:\n")

        entries = self.get_csv_data()
        dates_list = self.get_dates_list(entries)
        unique_dates = self.remove_duplicate_dates(dates_list)

        for dates in unique_dates:
            print(dates)

        print()

        date = self.validate_user_date_choice()

        while date not in unique_dates:
            print("\nInvalid Choice, please select a data from provided options.\n")
            date = self.validate_user_date_choice()

        entry_matches = []

        for entry in entries:
            if date == entry.date:
                entry_matches.append(entry)

        self.print_entries(entry_matches)

        self.search_again()

    def find_by_date_range(self):
        """Finds entries between two date ranges"""

        print("\nFind By Date Range: \n")

        start_date = self.validate_user_date_choice("Starting date")
        end_date = self.validate_user_date_choice("End date")

        start_date = datetime.strptime(start_date, "%m-%d-%Y")
        end_date = datetime.strptime(end_date, "%m-%d-%Y")

        entries = self.get_csv_data()

        entry_matches = []

        for entry in entries:
            entry_date = datetime.strptime(entry.date, "%m-%d-%Y")
            if start_date <= entry_date <= end_date:
                entry_matches.append(entry)

        if entry_matches:
            self.print_entries(entry_matches)
        else:
            print(f"No entries found between {start_date} and {end_date}")

        self.search_again()

    def find_by_keyword(self):
        """Finds entries by exact keyword"""

        entries = self.get_csv_data()
        keyword = input("Enter a search term: ")

        entry_matches = []

        for entry in entries:
            if re.search(r'\b{}\b'.format(keyword), entry.name) or re.search(r'\b{}\b'.format(keyword), entry.notes):
                entry_matches.append(entry)

        if entry_matches:
            self.print_entries(entry_matches)
        else:
            print(f"No entries found with {keyword} in Task Name or Notes.")

        self.search_again()

    def find_by_pattern(self):
        """Finds entries by regex pattern"""

        entries = self.get_csv_data()

        pattern = input("\nEnter pattern(regex) to search by: ")

        entry_matches = []

        for entry in entries:
            if re.search(r'{}'.format(pattern), entry.name) or re.search(r'{}'.format(pattern), entry.notes):
                entry_matches.append(entry)

        if entry_matches:
            self.print_entries(entry_matches)
        else:
            print(f"\nNo entries found with {pattern} in Task Name or Notes.")

        self.search_again()

    def find_by_time_spent(self):
        """Finds entries by time spent"""

        entries = self.get_csv_data()

        time_spent = input("\nEnter the time (mins) to search by: ")

        if not time_spent.isdigit():
            input("\nTime spent must be a number, please try again.")
            self.find_by_time_spent()

        entry_matches = []

        for entry in entries:
            if re.search(r'{}'.format(time_spent), entry.time):
                entry_matches.append(entry)

        if entry_matches:
            self.print_entries(entry_matches)
        else:
            print(f"\nNo entries found with {time_spent} mins time spent.")

        self.search_again()

    def edit_entry(self, index, entries):
        """Provides entry editing options,
        gets user input and updates entry
        """

        edit_options = {"1": "Task Name",
                        "2": "Time Spent", "3": "Notes", "4": "Date"}

        print()

        for k, v in edit_options.items():
            print(k + ". " + v)

        while True:
            user_choice = input(
                "\nEnter the number of the value you would like to edit: ")

            print()

            if user_choice == '1':
                entries[index].set_name()
                self.update_entries(entries)
                print("Task name has been updated.")
                self.main_menu()
            elif user_choice == '2':
                entries[index].set_time_spent()
                self.update_entries(entries)
                print("Time spent has been updated.")
                self.main_menu()
            elif user_choice == '3':
                entries[index].set_notes()
                self.update_entries(entries)
                print("Task notes have been updated.")
                self.main_menu()
            elif user_choice == '4':
                entries[index].set_date()
                self.update_entries(entries)
                print("Task date has been updated.")
                self.main_menu()
            else:
                self.main_menu()

    def delete_entry(self, index, entries):
        """Deletes and entry"""

        all_entries = self.get_csv_data()

        for entry in all_entries:
            if entries[index] == entry:
                all_index = all_entries.index(entry)
                del all_entries[all_index]

        self.update_entries(all_entries)

        print("Entry has been deleted.")

        self.main_menu()


if __name__ == "__main__":
    Worklog()
