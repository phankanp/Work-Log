from datetime import datetime


class Entry:

    def __init__(self, **kwargs):
        """Checks if arguments were passed in, gets user input if not"""

        self.name = (self.get_name() if "Task Name" not in kwargs else kwargs["Task Name"])
        self.time = (self.get_time_spent() if "Time Spent (mins)" not in kwargs else kwargs["Time Spent (mins)"])
        self.notes = (self.get_notes() if "Notes" not in kwargs else kwargs["Notes"])
        self.date = (self.get_date() if "Date" not in kwargs else kwargs["Date"])

    def get_name(self):
        """Get task name from user"""

        entry_name = input("Enter the task name:")

        if len(entry_name) == 0:
            input("\nTask name cannot be empty!\n")
            return self.get_name()
        else:
            return entry_name

    def set_name(self):
        """Updates task name"""

        new_name = input("Enter the new task name: ")

        if len(new_name) == 0:
            input("\nTask name cannot be empty!\n")
            return self.set_name()
        else:
            self.name = new_name

    def get_time_spent(self):
        """Get time spent from user"""

        entry_time = input("Enter the time spent on the task in minutes: ")

        try:
            int(entry_time)
        except ValueError:
            input("\nInvalid entry, time spent must be an integer\n")
            return self.get_time_spent()
        else:
            return entry_time

    def set_time_spent(self):
        """Updates time spent"""

        new_time_spent = input("Enter the new time spent: ")

        try:
            int(new_time_spent)
        except ValueError:
            input("\nInvalid entry, time spent must be an integer\n")
            return self.set_time_spent()
        else:
            self.time = new_time_spent

    def get_notes(self):
        """Get task notes from user"""

        notes = input("Enter notes for this task: ")

        if len(notes) == 0:
            notes = "None"

        return notes

    def set_notes(self):
        """Updates task notes"""

        new_notes = input("Enter new notes: ")

        if len(new_notes) == 0:
            new_notes = "None"

        self.notes = new_notes

    def get_date(self):
        """Get task date from user"""

        date = input("Enter a date for the task(MM-DD-YYYY): ")

        try:
            datetime.strptime(date, "%m-%d-%Y")
            return date
        except ValueError:
            input("\nInvalid entry, format of date must be MM-DD-YYYY\n")
            return self.get_date()

    def set_date(self):
        """Updates task date"""

        new_date = input("Enter new date: ")

        try:
            datetime.strptime(new_date, "%m-%d-%Y")
            return new_date
        except ValueError:
            input("\nInvalid entry, format of date must be MM-DD-YYYY\n")
            return self.set_date()
        else:
            self.date = new_date

    def __eq__(self, other):
        """Compares objects"""

        return self.name == other.name and self.time == other.time and self.notes == other.notes and self.date == other.date