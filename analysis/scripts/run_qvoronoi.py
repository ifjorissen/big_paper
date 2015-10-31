#!/bin/python3
import os
import io
import shutil
import glob
import subprocess

BASEDIR="/Users/ifjorissen/big_paper/big_paper_code"
QHULLDIR="/Users/ifjorissen/big_paper/big_paper_code/qhull"
DATADIR="/Users/ifjorissen/big_paper/big_paper_code/analysis/data/"
RESULTDIR="/Users/ifjorissen/big_paper/big_paper_code/analysis/results/"

EXT=".txt"

def clean():
  print(clean)
  shutil.rmtree(RESULTDIR + '/*')

def main():
  clean()
  os.chdir(DATADIR)
  for f in glob.iglob("ps*/qhull/*.txt"):
    fpath = f.split('.')[0]
    fdir, tmp, fname = fpath.split('/')
    qvor_res_dir = RESULTDIR + fdir + "/qhull/"
    fdest = qvor_res_dir + "res_" + fname + EXT
    qvor_results = RESULTDIR + "qhull_time_" + fdir + EXT

    # make results directories if necessary
    if not os.path.exists(qvor_res_dir):
      print("creating directory @{}".format(qvor_res_dir))
      os.makedirs(qvor_res_dir)

    #automatically pipe this output into a results file
    # cmd = "{}/bin/qvoronoi Ts s TI {} | {}".format(QHULLDIR, f, fdest)

    cmd = "{}/bin/qvoronoi Ts s TI {}".format(QHULLDIR, f)
    output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
    output_as_string = output.decode(encoding='UTF-8')

    print("writing to fdest: {}".format(fdest))
    result_file = open(fdest, 'w')
    result_file.write(output_as_string)
    result_file.close()

    #get info:
    finfo, run_num = fname.split("_")
    points = int(finfo[2:])

    #get the cpu seconds and write them to an aggregate file
    result_file = open(fdest, 'r')
    time_results = open(qvor_results, 'a')
    for line in result_file:
      if "CPU seconds to compute hull" in line:
        cpu_time = line.split(":")[1]
        res_str = "{} {}".format(points, cpu_time)
        time_results.write(res_str)
    time_results.close()
    result_file.close()

#to do: write a little function to clean out the old time results

if __name__ == "__main__":
  main()
