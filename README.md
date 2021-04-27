# GoPhiPy : an AMR to ENGLISH VERBALIZER

GoPhiPy (*Generation Of Parenthesized Human Input in Python*) is a system for generating a literal reading of Abstract Meaning Representation (AMR) structures. The system, written in Python, uses a symbolic approach to transform the original rooted graph into a tree of constituents which is used as input for [jsRealB](https://github.com/rali-udem/JSrealB "GitHub - rali-udem/JSrealB: A JavaScript bilingual text realizer for web development") to realize an English sentence. 

This is a Python (re)implementation of GoPhi ([described in this paper](https://github.com/rali-udem/gophi/blob/master/documentation/GoPhi.pdf)) which used Prolog for the tree to tree transformation between the AMR and the syntactic representation given as input to jsRealB. This version makes use of Python classes to represent the syntactic representation which is then serialized to the appropriate format.

More information about the design and the rationale of the system [in this paper](docs/GoPhiPy.pdf).

# Running GoPhiPy

## Using the web interface at RALI

* browse [GoPhiPy](http://rali.iro.umontreal.ca/amr/python/current/export/cgi-bin/amrVerbalizer.cgi) to edit an AMR that can be verbalized

## Using the web interface with the internal Python web server
* Launch a shell console

    * go to the gophipy directory, and launch the Python web server  
        `cd /path/to/gophipy`  
        `python3 -m http.server --cgi `
    * In a web browser, browse : [http://localhost:8000/cgi-bin/amrVerbalizer.py](http://0.0.0.0:8000/cgi-bin/amrVerbalizer.py) to edit an AMR that can be verbalized

## From the Python console

* Launch the [jsRealB interpreter](https://github.com/rali-udem/JSrealB "GitHub - rali-udem/JSrealB: A JavaScript bilingual text realizer for web development") in another window/process  
`node /path/to/gophipy/tools/gophiPy-jsRealB-server.js  `
     
* Launch the Python interpreter in the `src` directory, and import the `amr2text` function

        cd('/path/to/the/src').  
        python3
        import amr2text

* call `amr2text.amr2text(amrString,trace=False)` to return the English sentence. For example:
    
        >>> amr2text.amr2text('(s / say-01 :ARG0 (i/I) :ARG1 (h/hello) :ARG2 (w/world))')
        'I say the hello to the world.'
        >>> amr2text.amr2text('(s / say-01 :ARG0 (i/I) :ARG1 (h/hello) :ARG2 (w/world))',True)
        *** AMR
        (s / say-01 :ARG0 (i/I) :ARG1 (h/hello) :ARG2 (w/world))
        *** Semantic Representation
        (s say-01 [:ARG0 (i I [] ↑s),
                   :ARG1 (h hello [] ↑s),
                   :ARG2 (w world [] ↑s)])
        *** Syntactic Representation
        S(Pro("I").pe(1),
          VP(V("say"),
             NP(D("the"),
                N("hello")),
             PP(P("to"),
                NP(D("the"),
                   N("world")))))
        'I say the hello to the world.'
    
* To process a whole file containing AMRs, call  
  `amr2text.showAMRsFile(fileName,regex=r"",trace=False,createExcel=False)`

  This call shows the input AMRs in the file *fileName* that match the *regex* which can be an empty string to match all AMRs. Matching is performed with the `re.DOTALL` flag for ignoring end of lines.   
    * If `trace` is `True` display the intermediary structures leading to their English realization.  
    * if `createExcel` is True, create an Excel file for evaluation in the same directory as the *fileName*
    * when the regex is an empty string, the BLEU score is computed and the differences between 
    the reference and the generated sentences are displayed on the standard output
    * when the regex is not an empty string, no file is created and no differences are displayed
        
# File organization of GoPhiPy

## Python (.py) files (`src` directory)

### Transformations:

* AMR → Semantic Representation (SemR)
    * `amr2text.py`      : main script that starts the whole process
    * `SemanticRep.py`   : parse with error messages in the case of a malformed AMR
    
* Semantic Representation → Syntactic Representation (syntR)
    * `SemR2SyntR.py`          : basic transformations into syntR 
    * `dereification.py`       : apply dereification on the input AMR
    * `roleProcessing.py`               : deal with most of the roles
    * `specialConcept.py`      : deal with some special concepts
    * `utils.py`         : utilities for tracing, transforming concept strings

* Syntactic Representation 
    * `jsRealBclass.py`  : class for creating *jsRealB-like* expressions in Python

* Utilities
    * `levenshtein.py`  : compute the Levenshtein distance between two strings and display them using console escape codes
    * `calculatebleu.py`: compute BLEU scores over two lists of lines

### Dictionaries
* `amdDicoGen.py`      : automatically generated dictionary using `tools/createDico.py` that parses PropBank frames and add missing words from the jsRealB lexicon 
* `amrDico.py`         : additions and corrections to `amrDicoGen.py`
* `lexicalSemantics.py`: definition of the format of dictionary entries with classes for representing the environment and the options

### Data (`data` directory)

Useful linguistic information used mainly by `tools/createDico.py`
 
* `morph-examples.txt` : a few tests AMRs for checking the morpholization algorithm
* `morph-verbalization-v1.01.txt` : list of morpholizations and verbalizations (copied for ISI)
* `prepositions.txt` : list of English prepositions
* `verbalization-list-v1.06.txt ` : list of verbalization (copied from ISI)

### Web application

A  Python CGI that creates a web page in which a user can edit an AMR, which is then transformed and realized by jsRealB in that same web page.
  
* `cgi-bin` directory
    * `amrVerbalizer.py` : shows the input page with either an initial AMR or the current one, it has the following functions
        * `inputPage`     : creates a web page with an embedded editor that contains an AMR with checkboxes for selecting the intermediary structures to show.
        * `replyPage` : creates a web page showing the original AMR, the selected representations and the English realization. 
        The generated web pages load some files from the the gophi-web directory.
    * `markup.py` : package for creating HTML from Python  
* `gophi-web` directory
    * `ace` directory : embedded editor for the web page
    * `addLexicon-dme.js` : load *big* lexicon `lexicon-dme.json` and make some local modifications
    * `amr-verb.css` : CSS for the generated web pages
    * `amr-verb.js`  : javascript for use in the generated web pages
    * `jsRealB.min.js` : minified jsRealB that generates from the SSurfR
    * `lexicon-dme.js` : *big* lexicon in JSON format
    * `realize.js`     : load the dme lexicon and realize the expression saved as string in the `syntR` global variable

## Tools
* `createDico.py`        : parses PropBank frames and jsRealB lexicon to create `dictionaryGenerated.pl`. It parses XML files from `propbank-amr-frames-xml-2018-01-25` distributed with AMR 3.0 
* `lambdaApplication.py` : illustrates the lambda application process using a simplistic example. This was useful for developing the notation.
* `sampleTest.py`        : create a sample from the AMR 3.0 split/test/ corpora
* `lexicalSemanticsSimple.py` : the example of lambda application used in the appendix of the paper
* `gophiPy-jsRealB-server.js` : node script for launching the GoPhiPy web server
* `jsRealB-node.js` : node version of jsRealB

## Informations (`Doc` directory)
* `GoPhiPy.pdf` : paper describing the rationale and design of `GoPhiPy`

## AMR files
Text files containing AMRs for developing and testing in three directories some of which are not given here because of copyrights:

* `amr_annotation_3.0` : should be filled with content downloaded [from LDC](https://catalog.ldc.upenn.edu/LDC2020T02 "Abstract Meaning Representation (AMR) Annotation Release 3.0  - Linguistic Data Consortium")
* `amr-examples` : examples gathered for developing GoPhiPy:
    * `amr-examples.txt` : simple examples gathered from different papers
    * `amr-dict-examples.txt` : examples extracted from the [AMR dictionary](https://www.isi.edu/~ulf/amr/lib/amr-dict.html "AMR dict")
    * `amr-guidelines-1_2_5.txt` : examples extracted from the [AMR Guidelines](https://github.com/amrisi/amr-guidelines/blob/master/amr.md "amr-guidelines/amr.md at master · amrisi/amr-guidelines · GitHub")
* `amr-ISI` : examples to be downloaded from the [ISI download page](https://amr.isi.edu/download.html "Download &nbsp; Abstract Meaning Representation (AMR)")  
  
## Data file extensions
* `*.txt`                   : input AMRs
* `*.out`                   : input AMRs augmented with output of gophi and baselinegen
* `*.xlsx`                  : Excel file (AMR, Basegen, reference sent, gophi output) for development or comparative evaluation, conventionally we add information about the evaluator before `.xlsx`

[Guy Lapalme](mailto:lapalme@iro.umontreal.ca)