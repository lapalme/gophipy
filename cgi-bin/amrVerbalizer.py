#!/usr/bin/env python3

### simplistic web application for GoPhiPy
###      shows an editor (ACE) in which the AMR can be entered and edited
###      when the user clicks on "verbalize", the AMR is parsed
###         - if there are syntactic errors, the editor is redisplayed with the error message
###         - otherwise the corresponding English sentence is displayed
##            the semantic and syntactic representations are displayed on request
##     it uses markup.py for generating the HTML
##     it is transposition of the web page http://rali.iro.umontreal.ca/amr/current/build/amrGenerate.cgi 
import sys,cgi,os,io,re
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'src'))

import markup
from markup import oneliner as e

from contextlib import redirect_stdout
import SemR2SyntR,SemanticRep,dereification

initialAMR='''(d / desire-01
    :ARG0 (b/boy)
    :ARG1 (g/girl
           :ARG0-of (l/like-01
                       :polarity - 
                       :ARG1 b)))
'''

##   get info from parameters
form = cgi.FieldStorage()
def getArg(arg,default):
    return form.getvalue(arg) if arg in form else default

mode        = getArg("mode","input")
amrString   = getArg("amr",initialAMR)
editorHeight= getArg("editorHeight","300")
semRflag    = getArg("semR","off")
syntRflag   = getArg("syntR","off")

##  show a checkbox (checked or not)
def makeCB(cbName):
    if getArg(cbName,"off")=="off":
        return e.input(type="checkbox",name=cbName,id=cbName)
    return e.input(type="checkbox",name=cbName,id=cbName,checked="checked")

##  display the editor for the AMR 
def inputPage(amrString,errors):
    page = markup.page(mode='html')
    page.init( lang="en", charset='utf-8', doctype=markup.doctype.strict,
               title="GoPhiPy: an AMR Verbalizer",
               script=('http://code.jquery.com/jquery-latest.min.js',
                       '../gophi-web/ace/ace.js',
                       '../gophi-web/amr-verb.js'),
               css=( '../gophi-web/amr-verb.css' ))

    page.form(action="",method="POST",id='form')
    page.h1(e.a('Γω-Φ-∏',href="https://github.com/rali-udem/gophipy")+': an AMR verbalizer')
    page.p('AMR Color coding: '+
            e.span('variable',class_='ace_variable')+", "+
            e.span('concept',class_='ace_concept')+", "+
            e.span('role',class_='ace_role')+
            e.span(e.a("Editor help",target="_blank",
                       href='https://github.com/ajaxorg/ace/wiki/Default-Keyboard-Shortcuts')+" "+
                   e.a('Drag bottom border to resize editor',class_='resize'),
                   class_="help")
           )
    page.div(e.div("",id="amr",style="height:"+editorHeight+"px")+
             e.div("",id="amr_dragbar",class_="app_editor_dragbar"))
    page.div(amrString,id="inputAMR",name="amr")
    page.textarea("",name="amr")
    if len(errors)>0:
        page.pre(e.code(errors))
        m=re.match(r"line +(\d+),(\d+) :",errors)
        if m!=None:
            page.script('$(document).ready(function() {ace.edit("amr").gotoLine(%s,%s,true);})'%m.groups())
    page.input(id="indent",type="button",value="Indent")
    page.input(name="submit",type="submit",value="Verbalize")
    page.input(name="editorHeight",type="hidden",value="editorHeigth")
    page.fieldset(
       e.legend("Show Representations")+
       e.label("Semantic",for_="semR")+makeCB("semR")+
       e.label("Syntactic",for_="syntR")+makeCB("syntR")
    )
    page.input(name="mode",type="hidden",value="reply")
    page.form.close()
    return page

## parse the AMR to produce the semantic and syntactic representation if no error
##            or to return a string with error messages  
def amr2syntR(amrString):
    syntErrOut=io.StringIO()
    with redirect_stdout(syntErrOut):
        semR=SemanticRep.SemanticRep.fromString(amrString)
    syntErrors=syntErrOut.getvalue()
    if len(syntErrors)>0:
        return ("syntErr",syntErrors)
    dereified=dereification.dereify(semR)
    if dereified!=None:
        semR=dereified
    semR.elimInv() # transform inverse roles
    semErrOut=io.StringIO()
    with redirect_stdout(semErrOut):
        syntR=SemR2SyntR.makeSyntR(semR)
    semErrors=semErrOut.getvalue()
    if len(semErrors)>0:
        return ("semErr",semR,syntR.show(),semErrors)
    return ("ok",semR,syntR.show())

##  display the AMR and call jsRealB on the syntactic representation to realize the English sentence
##  if requested show the semantic or syntactic representations  
def replyPage(amrString,semR,syntR,semErrors):
    page = markup.page(mode='html')
    page.init(lang="en", charset='utf-8', doctype=markup.doctype.strict,
              title="AMR verbalized by Γω-Φ-∏",
              script=('http://code.jquery.com/jquery-latest.min.js',
                      '../gophi-web/jsRealB.min.js',
                      '../gophi-web/addLexicon-dme.js',
                      '../gophi-web/realize.js')
    )
    page.style('.sent {font-weight:bold} textarea {font-family:monospace;font-size:large}')
    page.h1('AMR verbalized by '+e.a('Γω-Φ-∏',href="https://github.com/rali-udem/gophipy"))
    page.h2("AMR")

    page.form(action="",method="POST",id='form')
    page.pre(e.code(amrString))
    if semRflag!="off":
        page.h2("Semantic Representation")
        page.pre(semR.prettyStr())
    if len(semErrors)>0:
        page.h3("Errors in semantic to syntactic representation transformation")
        page.pre(semErrors)
    if syntRflag!="off":
        page.h2("Syntactic Representation")
        page.pre(syntR)
    page.h2("English Sentence")
    ## HACK: combined uses of multiline strings in both Python and Javascript, this is "delicate"
    page.script(f'''var syntR=`{syntR}`; ''') # syntR must be quoted to prevent immediate evaluation
    page.p('',id="realization")

    page.input(name="amr",type="hidden",value=amrString)
    page.input(name="editorHeight",type="hidden",value=editorHeight)
    page.input(name="semR",type="hidden",value=semRflag)
    page.input(name="syntR",type="hidden",value=syntRflag)
    page.input(name="submit",type="submit",value="Edit the AMR")
    page.input(name="mode",type="hidden",value="input")
    page.form.close()
    return page


## start of application logic
print ('Content-type: text/html\n')
if mode=="input":
    print(inputPage(amrString,""))
else:
    res=amr2syntR(amrString) # parse
    if res[0]=="syntErr":  # there were errors in the input AMR
        print(inputPage(amrString,res[1]))
    elif res[0]=="semErr":
        print(replyPage(amrString,res[1],res[2],res[3]))
    elif res[0]=="ok":                    # no errors show the realization 
        print(replyPage(amrString,res[1],res[2],""))
    else:
        print("$$$ unknown return code:"+res[0])

