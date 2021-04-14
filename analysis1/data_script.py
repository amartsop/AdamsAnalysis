import csv
import os

class AdamsDataParser:
    def __init__(self):
        
        # Input forces
        self.__input_forces = { "Time (s)": [], "Input Force x (m)": [],
            "Input Force y (m)": [], "Input Force z (m)": []}

        # Input moments
        self.__input_moments = {"Time (s)": [], "Input Moment x (m)": [],
            "Input Moment y (m)": [], "Input Moment z (m)": []}

        # Handle position
        self.__handle_position = {"Time (s)": [], "Handle Position x (m)": [],
            "Handle Position y (m)": [], "Handle Position z (m)": []}

        # Handle orientation
        self.__handle_orientation = {"Time (s)": [],
            "Handle Euler phi (rad)": [], "Handle Euler theta (rad)": [],
            "Handle Euler psi (rad)": []}

        # Reaction forces
        self.__reaction_forces = {"Time (s)": [],
            "Reaction Force x (m)": [], "Reaction Force y (m)": [],
            "Reaction Force z (m)": []}

        # Reaction moments
        self.__reaction_moments = {"Time (s)": [],
            "Reaction Moment x (m)": [], "Reaction Moment y (m)": [],
            "Reaction Moment z (m)": []}

        # Tip position
        self.__tip_position = {"Time (s)": [], "Tip Position x (m)": [],
            "Tip Position y (m)": [], "Tip Position z (m)":[]}

        # Tip orientation
        self.__tip_orientation = {"Time (s)": [], "Tip Euler phi (rad)": [],
            "Tip Euler theta (rad)": [], "Tip Euler psi (rad)": []}

        # File names
        self.__filenames = ["input_forces.csv", "input_moments.csv", 
            "handle_position.csv", "handle_orientation.csv",
            "reaction_forces.csv", "reaction_moments.csv", 
            "tip_position.csv", "tip_orientation.csv"]

        self.__filenames = [ "handle_position.csv", "handle_orientation.csv",
            "reaction_forces.csv", "reaction_moments.csv", 
            "tip_position.csv", "tip_orientation.csv",
            "input_forces.csv", "input_moments.csv"]


        self.__parser_lists = [ self.__handle_position, self.__handle_orientation, 
            self.__reaction_forces, self.__reaction_moments,
            self.__tip_position, self.__tip_orientation,
            self.__input_forces, self.__input_moments]


        ######################################################################

        # Create dictionary of filestructrure
        self.__filename_values = {}

        for i in range(len(self.__filenames)):
            self.__filename_values[self.__filenames[i]] = self.__parser_lists[i]

        # Output file default
        self.__default_output_filename = os.path.basename(os.path.abspath("./"))
        self.__default_output_filename += '.csv'


    # Isolate numbers for each row
    def __search_numbers_per_row(self, list):
        list_out =[]
        for i in range(len(list)):
            if list[i] != "":
                list_out.append(list[i])
        return list_out
    
    def __search_char(self, list, char):
        for i in range(len(list)):
            if list[i] == char:
                return True
        return False

    def __parse_file(self, filename):

        with open(filename) as csv_file:

            # csv reader handler
            csv_reader = csv.reader(csv_file, delimiter=' ')

            # set line count
            line_count = 0

            # initialize reading numerical flag
            read_numerical = False

            numerical_count = 0

            for row in csv_reader:

                if(read_numerical):
                    num_list = self.__search_numbers_per_row(row)

                    data_structure = self.__filename_values[filename]

                    count = 0
                    for identifier in data_structure:
                        (data_structure[identifier]).append(num_list[count])
                        count += 1

                if(self.__search_char(row, 'A') & self.__search_char(row, 'B') & \
                    self.__search_char(row, 'C')) & self.__search_char(row, 'D'):
                    read_numerical = True

                line_count += 1

    # Generate global dictionary
    def __generate_global_dictionary(self, header):

        # Initialize global dictionary
        global_dict = {}

        for header_i in header:
           global_dict[header_i]  = self.__list_from_key(header_i)

        return global_dict



    def __list_from_key(self, input_key):

        for filename in self.__filename_values:
            file_key_values = self.__filename_values[filename]

            for key in file_key_values:
                if (key == input_key):
                    return file_key_values[key]

    # Generate total header for output file
    def __generate_header(self):
        file_count = 0
        names_list = []

        for file_id in self.__filename_values:
            values = self.__filename_values[file_id]
            
            key_list = []

            for key in values:
                key_list.append(key)

            # Remove first element except for the first list
            if (file_count != 0):
                key_list.pop(0)

            # Total names lost
            names_list += key_list

            # Update file count
            file_count += 1

        return names_list


    def parse_data(self):
        for key in self.__filename_values:
            self.__parse_file(key)

    def get_data(self):
        self.parse_data()
        return self.__filename_values

    def write_data(self, filename=''):

        # Check filename and assign default
        if filename == '':
            filename = self.__default_output_filename

        # Generate header
        header = self.__generate_header()

        # Generate global dictionary
        global_dict = self.__generate_global_dictionary(header)

        # Total number of measurements
        measurements_num = len(global_dict[header[0]])

        # Create file data
        file_data = []
        file_data.append(header)

        for i in range(measurements_num):
            row_to_write = []
            for key in global_dict:
                row_to_write.append(global_dict[key][i])

            file_data.append(row_to_write)

        f = open(filename, 'w')

        with f:
            writer = csv.writer(f)
            for row in file_data:
                writer.writerow(row)




def data_script_main():
    adams_parser = AdamsDataParser()

    # parse data
    adams_parser.parse_data()

    # write data to file
    adams_parser.write_data()



if __name__ == "__main__":
    data_script_main()
