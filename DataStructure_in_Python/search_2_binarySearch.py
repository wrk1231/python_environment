############################  simple version #####################################
def binarySearch(aList,item):
	start = 0
	end = len(aList) -1
	Found = False
	while not Found and(start < end):
		mid = (start + end)/2

		if aList[mid] == item:
			Found = True

		else:
			if aList[mid] < item:
				start = mid +1
			else:
				end = mid

	return Found



print binarySearch([1,2,3,4,5,6,7,8,9], 6)


######################### recursive version #########################################


def binarySearch(alist, item):
	    if len(alist) == 0:
	        return False
	    else:
	        midpoint = len(alist)//2
	        if alist[midpoint]==item:
	          return True
	        else:
	          if item<alist[midpoint]:
	            return binarySearch(alist[:midpoint],item)
	          else:
	            return binarySearch(alist[midpoint+1:],item)

testlist = [0, 1, 2, 8, 13, 17, 19, 32, 42,]
print(binarySearch(testlist, 3))
print(binarySearch(testlist, 13))
