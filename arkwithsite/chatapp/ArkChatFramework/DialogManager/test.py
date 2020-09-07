'''
Created on 2018. 2. 9.

@author: phs
'''



import sys, json


#Read data from stdin
def read_in():
    lines = sys.stdin.readlines()
    #question = sys.stdin.read()
#     question = {}
#     question['userId'] = "arkwith1"
#     question['message'] = "?•ˆ?…•?•˜?„¸?š”."
    #question = {userId : "arkwith1", message : "?•ˆ?…•?•˜?„¸?š”."}
    # Since our input would only be having one line, parse our JSON data from that
    return json.loads(lines[0])
#     return question

def main():
    #get our data as an array from read_in()
    answer = read_in()
    print(answer.get('userId') + " : " + answer.get('message'))
    #lines = read_in()

    # Sum  of all the items in the providen array
#     total_sum_inArray = 0
#     for item in lines:
#         total_sum_inArray += item
# 
#     #return the sum to the output stream
#     print(total_sum_inArray)

# Start process
if __name__ == '__main__':
    main()
