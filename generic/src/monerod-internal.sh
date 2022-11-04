#!/bin/bash -e

# Internal functions for monerod-looped.sh
# They may be modified while the parents script is running, as they'll be reloaded.
# Add this example command to your crontab (with crontab -e) in order to have a cyclically generated snapshot.
# 0 12 * * MON  killall monerod # Restart MoneroD loop on each Monday at noon.
# or: 
# 0 12 1 * *    killall monerod # Restart MoneroD loop on each 1st day of the month.
#
# Author: mj-xmr

OUT_DIR=/spinny/readfrom/mj/public/blockchains/xmr/
WORK_DIR=/scratch/mj/own/
CONV=$HOME/devel/transactions-export-mj/b/xmr2csv
FILE_DB=data.mdb
FILE_REP=xmr_report.csv
IN_PATH=$HOME/.bitmonero/lmdb/$FILE_DB
OUT_PATH=$OUT_DIR/$FILE_DB

archive() {
        FILE=$1
        echo "Archiving $FILE"
        if which pv; then
                echo "Calculating size of ${FILE} ..."
                pwd
                ls -Hhl
                #SIZE=$(du -sb "${FILE}/" | awk '{print $1}')
                SIZE=$(ls -Hl "${FILE}" | awk '{print $5}')
                echo "Calculated $(($SIZE/1024/1024)) MB"
                #tar -chf - "${FILE}" | pv -s $SIZE | xz -9 -c - > "${FILE}".txz
                tar -chf - "${FILE}" | pv -s $SIZE | pigz -k - > "${FILE}".tgz
                #bretbeep.sh $?
        else
                #tar -chJf "${FILE}".txz "${FILE}"
                tar -chf "${FILE}".tgz -I pigz "${FILE}"
                #pigz -k "${FILE}"
        fi
}

testing() {
        echo "Testing!"
        OUT_DIR_TEST=$OUT_DIR/test/
        mkdir -p $OUT_DIR_TEST
        FILE=$OUT_DIR_TEST/bchai.dat

        touch $FILE
        chmod -v o-w $FILE
        date --iso > $OUT_DIR_TEST/timestamp-test.txt
}

export_dat() {
        pushd $WORK_DIR
                $CONV --all-outputs --out-csv-file $FILE_REP
                #tar -cJvf $OUT_DIR/$FILE_REP.txz.tmp $FILE_REP
                # Swap atomically
                #mv $OUT_DIR/$FILE_REP.txz.tmp $OUT_DIR/$FILE_REP.txz
                #mv $FILE_REP $OUT_DIR
        popd
        pushd $OUT_DIR
                rm $FILE_REP || true
                ln -s $WORK_DIR/$FILE_REP
                archive $FILE_REP
                rm $FILE_REP
        popd
        # Make some space in the work dir
        mv -v $WORK_DIR/$FILE_REP $OUT_DIR
}

process() {
        echo "Process"
        mkdir -p $OUT_DIR
        if [ -f $OUT_PATH ]; then
                rm -v $OUT_PATH
        fi
        #cp -v $IN_PATH $OUT_DIR
        echo "Copying blockchain to $OUT_DIR"
        rsync --progress $IN_PATH $OUT_PATH.tmp
        # Swap atomically
        mv -v $OUT_PATH.tmp $OUT_PATH
        chmod -v o-w $OUT_PATH
}

# Entry function
process_iteration() {
        #testing
        process
        export_dat
        date --iso > $OUT_DIR/timestamp.txt
}


