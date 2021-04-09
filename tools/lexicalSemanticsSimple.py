'''
Simplified LexSem used in the paper

@author: lapalme
'''

from jsRealBclass import N,A,Pro,D,Adv,V,C,P,DT,NO,Q,  NP,AP,AdvP,VP,CP,PP,S,SP,\
                         Constituent, Terminal, Phrase, jsRealB

class Env:
    def __init__(self,pairs=None):
        self.pairs=pairs if pairs!=None else []

    def __contains__(self,kind):
        for rolei,_ in self.pairs:
            if kind==rolei:return True
        return False
    def __getitem__(self,arg):
        for key,val in self.pairs:
            if key==arg:return val
        return None

    def put(self,arg,value):
        self.pairs.append((arg,value))
        return self

    ## returns a list of elements associated with kind and remove them from the environment 
    def get(self,kind):
        res=[]
        i=0
        while i<len(self.pairs):
            argi,rolei=self.pairs[i]
            if kind==argi:
                res.append(rolei)
                self.pairs.pop(i)
            else:
                i+=1            
        return res
    
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
    
    def apply(self,syntR):
        for opt,value in self.opts:
            # adapted from https://stackoverflow.com/questions/3061/calling-a-function-of-a-module-by-using-its-name-a-string
            getattr(syntR, opt)(value)
        return syntR

pp       = lambda prep, arg: PP(P(prep),arg) if arg!=None else None
optD     = lambda det : det if det!=None else D("the")

class LexSem:
    def __init__(self,lemma,pos,args,lambda_):
        self.lemma=lemma     # useful for str(..)
        self.pos=pos         # part of speech, useful for str(...)
        self.args=args       # list of arguments as they appear in the AMR
        self.lambda_=lambda_ # function associated with the word
        
    def apply(self,env=None,opts=None):
        if env==None:env=Env()
        if opts==None:opts=Options()
        ## process args from dictInfo building the list of arguments or None
        argV=[env.get(arg) if arg in env else None for arg in self.args]
        syntR = self.lambda_(*argV)
        return opts.apply(syntR)
   
##   for unit testing
if __name__ == '__main__':
    def showSyntR(syntR):
        print(syntR.show())  # show the indented structure
        print(jsRealB(syntR.show(-1))) # get realized string

    ## a few lexicon entries
    verbs={}
    nouns={}

    verbs['give-01']=LexSem("V","give",[":ARG0",":ARG1",":ARG2"],
                            lambda arg0,arg1,arg2:S(arg0,VP(V("give"),arg1,pp("to",arg2))))    
    nouns['envelope'] = LexSem("envelope","N",[":D",":A"],lambda d,a:NP(optD(d),a,N("envelope")))
    nouns['boy']      = LexSem("boy","N",[":D",":A"],lambda d,a:NP(optD(d),a,N("boy")))
    nouns['girl']     = LexSem("girl","N",[":D",":A"],lambda d,a:NP(optD(d),a,N("girl")))

    boyEnv=Env([(':D',D("a"))])
    boyEnv.put(":A",A("nice")).put(":A",A("little"))
    boySyntR=nouns["boy"].apply(boyEnv,Options([("n","p")]))
    showSyntR(boySyntR) 
# NP(D("a"),
#    A("nice"),
#    A("little"),
#    N("boy")).n("p")
# nice little boys
    
    envelope=nouns["envelope"]
    envelopeSyntR=envelope.apply()
    showSyntR(envelopeSyntR)
# NP(D("the"),
#    N("envelope"))
# the envelope
     
    girl=nouns["girl"]
    girlSyntR=girl.apply(Env([(":D",D("this"))]))
    showSyntR(girlSyntR)
# NP(D("this"),
#    N("girl"))
# this girl
          
    give=verbs["give-01"]
    giveSyntR=give.apply(Env([(":ARG0",boySyntR),(":ARG1",envelopeSyntR),(":ARG2",girlSyntR)]),
                         Options([("typ",{"neg":True})]))
    showSyntR(giveSyntR)
# S(NP(D("a"),
#      A("nice"),
#      A("little"),
#      N("boy")).n("p"),
#   VP(V("give"),
#      NP(D("the"),
#         N("envelope")),
#      PP(P("to"),
#         NP(D("this"),
#            N("girl"))))).typ({"neg": true})
# Nice little boys do not give the envelope to this girl.
