import os

#file=open("exemple.txt", "w")
#file.write("Hello,world!")
#file.close()

#with open("exemple2.txt", "w") as file:
 #   file.write("Super duper")

#with open("exemple2.txt", "r") as file2:
#    data=file2.read()
#    print(data)

#with open("exemple2.txt", "r") as file3:
#    for line in file3.readlines():
#        print(line)

#printing first line of the file
def get_first_line_of_file():
    with open("exemple2.txt", "r") as file3:
        data=file3.readline()
        #first_elem=data[0]
        print(data)

get_first_line_of_file()

#we use "a" when wwe want to append at the end of the file
#scandir to see anyhting you have in a dir (batter to use absolute path) - from importaded library