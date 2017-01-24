#!/bin/sh
export DYLD_LIBRARY_PATH=/Users/amaro/GitHub/poker/PokerBots_2017/pbots_calc-master/export/darwin/lib:$LD_LIBRARY_PATH
java -cp /Users/amaro/GitHub/poker/PokerBots_2017/pbots_calc-master/java/jnaerator-0.11-SNAPSHOT-20121008.jar:/Users/amaro/GitHub/poker/PokerBots_2017/pbots_calc-master/java/bin pbots_calc.Calculator $@