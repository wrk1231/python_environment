class Qustion(object):
    def __init__(self,ques,ans):
        self.ques=ques
        self.ans=ans

    def answer(self,ans2):
        self.ans=self.ans+ans2
        
    def __str__(self):
        return('ques:%s\nanswer:%s'%(self.ques,self.ans))
que=Qustion('who are you','Mike')
que.answer('John')

print(str(que))