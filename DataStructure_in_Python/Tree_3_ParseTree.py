import Tree_2_BinaryTreeClass_byNode
from Tree_2_BinaryTreeClass_byNode import *
import stack_Class 
from stack_Class import Stack
import operator

def buildParseTree(fpexp):
    fplist = fpexp.split()
    pStack = Stack()
    eTree = BinaryTree('')
    pStack.push(eTree)
    currentTree = eTree
    for i in fplist:
        if i == '(':
            currentTree.insertLeft('')
            pStack.push(currentTree)
            currentTree = currentTree.getLeftChild()
        elif i not in ['+', '-', '*', '/', ')']:
            currentTree.setRootVal(int(i))
            parent = pStack.pop()
            currentTree = parent
        elif i in ['+', '-', '*', '/']:
            currentTree.setRootVal(i)
            currentTree.insertRight('')
            pStack.push(currentTree)
            currentTree = currentTree.getRightChild()
        elif i == ')':
            currentTree = pStack.pop()
        else:
            raise ValueError
    return eTree

pt = buildParseTree("( ( 100 + 5 ) * 3 )")
pt.postorder()

def evaluate(parseTree):
    opers = {'+':operator.add, '-':operator.sub, '*':operator.mul, '/':operator.truediv}

    leftC = parseTree.getLeftChild()
    rightC = parseTree.getRightChild()

    if leftC and rightC:
        fn = opers[parseTree.getRootVal()]
        return fn(evaluate(leftC),evaluate(rightC))
    else:
        return parseTree.getRootVal()
##### My own version ######################
def calculate_parseTree(t):
    opers = {'+':operator.add, '-':operator.sub, '*':operator.mul, '/':operator.truediv}    
    if t.key in ['+','-','*','/']:
        # if t.key == '+':
        #     return calculate_parseTree(t.leftChild) + calculate_parseTree(t.rightChild)
        # if t.key == '-':
        #     return calculate_parseTree(t.leftChild) - calculate_parseTree(t.rightChild)
        # if t.key == '*':
        #     return calculate_parseTree(t.leftChild) * calculate_parseTree(t.rightChild)
        # if t.key == '/':
        #     return calculate_parseTree(t.leftChild) / calculate_parseTree(t.rightChild)
#############  a more consice way #######################
        t_op = opers[t.key]
        return t_op(calculate_parseTree(t.leftChild),calculate_parseTree(t.rightChild))
    else:
        return t.key
def printexp(tree):
    sVal = ""
    if tree:
        sVal = '(' + printexp(tree.getLeftChild())
        sVal = sVal + str(tree.getRootVal())
        sVal = sVal + printexp(tree.getRightChild())+')'
    return sVal
res = calculate_parseTree(pt)
res2 = printexp(pt)
print res2
print res
#defined and explained in the next section
