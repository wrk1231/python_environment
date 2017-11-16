## first define merge function
def merge(list1,list2):
    len_list1 = len(list1)
    len_list2 = len(list2)
    res = []
    i,j = 0,0
    while i<len_list1 and j<len_list2:
        if list1[i] <= list2[j]:
            res.append(list1[i])
            i += 1
        else:
            res.append(list2[j])
            j += 1

    res += list1[i:]
    res += list2[j:]

    return res

## define by recursion
def mergeSort(list):
    if (len(list) <= 1):
        return list

    half = len(list)/2
    left = mergeSort(list[:half])
    right = mergeSort(list[half:])       
    return merge(left, right)








alist = [1,3,5,7,9,2,4,6,8,10]
print mergeSort(alist)