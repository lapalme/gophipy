'''
Created on 6 févr. 2021

@author: lapalme
'''


import re,json
from jsRealBclass import N,A,Pro,D,Adv,V,C,P,DT,NO,Q,  NP,AP,AdvP,VP,CP,PP,S,SP,\
                         Constituent, Terminal, Phrase, jsRealB

verbs={}
nouns={}
adjectives={}
conjunctions={}

## environment management
##    manage an environment as a list of pairs [(str,Constituent)] 
##    CAUTION: args can be repeated
##       put(arg,value) : adds to the environment
##       get(arg) : returns a list of all values associated with this arg
##       putAll(pairs) : adds all pairs to the environment
##       arg in self : check if arg appears at least one in the environment
##     
class Env:
    def __init__(self,pairs=None):
        self.pairs=pairs if pairs!=None else []
    
    def __contains__(self,kind):
        for rolei,_ in self.pairs:
            if re.match(kind,rolei):return True
        return False
    
    def __len__(self):
        return len(self.pairs)
    
    def put(self,arg,value):
#         if not isinstance(value,Constituent):
#             print("Env.put:%s : %s is not a Constituent"%(arg,value))
        self.pairs.append((arg,value))
        return self
    
    def putAll(self,pairs):
        [self.put(key,value) for key,value in pairs]
        return self
    
    ## returns a list of elements associated with kind and remove them from the environment 
    def get(self,kind):
        res=[]
        i=0
        while i<len(self.pairs):
            argi,rolei=self.pairs[i]
            if re.match(kind,argi):
                res.append(rolei)
                self.pairs.pop(i)
            else:
                i+=1            
        return res
    
    ### most often we push at the end... or unshift at the start (like in JavaScript)
    def push(self,value):
        return self.put(':start',value)
    def unshift(self,value):
        return self.put(':end',value)
    
    def insertBefore(self,befKey,key,value):
        nb=len(self.pairs)
        i=0
        while i<nb and self.pairs[i][0]!=befKey:i+=1
        self.pairs.insert(i,(key,value))
    
    def insertAfter(self,aftKey,key,value):
        i=len(self.pairs)-1
        while i>=0 and self.pairs[i][0]!=aftKey:i-=1
        self.pairs.insert(i+1,(key,value))

class Options:
    def __init__(self,opts=None):
        self.opts=opts if opts!=None else []
    
    def add(self,opt,value):
        if opt in ["typ","dOpt"]:
            try:
                idx=self.opts.index(opt)
                self.opts[idx].update(value)
            except ValueError :
                self.opts.append((opt,value))
        else:         
            self.opts.append((opt,value))
        return self
    
    def __str__(self):
        return "".join(['.%s(%s)'%(opt,json.dumps(value)) for opt,value in self.opts])
    
    def apply(self,syntR):
        for opt,value in self.opts:
            # adapted from https://stackoverflow.com/questions/3061/calling-a-function-of-a-module-by-using-its-name-a-string
            getattr(syntR, opt)(value)
        return syntR

class LexSem:
    def __init__(self,lemma,pos,args,lambda_):
        self.lemma=lemma
        self.pos=pos
        self.args=args
        self.lambda_=lambda_
        
    def __str__(self):
        return "LexSem(%s,%s)"%(self.lemma,self.pos)
    
    def apply(self,env=None,opts=None):
        if env==None:env=Env()
        if opts==None:opts=Options()
        ## process args from dictInfo building the list of arguments or None
        argV=[env.get(arg) if arg in env else None for arg in self.args]
        syntR = self.lambda_(*argV)
        if len(env)>0:    
            ## add unprocessed args
            syntR.add(env.get(":start"),0)
            syntR.add(env.get(".*")) 
        return opts.apply(syntR)
    

pp = lambda prep, arg: PP(P(prep),arg) if arg!=None else None
optD = lambda det : det if det!=None else D("the")

verbs['give-01']=LexSem("V","give",[":ARG0",":ARG1",":ARG2"],
                        lambda arg0,arg1,arg2:S(arg0,VP(V("give"),arg1,pp("to",arg2))))


nouns['envelope'] = LexSem("envelope","N",[":D",":A"],lambda d,a:NP(optD(d),a,N("envelope")))
nouns['boy']      = LexSem("boy","N",[":D",":A"],lambda d,a:NP(optD(d),a,N("boy")))
nouns['girl']     = LexSem("girl","N",[":D",":A"],lambda d,a:NP(optD(d),a,N("girl")))

adjectives["little"]=LexSem("little","A",[],lambda :A("little"))
adjectives["nice"]  =LexSem("nice","A",[],lambda :A("nice"))

nounInfo = lambda lemma:LexSem(lemma,"N",[":D",":A"],lambda d,a:NP(optD(d),a,N(lemma)))
adjInfo  = lambda lemma:LexSem(lemma,"A",[],lambda:A(lemma))

def showSyntR(syntR):
    print(syntR)
    print(syntR.show())
    print(jsRealB(syntR.show(-1)))

def op16(conj):
    return LexSem(conj,"C",[":op1",":op2",":op3",":op4",":op5",":op6"],
                  lambda op1,op2,op3,op4,op5,op6:CP(C(conj),op1,op2,op3,op4,op5,op6))  
conjunctions["or"]=op16("or")
conjunctions["and"]=op16("and")

if __name__ == '__main__':
    boyEnv=Env([(':D',D("a"))])
    little=adjectives["little"].apply()
    boyEnv.putAll([(":A",little),(":A",A("nice"))])
    boy=nouns["boy"]
    print(boy)
    boySyntR=boy.apply(boyEnv,Options([("n","p")]))
    showSyntR(boySyntR)
    
    envelope=nouns["envelope"]
    envelopeSyntR=envelope.apply()
    showSyntR(envelopeSyntR)
     
    girl=nouns["girl"]
    girlSyntR=girl.apply(Env([(":D",D("this"))]))
    showSyntR(girlSyntR)
          
    give=verbs["give-01"]
    giveSyntR=give.apply(
                       Env([(":ARG0",boySyntR),(":ARG1",envelopeSyntR),(":ARG2",girlSyntR)]),
                       Options([("typ",{"neg":True})]))
    showSyntR(giveSyntR)
 
    boySyntR=nouns["boy"].apply(boyEnv)
    envelopeSyntR=nouns["envelope"].apply()
    bookSyntR=nounInfo("book").apply(Env([(":D",D("a"))]))
    penSyntR=nounInfo("pen").apply()
    envelopeBookSyntR=conjunctions["or"].apply(
                               Env([(":op1",envelopeSyntR),
                                    (":op2",bookSyntR),
                                    (":op6",penSyntR)]))
    showSyntR(envelopeBookSyntR)
    giveSyntR=give.apply(
                       Env([(":ARG0",boySyntR),
                            (":ARG1",envelopeBookSyntR),
                            (":ARG2",girlSyntR),
                            (":start",Q("start")),
                            (":test",Q("test")),
                            (":end",Q("end")),
                            ]))
    showSyntR(giveSyntR)
    giveSyntR=give.apply(
                       Env([(":ARG1",envelopeBookSyntR),
                            (":ARG2",girlSyntR)]))
    showSyntR(giveSyntR)
    