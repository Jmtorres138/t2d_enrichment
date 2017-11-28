#!/usr/bin/python -O
# Jason Matthew Torres
'''
Run fGWAS across annotations
Usage: python fgwas_wrapper_genome-wide.py
'''
# libraries
import sys,os,gzip
import subprocess as sp
import operator
import time
from select import select
from math import ceil
from math import floor
import moniter_rescomp_jobs

# globals
fgwas = "LD_LIBRARY_PATH=/apps/well/gsl/2.2.1-gcc4.9.3/lib /users/mccarthy/jmtorres/software/fgwas-0.3.6/bin/fgwas"
home_dir = "/well/got2d/jason/projects/t2d_enrichment/fgwas/"
in_dir=home_dir+"fgwas_input/"
out_dir = home_dir + "fgwas_output/"
input_file=in_dir+"ukbb_diamante-euro.fgwas.gz" # Optional: Run 01.1 script and use this for abbreviated annotations: in_dir+"fgwas_input_file.renamed.fgwas.gz"
job_dir=home_dir+"jobs/"
log_dir=home_dir+"logs/"
if os.path.isdir(out_dir)==False:
    os.mkdir(out_dir)
if os.path.isdir(job_dir)==False:
    os.mkdir(job_dir)
if os.path.isdir(log_dir)==False:
    os.mkdir(log_dir)
start_index = 9 #0-based index of column in fgwas input file where annotations start
job_prefix = "cells_" # change this if you have concurrent runs of the fgwas_wrapper (for example, running wrapper seperately across tissues)


def step1():
    '''
    Start index is the first index for an annotation in the file
    Here, the start index is 10 (column 11)
    '''
    fin = gzip.open(input_file,'rb')
    annot_list = fin.readline().strip().split()[start_index:]
    fin.close()
    for annot in annot_list:
        job_file = job_dir+job_prefix+annot+".sh"
        fout=open(job_file,'w')
        if annot == "distance_tss":
            command_list = [fgwas, "-i", input_file, "-cc",  "-dists",
                            annot+":"+home_dir+"dist_model", "-o", out_dir+annot]
        else:
            command_list = [fgwas, "-i", input_file, "-cc",  "-w",
                            annot, "-o", out_dir+annot]
        command = " ".join(command_list)
        # removed #$ -V from script
        script='''
#$ -N %s%s
#$ -pe shmem 1
#$ -P mccarthy.prjc
#$ -q short.qc
#$ -e %s%s.error
#$ -o %s%s.out
echo "start time" `date`
%s
echo "end time" `date`
        ''' % (job_prefix,annot, log_dir,job_prefix+annot,log_dir,job_prefix+annot, command)
        fout.write(script)
        fout.close()
        call = ["qsub", job_file]
        out_path = out_dir+annot+".llk"
        if os.path.exists(out_path) == False:
            sp.check_call(call)
        if os.path.exists(out_path) == True and os.stat(out_path).st_size == 0:
            sp.check_call(call)
    job_list = moniter_rescomp_jobs.get_job_ids(job_prefix)
    moniter_rescomp_jobs.wait_for_jobs(job_list)

def sig_annot_list():
    fin1 = gzip.open(input_file,'rb')
    annot_list = fin1.readline().strip().split()[start_index:]
    fin1.close()
    sig_list = []
    for annot in annot_list:
        f = out_dir+annot+".params"
        fin=open(f,'r')
        fin.readline() # header
        fin.readline() # pi_region
        l = fin.readline().strip().split() # annotation param val list
        aname, ci_low, est, ci_hi = l[0],l[1],l[2],l[3]
        try:
            if (float(ci_hi.replace(">","")) > 0 and float(ci_low.replace("<","")) < 0) != True:
                sig_list.append(annot)
        except:
            print ("Annotation Failed: %s" % annot)
        fin.close()
    print sig_list
    return(sig_list)



def wrapper():
    sys.stdout.write("Step 1: Running each annotation separately and identifying signficant annotations\n")
    step1()
    sig_list = sig_annot_list() # limiting to only annotations that didn't overlap zero (log2FE) from single analysis
    print sig_list


def main():
    wrapper()

if (__name__=="__main__"): main()
