#!/usr/bin/python -O
# Jason Matthew Torres
'''
Build input bed file
Usage: python script.py
'''
# libraries
import sys,os,gzip
import subprocess as sp

# globals
bedtools = "/apps/well/bedtools/2.24.0/bedtools"
cur_dir = "/well/got2d/jason/projects/t2d_enrichment/input_bedfiles/"

file_list = ["/well/got2d/jason/reference/islet/stretch_enhancers/islet_stretch_enhancers.bed",
             "/well/got2d/jason/reference/genomic/all_genomic.bed",
             "/well/got2d/jason/reference/islet/atac_peaks/oxford_islet_atac_macs2_n17.bed",
             "/well/got2d/jason/reference/islet/chromatin_states/islet_chromatin_states15_fullnames.bed",
             "/well/got2d/jason/reference/chromatin_segmentation/varshney_2016/bed_files/complete_varshney_chromHMM_states.bed",
             "/well/got2d/jason/reference/islet_development_Wang2015/complete_wang2015_chip_peaks.bed"]#,
             #"/well/got2d/jason/reference/epigenome_roadmap/complete_erm_chromHMM_18states_core_K27ac.bed"]

out_name = cur_dir + "temp_input.bed"

def build_complete_input_file():
    fout = open(out_name,'w')
    for f in file_list:
        print f
        fin = open(f,'r')
        for line in fin:
            l = line.strip()
            fout.write(l+"\n")
        fin.close()
    fout.close()


def main():
    build_complete_input_file()
    command = "sort -k 1,1 -k2,2n " +  out_name + " > "  + cur_dir+"complete_input.bed"
    sp.check_call(command,shell=True)

if (__name__=="__main__"): main()
