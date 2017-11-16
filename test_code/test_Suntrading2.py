def num_bits(a, b):
	res = 0
	if a > b:
		res = 0
		return res
	else:
		for x in range(a,b+1):
			bin_x = bin(x).count('1')
			res += float(bin_x)/float(b-a+1)
		return res
print num_bits(1, 2)