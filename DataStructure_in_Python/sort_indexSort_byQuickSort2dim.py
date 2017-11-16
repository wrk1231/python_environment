
alist = [[1,3,5,7,9,2,4,6],[0,1,2,3,4,5,6,7]]



def q_sort(num_list,start,end):
	flag = num_list[0][end]
	i,j = start-1,start
	while j < end:
		if num_list[0][j]<=flag:
			### if we want to sort from big->small : num_list[j]>=flag
			i+=1
			num_list[0][i],num_list[0][j] = num_list[0][j],num_list[0][i]
			num_list[1][i],num_list[1][j] = num_list[1][j],num_list[1][i]

			
		j+=1
	num_list[0][i+1],num_list[0][end] = num_list[0][end],num_list[0][i+1]
	num_list[1][i+1],num_list[1][end] = num_list[1][end],num_list[1][i+1]

	
	return i+1
 

def quickSort(num_list,start,end):
	
	if start >= end:
		return 
	
	mid = q_sort(num_list,start, end)
	quickSort(num_list, start, mid-1)
	quickSort(num_list, mid+1, end)


quickSort(alist,0,len(alist[0])-1)
print alist






