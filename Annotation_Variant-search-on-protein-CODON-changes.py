#!/usr/bin/python


"""
#Script to Pars vcf...

#####------Inputs-------
# Annotation_Variant-search-on-protein-CODON-changes.py INPUT1=Inputfile2(filtered-file) INPUT2=Outputfile INPUT3=Inputfile1(Protein-CODON file) DIR=Directory-fullpath

# python ./Annotation_Variant-search-on-protein-CODON-changes.py HCM_B00H7EW-B00H7EX-B00H7EY_chr1-MT_Variants_Het_PASS_MAF5%_CRL_RE-RG-LDB.txt HCM_B00H7EW-B00H7EX-B00H7EY_chr1-MT_Variants_Het_PASS_MAF5%_CRL_RE-RG-LDB_PCOD.txt samp12345_withoutgel_1720017671182881920819237_Protein-CODON_changes.txt /media/varma/SAMSUNG/HCM_WGS_ANNOTATION_ANNOVAR/

# python ./Annotation_Variant-search-on-protein-CODON-changes.py HCM_B00H7EW-B00H7EX-B00H7EY_chr1-MT_Variants_GATK_ANNOVAR_het_old.txt HCM_B00H7EW-B00H7EX-B00H7EY_chr1-MT_Variants_GATK_ANNOVAR_het_old_PCOD.txt samp12345_withoutgel_1720017671182881920819237_Protein-CODON_changes.txt /media/varma/SAMSUNG/HCM_WGS_ANNOTATION_ANNOVAR/

"""

import sys
import re
import os
import tempfile
import commands
import subprocess
#import subprocess32
from subprocess import *
from subprocess import call


class fileHandler:
	def __init__(self):
		self.data = []
		#print "Calling fileHandler constructor"
	def open_file(self,readfl):
		self.rfile = open(readfl,'r').readlines()
		return self.rfile
	def write_file(self,writefl):
		self.wfile = open(writefl,'w')
		return self.wfile

class SearchDB(fileHandler):

	def __init__(self):
		self.data = []
		from collections import defaultdict
		self.ident_ranges_HMBM = defaultdict(list)

	def Search_CODON(self,readfl1,outfl1,readfl2COD,writedir):
		"""
		Calling Search CODON 
		"""
		with open(writedir+readfl2COD,'r') as f2, open(writedir+"temp-outfile.tsv",'w') as output1:
			first_line = f2.readline().strip()
			for gg in f2:
				g1 = gg.strip().split("\t")
				wcolns = str(g1[0]+"\t"+g1[1]+"\t"+g1[-7]+"\t"+g1[-6]+"\t"+g1[-5]+"\t"+g1[-4]+"\t"+g1[-3]+"\t"+g1[-2]+"\t"+g1[-1])
				output1.write(wcolns+"\n")

		cmd1 = "bgzip -c "+writedir+"temp-outfile.tsv > "+writedir+"temp-outfile.tsv.gz"
		cmd2 = "tabix -s 1 -b 2 -e 2 -f "+writedir+"temp-outfile.tsv.gz"
		subprocess.check_output(cmd1, shell=True)
		subprocess.check_output(cmd2, shell=True)
		
		def srchdb1(self,RR1,RR2):
			try:
				True
				cmdFls1 = "tabix -f "+writedir+"temp-outfile.tsv.gz "+RR1+":"+RR2+"-"+RR2
				grepout =  subprocess.check_output(cmdFls1, shell=True)
			except subprocess.CalledProcessError:
				False
			return grepout

		with open(writedir+readfl1,'r') as f1, open(writedir+outfl1,'w') as output2:
			first_line = f1.readline().strip()
			HeadDB1 = "CHR	POS	AAChange	Refcodon	Altcodon	Altcodon_merge-2VAR	AA-change-2VAR	Altcodon_merge-3VAR	AA-change-3VAR"
			output2.write(first_line+"\t"+HeadDB1+"\n")
			for g in f1:
				g1 = g.strip()
				gg = g1.split("\t")
				CODONout = srchdb1(self,gg[0],gg[8])
				CDS = CODONout.split()
				if len(CDS)==0:
					True
					#output2.write(str(g1+"\t"+"."+"\t"+"."+"\t"+"."+"\t"+"."+"\t"+"."+"\t"+"."+"\t"+"."+"\n"))
				else:
					True
					CDS_OUT = '\t'.join(CDS)
					output2.write(str(g1+"\t"+CDS_OUT+"\n"))
		subprocess.check_output("rm "+writedir+"temp-outfile.*", shell=True)
		print "Done seach for CADD...."
		return None

# file1: Input files # write1: Output files 

clF1 = SearchDB().Search_CODON(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])




