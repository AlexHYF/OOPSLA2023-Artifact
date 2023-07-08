# echo > out.txt
# echo > log.txt

SOLVER=cvc5
BASE_DIR=./impls/$SOLVER
time for i in `find $BASE_DIR -name 'spec-2.sl'`; do
    BENCH=$( echo $i | sed "s/\.\/impls\/$SOLVER\///" | sed 's/\/spec-2\.sl$//' )
    if [[ $( cat $BASE_DIR/$BENCH/holes.txt | wc -l ) -le 100 ]]; then
        echo $BENCH >> out.txt
        cat $BASE_DIR/$BENCH/holes.txt | \
            ./run.sh $BASE_DIR/$BENCH/spec-2.sl $BASE_DIR/$BENCH/impl-2.sl \
            > /dev/null 2> /dev/null
#             >> out.txt 2>> log.txt
        echo $( date +%s.%N ), $BENCH, $?
    fi
done > test.csv


SOLVER=cvc5; BENCH=General_Track/MPwL_d4s7; ./run.sh ./impls/$SOLVER/$BENCH/spec-2.sl ./impls/$SOLVER/$BENCH/impl-2.sl < ./impls/$SOLVER/$BENCH/holes.txt



SOLVER=cvc5; BENCH=PBE_BV_Track/22_1000; ./run.sh ./impls/$SOLVER/$BENCH/spec-2.sl ./impls/$SOLVER/$BENCH/impl-2.sl < ./impls/$SOLVER/$BENCH/holes.txt
SOLVER=cvc5; BENCH=General_Track/inv_gen_w1; ./run.sh ./impls/$SOLVER/$BENCH/spec-2.sl ./impls/$SOLVER/$BENCH/impl-2.sl < ./impls/$SOLVER/$BENCH/holes.txt
SOLVER=cvc5; BENCH=General_Track/hd-15-d0-prog; ./run.sh ./impls/$SOLVER/$BENCH/spec-2.sl ./impls/$SOLVER/$BENCH/impl-2.sl < ./impls/$SOLVER/$BENCH/holes.txt
SOLVER=cvc5; BENCH=PBE_BV_Track/81_10; ./run.sh ./impls/$SOLVER/$BENCH/spec-2.sl ./impls/$SOLVER/$BENCH/impl-2.sl < ./impls/$SOLVER/$BENCH/holes.txt
SOLVER=cvc5; BENCH=General_Track/hd-13-d5-prog; ./run.sh ./impls/$SOLVER/$BENCH/spec-2.sl ./impls/$SOLVER/$BENCH/impl-2.sl < ./impls/$SOLVER/$BENCH/holes.txt
SOLVER=cvc5; BENCH=PBE_Strings_Track/lastname; ./run.sh ./impls/$SOLVER/$BENCH/spec-2.sl ./impls/$SOLVER/$BENCH/impl-2.sl < ./impls/$SOLVER/$BENCH/holes.txt

./run.sh ./tests/max2/spec.sl ./tests/max2/impl.sl < ./tests/max2/hole.txt







echo > test.txt
echo > log.txt
tsp -S 10
SOLVER=cvc5
BASE_DIR=./impls/$SOLVER
time for i in `find $BASE_DIR -name 'spec-2.sl'`; do
    BENCH=$( echo $i | sed "s/\.\/impls\/$SOLVER\///" | sed 's/\/spec-2\.sl$//' )
    if [[ $( cat $BASE_DIR/$BENCH/holes.txt | wc -l ) -le 100 ]]; then
        echo '---------------------------------------------------------------------------------------------' >> test.txt
        echo Starting, $BENCH, $( date +%s.%N ) >> test.txt
        ./run.sh $BASE_DIR/$BENCH/spec-2.sl $BASE_DIR/$BENCH/impl-2.sl \
            < $BASE_DIR/$BENCH/holes.txt \
            >> test.txt 2>> log.txt
        STATUS=$?
        echo Summary, $BENCH, $( date +%s.%N ), $STATUS >> test.txt
    fi
done
