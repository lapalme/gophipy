'''
Created on Mar 22, 2021

@author: lapalme
'''

import random,os,re

amrDir="/Users/lapalme/Dropbox/AMR/"

def walkAMRdirs(path,operation,nbAMRs):
    # parse a file to count roles and concepts
    if os.path.isdir(path):
        for dirName,subdirNames,files in os.walk(path):
            for subdirName in subdirNames:
                if subdirName in ["training","dev"]:
                    nbAMRs=walkAMRdirs(os.path.join(dirName,subdirName),operation,nbAMRs)
            for fileName in files:
                if re.match(r'amr-.*\.txt',fileName):
                    nbAMRs=walkAMRdirs(os.path.join(dirName,fileName),operation,nbAMRs)
            return nbAMRs
    else:
        return operation(path,nbAMRs)


def sample(path,nb,samplePath):
    global totalOriginal,totalLong
    with open(path,"r",encoding="utf-8") as f:
        blocks = f.read().split("\n\n")
    nbOriginal=len(blocks)
    totalOriginal+=nbOriginal 
    # skip first block which is a file header
    blocks = [block for block in blocks[1:] if block.count("\n")>7] # keep only AMR of 5 lines or more + 3 lines of comment
    nbLong=len(blocks)
    print("%s [%d,%d]"%(re.sub(r".*/(.*)",r"\1",samplePath),nbOriginal,nbLong))
    totalLong+=nbLong
    sampleF=open(samplePath,"w",encoding="utf-8")
    for block in random.sample(blocks,nb):
        sampleF.write(block)
        sampleF.write("\n\n")
    print(samplePath+" written")
    

totalOriginal=0
totalLong=0
testDir=amrDir+"amr_annotation_3.0/data/amrs/split/test/"
sampleDir=testDir+"sample5/"
for file in os.listdir(testDir):
    if file.endswith(".txt"):
        sample(testDir+file,25,sampleDir+file)
print("%s [%d,%d]"%("total",totalOriginal,totalLong))

# output
# amr-release-3.0-amrs-test-proxy.txt [824,716]
# amr-release-3.0-amrs-test-xinhua.txt [87,73]
# amr-release-3.0-amrs-test-bolt.txt [134,102]
# amr-release-3.0-amrs-test-sample-25.txt [151,124]
# amr-release-3.0-amrs-test-consensus.txt [101,78]
# amr-release-3.0-amrs-test-sample-25-5.txt [151,149]
# amr-release-3.0-amrs-test-lorelei.txt [529,350]
# amr-release-3.0-amrs-test-dfa.txt [231,196]
# total [2208,1788]