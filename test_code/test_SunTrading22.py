def max_chain(arr, m):
	dp = [0] * (len(arr)+1)
	dp[0] = 0
	for x in range(1,m):
		dp[x] = dp[x-1] + max(0,arr[x-1])
	for i in range(m,len(arr)+1):
		maxnum = dp[i-2]
		## dp[i] = max{dp[j] + \sum{arr[k]}}
		t =1
		while t<m:
			j,sumnum = 0,0
			while j<t:
				sumnum+=arr[i-1-j]
				j+=1
			sumnum+=dp[i-1-t]
			t+=1
			if sumnum> maxnum:
				maxnum = sumnum
		dp[i] = maxnum




	return dp[len(arr)]
print max_chain([1,2,3,4,5,6], 6)