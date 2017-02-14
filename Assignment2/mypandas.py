import datetime
import math
class DataFrame(object):
    def __init__(self, list_of_lists):
            self.data = list_of_lists[1:]
            self.header= list_of_lists[0]
            if len(self.header)>len(set(self.header)):
                raise Exception('Identical headers found')
            for i in range(len(self.data)):
                for j in range(len(self.data[i])):
                    self.data[i][j]=self.data[i][j].strip()
    def __getitem__(self, item):
        return self.data[item]
    def min(self,column_name):
        indx=[i for i in range(len(self.header)) if self.header[i]==column_name]
        if not indx:
            raise Exception('No such Column found!')
        elif indx[0] in [1,3,4,5,6,7]:
            raise Exception('Not a Valid Column to operate on')
        elif indx[0] in [0,8,9]:
            temp_list = []
            for i in range(len(self.data)):
                temp_list.append(self.data[i][indx[0]])
                temp_list[i]=datetime.datetime.strptime(temp_list[i],"%x %H:%M")
        elif indx[0] in [10,11]:
            temp_list = []
            for i in range(len(self.data)):
                temp_list.append(self.data[i][indx[0]])
                temp_list[i] = float(temp_list[i]);
        else:
            temp_list=[]
            for i in range(len(self.data)):
                temp_list.append(self.data[i][indx[0]])
                temp_list[i]=temp_list[i].replace(",","")
                temp_list[i]=int(temp_list[i])
        return min(temp_list)
    def max(self,column_name):
        indx=[i for i in range(len(self.header)) if self.header[i]==column_name]
        if not indx:
            raise Exception('No such Column found!')
        elif indx[0] in [1,3,4,5,6,7]:
            raise Exception('Not a Valid Column to operate on')
        elif indx[0] in [0,8,9]:
            temp_list = []
            for i in range(len(self.data)):
                temp_list.append(self.data[i][indx[0]])
                temp_list[i]=datetime.datetime.strptime(temp_list[i],"%x %H:%M")
        elif indx[0] in [10,11]:
            temp_list = []
            for i in range(len(self.data)):
                temp_list.append(self.data[i][indx[0]])
                temp_list[i] = float(temp_list[i]);
        else:
            temp_list=[]
            for i in range(len(self.data)):
                temp_list.append(self.data[i][indx[0]])
                temp_list[i]=temp_list[i].replace(",","")
                temp_list[i]=int(temp_list[i])
        return max(temp_list)
    def sum(self,column_name):
        indx=[i for i in range(len(self.header)) if self.header[i]==column_name]
        if not indx:
            raise Exception('No such Column found!')
        elif indx[0] in [0,1,3,4,5,6,7,8,9]:
            raise Exception('Not a Valid Column to operate on')
        elif indx[0] in [10,11]:
            temp_list = []
            for i in range(len(self.data)):
                temp_list.append(self.data[i][indx[0]])
                temp_list[i] = float(temp_list[i]);
        else:
            temp_list=[]
            for i in range(len(self.data)):
                temp_list.append(self.data[i][indx[0]])
                temp_list[i]=temp_list[i].replace(",","")
                temp_list[i]=int(temp_list[i])
        return sum(temp_list)
    def mean(self,column_name):
        return self.sum(column_name)/len(self.data)
    def median(self,column_name):
        indx=[i for i in range(len(self.header)) if self.header[i]==column_name]
        if not indx:
            raise Exception('No such Column found!')
        elif indx[0] in [0,1,3,4,5,6,7,8,9]:
            raise Exception('Not a Valid Column to operate on')
        elif indx[0] in [10,11]:
            temp_list = []
            for i in range(len(self.data)):
                temp_list.append(self.data[i][indx[0]])
                temp_list[i] = float(temp_list[i]);
        else:
            temp_list=[]
            for i in range(len(self.data)):
                temp_list.append(self.data[i][indx[0]])
                temp_list[i]=temp_list[i].replace(",","")
                temp_list[i]=int(temp_list[i])
        temp_list=sorted(temp_list,key=float);
        return temp_list[(len(self.data)/2)-1]+temp_list[len(self.data)/2]/2
    def std(self, column_name):
        indx = [i for i in range(len(self.header)) if self.header[i] == column_name]
        if not indx:
            raise Exception('No such Column found!')
        elif indx[0] in [0, 1, 3, 4, 5, 6, 7, 8, 9]:
            raise Exception('Not a Valid Column to operate on')
        elif indx[0] in [10, 11]:
            temp_list = []
            for i in range(len(self.data)):
                temp_list.append(self.data[i][indx[0]])
                temp_list[i] = float(temp_list[i]);
        else:
            temp_list = []
            for i in range(len(self.data)):
                temp_list.append(self.data[i][indx[0]])
                temp_list[i] = temp_list[i].replace(",", "")
                temp_list[i] = int(temp_list[i])
        mean=self.mean(column_name)
        sum_diff=0
        for i in temp_list:
            sum_diff=sum_diff+(i-mean)**2
        return math.sqrt(sum_diff/len(temp_list))
    def add_rows(self,lst):
        if(isinstance(lst[0],list)):
            for i in range(len(lst)):
                if((len(lst[i])!=len(self.data[0]))):
                    raise Exception("Number of columns to be added is not same as columns in DataFrame")
        else:
            if (len(lst) != len(self.data[0])):
                raise Exception("Number of columns to be added is not same as columns in DataFrame")
        if (isinstance(lst[0], list)):
            self.data.extend(lst)
        else:
            self.data.append(lst)
    def add_column(self, lst, colmn_name):
        if(len(lst)!=len(self.data)):
            raise Exception("Number of rows to be added is not same as rows in DataFrame")
        self.header.append(colmn_name)
        for i in range(len(self.data)):
            self.data[i].append(lst[i])
infile=open("SalesJan2009.csv")
lines=infile.readlines()
lines=lines[0].split('\r')
data=[l.split(',')for l in lines]
things = lines[559].split('"')
data[559] = things[0].split(',')[:-1] + [things[1]] + things[-1].split(',')[1:]
df=DataFrame(data)
