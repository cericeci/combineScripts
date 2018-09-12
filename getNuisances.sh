#!/bin/bash
#Usage: sh getNuisances.sh [DATACARD NAME] [What to use as data: d (data), t0 (background only Asimov), t1 (s+b Asimov)] [Number of parallel jobs] [EXTRA INPUT]

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
fi

if [ "$ASIMOV" = "d" ]; then
   echo "Using data"
   ASIMOV=""
fi

if [ "$ASIMOV" = "t0" ]; then
   echo "Using background-only Asimov dataset"
   ASIMOV=" -t -1 --expectSignal 0 --rMin -0.1"
fi

if [ "$ASIMOV" = "t1" ]; then
   echo "Using signal + background Asimov dataset"
   ASIMOV=" -t -1 --expectSignal 1 "
fi


echo "---------------------------------"
echo "---------------------------------"

combine -M FitDiagnostics $ASIMOV $DATACARD $EXTRA

python $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py  -a fitDiagnostics.root -g plots.root >> $OUTPUT
