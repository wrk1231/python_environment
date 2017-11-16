def search_item_in_sequence(sequence,item):
	Found = False
	flag = 0
	while (not Found) and flag < len(sequence):
		if sequence[flag] == item:
			Found = True
		else:
			flag = flag+1
	return Found

print search_item_in_sequence([1,2,3,4,5], 6)
print sorted([1,4,5,8,22,7])