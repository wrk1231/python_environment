def bubbleSort(list):
	m = len(list)
	for i in range(m):
		for j in range(i,m-1):
			if list[j] > list[j+1]:
				
				list[j],list[j+1] = list[j+1],list[j]
			
	return list
