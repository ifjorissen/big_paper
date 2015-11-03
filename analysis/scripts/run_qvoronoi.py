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

def clean_qhull(pattern):
  print("\n *** Cleaning out old qhull results ... ***")
  for f in glob.iglob(RESULTDIR + pattern):
    print("... removing {}".format(f))
    shutil.rmtree(f)
  for f in glob.iglob(RESULTDIR + "*qhull*.txt"):
    print("... removing {}".format(f))
    os.remove(f)
  # shutil.rmtree(RESULTDIR)

def main():
  PATTERN = "ps*/qhull/ps*"
  clean_qhull(PATTERN)
  os.chdir(DATADIR)
  for f in glob.iglob(PATTERN):
    fpath = f.split('.')[0]
    fdir, tmp, fname = fpath.split('/')

    #get info:
    finfo, base, order, run_num = fname.split("_")
    points = int(base)**(int(order))
    print(finfo, base, order, points)


    qvor_res_dir = RESULTDIR + fdir + "/qhull/"
    fdest = qvor_res_dir + "res_" + fname + EXT
    qvor_results = RESULTDIR + "qhull_base" + base + "_ord " + order + EXT

    # either specify a base or chage to glob on the fly
    all_results = RESULTDIR + "qhull_all_base" + base + EXT

    # make results directories if necessary
    if not os.path.exists(qvor_res_dir):
      print("\ncreating directory @{}".format(qvor_res_dir))
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


    #get the cpu seconds and write them to an aggregate file
    result_file = open(fdest, 'r')
    time_results = open(qvor_results, 'a')
    aggregate_res = open(all_results, 'a')
    for line in result_file:
      if "CPU seconds to compute hull" in line:
        cpu_time = line.split(":")[1]
        res_str = "{} {}".format(points, cpu_time)
        time_results.write(res_str)
        aggregate_res.write(res_str)
        break
    aggregate_res.close()
    time_results.close()
    result_file.close()

#to do: write a little function to clean out the old time results

if __name__ == "__main__":
  main()
