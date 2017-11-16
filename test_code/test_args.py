# -*- coding: utf-8 -*-


# def funargs(*args): #可以传入任意数量个参数（包括零个）
#     for i in args:
#         print i,

# funargs(1,2,3,4,5)
# list2 = (1,2,3,4,5,6,7,8,9,0)
# print type (list2),'\n'


# def fun_var_args(farg, *args):
#     print 'args:', farg
#     for value in args:
#         print 'another arg:',value

# fun_var_args(1,list2)

def fun_var_kwargs(farg, **kwargs):
    print 'args:',farg
    for key in kwargs:
        print 'another keyword arg:%s:%s' % (key, kwargs[key])

fun_var_kwargs(1, m1='1', m2='3', m4='5')


def fun_args_kwargs(*args, **kwargs):
    print 'args:', args
    print 'kwargs:', kwargs

args = [1, 2, 3, 4]
kwargs = {'name': 'BeginMan', 'age': 22}
fun_args_kwargs(args,kwargs)