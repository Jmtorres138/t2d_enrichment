#!/usr/bin/python -O
# Jason Matthew Torres
'''
Input a gwas bed file and an annotation bed file
Usage: python JTbuild_fgwas_bedfile.py
'''
# libraries
import sys,os,gzip
import subprocess as sp

# globals
cur_dir = "/well/got2d/jason/projects/t2d_enrichment/garfield/"
input_dir = "/well/got2d/jason/projects/t2d_enrichment/fgwas/fgwas_input/"
input_file = input_dir + "ukbb_diamante-euro.fgwas.gz"
pval_dir = cur_dir + "pval/"
annot_dir = cur_dir + "annotation/"
start_pos = 9
# functions

def build_inputs():
    fin = gzip.open(input_file,'rb')
    fin.readline() # header
    count = 0
    for line in fin:
        count+=1
        sys.stdout.write("\r%d" % count)
        sys.stdout.flush()
        l = line.strip().split()
        chrom = l[0]
        pos = l[2]
        pval = l[6]
        annot_list = l[start_pos:-1]
        annot_string = "".join(annot_list)
        try:
            with open(pval_dir + chrom, "a") as fout1:
                fout1.write(" ".join([pos,pval])+"\n")
            with open(annot_dir + chrom, "a") as fout2:
                fout2.write(" ".join([pos,annot_string])+"\n")
        except:
            fout1 = open(pval_dir + chrom,'w')
            fout1.write(" ".join([pos,pval])+"\n")
            fout2 = open(annot_dir + chrom,'w')
            fout2.write(" ".join([pos,annot_string])+"\n")
        fout1.close()
        fout2.close()
    fin.close()


def main():
    build_inputs()

if (__name__=="__main__"): main()
