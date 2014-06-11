"""
Sort Excel/CSV File Utility - Reads a file of records, sorts them, and then writes them back to the file.
Allow the user to choose various sort style and sorting based on a particular field.
"""


class CsvReader:
    # Constants used for coloring the output
    MESSAGE_COLOR_RED = '\033[91m'
    MESSAGE_COLOR_GREEN = '\033[92m'
    MESSAGE_COLOR_BLUE = '\033[94m'

    def __init__(self, file_path):
        """
        Class constructor

        file_path:  String  - Full path to CSV file
        """
        # Open file,
        # read its content into a list,
        # convert each row into a sub list of items,
        # strip each item in the sub list
        file_object = open(file_path, 'r')
        self.records = map(lambda x: x.strip().split(','), file_object.readlines())
        file_object.close()

        # Extract column header
        self.header = self.records.pop(0)

        # Init sort attributes
        self.sort_field = None
        self.sort_order = None

    def display_header(self):
        """
        Display program header with message and list of columns
        """
        self.info('The following columns exists in the CSV file.')
        for index, column in enumerate(self.header):
            self.info('%i - %s' % (index, column))
        print  # Empty line

    def ask_for_sort_field(self):
        """
        Ask user to select a column for sorting the records
        """
        while True:
            try:
                # User must select a valid column index
                field = int(raw_input('Sort by field: [Enter column number] '))
                if field >= len(self.header):
                    raise Exception('Please enter a value number.')
                else:
                    self.sort_field = field
                    break
            except:
                self.error('Please enter a value number.')

    def ask_for_sort_order(self):
        """
        Ask user to select a sort order. Ascending or Descending.
        """
        while True:
            # User must select asc or desc
            order = raw_input('Sort order: [ASC or DESC] ').lower()
            if order not in ['asc', 'desc']:
                self.error('Please enter a value sort order.')
            else:
                self.sort_order = order
                break

    def sort_records(self):
        """
        Sort the current records based on the sort attributes
        """
        # Only sort records if we have a valid field selected
        if self.sort_field is not None:
            order = False if self.sort_order == 'asc' else True
            self.records = sorted(self.records, key=lambda i: i[self.sort_field], reverse=order)

    def save_sorted_records(self):
        """
        Save the sorted records into a new CSV file
        """
        # Open file for writing
        file_path = 'csvsort_output.csv'
        file_object = open(file_path, 'w')

        # Export header
        file_object.write(','.join(self.header) + '\n')

        # Export records
        for record in self.records:
            file_object.write(','.join(record) + '\n')

        # Close file
        file_object.close()

        # Output complete message
        self.print_message('Records sorted and exported to a new CSV file: %s' % file_path, self.MESSAGE_COLOR_GREEN)

    def start(self):
        """
        The main program method to start reading and writing records
        """
        # Display header
        self.display_header()

        # Ask user for a field to sort by and the order of the sort
        self.ask_for_sort_field()
        self.ask_for_sort_order()

        # Sort records
        self.sort_records()

        # Save into a file
        self.save_sorted_records()

    def error(self, message):
        """
        Display error message

        message:  String - The message to display
        """
        self.print_message(message, self.MESSAGE_COLOR_RED)

    def info(self, message):
        """
        Display info message

        message:  String - The message to display
        """
        self.print_message(message, '')

    @staticmethod
    def print_message(message, color):
        """
        Static method to display a colored message

        message:    String - The message to display
        color:      String - The color of the message
        """
        print "%s%s\033[0m" % (color, message)


# Start the program
if __name__ == '__main__':
    CsvReader('csvsort_records.csv').start()
