#!/usr/bin/python

import sys
import subprocess 
import os
from datetime import datetime
import getopt


def main(argv):
    device = 'nvme1n1'
    operation = 'randread'
    jobs = 10
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print
        'test.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print
            'test.py -i <inputfile> -o <outputfile>'
            sys.exit()
        elif opt in ("-d", "--device"):
            device = arg
        elif opt in ("-o", "--operation"):
            operation = arg
        elif opt in ("-c", "--core"):
            jobs = arg

    # dir_path = "result/" + device + "/" + operation
    # os.mkdir(path=dir_path)

    for test_id in range(1, jobs+1):
        subpath = operation + "-" + device + "-" + str(test_id)
        test_name = "test/" + subpath + ".fio"
        create_randread_test(test_name, operation, device, test_id)

        result_name = "result/" + subpath
        f = open(result_name, 'w')
        subprocess.call(["sudo", "fio", test_name], stdin=sys.stdin, stdout=f)
        f.close()

        print("test:", test_id, "is done!")


def create_randread_test(filename: str, operation: str, device: str, jobs: int):

    ff = open(filename, "w+")

    ff.write("[global]\nname=random_read\n")
    ff.write("rw=" + operation + "\n")
    ff.write("direct=1\nioengine=libaio\nsize=1G\ngtod_reduce=0\ncpus_allowed_policy=split\nthread\ngroup_reporting\ntime_based\nruntime=60\n\n")

    ff.write("; controllable variables\nbs=4k\niodepth=128\ncpus_allowed=0-15\n")
    ff.write("numjobs=" + str(jobs) + "\n\n")

    ff.write("; Remote device\n[device]\nfilename=/dev/" + device + "\n\n")
    ff.close()


# def create_randread_test(self, filename: str, device: str, size: int = 1, runtime: int = 60, bs: int = 4, iodepth: int = 128, cpus: int = 15, jobs: int = 16):
#
#     ff = open(filename, "w+")
#     ff.write("; Remote device\n[device]\nfilename=/dev/" + device + "\n\n")
#     ff.write("[global]\nname=random_read\nrw=randread\ndirect=1\nioengine=libaio\n")
#     ff.write("size=" + str(size) + "G\n")
#     ff.write("gtod_reduce=0\ncpus_allowed_policy=split\nthread\ngroup_reporting\ntime_based\n")
#     ff.write("runtime=" + str(runtime) + "\n\n")
#     ff.write("; controllable variables\n")
#     ff.write("bs=" + str(bs) + "k\n")
#     ff.write("iodepth=" + str(iodepth) + "k\n")
#     ff.write("cpus_allowed=0-" + str(cpus) + "\n")
#     ff.write("numjobs=" + str(jobs) + "\n")
#     ff.close()


if __name__ == "__main__":
    main(sys.argv[1:])

