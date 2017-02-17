import csv
import datetime
from collections import OrderedDict
from operator import itemgetter
from collections import defaultdict

class Series(list):
    def __init__(self, list_of_values):
        self.data = list_of_values

    def __eq__(self, other):
        ret_list = []

        for item in self.data:
            ret_list.append(item == other)

        return ret_list

    def __gt__(self, other):
        ret_list = []

        for item in self.data:
            ret_list.append(item > other)

        return ret_list

    def __ge__(self, other):
        ret_list = []

        for item in self.data:
            ret_list.append(item >= other)

        return ret_list

    def __lt__(self, other):
        ret_list = []

        for item in self.data:
            ret_list.append(item < other)

        return ret_list

    def __le__(self, other):
        ret_list = []

        for item in self.data:
            ret_list.append(item <= other)

        return ret_list



class DataFrame(object):

    @classmethod
    def from_csv(cls, file_path, delimiting_character=',', quote_character='"'):
        """
        Opens a file using the csv module.
        https://docs.python.org/2/library/csv.html
        :param file_path: a string representing the path to the file e.g. ~/Documents/textfile.txt
        :param delimiting_character: a string representing the char(s) that separate columns in a row of data
        :param quote_character: a string for the char(s) that surround values in a column, e.g. "value" -> "
        :return: returns a DataFrame object with the data from the csv file at file_path
        """
        # opens a file in read, universal newline mode and store the file object in infile for this with block
        with open(file_path, 'rU') as infile:

            # create a csv.reader object to process the file and store it in the variable reader
            reader = csv.reader(infile, delimiter=delimiting_character, quotechar=quote_character)

            # creates a variable data and assigns it an empty list
            data = []

            # for each row read (past tense) in from the csv by reader
            for row in reader:
                # append a row (a list) to data
                data.append(row)

            # return an instantiated object of the current class (DataFrame if this is my original code)
            # passing data into the list_of_lists argument
            return cls(list_of_lists=data)
        # end of with block, infile is closed automatically



    def __init__(self, list_of_lists, header=True):

        list_of_lists = [[item1.strip() for item1 in column] for column in list_of_lists]
        for i in range(0, len(list_of_lists)):
            for j in range(0, len(list_of_lists[i])):
                try:
                    list_of_lists[i][j] = float(list_of_lists[i][j].replace(",", ""))
                except:
                    try:
                         list_of_lists[i][j] = datetime.datetime.strptime(list_of_lists[i][j], "%x %H:%M")
                    except:
                        pass

        # if what was passed into header is True or has a value that is equivalent to false, i.e. bool(header) is True
        if header: # then do this

            # set the header attribute of this DataFrame object that is being instantiated to the first row of what
            # was passed into list_of_lists
            self.header = list_of_lists[0]
            # set the data attribute of this DataFrame object to all the rows after the first row
            # (remember things start from 0 in python not 1)
            self.data = list_of_lists[1:]

        # if what was passed into header is False or has a value that is equivalent to false, i.e. bool(header) is False
        else: # then do this
            # set the data attr to list_of_lists (there's no header here)
            self.data = list_of_lists

            # create a variable called generated_header and set it as an empty list
            generated_header = []

            # choose the first row of the data set as a sample row to iterate through the columns, enumerate it so
            # we can keep a count of what index we're at in the row
            for index, column in enumerate(self.data[0]): # for each index and row in this first row of data
                # append a string that is 'column' concatenated with a string of the current index + 1
                generated_header.append('column' + str(index + 1))

            # set our header attr to this generated_header
            self.header = generated_header

        # we're now outside of the if/else

        # create an empty list called ordered_dict_rows
        ordered_dict_rows = []

        # for each row in self.data
        for row in self.data:
            # for each iteration of the above loop create an empty list called ordered_dict_data
            ordered_dict_data = []

            # for each index and value of this row in self.data
            for index, row_value in enumerate(row):
                # append a tuple to ordered_dict_data that contains the value in header that's at the same index as
                # this value in row
                ordered_dict_data.append((self.header[index], row_value))

            # outside of the inner loop (for index, row_value in enumerate(row))
            # ordered_dict_data now contains a list of tuples

            # create an OrderedDict using ordered_dict_data and assign it to ordered_dict_row
            # now we've converted this row to an OrderedDict!
            ordered_dict_row = OrderedDict(ordered_dict_data)

            # append ordered_dict_row to ordered_dict_rows
            ordered_dict_rows.append(ordered_dict_row)

        # now ordered_dict_rows has all the data from before but each row is an OrderedDict instead of just a list of
        # values
        # assign these to the data attr of this DataFrame object
        self.data = ordered_dict_rows



    def group_by(self,group_column, column, agg):
        my_dd = defaultdict(list)

        for i in range(0, len(self.data)):
            if(isinstance(group_column,list)):
                [my_dd[self.data[i][grp]].append(self.data[i][column])for grp in group_column]
            else:
                my_dd[self.data[i][group_column]].append(self.data[i][column])

            #print my_dd[self.data[i][group_column]]

        print_out = []
        for key in my_dd:
            print_out.append(str(key) + " : " + str(agg(my_dd[key])))

        return print_out

    def __getitem__(self, item):
        """
        the __getitem__ magic method is called whenenver you use square brackets on an object, e.g.  obj[item]

        :param item: this is the object that is inside of the brackets, e.g. df[item]
        :return: returns different things based on what item is, see below
        """
        # this is for rows only
        # if item is an integer or a slice object
        if isinstance(item, (int, slice)):
            return self.data[item]

        # this is for columns only
        # if item is a string or unicode object
        elif isinstance(item, (str, unicode)):
            return Series([row[item] for row in self.data])

        # this is for rows and columns
        # if item is a tuple
        elif isinstance(item, tuple):
            if isinstance(item[0], list) or isinstance(item[1], list):

                if isinstance(item[0], list):
                    rowz = [row for index, row in enumerate(self.data) if index in item[0]]
                else:
                    rowz = self.data[item[0]]

                if isinstance(item[1], list):
                    if all([isinstance(thing, int) for thing in item[1]]):
                        return [[column_value for index, column_value in enumerate([value for value in row.itervalues()]) if index in item[1]] for row in rowz]
                    elif all([isinstance(thing, (str, unicode)) for thing in item[1]]):
                        return [[row[column_name] for column_name in item[1]] for row in rowz]
                    else:
                        raise TypeError('What the hell is this?')

                else:
                    return [[value for value in row.itervalues()][item[1]] for row in rowz]
            else:
                if isinstance(item[1], (int, slice)):
                    return [[value for value in row.itervalues()][item[1]] for row in self.data[item[0]]]
                elif isinstance(item[1], (str, unicode)):
                    return [row[item[1]] for row in self.data[item[0]]]
                else:
                    raise TypeError('I don\'t know how to handle this...')

        # only for lists of column names
        elif isinstance(item, list):
            if all([isinstance(item1, bool) for item1 in item]):
                ret_list = []
                for i in range(0, len(item)):
                    if item[i]:
                        ret_list.append(self.data[i])
                return ret_list
            else:
                return [[row[column_name] for column_name in item] for row in self.data]

    def get_rows_where_column_has_value(self, column_name, value, index_only=False):
        if index_only:
            return [index for index, row_value in enumerate(self[column_name]) if row_value==value]
        else:
            return [row for row in self.data if row[column_name]==value]

    def sort_by(self,column, choose_reverse = False):
       # header_dict = {i:col_name for i,col_name in enumerate(self.header)}
       if(isinstance(column,str)):
            self.data =  sorted(self.data, key=lambda data_list_item: data_list_item[column], reverse=choose_reverse)
            print 'true'
       else:
            self.data = sorted(self.data, key=lambda data_list_item: [data_list_item[col] for col in column], reverse=choose_reverse)


       return self.data

def avg(list_of_values):
    return sum(list_of_values)/float(len(list_of_values))


infile = open('SalesJan2009.csv')
lines = infile.readlines()
lines = lines[0].split('\r')
data = [l.split(',') for l in lines]
things = lines[559].split('"')
data[559] = things[0].split(',')[:-1] + [things[1]] + things[-1].split(',')[1:]


df = DataFrame(list_of_lists=data)
# get the 5th row
fifth = df[4]
sliced = df[4:10]

#Task 3
#print(df.group_by(['Payment_Type','Product'],'Price',avg))
#Task 2
#print(df[df["Transaction_date"] <= datetime.datetime.strptime("1/1/09 1:55","%x %H:%M")])
#print(df[df["Price"] <= 900])
#Task 1
# lo = df.sort_by("Transaction_date")
# print(lo)

# print(df[:5])
# print(df.header)


