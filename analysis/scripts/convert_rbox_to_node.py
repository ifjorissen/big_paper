#!/bin/python3
import os
import io
import shutil
import glob

#goal: go through all of the ps*.txt files and make them into .node files for triangle to consume
DATADIR="/Users/ifjorissen/big_paper/big_paper_code/analysis/data/"
EXT = ".node"

os.chdir(DATADIR)
for f in glob.iglob("ps*/qhull/ps*.txt"):
  #filename, new file name, full path to each
  fpath = f.split('.')[0]
  fdir, tmp, fname = fpath.split('/')
  node_fname = fname + EXT
  fsrc = DATADIR + f
  fdest_dir = DATADIR + fdir + "/triangle/"
  fdest = fdest_dir + fname + EXT

  #make the triangle data subdirectories, if necessary
  if not os.path.exists(fdest_dir):
    print("creating directory @{}".format(fdest_dir))
    os.makedirs(fdest_dir)

  #info about the problem from the filename
  finfo, run_num = fname.split("_")
  points = int(finfo[2:])
  order = len(finfo[3:])

  print("\n *** .NODE file creation for problem size: {} run number: {} ***".format(points, run_num))
  print("creating/updating .node file called {}".format(fdest))
  print("populating .node file with data from {}".format(fsrc))

  #get dimension of diagram from fsrc
  content = open(f, 'r+')
  dim = content.readline()
  bounds = content.readline()
  content.close()

  #remove any content in the new file and write the initial line
  node_file = open(fdest, 'a')
  node_file.seek(0)
  node_file.truncate()
  tri_ln1 = "{} {}".format(points, dim)
  node_file.write(tri_ln1)

  #rewrite each line of f by adding a vertex id to the beginning of each line of f
  for i, line in enumerate(content):
    comp = 10**(order-1) 
    if (i+1) % comp is 0 and points > 100:
      percent = ((i+1) / points)*100
      print("{}%".format(percent))
    node_ln = "{} {}".format(i+1, line)
    node_file.write(node_ln)
  node_file.close()
  print("*** COMPLETE: done writing to {} ***".format(fdest))