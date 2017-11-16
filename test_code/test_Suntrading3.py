def perms(elements):
    if len(elements) <=1:
        yield elements
    else:
        for perm in perms(elements[1:]):
            for i in range(len(elements)):
                yield perm[:i] + elements[0:1] + perm[i:]

def inner_product(array1,array2):
	res = 0
	if len(array1)!= len(array2):
		return res
	else:
		for i in range(len(array1)):
			res += array1[i]*array2[i]
		return res

def max_profit(arr):			
	tran = len(arr)/2
	res = []
	while(tran >= 0):
		#### permulates the array of buy/sell
		elements = [0] * len(arr)
		for i in range(tran):
			elements[i] = 1
		for i in range(tran,2*tran):
			elements[i] = -1
		for i in range(2*tran,len(arr)):
			elements[i] = 0

		for x in perms(elements):
			res.append(inner_product(arr,x))

		tran -= 1
	return max(res)

print max_profit([1,2,3,4])	

