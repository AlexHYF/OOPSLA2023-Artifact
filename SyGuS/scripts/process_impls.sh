#!/usr/bin/env bash
########################################################################################################################
# 2. Remove let expressions and collect statistics

for SOLVER in cvc5 eusolver; do
    BASE_DIR=./impls/$SOLVER
    time (
        echo "Name, ," \
             "HasSynthInv, NumSynthFunS1, NumDefineFunS1, ," \
             "SyGuSStartTime, SyGuSEndTime, SyGuSRunTime, SyGuSStatus, ," \
             "NumSynthFunI1, NumDefineFunI1, ," \
             "SpecHasLet, SpecUnletStatus, SpecNumDiff, ," \
             "NumSynthFunS2, NumDefineFunS2, ," \
             "ImplHasLet, ImplUnletStatus, ImplNumDiff, ," \
             "NumSynthFunI2, NumDefineFunI2, ," \
             "EnumeratorStatus, NumHoles"

        for i in `find $BASE_DIR -name 'spec-1.sl'`; do
            BENCH=$( echo $i | sed "s/\.\/impls\/$SOLVER\///" | sed 's/\/spec-1\.sl$//' )

            ####
            # a. spec-1.sl
            if [[ $( cat $BASE_DIR/$BENCH/spec-1.sl | grep 'synth-inv' | wc -l ) == "0" ]]; then
                HAS_SYNTH_INV=FALSE
            else
                HAS_SYNTH_INV=TRUE
            fi
            NHS1=$( cat $BASE_DIR/$BENCH/spec-1.sl | ./scripts/funCounter.sh 2> /dev/null )
            if [[ $? -ne 0 ]]; then
                NHS1=", "
            fi

            ####
            # b. SyGuS solver
            START_TIME=$( cat $BASE_DIR/$BENCH/sygus.log | grep '^Start time:' | sed 's/.*: //' )
            END_TIME=$( cat $BASE_DIR/$BENCH/sygus.log | grep '^End time:' | sed 's/.*: //' )
            EXIT_STATUS=$( cat $BASE_DIR/$BENCH/sygus.log | grep '^Exit status:' | sed 's/.*: //' )

            ####
            # c. impl-1.sl
            NHI1=$( cat $BASE_DIR/$BENCH/impl-1.sl | ./scripts/funCounter.sh 2> /dev/null )

            ####
            # d. spec-2.sl
            if [[ $( cat $BASE_DIR/$BENCH/spec-1.sl | grep 'let' | wc -l ) == "0" ]]; then
                SPEC_HAS_LET=FALSE
            else
                SPEC_HAS_LET=TRUE
            fi
            cat $BASE_DIR/$BENCH/spec-1.sl | ./scripts/unletter.sh > $BASE_DIR/$BENCH/spec-2.sl 2> /dev/null
            SPEC_UNLET_STATUS=$?
            SPEC_NUM_DIFF=$( diff $BASE_DIR/$BENCH/spec-1.sl $BASE_DIR/$BENCH/spec-2.sl | wc -l )
            NHS2=$( cat $BASE_DIR/$BENCH/spec-2.sl | ./scripts/funCounter.sh 2> /dev/null )

            ####
            # e. impl-2.sl
            if [[ $( cat $BASE_DIR/$BENCH/impl-1.sl | grep 'let' | wc -l ) == "0" ]]; then
                IMPL_HAS_LET=FALSE
            else
                IMPL_HAS_LET=TRUE
            fi
            cat $BASE_DIR/$BENCH/impl-1.sl | ./scripts/unletter.sh > $BASE_DIR/$BENCH/impl-2.sl 2> /dev/null
            IMPL_UNLET_STATUS=$?
            IMPL_NUM_DIFF=$( diff $BASE_DIR/$BENCH/impl-1.sl $BASE_DIR/$BENCH/impl-2.sl | wc -l )
            NHI2=$( cat $BASE_DIR/$BENCH/impl-2.sl | ./scripts/funCounter.sh 2> /dev/null )

            ####
            # f. Enumerate holes
            cat $BASE_DIR/$BENCH/impl-2.sl | ./scripts/holeEnumerator.sh > $BASE_DIR/$BENCH/holes.txt 2> /dev/null
            ENUMERATOR_STATUS=$?
            NUM_HOLES=$( cat $BASE_DIR/$BENCH/holes.txt | wc -l )

            ####
            # g. Print
            echo "$BENCH, ," \
                 "$HAS_SYNTH_INV, $NHS1, ," \
                 "$START_TIME, $END_TIME, , $EXIT_STATUS, ," \
                 "$NHI1, ," \
                 "$SPEC_HAS_LET, $SPEC_UNLET_STATUS, $SPEC_NUM_DIFF, ," \
                 "$NHS2, ," \
                 "$IMPL_HAS_LET, $IMPL_UNLET_STATUS, $IMPL_NUM_DIFF, ," \
                 "$NHI2, ," \
                 "$ENUMERATOR_STATUS, $NUM_HOLES"
        done
    ) #> $BASE_DIR/impls-stats.csv
done
