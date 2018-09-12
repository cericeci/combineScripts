Repository containing several scripts to automate checks on the fits performed with the Combine RooStats tool

- Running the impacts for a given datacard:

sh estimateImpact.sh [DATACARD NAME] [What to use as data: d (data), t0 (background only Asimov), t1 (s+b Asimov)] [OUTPUT shortname] [Number of parallel jobs] [Extra commands to be feeded to combineToools]

- Running the closure tests on the Asimov dataset:

sh getNuisances.sh [DATACARD NAME] [What to use as data: d (data), t0 (background only Asimov), t1 (s+b Asimov)] [Number of parallel jobs] [OUTPUT shortname] [EXTRA INPUT]


