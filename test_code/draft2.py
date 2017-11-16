
dp = [0]*100
for i in range (100):
	if i == 0 or i ==1:
		dp[i] = 1
	else :
		dp[i] = dp[i-1]+dp[i-2]

for i in range(90):
	print dp[i],' '