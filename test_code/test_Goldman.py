

# def special_array(inputstring,sublen):
# 	empty_list = []
# 	for i in xrange(len(inputstring) - sublen + 1 ):
# 		empty_list.append(inputstring[i:i+sublen])

# 	return_set = set(empty_list)
# 	return_list = list(return_set)

# print special_array('caaab', 2)

# def countPairs(k,a):#a: array
# 	res = 0
# 	for i in range(len(a)):
# 		for j in range(i+1,len(a)):
# 			if a[i]+a[j] == k:
# 				res += 1
# 	return res
# input = 'racecars'
# for x in input:
# 	if input.count(x) == 1:
# 		print x
# 		break
# def sumof2(a,k):
# 	emtpy_dic = {}
# 	total = 0
# 	for x in a:
# # 		emtpy_dic[x] = a.count(x)
# # 	for x in a:
# # 		total += emtpy_dic[k - x]
# # 		if (x+x) == k:
# # 			total -= 1
# # 	total = total/2
# # 	return total

# # def highest_average(scores):
# # 	highest = -1000
	
# # 	for pair in scores:
# # 		sum_of_this_pair = 0.0

# # 		for num in pair[1:]:
# # 			num = float(num)
# # 			if num < 0.0:
# # 				num = int(num) - 1 

# # 			sum_of_this_pair += num

# # 		ave = sum_of_this_pair/(len(pair) - 1)
# # 		if ave >= highest:
# # 			highest = ave

# # 	print int(highest)


# # a = ['','100']
# # highest_average(a)


# def s_count(input):
# 	res = ''
# 	uniqueset = []
#  	for x in input:
#  		if x not in uniqueset:
#  			uniqueset.append(x)
# 	 		res += str(input.count(x)) 
# 	 		res += x
# 	return res


#  	for  i in range(len(input)):
#  		if i==0:





# print s_count('GGrrYYYYY')

# def inner_product(array1,array2):
# 	res = 0
# 	if len(array1)!= len(array2):
# 		return res
# 	else:
# 		for i in range(len(array1)):
# 			res += array1[i]*array2[i]
# 		return res

# def stairs(n):
# 	res = [None]*1000
# 	res[0] = 0
# 	for i in range(1,n+1):
# 		if i == 1:
# 			res[i] = 1
# 		elif i ==2:
# 			res[i] = 2
# 		elif i == 3:
# 			res[i] = 4
# 		elif i > 3:
# 			res[i] = res[i-1] + res[i-2] + res[i-3]
# 	return res[n]

# print stairs(17)




















