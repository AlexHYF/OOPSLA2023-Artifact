# 1 spec size + impl size
# 2 subspec final size + subspec final time
# 3 preprocessed time + preprocessed size

# cvc5 solved: 1384 hole <=100: 1124 total hole: 26472 solved hole: 24771
# eusolver solved: 1360 hole <=100: 1254 total hole 25689 solved hole: 24625


import os
import csv
import re

def proc(path):
    solved_benchmark = 0
    hole_exist = 0
    total_holes = 0
    for root, dirs, files in os.walk(path):
        if 'sygus.log' in files:
            sygus_log = open(os.path.join(root, 'sygus.log'), 'r').readlines()
            if ("Exit status: 0\n" in sygus_log):
                solved_benchmark = solved_benchmark + 1
                if 'holes.txt' in files:
                    hole = open(os.path.join(root, 'holes.txt'), 'r').readlines()
                    if len(hole) <= 100:
                        hole_exist = hole_exist + 1
                        total_holes = total_holes + len(hole)
    return solved_benchmark, hole_exist, total_holes


def get_all_data(path):
    ret = [["synthesis_time","spec_size","impl_size","preprocessed_time","preprocessed_size","final_time","final_size","triv_size"]]
    for root, dirs, files in os.walk(path):
        if not (('sygus.log' in files) and ('run.log' in files)):
            continue
        sygus_log = open(os.path.join(root, 'sygus.log'), 'r').readlines()
        if not ("Exit status: 0\n" in sygus_log):
            continue
        synthesis_time = str(float(re.split(': |\n', sygus_log[2])[1])-float(re.split(': |\n', sygus_log[0])[1]))
        log_file = open(os.path.join(root, 'run.log'))
        spec_size = ""
        impl_size = ""
        preprocessed_time = ""
        preprocessed_size = ""
        final_time = ""
        final_size = ""
        triv_size = ""
        if "Hole Summary" in log_file.read():
            log_file = open(os.path.join(root, 'run.log')) 
            for line in log_file.readlines():
                if "Specification size:" in line:
                    spec_size = line.split(": ")[-1].strip()
                if "Implementation size:" in line:
                    impl_size = line.split(": ")[-1].strip()
                if "Hole Summary" in line:
                    datas = line.split(", ")
                    #if datas[1] != "0 4 -1":
                    #    continue
                    triv_size = datas[-8]
                    preprocessed_time = datas[-4]
                    preprocessed_size = datas[-5]
                    final_time = datas[-1].strip()
                    final_size = datas[-2]
                    ret.append([synthesis_time, spec_size, impl_size, preprocessed_time, preprocessed_size, final_time, final_size, triv_size])
    return ret

ret = get_all_data("./SyGuS/impls/cvc5")
import csv
with open('cvc5.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')

    for l in ret:
        writer.writerow(l)

ret = get_all_data("./SyGuS/impls/eusolver")
import csv
with open('eusolver.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')

    for l in ret:
        writer.writerow(l)
