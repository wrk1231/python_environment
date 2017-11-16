from node_Class import Node

class UnorderedList(Node):

    def __init__(self):
        self.head = None

    def isEmpty(self):
    	return self.head == None

    def add(self,item):
	    temp = Node(item)
	    temp.setNext(self.head)
	    self.head = temp
	def size(self):
		pass