
alist = [1.1, 2.3, 5.6, 9.9, 2.1, 1.8, 3.7, 6.66, 1.23, 4.55]
index_list = [i for i in range(len(alist))]

def q_sort(num_list,index_list,start,end):
	flag = num_list[end]
	i,j = start-1,start
	while j < end:
		if num_list[j]>=flag:
			### if we want to sort from big->small : num_list[j]>=flag
			i+=1
			num_list[i],num_list[j] = num_list[j],num_list[i]
			index_list[i],index_list[j] = index_list[j],index_list[i]
		j+=1
	num_list[i+1],num_list[end] = num_list[end],num_list[i+1]
	index_list[i+1],index_list[end] = index_list[end],index_list[i+1]
	
	return i+1
 

def quickSort(num_list,start,end):
	
	if start >= end:
		return 
	
	mid = q_sort(num_list,index_list,start, end)
	quickSort(num_list, start, mid-1)
	quickSort(num_list, mid+1, end)


quickSort(alist,0,len(alist)-1)
print alist,index_list






