#!/bin/python3
import os
import io
import shutil
import glob
import subprocess

BASEDIR="/Users/ifjorissen/big_paper/big_paper_code"
TRIDIR="/Users/ifjorissen/big_paper/big_paper_code/triangle"
DATADIR="/Users/ifjorissen/big_paper/big_paper_code/analysis/data/"
RESULTDIR="/Users/ifjorissen/big_paper/big_paper_code/analysis/results/"

PATTERN = "ps*/triangle/ps*"
EXT=".txt"

def clean_triangle(pattern):
    print("\n *** Cleaning out old triangle results ... ***")
    #removes all files in the results corresponding to the pattern
    for f in glob.iglob(RESULTDIR + pattern):
        print("... removing {}".format(f))
        shutil.rmtree(f)

    #removes all the aggregate files regardless of pattern
    for f in glob.iglob(RESULTDIR + "*tri *.txt"):
        print("... removing {}".format(f))
        os.remove(f)

def main(alg):
    for f in glob.iglob(PATTERN):
        print(f)
        if alg is "fortune_sweepline":
            alg_name = "fortune"
            cmd = "{}/triangle -v -V -N -E -B -P -F {}".format(TRIDIR, f)
        elif alg is "incremental":
            alg_name = "inc"
            cmd = "{}/triangle -v -V -N -E -B -P -i {}".format(TRIDIR, f)
        else:
            alg_name = "divconq"
            cmd = "{}/triangle -v -V -N -E -B -P {}".format(TRIDIR, f)

        fpath = f.split('.')[0]

        #get info:
        fdir, tmp, fname = fpath.split('/')
        finfo, base, order, run_num = fname.split("_")
        points = int(base)**(int(order))

        #create directory & file names
        trivor_res_dir = RESULTDIR + fdir + "/triangle" + "_" + alg_name + "/"

        fdest = trivor_res_dir + "res_" + fname + "_" + alg_name + EXT
        all_results = RESULTDIR + "triangle_all_base"+ base + "_" + alg_name + EXT
        all_DT_results = RESULTDIR + "del_tri_all_base"+ base + "_" + alg_name + EXT

        trivor_results = RESULTDIR + "triangle_base"+ base + "_ord" + order + "_" + alg_name + EXT
        del_res = RESULTDIR + "del_tri_base_" + base + "_ord" + order + "_" + alg_name + EXT

        # make results directories if necessary
        if not os.path.exists(trivor_res_dir):
            print("creating directory @{}".format(trivor_res_dir))
            os.makedirs(trivor_res_dir)

        #automatically pipe this output into a results file
        # cmd = "{}/bin/qvoronoi Ts s TI {} | {}".format(QHULLDIR, f, fdest)

        #command to run triangle: -v = Voronoi -V = verbose -N = suppress .node output
        # -E = suppress .edge output -B=suppress boundary output -P=suppress .poly output
        # Note: -N and -E flags are not respected if you use -v, so I changed that 
        # in my personal version of Triangle. 
        # (Added a condition to check switches in triangle.c where write_voronoi is called)
        # cmd = "{}/triangle -v -V -N -E -B -P {}".format(TRIDIR, f)
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
        output_as_string = output.decode(encoding='UTF-8')

        #write all the results to a result_file
        print("writing to fdest: {}".format(fdest))
        result_file = open(fdest, 'w')
        result_file.write(output_as_string)
        result_file.close()


        #one file to write (Total Running - Output milliseconds)/1000 for THIS problem size
        #a second file to write Delaunay Milliseconds / 1000 for THIS problem size
        #one more file to hold ALL the results (i.e all problem sizes for THIS base) for Delaunay
        #a fourth file to hold ALL the results (i.e all problem sizes for THIS base) for (Total Running - Output)

        result_file = open(fdest, 'r')
        time_results = open(trivor_results, 'a')
        del_time_results = open(del_res, 'a')
        all_DT = open(all_DT_results, 'a')
        aggregate_res = open(all_results, 'a')

        output_ms = None
        total_ms = None
        for line in result_file:
            if "Delaunay milliseconds" in line:
                del_ms = float(line.split(":")[1].split("\n")[0])/1000.0
                res_str = "{} {}\n".format(points, del_ms)
                del_time_results.write(res_str)
                all_DT.write(res_str)
            elif "Output milliseconds" in line:
                output_ms = float(line.split(":")[1].split('\n')[0])
                # print(output_ms)
            elif "Total running milliseconds" in line:
                total_ms = float(line.split(":")[1].split("\n")[0])
                # print(total_ms)
            if total_ms is not None and output_ms is not None:
                time_ms = (total_ms - output_ms)/1000.0
                res_str = "{} {}\n".format(points, time_ms)
                time_results.write(res_str)
                aggregate_res.write(res_str)
                break

        aggregate_res.close()
        all_DT.close()
        del_time_results.close()
        time_results.close()
        result_file.close()

if __name__ == "__main__":
    print("hah")
    clean_triangle(PATTERN)
    os.chdir(DATADIR)
    algs = ["fortune_sweepline", "divide_and_conquer", "incremental"]
    for alg in algs:
        print(alg)
        main(alg)
    main("incremental")

