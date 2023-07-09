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
[sudo] docker rmi prosynth     # To delete the prosynth image
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
./scripts/do-runs.sh
cd ..
python extract_sygus_data.py
```

Notice that the second command takes approximately 6 hours on a Ryzen 5950X and the third command takes approximately 24
hours. We use tsp to schedule the jobs and we recommand using `htop` to determine if the experiment is complete.

The raw data from the second and the third command are stored in `./SyGuS/impls`, and the last command will produce the
all the data necessary for reproducing the figures and table in `cvc5.csv` and `eusolver.csv` under
`/OOPSLA2023-Artifact`. 


Reproducing SyGuS benchmark experiment
--------------------------------------

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
python draw_reduction.py
```
The script will print 2 lines, each has 3 numbers. These 6 numbers are __Table 1__. It will also produce
`reduction.pdf` which is __Figure 4__.
To obtain __Figure 5a and 5b__, run:
```
python draw_runtime_dist.py
python draw_compare_time.py
```
The first script will produce __Figure 5a__ in `runtime-dist.pdf` and the second script will produce __Figure 5b__ in 
`compare-time.pdf`.
 

