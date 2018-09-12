#!/bin/bash
#Usage: sh getNuisances.sh [DATACARD NAME] [What to use as data: d (data), t0 (background only Asimov), t1 (s+b Asimov)] [Number of parallel jobs] [OUTPUT shortname] [EXTRA INPUT]

DATACARD=$1
ASIMOV=$2
OUTPUT=$3
EXTRA=$4

if [ "$DATACARD" = "" ]; then
   echo "You need to provide a datacard!!"
   exit
fi

if [ "$ASIMOV" = "" ]; then
   echo "Defaulting to data. Are you sure this is what you want to do?"
   ASIMOV=""
   PREFIX="d"
fi

if [ "$ASIMOV" = "d" ]; then
   echo "Using data"
   ASIMOV=""
   PREFIX="d"
fi

if [ "$ASIMOV" = "t0" ]; then
   echo "Using background-only Asimov dataset"
   ASIMOV=" -t -1 --expectSignal 0 --rMin -10"
   PREFIX="t0"
fi

if [ "$ASIMOV" = "t1" ]; then
   echo "Using signal + background Asimov dataset"
   ASIMOV=" -t -1 --expectSignal 1 "
   PREFIX="t1"
fi

if [ "$OUTPUT" = "" ]; then
   OUTPUT="./"   
fi

if [[ "$DATACARD" != *"root"* ]]; then
   echo "Preliminary: convert to rootspace"
   echo "---------------------------------"
   text2workspace.py ${DATACARD}
   DATACARD="${DATACARD//.txt/.root}"
   echo "Card is $DATACARD"
fi

echo "---------------------------------"
echo "---------------------------------"

combine -M FitDiagnostics $ASIMOV $DATACARD $EXTRA

echo "Run nuisances for datacard $DATACARD. Additional toy options are set to $ASIMOV. Extra parameters to be passed to combine are: $EXTRA" >> $OUTPUT/fitResults 
python $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py  -a fitDiagnostics.root -g plots.root >> $OUTPUT/fitResults
mv plots.root $OUTPUT/plots_$PREFIX.root
mv fitDiagnostics.root $OUTPUT/fitDiagnostics_$PREFIX.root
mv higgsCombineTest.FitDiagnostics.mH120.root $OUTPUT/higgsCombineTest.FitDiagnostics.mH120_$PREFIX.root
