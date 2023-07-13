Explainable Program Synthesis by Localizing Specifications
==========================================================

Amirmohammad Nazari, Yifei Huang, Roopsha Samanta, Arjun Radhakrishna, Mukund Raghothaman

Introduction
------------

This is the artifact package accompanying our OOPSLA 2023 submission titled _Explainable Program Synthesis By
Localizing Specifications_. Our paper presents a new approach to explain the programs produced by program synthesis
tools. We call this concept the _sub-specification_. Our paper presents examples of how subspecs can be useful and an
algorithm to synthesize subspecifications. We have implemented this algorithm, which we call S3, for two program
synthesis settings, SyGuS and DreamCoder. Our paper includes a user study and an experimental evaluation of the subspec
synthesis procedure.

This artifact contains all the tools (S3, CVC5, EUSolver), benchmark files, and scripts to reproduce the experiments
described in the paper. In this document, we will describe the outline of these experiments, how to run them, and also
describe how one may use S3 to calculate sub-specifications on SyGuS solver and DreamCoder's results of their own.

The reviewers expressed a desire to see the user study instruments. We have accordingly included saved copies of the
Qualtrics surveys that we used in the study. These may be found in the directory `User-Study/`.

Installing the Artifact
-----------------------

The recommended way to install this artifact is by using Docker:
```
git clone https://github.com/AlexHYF/OOPSLA2023-Artifact.git
cd OOPSLA2023-Artifact
[sudo] docker build -t s3 .
[sudo] docker run -it s3
```
The list of running containers may be obtained by executing the following command on the host:
```
[sudo] docker container ls
```
Each container is automatically assigned a mnemonic name, using which one may open new Bash prompts as follows:
```
[sudo] docker exec -it $NAME /bin/bash
```

To uninstall the artifact, run the following commands:
```
[sudo] docker images           # To list the currently installed images
[sudo] docker rmi s3           # To delete the prosynth image
[sudo] docker images           # To verify successful deletion
```

Structure of the Experiments
----------------------------

In this paper, we present a tool called S3 to calculate the sub-specification for SyGuS and DreamCoder. S3 consists of
two parts that calculate the sub-specifications for SyGuS and DreamCoder tasks respectively. All the results presented
in the paper can be reproduced the following 3 steps:

1. __Apply S3 to SyGuS problems:__ Run CVC5 and EUSolver on synthesis tasks from the 2017 SyGuS Competition. We then
   obtain the implementations and finally run S3 on all the program locations on the previously obtained
   implementations.
  
   The data from this experiment is used to produce __Figure 4 and 5__, and __Table 1__ in the main paper.

2. __Apply S3 to DreamCoder problems:__ Run S3 to the synthesis tasks from DreamCoder that involve list processing. We
   provide the tasks and synthesized implementations in the file `synthesized_code.json`.

   The data from this experiment is used to produce __Figure 4__ in the main paper.

3. __Generate Figures:__ Run the data processing scripts to extract data from the first two steps and draw the figures.

Reproducing SyGuS Benchmark Experiment
--------------------------------------

This experiment consists of two steps: Obtaining the synthesis result from SyGuS solver and calculate their
sub-specifications. Execute the following commands:
```
cd /OOPSLA2023-Artifact/SyGuS
./scripts/get-impls.sh
./scripts/process-impls.sh
./scripts/do-runs.sh
cd ..
python3 extract_sygus_data.py
```

The second command took approximately 3 hours on a Ryzen 5950X and the fourth command takes approximately 8 hours. Note
that the script uses the `task-spooler` utility to concurrently schedule jobs. As a result, the tasks are not
necesssarily all complete when the top-level command exits. We recommend running `tsp` to monitor the status of these
scheduled tasks.

The raw data are stored in `./SyGuS/impls`. The last command will produce all the statistics necessary for reproducing
the figures and table in `cvc5.csv` and `eusolver.csv` under `/OOPSLA2023-Artifact`. 


Reproducing DreamCoder Benchmark Experiment
-------------------------------------------

This experiment consists of a single step, which is to calculate the sub-specification for all the implementations
listed in `synthesized_code.json`. Execute the following command:

```
cd /OOPSLA2023-Artifact/DreamCoder
python3 main.py synthesized_code.json > output.txt
```

This experiment is very quick and should only require a few minutes to complete. After the execution, the
sub-specifications are stored in `output.txt` and the statistics are stored in the file `DC.csv`.


Reproducing the Figures and Tables from the Paper
-------------------------------------------------

After running the 2 experiments above, we should have `cvc5.csv` and `eusover.csv` under `/OOPSLA2023-Artifact` and
`DC.csv` under `/OOPSLA2023-Artifact/DreamCoder`.

Start by returning to the root directory of the artifact:
```
cd /OOPSLA-Artifact
```

To obtain __Figure 4__ and __Table 1__, run:
```
python3 draw_reduction.py
```
The script will print two lines, each having three numbers. These 6 numbers are the statistics reported in __Table 1__.
It will also produce a new file named `reduction.pdf` which is __Figure 4__.

To obtain __Figures 5a__ and __5b__, run:
```
python3 draw_runtime_dist.py
python3 draw_compare_time.py
```
The two scripts will produce the corresponding figures in the files named `runtime-dist.pdf` and `compare-time.pdf`
respectively.
 
Tutorial to Run S3
------------------

We now present a brief tutorial to run S3 on specification-implementation pairs of the user's choosing. As we mentioned
earlier, our S3 artifact contains two implementations that target SyGuS and DreamCoder respectively.

SyGuS
-----

1. Pick a specification from the tests directory:

   ```
   cd SyGuS
   find tests -name ‘*.sl’
   ```

   a. Specifications are described using Version 1.0 of the SyGuS language. The specification language is defined in
      (https://sygus.org/assets/pdf/SyGuS-IF.pdf).

   b. We provide copies of the problems from the 2017 SyGuS Competition in the directory
      `tests/sygus-benchmarks/comp/2017`.

2. Run the SyGuS solver of your choice. For example

   ```
   $ export SPEC_SL=tests/sygus-benchmarks/comp/2017/General_Track/max2.sl
   $ [./run_cvc5.sh | ./run_eusolver.sh] $SPEC_SL | tee impl.sl
   ```

3. Examine the implementation and determine the program location of interest. For example, say the implementation
   produced is:

   ```
   (define-fun max2 ((x Int) (y Int)) Int (ite (<= x y) y x))
   ```

   Every sub-expression of this implementation may be identified with an address. For example, the then-branch of the
   conditional has the address `0 4 2 -1`, corresponding sequentially to the indices of its ancestors in the
   s-expression. The final -1 is an end-of-address marker.

4. Run S3:

   ```
   echo 0 4 2 -1 | ./run_s3.sh $SPEC_SL impl.sl 2> /dev/null
   ```

   The implementation also prints detailed logs from various points in its execution. These logs may be viewed by
   removing the final stderr redirect to `/dev/null`.

DreamCoder
----------

We provide copies of problems and their corresponding implementations from the DreamCoder artifact
(https://dl.acm.org/do/10.1145/3410302/full/) in the `synthesized_code.json`. We produced this file by pre-processing
data in the `list_tasks.json` file in the artifact distribution. For the sake of experimentation, we provide a minimal
version of this file with one specification-implementation pair in `minimal.json`. To execute S3:

```
cd DreamCoder
python3 main.py minimal.json
```

Implementations produced by DreamCoder are lambda-expressions written using de Bruijn indices. Some sub-expressions are
highlighted with a pound sign, indicating their status as elements of the constructed library. S3 prints subspecs for
each of these highlighted functions.
