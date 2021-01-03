import functions
pos_indx= functions.constract("D:\Abdoo\Level 3\Semester 1\IR\Project\documents")
while (1):
    print("enter your query")
    query = input()
    print("enter 1 to find by positional and 2 for vector space ")
    i = input()
    if (i == '1'):
        result= functions.find_query(query,pos_indx)
        if(result != 0):
            print("There's" ,result[0],"similar strings have the text you entered")
            documents = result[1].keys()
            for id in documents:
                print("document ",id+1)
        else:
            print("There's" ,0,"similar strings have the text you entered")
    elif (i == '2'):
        result = functions.find_args('D:\Abdoo\Level 3\Semester 1\IR\Project\documents',pos_indx,query)
        sorted_dict = dict( sorted(result.items(),
                           key=lambda item: item[1],
                           reverse=True))
        print(sorted_dict)
    else:
        print("!!!Wrong input please try again with a valid one!!!")
        exit()

        #D:\Abdoo\Level 3\Semester 1\IR\Project\documents