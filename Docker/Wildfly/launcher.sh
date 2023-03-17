#! /bin/bash
# use git-stein
python launcher_gitrepoMaker.py -p WFARQ -g Wildfly
python launcher_gitrepoMaker.py -p WFMP -g Wildfly
python launcher_gitrepoMaker.py -p SWARM -g Wildfly
# add digest option
python launcher_gitrepoMaker.py -p ELY -g Wildfly -d
python launcher_gitrepoMaker.py -p WFCORE -g Wildfly -d
python launcher_gitrepoMaker.py -p WFLY -g Wildfly -d

# Change the src folder for each version to a method-level repository
python launcher_GitInflator.py

# Link the actual modified method files
python launcher_repoMaker.py
python launcher_DupRepo.py

# Count bugs and files
python Counting.py

# change java version from 11 to 8
update-alternatives --config java
