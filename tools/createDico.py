## create initial dictionary as python program
outFile="amrDicoGen3-new.py"

# from the XML files of propbank frames 
#     in directory: propbank-frames-master/frames
amrDir="/Users/lapalme/Dropbox/AMR/"
dirname=amrDir+"amr_annotation_3.0/data/frames/propbank-amr-frames-xml-2018-01-25"

import re,os

import xml.etree.ElementTree as ET 
import json

# loal jsReal lexicon
lexicon=json.load(open("/Users/lapalme/Documents/GitHub/jsRealB/data/lexicon-dme.json"))
nbMissing={"N":0,"A":0,"V":0,"P":0,"Adv":0}
nbFound={"N":0,"A":0,"V":0,"P":0,"Adv":0}

def checkInLexicon(word,cat):
    if word not in lexicon or cat not in lexicon[word]:
#         print "%s :: %s"%(cat,word)
        nbMissing[cat]+=1
        return False
    else:
        nbFound[cat]+=1
#         del lexicon[word][cat]
        return True

nouns={}
adjectives={}
verbs={}
adverbs={}

prepositions=set([l.strip() for l in open("../data/prepositions.txt").readlines() if l[0]!="#"])
usedPrepositions=set()

## list of adverbs (or pseudo adverbs) that can appear after a verb
##   for the moment all "compound" nouns and adjectives are ignored 
allAdverbs=set(["in","out","over","under","up","down","on","off","about","into","for",
                "around","away","back","through","along","to","across","by","apart",
                "upon","after","forward","behind","even","aback"])
# print(sorted(allAdverbs))

# remove framenumber if it exists
def removeFN(w):
    return re.sub(r"-\d+$","",w)

def checkAdverb(xmlfile,rolesetId):
    parts=rolesetId.split("_")
    if len(parts)!=2:
        print("*** %s : strange splitting in %s"%(xmlfile,rolesetId))
        return None
    if parts[1] in allAdverbs:
        return parts
    print("*** %s : strange preposition in %s"%(xmlfile,rolesetId))
    return None

def getNounAttrs(noun):
    attrs=[]
    for (key,val) in lexicon[noun]["N"].items():
        if key!="tab":
            attrs.append('"%s":"%s"'%(key,val))
    return ",".join(attrs)
    
nounPattern='nounInfo("%s")'

def addNoun(xmlfile,rolesetId,noun):
    if "_" in noun:return
#         print("*** name with preposition:"+noun+" in "+rolesetId)
    checkInLexicon(noun, "N")
    if removeFN(rolesetId)!=noun: # use noun if rolesetId is different
        rolesetId=noun
    nounS=nounPattern%noun
    if noun in lexicon and "N" in lexicon[noun]:
        attrs=getNounAttrs(noun)
        if len(attrs)>0:
            nounS+='.addAttributes({%s})'%attrs
    nouns[rolesetId]=(nounS,xmlfile)

adjPattern='adjInfo("%s")'
def addAdjective(xmlfile,rolesetId,adjective):
    if "_" in adjective:return
#         print("*** adjective with preposition:"+adjective+" in "+rolesetId)
    checkInLexicon(adjective, "A")
    if removeFN(rolesetId)!=adjective: # use adjective if rolesetId is different
        rolesetId=adjective
    adjectives[rolesetId]=(adjPattern%adjective,xmlfile)

advPattern='"%s"'
def addAdverb(xmlfile,rolesetId,adverb):
    checkInLexicon(adverb, "Adv")
    if removeFN(rolesetId)!=adverb: # use adjective if rolesetId is different
        rolesetId=adverb
    adverbs[rolesetId]=(advPattern%adverb,xmlfile)

prepPattern='P("%s")'
    

def addVerb(xmlfile,rolesetId,verb,args):
    adverb=None
    if "_" in verb:
#         print("*** verb with adverb:"+verb+" in "+rolesetId)
        r=checkAdverb(xmlfile,verb)
        if r!=None:
#             print("parts:%s"%r)
            verb=r[0].replace("_","-")
            rolesetId=rolesetId.replace("_","-")
            adverb=r[1]
        else:
            return
    checkInLexicon(verb, "V")
    pat='LexSem("V","%s",[%s]'%(verb,",".join(['":%s"'%a for a in args]))
    start=1
    # le premier argument est le sujet!!
    pat+=',lambda '+(",".join([a.lower() for a in args]))+':S('
    if "ARG0" in args: 
        pat+='arg0,'
    elif "ARG1" in args:
        pat+='arg1,'
        start=2
    pat+='VP(V("%s")'%verb
    if adverb!=None:
        pat+=',Adv("%s")'%adverb
    for i in range(start,6):
        argi="ARG"+str(i)
        if argi in args:
            # tenter de trouver la bonne préposition en examinant les prépositions dans les exemples
            # pour le moment prendre la première...
            prep=args[argi]["prep"] 
            if len(prep)==0:
                pat+=',%s'%argi.lower()
            else:  
                mostCommonPrep=prep[0]
                if mostCommonPrep=="**":
                    pat+=',%s'%argi.lower()
                else:
                    pat+=',pp("%s",%s)'%(mostCommonPrep,argi.lower())              
    pat+=')))'
    verbs[rolesetId]=(pat, 
         # ajouter les noms des arguments pour les commentaires
         " / ".join([(name.upper()+":"+val["descr"]) for (name,val) in list(args.items())]),
         xmlfile)

def showTable(out,table,name):
    out.write(name+' = {\n')
    for (id_,val) in sorted(table.items()):
        out.write(" "+repr(id_)+":"+val[0]+(", # [%s]"%val[1])+"\n")
    out.write("}\n")

def showVerbs(out):
    out.write('verbs = {\n')
    for (id_,val) in sorted(verbs.items()):
        out.write(" %s: # %s [%s]\n   %s,\n\n"%(repr(id_),val[1],val[2],val[0]))
    out.write("}\n")
    
def parseXML(filename):
    root=ET.parse(open(filename,encoding='utf-8')).getroot()
    xmlfile=re.sub(".*/(.*)$","\\1",filename)
    for predicate in root.iter("predicate"):
#         print("%s:%s"%(filename,predicate.attrib["lemma"]))
        if predicate.attrib["lemma"].endswith("-91"):continue  # ignore "constructions"
        for roleset in predicate.iter("roleset"):
            rolesetId=roleset.attrib["id"].replace(".","-")
#             print(rolesetId)
            for alias in roleset.iter("alias"):
                pos=alias.attrib["pos"].lower()
                if pos=="n":
                    if rolesetId not in nouns:# n'ajouter que le premier rôle qui est le plus courant
                        addNoun(xmlfile,rolesetId,alias.text)
                elif pos=="j":
                    if rolesetId not in adjectives:
                        addAdjective(xmlfile,rolesetId,alias.text)
                elif pos=="v":
                    args={}
                    for role in roleset.iter("role"):
                        n=role.attrib["n"]
                        if n.isdigit():
                            args["ARG"+n]={"descr":role.attrib["descr"],"prep":[]}
                    # passer dans les exemples pour récupérer la préposition associée à chaque argument
                    for example in roleset.iter("example"):
                        for arg in example.iter("arg"):
                            argn="ARG"+arg.attrib["n"]
                            if (argn) in args:
                                text=arg.text
                                if text!=None:
                                    firstWord=text.split()[0]
#                                     print "arg:%s:%s"%(text,firstWord)
                                    if firstWord in prepositions:
                                        args[argn]["prep"].append(firstWord)
                                        usedPrepositions.add(firstWord)
                                    else: ## compter le nombre de fois SANS préposition
                                        args[argn]["prep"].append("**")
#                     print("%s:%s:%s"%(rolesetId,alias.text,args))                    
                    if rolesetId not in verbs: 
                        addVerb(xmlfile,rolesetId,alias.text,args)
                elif pos=="adv":
                    if rolesetId not in adverbs:
                        addAdverb(xmlfile, rolesetId, alias.text)
                elif pos in ["m","l","x"]:
                    pass # ignore locutions
                else:
                    print(xmlfile+":"+rolesetId+":strange POS:"+pos)

i=0
import sys
ignoredFiles=set(["have-property.xml","role-reification.xml","discourse-connective.xml"])
for file in os.listdir(dirname):
    # file="go.xml"
    if file[-4:]==".xml":
        if file in ignoredFiles:continue
        i+=1
        if (i%1000==0):print(str(i)+"::"+file) # show progress of file reading
        parseXML(dirname+"/"+file)
#         if i==10:break

for prep in usedPrepositions:
    checkInLexicon(prep, "P")
print("\nStatistiques des mots de propBank par rapport au lexique jsReal\n")
print("%3s:%5s:%5s:%5s"%("","ABS","OK","TOTAL"))
for cat in list(nbMissing.keys()):
    print("%3s:%5d:%5d:%5d"%(cat,nbMissing[cat],nbFound[cat],nbMissing[cat]+nbFound[cat]))
 
# sys.exit()
sep="\n# ======== %s \n"
## create output
print("\ncréation de "+outFile)
import time
out=open(outFile,"w",encoding='utf-8')
out.write("# coding=utf-8\n")
out.write("#  "+time.strftime("%c") +" : "+dirname+"\n")
out.write('''
from jsRealBclass import N,A,Pro,D,Adv,V,C,P,DT,NO,Q,  NP,AP,AdvP,VP,CP,PP,S,SP,\\
                         Constituent, Terminal, Phrase, jsRealB

from lexicalSemantics import LexSem, nounInfo,adjInfo,pp,optD

''')
out.write(sep%"NOUNS")
showTable(out,nouns,'nouns')
out.write(sep%"ADJECTIVES")
showTable(out,adjectives,'adjectives')
out.write(sep%"ADVERBS")
showTable(out,adverbs,'adverbs')

out.write(sep%"VERBS")
showVerbs(out)
# sys.exit()

out.write(sep%"New Words from the jsReal lexicon")
out.write("prepositions={}\n")
for key in sorted(lexicon.keys()):
    if re.search(r'[^a-z]',key):continue
    cats=lexicon[key]
    for cat in cats:
        if cat=="N":
            nounS=nounPattern%key
            if key in lexicon and "N" in lexicon[key]:
                attrs=getNounAttrs(key)
                if len(attrs)>0:
                    nounS+='.addAttributes({%s})'%attrs
            out.write("nouns['%s']=%s\n"%(key,nounS))
        elif cat=="A":
            out.write(("adjectives['%%s']=%s\n"%adjPattern)%(key,key))
        elif cat=="Adv":
            out.write(("adverbs['%%s']=%s\n"%advPattern)%(key,key))
        elif cat=="P":
            out.write(("prepositions['%%s']=%s\n"%prepPattern)%(key,key))
        else:
            pass
#             print("%s:%s ignored"%(cat,key))

### ajouter les verbalisations
morphVerbalizationFile="data/morph-verbalization-V1.01.txt"
  
morphVerbRE=r'::DERIV-VERB "(.*?)" ::DERIV-NOUN(-ACTOR)? "(.*?)"( ::DERIV-NOUN(-ACTOR)? "(.*?)")?$' 
out.write(sep%'MORPHVERBALIZATIONS')
out.write("morphVerbalizations={\n")
for line in open(morphVerbalizationFile,encoding="utf-8"):
    line=line.strip()
    if line.startswith("#"):continue
    m=re.match(morphVerbRE, line)
    if m:
        infos={}
        infos["noun" if m.group(2)==None else "actor"] = m.group(3)
        if m.group(4)!=None:
            infos["noun" if m.group(5)==None else "actor"] = m.group(6)
        out.write(" '%s':%s,\n"%(m.group(1),infos))
    else:
        print(line+":no match")
out.write("}\n")
import pprint
pp=pprint.PrettyPrinter(indent=3)
verbalizations={}

def addVbn(concept,role,value,vrb):
    try:
        if concept in verbalizations:
            if role in verbalizations[concept]:
                verbalizations[concept][role][value]=vrb
            else:
                verbalizations[concept][role]={value:vrb}
        else:
            verbalizations[concept]={role:{value:vrb}}
    except TypeError as err:
        print(err)
        print("addVbn(%s,%s,%s,%s)"%(concept,role,value,vrb))
        for (key,value) in sorted(verbalizations.items()):
            print(key+":"+str(value))

        
## process only "good" verbalization
##  depending on the length of the second "list"
##  methylate-01:{"":"methylation"}                                  # 1:simple case
##  person:{":ARG0-of":{"abuse-01":"abuser",                    # 3: single constraint
##                      "keep-01":[":ARG1","bee","beekeeper"] } # 5: complex constraint (not yet implemented)
##    
verbalizationFile="data/verbalization-list-v1.06.txt"
verbRE=r'^VERBALIZE (.*?) TO (.*)'
ignoreRE=r'^(#|DO-NOT-|MAYBE)'
out.write(sep%'MORPHVERBALIZATIONS')
out.write("verbalizations=\\\n")
for line in open(verbalizationFile,encoding="utf-8"):
    line=line.strip()
#     print(line)
    if re.match(ignoreRE,line):continue
    m=re.match(verbRE,line)
    if m:
        conceptArgs=m.group(2).split()
        concept=conceptArgs[0]
        if len(conceptArgs)==1:
            verbalizations[concept]={"":m.group(1)}
        elif len(conceptArgs)==3:
            if conceptArgs[1].endswith("-of"):
                conceptArgs[1]=re.sub(r"^(.*)-of$",r":*\1",conceptArgs[1])
            addVbn(concept,conceptArgs[1],conceptArgs[2],m.group(1))
        else: ## when len==5 not yet implemented...
            pass
#             print("not yet implemented")
    else:
        print(line+":no match")
pprint.pprint(verbalizations,stream=out)


    