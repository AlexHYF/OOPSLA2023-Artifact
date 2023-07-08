#!/usr/bin/env bash

########################################################################################################################
# Main Build Script

# Intended to be run from the root directory of the repository
# ./scripts/build.sh [cpython] [pypy3] [cvc5] [eusolver]

########################################################################################################################

# https://sipb.mit.edu/doc/safe-shell/
set -euf -o pipefail

########################################################################################################################

####
# CPython

if [[ "$@" =~ "cpython" ]]; then
    mkdir -p python
    pushd python

    # CPython

    # sudo dnf install dnf-plugins-core  # install this to use 'dnf builddep'
    # sudo dnf builddep python3

    wget -c https://www.python.org/ftp/python/3.10.5/Python-3.10.5.tar.xz
    tar -xf Python-3.10.5.tar.xz
    pushd Python-3.10.5
    ./configure --enable-optimizations --with-lto
    make -j
    popd

    popd
fi

####
# Pypy3

if [[ "$@" =~ "pypy3" ]]; then
    mkdir -p python
    pushd python

    # Pypy3, https://doc.pypy.org/en/latest/build.html

    # sudo dnf install pypy gcc make libffi-devel pkgconfig zlib-devel bzip2-devel \
    #                  sqlite-devel ncurses-devel expat-devel openssl-devel tk-devel \
    #                  gdbm-devel python-cffi gc-devel \
    #                  xz-devel # For lzma on PyPy3

    # sudo apt install gcc make libffi-dev pkg-config zlib1g-dev libbz2-dev \
    #                  libsqlite3-dev libncurses5-dev libexpat1-dev libssl-dev libgdbm-dev \
    #                  tk-dev libgc-dev python-cffi \
    #                  liblzma-dev libncursesw5-dev # these two only needed on PyPy3

    wget -c https://downloads.python.org/pypy/pypy3.9-v7.3.9-src.tar.bz2
    tar -xf pypy3.9-v7.3.9-src.tar.bz2
    pushd pypy3.9-v7.3.9-src
    pushd pypy/goal
    pypy ../../rpython/bin/rpython --opt=jit
    PYTHONPATH=../.. ./pypy3.9-c ../../lib_pypy/pypy_tools/build_cffi_imports.py
    popd
    popd

    popd
fi

####
# virtualenv

# Requires:
# 1. sexpdata for parsing s-expressions
# 2. toml for CVC5
# 3. pyparsing and z3-solver for EUSolver

# virtualenv --python=python3 venv
# . venv/bin/activate

pip install --upgrade pip
pip install sexpdata==0.03 \
                toml \
                pyparsing z3-solver

####
# CVC5

if [[ "$@" =~ "cvc5" ]]; then
    pushd ./solvers/cvc5
    ./contrib/get-antlr-3.4
    ./configure.sh # --auto-download
    pushd build
    make -j
    popd
    popd
fi

####
# EUSolver

if [[ "$@" =~ "eusolver" ]]; then
    pushd ./solvers/eusolver
    ./scripts/build.sh
    popd
fi
