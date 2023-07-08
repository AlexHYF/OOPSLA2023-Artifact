# sudo setenforce Permissive
# sudo systemctl start docker
# # See https://www.youtube.com/watch?v=YFl2mCHdv24

########################################################################################################################

FROM ubuntu:22.04
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y git autoconf automake make\
                       gcc g++ mcpp cmake\
                       python3 python3-pip openjdk-8-jre\
                       sqlite libsqlite-dev sqlite3 libsqlite3-dev \
                       zlib1g zlib1g-dev \
                       doxygen libncurses5-dev libtool libffi-dev wget graphviz gnupg2 \
                       task-spooler procps passwd openssh-server vim curl\
                       libmpfr-dev libgmp-dev libboost-all-dev

RUN pip install --upgrade pip

RUN pip install pandas matplotlib scipy

RUN  git clone https://github.com/AlexHYF/OOPSLA2023-Artifact.git && cd OOPSLA2023-Artifact &&  cd SyGuS && ./scripts/build.sh cvc5 && ./scripts/build.sh eusolver 

CMD /bin/bash

########################################################################################################################

# sudo docker build -t IMAGE_NAME .
# sudo docker images
# sudo docker run -it IMAGE_NAME /bin/bash

########################################################################################################################

# sudo docker images
# sudo docker rmi IMAGE_NAME
# sudo docker images
