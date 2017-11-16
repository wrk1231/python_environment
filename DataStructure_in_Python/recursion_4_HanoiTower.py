def hanoi(height,fromPole, toPole, withPole):
	if height == 1:
		print fromPole,"-->>",toPole
	else:
		hanoi(height-1, fromPole,withPole,toPole)
		print fromPole,"-->>",toPole
		hanoi(height-1, withPole, toPole, fromPole)

hanoi(3, 'A', 'B', 'C')