def sumpair(target,num):
	num.sort()
	num.insert(0,None)
	num.append(None)
	i = 0
	result = 0
	while(i<=len(num) - 2):
		count_i = 1		
		while(num[i+1] == num[i]):
			i += 1
			count_i += 1
		#print '\ni:',i,', count_i:',count_i,', num[i]:',num[i]
		j = len(num)-1
		while(j>=0):
			count_j = 1
			if(j>=1):
				while(num[j-1] == num[j]):
					j -= 1
					count_j += 1
			#print 'j:',j,'count_j:',count_j,', num[j]:',num[j]			
			if(num[i]!=None and num[j]!= None and num[i]+num[j] == target):
				if(num[i]!=num[j]):
					result += (count_j*count_i)
				elif(num[i] == num[j]):
					result += count_i*(count_i-1)			
			j -= 1
		i += 1	

	return result/2












