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
[sudo] docker rmi s3     # To delete the prosynth image
[sudo] docker images           # To verify successful deletion
```

Structure of the Experiments
----------------------------

In this paper, we present a tool called S3 to calculate the sub-specification for SyGuS and DreamCoder. S3 consists of
2 parts that calculate the sub-specification for SyGuS tasks and DreamCoder tasks respectively. All the results
presented in the paper can be reproduced the following 3 steps:

1. __SyGuS:__ Run CVC5 and EUSolver on SyGuS competition 2017 benchmarks, obtain the implementations and the runtime
  statistics. Then run S3 on all the program locations on the previously obtained implementations.
  
  The data from this experiment is used to produce __Figure 4 and 5__, and __Table 1__ in the main paper.

2. __DreamCoder:__ Run S3 on DreamCoder List benchmark. We provide the tasks and synthesized implementations in
   `synthesized_code.json`.

  The data from this experiment is used to produce __Figure 4__ in the main paper.

3. __Generate Figure:__ Run the data processing scripts to extract data from the first 2 steps and draw the figures.

Reproducing SyGuS benchmark experiment
--------------------------------------

This experiment consists of 2 steps: Obtaining the synthesis result from SyGuS solver and calcute their
sub-specifications. Execute the following sub-tasks:
```
cd /OOPSLA2023-Artifact/SyGuS
./scripts/get-impls.sh
./scripts/process-impls.sh
./scripts/do-runs.sh
cd ..
python3 extract_sygus_data.py
```

Notice that the second command takes approximately 3 hours on a Ryzen 5950X and the forth command takes approximately 8 
hours. We use `task-spooler` to schedule the jobs so the tasks are not necessarily completed when the command exits and we
recommand using `tsp` to determine if the experiment is completed(no more queued and running tasks).

The raw data from the second and the third command are stored in `./SyGuS/impls`, and the last command will produce the
all the statistics necessary for reproducing the figures and table in `cvc5.csv` and `eusolver.csv` under
`/OOPSLA2023-Artifact`. 


Reproducing DreamCoder benchmark experiment
-------------------------------------------

This experiment consists of 1 step, which is to calculate the sub-specification for all the implementations in
`synthesized_code.json`. Execute the following command:

```
cd /OOPSLA2023-Artifact/DreamCoder
python main.py synthesized_code.json > output.txt
```

This experiment runs very fast and should complete within minutes. After the execution, the sub-specifications are
stored in `output.txt` and the statistics are stored in `DC.csv`


Reproducing all the figures and table
-------------------------------------

After running the 2 experiments above. We should have `cvc5.csv` and `eusover.csv` under `/OOPSLA2023-Artifact` and
`DC.csv` under `/OOPSLA2023-Artifact/DreamCoder`.

Go to the root of the artifact:
```
cd /OOPSLA-Artifact
```
To obtain __Figure 4__ and __Table 1__, run:
```
python3 draw_reduction.py
```
The script will print 2 lines, each has 3 numbers. These 6 numbers are __Table 1__. It will also produce
`reduction.pdf` which is __Figure 4__.
To obtain __Figure 5a and 5b__, run:
```
python3 draw_runtime_dist.py
python3 draw_compare_time.py
```
The first script will produce __Figure 5a__ in `runtime-dist.pdf` and the second script will produce __Figure 5b__ in 
`compare-time.pdf`.
 
Tutorial to run S3
------------------

As mentioned earlier, S3 consists of 2 parts that handles SyGuS and DreamCoder respectively.

SyGuS
-----

1. Pick a specification from the tests directory:

   ```
   $ cd SyGuS
   $ find tests -name ‘*.sl’
   ```

   a. Specifications are described using Version 1.0 of the SyGuS language. The specification
      language is defined in (https://sygus.org/assets/pdf/SyGuS-IF.pdf).

   b. We provide copies of the problems from the 2017 SyGuS Competition in the directory
      `tests/sygus-benchmarks/comp/2017`.

2. Depending on your platform, run the SyGuS solver of your choice. For example

   ```
   $ export SPEC_SL=tests/sygus-benchmarks/comp/2017/General_Track/max2.sl
   $ (./run_cvc5.sh | ./run_eusolver.sh) $SPEC_SL | tee impl.sl
   ```

3. Examine the implementation and determine the hole of interest. For example, say the
   implementation produced is:

   ```
   (define-fun max2 ((x Int) (y Int)) Int (ite (<= x y) y x))
   ```

   Every sub-expression of this implementation may be identified with an address. For example, the
   then-branch of the conditional has the address `0 4 2 -1`, corresponding sequentially to the
   indices of its ancestors in the s-expression. The final -1 is an end-of-address marker.

4. Run S3:

   ```
   echo 0 4 2 -1 | ./run_s3.sh $SPEC_SL impl.sl 2> /dev/null
   ```

  The implementation also prints detailed logs from various points in its execution. These logs may
  be viewed by removing the final stderr redirect to `/dev/null`.

DreamCoder
----------

We provide copies of problems and their corresponding implementations from the DreamCoder artifact
(https://dl.acm.org/do/10.1145/3410302/full/) in the `synthesized_code.json`. We produced this file
by pre-processing data in the `list_tasks.json` file in the artifact distribution. For the sake of
experimentation, we provide a minimal version of this file with one specification-implementation
pair in `minimal.json`. To execute S3:

```
$ cd DreamCoder
$ python3 main.py minimal.json
```

Implementations produced by DreamCoder are lambda-expressions written using de Bruijn indices. Some
sub-expressions are highlighted with a pound sign, indicating their status as elements of the
constructed library. S3 prints subspecs for each of these highlighted functions.
