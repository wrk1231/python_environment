# def game_price(n, m):
# 	if m == 0:
# 		return float(n+1)/float(2)
# 	else:

# 		if game_price(n, m-1) != int (   game_price(n, m-1)      ):

# 			p_smaller_than_before = float(int(game_price(n, m-1)))/float(n)
# 			p_greater_than_before = 1 - p_smaller_than_before
# 			addnum = float( (int(game_price(n, m-1))+1)  + n )/float(2)
# 			return p_smaller_than_before*game_price(n, 0) + p_greater_than_before*addnum


# 		if game_price(n, m-1) == int (   game_price(n, m-1)      ):
# 			p_smaller_than_before = float(int(game_price(n, m-1)))/float(n)
# 			p_greater_than_before = 1 - p_smaller_than_before
# 			addnum = float(int(game_price(n, m-1))+1 +n)/float(2)
# 			return p_smaller_than_before*game_price(n, 0) + p_greater_than_before*addnum


# print game_price(4,3)
			
def game_price(n,m):
	if m == 0 :
		return float(n+1)/float(2)
	else:
		flag = int(game_price(n, m-1))
		return float((n - flag)*(n+flag+1))/float(n*2) + float(flag)/float(n)*game_price(n, m-1)
			
print game_price(6, 1)


