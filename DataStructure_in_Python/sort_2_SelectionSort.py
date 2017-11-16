def selectionSort(list):
	m = len(list)

	for i in range(m):
		maxnum = i
		for j in range(i+1,m):
			
			if list[j] > list[maxnum]:
				maxnum = j
				
		list[i],list[maxnum] = list[maxnum],list[i]

	return list


a = [2,4,5,7,1,9,3,4]
print selectionSort(a)