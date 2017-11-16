def insert_sort(lists):

    count = len(lists)
    for i in range(1, count):
        key = lists[i]
        j = i - 1
        while j >= 0:
            if lists[j] > key:
                lists[j + 1] = lists[j]
                lists[j] = key
            j -= 1
    return lists

alist = [1,3,5,7,9,2,4,6,8,10]
insert_sort(alist)
print(alist)