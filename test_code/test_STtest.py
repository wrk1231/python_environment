# li = [1,2,3,4]
# print max(li)
# def factor(n):
# 	res = [None] * 60
# 	res[0] = 1
# 	for x in range(1,n+1):
# 		if x == 1:
# 			res[1] = 1
# 		else:
# 			 res[x] = x*res[x-1]

# 	return res[n]
# 	
# def perms(elements):
#     if len(elements) <=1:
#         yield elements
#     else:
#         for perm in perms(elements[1:]):
#             for i in range(len(elements)):
#                 yield perm[:i] + elements[0:1] + perm[i:]
# # for item in list(perms([1, 2, 3,4])):
# #     print type(item)
# tran = 3
# elements = [0] * 7
# for i in range(tran):
# 				elements[i] = 1
# for i in range(tran,2*tran):
# 	elements[i] = -1
# for i in range(2*tran,7):
# 	elements[i] = 0
# for x in perms(elements):
# 	print x
for i in range(1,7):
	print i

