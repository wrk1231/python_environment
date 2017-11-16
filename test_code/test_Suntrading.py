# def dice_prob(die_faces,total_sum):
# 	### first step: short cut the problem
# 	if (total_sum > max(die_faces)*2) or (total_sum < min(die_faces)*2):
# 		return 0
# 	### calculate by 	
# 	sum_list = []
# 	for i in range(len(die_faces)):
# 		for j in range(len(die_faces)):
# 			sum_list.append(die_faces[i] + die_faces[j])

# 	if total_sum not in sum_list:
# 		return 0;
# 	else:
# 		res = float(sum_list.count(total_sum))/float(len(sum_list))
# 		return res
# print dice_prob([1,2,3,4,5,6], 19)
def inner_product(array1,array2):
	res = 0
	if len(array1)!= len(array2):
		return res
	else:
		for i in range(len(array1)):
			res += array1[i]*array2[i]
		return res
print inner_product([1,2,3], [1,2,3])