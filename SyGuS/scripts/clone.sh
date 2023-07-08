# History of commands executed to clone CVC5, EUSolver and the SyGuS benchmarks into this repository
# Used subtree instead of submodule because the EUSolver repository contains some local changes to work with newer
# versions of Python

####
# To originally clone

git subtree add --prefix solvers/cvc5 https://github.com/cvc5/cvc5.git master --squash 
git subtree add --prefix solvers/eusolver https://bitbucket.org/abhishekudupa/eusolver.git master --squash
git subtree add --prefix tests/sygus-benchmarks https://github.com/SyGuS-Org/benchmarks.git master --squash

# CVC5 V1.8 is the last version to support SyGuS language standard 1.0
# https://github.com/cvc5/cvc5/releases/tag/1.8
wget -c https://github.com/cvc5/cvc5/archive/refs/tags/1.8.tar.gz
mv 1.8.tar.gz cvc5-1.8.tar.gz

####
# To subsequently update

git subtree pull --prefix solvers/cvc5 https://github.com/cvc5/cvc5.git main --squash
git subtree pull --prefix solvers/eusolver https://bitbucket.org/abhishekudupa/eusolver.git master --squash
git subtree pull --prefix tests/sygus-benchmarks https://github.com/SyGuS-Org/benchmarks.git master --squash

####
# Commit 1af865f3429c0dd5910b5a8d1e12d690c3623dfa was the last to support SyGuS V1

git subtree add --prefix solvers/cvc5 https://github.com/cvc5/cvc5.git 1af865f3429c0dd5910b5a8d1e12d690c3623dfa --squash
