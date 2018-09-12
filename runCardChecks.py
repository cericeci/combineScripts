import os
from optparse import OptionParser

parser = OptionParser(usage="%prog [options]")
parser.add_option("-m", "--modules", dest="modules",  type="string", default=[], action="append", help="Run these modules (impacts, closure, covariances). If none is provided it will run everything.");
parser.add_option("-j", "--jobs", dest="jobs", type="int", default=4, help="Number of paralell jobs that are allowed at the same time")
parser.add_option("-d", "--datacard", dest="datacards", type="string", default=[], action="append", help="Datacards for which the checks will be run")
parser.add_option("-o", "--outdir", dest="outdir", type="string", default="./temp/", help="Output directory for the summarized results")
parser.add_option("-n", "--nosave", dest="nosave", action="store_true", default=False, help="If active, no directory is created, only the commands are run")
parser.add_option("-p", "--pretend", dest="pretend", action="store_true", default=False, help="Print the commands but don't run them")
parser.add_option("-e", "--extra", dest="extra", type="string", default="", help="Extra options to be provided for combine/combineTool")
parser.add_option("-a", "--asimov", dest="asimov", type="string", default=[], action="append", help="What to use as dataset: data, b, s")
(options, args) = parser.parse_args()

class datacardChecks(object):
    def __init__(self, options):
        self.options = options
        self.collectModes()
        self.createStructure()
        self.createJobs()
        self.runJobs()
    def collectModes(self):
        #Collect all the checks that will be done 
        self.doimpacts     = any(["impacts" in a for a in self.options.modules]) or len(self.options.modules) == 0
        self.doclosure     = any(["closure" in a for a in self.options.modules]) or  len(self.options.modules) == 0
        self.docovariances = any(["covariances" in a for a in self.options.modules]) or  len(self.options.modules) == 0
        self.asimov = []
        if "data" in self.options.asimov:
            self.asimov.append("d")
        if "b" in self.options.asimov or len(self.options.asimov) == 0:
            self.asimov.append("t0")
        if "s" in self.options.asimov or len(self.options.asimov) == 0:
            self.asimov.append("t1")
      
    def createStructure(self):
        #Create the folder estructure with the plots of the checks
        if not self.options.nosave:
            self.easyName = options.datacard.split("/")[-1].replace(".txt", "").replace(".root", "").replace(".", "_")
            self.outDir   = options.outdir +"/" + self.easyName
            if not os.path.exists(self.outDir):
                if not(self.options.pretend): os.makedirs(self.outDir)
            os.system("cp %s %s"%(self.options.datacard,self.outDir))
            if self.doimpacts and not os.path.exists(self.outDir + "/Impacts/"):
                if not(self.options.pretend): os.makedirs(self.outDir + "/Impacts/")
            if self.doclosure and not os.path.exists(self.outDir + "/Closure/"):
                if not(self.options.pretend): os.makedirs(self.outDir + "/Closure/")
            if self.docovariances and not os.path.exists(self.outDir + "/Covariances/"):
                if not(self.options.pretend): os.makedirs(self.outDir + "/Covariances/")

    def createJobs(self):
        self.jobs = []
        #Create the commands to run
        for asi in self.asimov:
            if self.doimpacts:
                self.jobs.append("sh estimateImpact.sh [DATACARD] [ASIMOV] [JOBS] [OUTPUT] [EXTRA]".replace("[DATACARD]", self.options.datacard).replace("[ASIMOV]", asi).replace("[JOBS]", str(self.options.jobs)).replace("[EXTRA]", self.options.extra).replace("[OUTPUT]", self.outDir + "/Impacts/"))
            if self.doclosure:
                self.jobs.append("sh getNuisances.sh [DATACARD] [ASIMOV] [OUTPUT] [EXTRA]".replace("[DATACARD]", self.options.datacard).replace("[ASIMOV]", asi).replace("[OUTPUT]", self.outDir + "/Closure/").replace("[EXTRA]", self.options.extra))

    def runJobs(self):
        for j in self.jobs:
            if not(self.options.pretend): os.system(j)  
            else: print(j)

for d in options.datacards:
    options.datacard = d
    datacardChecks(options)
