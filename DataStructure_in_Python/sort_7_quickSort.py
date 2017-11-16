
alist = [1,3,5,7,9,2,4,6]


def q_sort(num_list,start,end):
	flag = num_list[end]
	i,j = start-1,start
	while j < end:
		if num_list[j]<=flag:
			### if we want to sort from big->small : num_list[j]>=flag
			i+=1
			num_list[i],num_list[j] = num_list[j],num_list[i]
			
		j+=1
	num_list[i+1],num_list[end] = num_list[end],num_list[i+1]
	

	
	return i+1


def quickSort(num_list,start,end):
	
	if start >= end:
		return 
	
	mid = q_sort(num_list,start, end)
	quickSort(num_list,start, mid-1)
	quickSort(num_list,mid+1, end)


quickSort(alist,0,len(alist)-1)
print alist






