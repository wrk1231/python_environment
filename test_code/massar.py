class Stack(list):## define a stack data structure for further use
     def __init__(self):
         self.items = []
     def isEmpty(self):
         return self.items == []
     def push(self, item):
         self.items.append(item)
     def pop(self):
         return self.items.pop()
     def peek(self):
         return self.items[len(self.items)-1]
     def size(self):
         return len(self.items)

##pre process for our input string:
def preprocess(input_string):
    symbolString = []
    for i in range(len(input_string)):
        if input_string[i] == '(' or input_string[i] == ')':
            symbolString.append((input_string[i],i))
    return symbolString

def parChecker(input_string): 
    symbolString = preprocess(input_string)
    record_list = [] ### used to record the location of the '(' & ')' pairs
    s = Stack() ## stack for match '(' and ')'
    index_s = Stack()
    balanced = True
    index = 0
    while index < len(symbolString) and balanced:
        symbol = symbolString[index][0]
        if symbol == "(":
            s.push(symbolString[index])
            
        else:
            if s.isEmpty():
                balanced = False
            else:
                record_list.append(symbolString[index])
                record_list.append(s.pop())
               
        index = index + 1

    if balanced and s.isEmpty():
        result = [] ## write down the match result of parenthesis
        for x in record_list:
            result.append(x[1])
        return result
    else:
        return 'Parenthesis can not be matched'

def find_match(input_string,num):
    temp_result = parChecker(input_string)
    for i in range(len(temp_result)):
        if num == temp_result[i]:
            if i%2 == 0:
                return temp_result[i+1]
            else:
                return temp_result[i-1]
input_1 =  "Sometimes (when I nest them (my parentheticals) too much (like this (and this))) they get confusing."
print find_match(input_1,10)
