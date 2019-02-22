#!/bin/bash

# -------------------------------------------------------------------
# user settings
# NB: ALWAYS check:
# - batch queue
# - copy of simulation files (and scripts, manually) to local machine
# - post-processing programs to run
# - which output files should be copied back
# - should previous dirs run* be deleted
# -------------------------------------------------------------------

# - copy simulation files to local machine (leave empty in case you don't want to copy back!):
#   NB: 
#   * if you require to avoid LSF emails, scp-ing won't actually involve the LSF files;
#     thus, each numerical directory will be recreated at the very end of the job,
#     containing only the LSF files;
#   * if you don't scp, the output on terminal of sixtrack is zipped, to save disk space;
#   . fullpath (it will be automatically created by the script)
LocalPWD=
#   . machine name
LocalMachine=
#   . user
LocalUser= whoami

# - queue type:
#   choose between LSF and HTCONDOR
batchSys=HTCONDOR
#   pick up a value amongst:
#   . LSF: test 8nm 1nh 8nh 1nd 2nd 1nw 2nw (see http://lsf-rrd.cern.ch/lrf-lsf/)
#   . HTCONDOR: espresso (20min) microcentury (1h) longlunch (2h) workday (8h) tomorrow (1d) testmatch (3d) nextweek (1w) (see http://batchdocs.web.cern.ch/batchdocs/local/lsfmigratepractical.html)
queue=tomorrow

# - list of files to be kept:
#fileList="dist0.dat screenout FirstImpacts.dat first_imp_average.dat LPI_BLP_out.s Coll_Scatter_real.dat collgaps.dat coll_summary.dat impacts_real.dat"
fileList="screenout collgaps.dat coll_summary.dat impacts_real.dat LPI* "

# - random seed is randomly chosen (false) or set equal to run index (true)
lseed=false

# - range of numerical dirs:
LIMITLOW=11
LIMITHIGH=1000

# - executables:
SixTOOLS="/afs/cern.ch/user/h/hgarciam/CollSoft"
SixExe="/afs/cern.ch/user/h/hgarciam/SixTrack_old/SixTrack_old/SixTrack" # HEIGENPART sixtrack
beamLossPatt="${SixTOOLS}/BeamLossPattern.exe"
cleanInel="${SixTOOLS}/CleanInelastic.exe"
cleanCollScatter="${SixTOOLS}/CleanCollScatter.exe"
cleanCollSum="${SixTOOLS}/correct_coll_summary.sh"
FirstImpactsAve="${SixTOOLS}/FirstImpacts--Average.sh"
fort3lib="/afs/cern.ch/user/h/hgarciam/scratch0/off_momentum_studies/LHC_2017_off_momentum_cleaning/B1_cleaning_IR3/test/fort_3_lib.sh"
HTCONDORtemplate="/afs/cern.ch/user/h/hgarciam/scratch0/off_momentum_studies/LHC_2017_off_momentum_cleaning/htcondor.sub"

# - avoid LSF mails (leave empty in case you want to be spammed):
#   (ignored in case of HTCONDOR)
LSFerrFile=
LSFoutFile=

# -------------------------------------------------------------------
# checks & settings
# -------------------------------------------------------------------

# some sanity checks:
echo "sanity checks about provided infos..."
labort=false
for tmpExe in ${SixExe} ${beamLossPatt} ${cleanInel} ${cleanCollScatter} ${cleanCollSum} ${FirstImpactsAve} ; do
    if [ ! -e ${tmpExe} ] ; then
	echo "fatal: ${tmpExe} does not exists!"
	labort=true
    fi
done
if ${labort} ; then
    echo "aborting..."
    exit 
else
    echo "...all fine!"
fi

# path on lxplus where simulation case is located:
PWD=`pwd`
echo "current dir: $PWD"

# scp? remind the user of the settings:
if [ -n "${LocalPWD}" -a -n "${LocalMachine}" -a -n "${LocalUser}" ] ; then
    echo "warning: copy simulation files to local machine:"
    echo "machine: ${LocalMachine}"
    echo "path: ${LocalPWD}"
    echo "user: ${LocalUser}"
    lcopy=true
else
    echo "warning: no copy of simulation files to local machine required"
    lcopy=false
fi

# batch system
batchSys=`echo "${batchSys}" | awk '{print (toupper($1))}'`
if [ "${batchSys}" != "LSF" ] && [ "${batchSys}" != "HTCONDOR" ] ; then
    echo "unknown batch system ${batchSys}!"
    echo "only LSF and HTCONDOR are presently supported!"
    echo "aborting..."
    exit 1
fi

# LSF emails:
doNotSpamMe=false
if [ "${batchSys}" == "LSF" ] ; then
    if [ -n "${LSFerrFile}" -a -n "${LSFoutFile}" ] ; then
	doNotSpamMe=true
	echo "warning: you won't receive emails from the LSF system;"
	echo "         thus, the same info is contained in ${LSFerrFile} and ${LSFoutFile} files,"
	echo "         locally saved in the numerical directory;"
    fi
fi

# -------------------------------------------------------------------
# actual script
# -------------------------------------------------------------------

# in case, set up directory on local machine
if ${lcopy} ; then
    ssh ${LocalUser}@${LocalMachine} "mkdir -p ${LocalPWD}"
    scp -r $PWD/clean_input ${LocalUser}@${LocalMachine}:"${LocalPWD}"

    # scp executables
#     for tmpExe in ${SixExe} ${beamLossPatt} ${cleanInel} ${cleanCollScatter} ${cleanCollSum} ${FirstImpactsAve} ; do
# 	scp $tmpExe ${LocalUser}@${LocalMachine}:"${LocalPWD}clean_input"
#     done

    # copy this script
    thisscript=`basename $0`
    thisdir=`dirname $0`
    scp ${thisdir}/${thisscript} ${LocalUser}@${LocalMachine}:"${LocalPWD}"/clean_input
fi

# some cleanup (-rf to avoid useless echos...)
if [ "${batchSys}" == "LSF" ] ; then
    rm -rf LSFJOB_*
fi

# loop over numerical dirs
for ((a = LIMITLOW; a <= LIMITHIGH ; a++)) ; do
    index=`printf "%04i" "$a"`
    rm -rf run$index
    mkdir run$index
    #echo run$index
    # do not cd run$index, otherwise $PWD changes value

    cat > run$index/SixTr--$index.job << EOF
#!/bin/bash
lcopy=${lcopy}
lseed=${lseed}

# ---------------------------------------------------------------------------------------------------
# load bash library for manipulating fort.3
source ${fort3lib}

# ---------------------------------------------------------------------------------------------------
# copy all needed files in tmp dir (just for the time of running)
cp $PWD/clean_input/*.* .
surveyFile=\`\ls -1 . | \grep -i survey | \head -1\`
collPosFile=\`\ls -1 . | \grep -i collpos | \head -1\`
apeFile=\`\ls -1 . | \grep -i allapert | \head -1\`
if [ "\${surveyFile}" != "SurveyWithCrossing_XP_lowb.dat" ] ; then
   mv \${surveyFile} SurveyWithCrossing_XP_lowb.dat
fi

# ---------------------------------------------------------------------------------------------------
# set seed
if \${lseed} ; then
    # seed is based on index of numerical dir
    set_seed $a
else
    # seed is randomly chosen by SixTrack
    set_seed 0
fi

# ---------------------------------------------------------------------------------------------------
# run SixTrack and save terminal output in dedicated file
$SixExe > screenout

# ---------------------------------------------------------------------------------------------------
# post-processing

$beamLossPatt lowb tracks2.dat BLP_out \${apeFile}
# remove binary characters in LPI file:
perl -pi -e 's/\0/ /g' LPI_BLP_out.s 

# clean lists of events in collimators from protons being lost in machine aperture beforehand
$cleanInel FLUKA_impacts.dat LPI_BLP_out.s \${collPosFile} coll_summary.dat
$cleanCollScatter Coll_Scatter.dat LPI_BLP_out.s \${collPosFile} coll_summary.dat

# create clean coll_summary with awk script
$cleanCollSum

# have a first feeling about the average beam impact parameter
${FirstImpactsAve} > first_imp_average.dat

# clean coll_ellipse
awk '\$2>1.0' coll_ellipse.dat > coll_ellipseRed.dat

# keep this for debugging in case of crashes
ls -lh

# copy files back to lxplus dir (-p: preserve date/time)
cp -p ${fileList} $PWD/run$index/
cp -r clean_input $PWD/run$index/

if \${lcopy} ; then
    gzip $PWD/run${index}/*
    scp -r $PWD/run${index} ${LocalUser}@${LocalMachine}:"${LocalPWD}"
    rm -r $PWD/run${index}/*
else
    # save some disk space
    gzip $PWD/run${index}/screenout
fi

exit
EOF
    if [ -d "run$index" ]; then
	chmod 777 run$index/SixTr--$index.job
	if [ "${batchSys}" == "LSF" ] ; then
	    if ${doNotSpamMe} ; then
		spamString="-o $PWD/run${index}/${LSFoutFile} -e $PWD/run${index}/${LSFerrFile}"
	    else
		spamString=""
	    fi
	    cd run$index
            # -sp : set priority, between 1 and 100
            # -R "rusage[pool=30000]" : allocate 30 GB hard drive space
	    bsub -q $queue -sp 100 -R "rusage[pool=50000]" ${spamString} SixTr--$index.job
            # echo the command line on a txt file, in case you need to submit the job again
	    echo "bsub -q $queue -sp 100 -R \"rusage[pool=50000]\" ${spamString} SixTr--$index.job" > .command.txt
	    cd ../
	fi
    fi
  
done

if [ "${batchSys}" == "HTCONDOR" ] ; then
    echo " Submitting jobs to htcondor..."
    #cp ${HTCONDORtemplate} .
    #sed -i "s/^+JobFlavour.*/+JobFlavour = \"${queue}\"/" ${HTCONDORtemplateName}
    sed -i "s/^+JobFlavour.*/+JobFlavour = \"${queue}\"/" htcondor.sub
   
    if ${lspool} ; then
        condor_submit -spool htcondor.sub
    else
        condor_submit htcondor.sub
    fi
 
 
    if [ $? -eq 0 ] ; then
        rm -f jobs.txt
    fi
fi
