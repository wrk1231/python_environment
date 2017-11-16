# -*- coding: utf-8 -*-
def get_shanno_entropy(self,values):
    "get Shanno Entropy due to the list of data"
    uniq_vals = set(values)
    val_nums = {key:values.count(key) for key in uniq_vals}
    probs = [v/len(values) for k,v in val_nums.items()]
    entropy = sum(-[prob*log2(prob) for prob in probs])
    return entropy