class BinaryTree:
    def __init__(self,rootObj):
        self.key = rootObj
        self.leftChild = None
        self.rightChild = None

    def insertLeft(self,newNode):
        if self.leftChild == None:
            self.leftChild = BinaryTree(newNode)
        else:
            t = BinaryTree(newNode)
            t.leftChild = self.leftChild
            self.leftChild = t

    def insertRight(self,newNode):
        if self.rightChild == None:
            self.rightChild = BinaryTree(newNode)
        else:
            t = BinaryTree(newNode)
            t.rightChild = self.rightChild
            self.rightChild = t

    def getRightChild(self):
        return self.rightChild

    def getLeftChild(self):
        return self.leftChild

    def setRootVal(self,obj):
        self.key = obj

    def getRootVal(self):
        return self.key
    def preorder(self):
        print(self.key)
        if self.leftChild:
            self.leftChild.preorder()
        if self.rightChild:
            self.rightChild.preorder()

    def postorder(self):
        if self.leftChild:
            self.leftChild.postorder()
        if self.rightChild:
            self.rightChild.postorder()
        print(self.key)

    def inorder(self):
        if self.leftChild:
            self.leftChild.inorder()
        print(self.key)
        if self.rightChild:
            self.rightChild.inorder()
        


##################### My Own Code ###################
# class myBinaryTree(object):
#     def __init__(self,root_obj):
#         self.root = root_obj
#         self.left = None
#         self.right = None

#     def insert_left(self,left_obj):
#         if self.left == None:
#             self.left = myBinaryTree(left_obj)
#         else:
#             t = BinaryTree(left_obj)
#             t.left = self.left
#             self.left = t

#     def insert_right(self,right_obj):
#         if self.right == None:
#             self.right = BinaryTree(right_obj)
#         else:
#             t = BinaryTree(right_obj)
#             t.right = self.right
#             self.right = t      

#     def get_left(self):
#         return self.left

#     def get_right(self):
#         return self.right

#     def set_root(self,value):
#         self.root = value

#     def get_root(self):
#         return self.root