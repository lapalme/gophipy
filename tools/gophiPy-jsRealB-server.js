///  node.js  jsRealBServer for GophiPy 
var http = require("http");
var url = require('url');
var fs = require('fs');

///////// 
//  load jsRealB file
const path=__dirname+'/jsRealB-node.js'
var jsRealB=require(path);

// "evaluate" the exports (Constructors for terminals and non-terminal) in the current context
// so that they can be used directly
for (var v in jsRealB){
    eval("var "+v+"=jsRealB."+v);
}

loadEn(true);
dmeLexicon = require(__dirname+"/../gophi-web/lexicon-dme.json")
eval(fs.readFileSync(__dirname+'/../gophi-web/addLexicon-dme.js').toString());
addLexiconEn(dmeLexicon);
setReorderVPcomplements(true);
console.log(Object.keys(getLexicon()).length+" lexicon entries");

http.createServer(function (request, response) {
   response.writeHead(200, {'Content-Type': 'text/plain; charset=UTF-8'});
   var req = url.parse(request.url, true);
   var query = req.query;
   var lang = query.lang
   var exp = query.exp
   if (lang=="en"){
       let errorType,sentence;
       try {        
           if (exp.startsWith("{")){
               errorType="JSON";
               jsonExp=JSON.parse(exp);
               sentence=fromJSON(jsonExp).toString();
           } else {
               errorType="jsRealB expression";
               sentence=eval(exp).toString();
           }
           response.end(sentence)
       } catch (e) {
           mess=`${e}\nErroneous realization from ${errorType}\n`
           if (errorType=="JSON"){
               try { // pretty-print if possible... i.e. not a JSON error
                   response.end(mess+ppJSON(JSON.parse(exp)))
               } catch(e){ // print line as is
                   response.end(mess+exp);
               }
           } else {
               response.end(mess+exp)
           }
       }
   } else {
       response.end('Language should be "en", but '+lang+' received\n')
   }
}).listen(8082);
// Console will print the message
console.log('jsRealB server [built on %s] running at http://127.0.0.1:8082/',jsRealB_dateCreated);

/* 
start server with : node /path/to/gophypPy-jsRealB-server.js
try this example in a browser to check that the dictionary has been updated...
http://127.0.0.1:8082/?lang=en&exp=S(NP(D("a"),A("american")),N("center")),VP(V("email")))
that should display:
An american center emails.
*/