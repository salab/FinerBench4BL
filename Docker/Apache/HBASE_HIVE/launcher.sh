#! /bin/bash
# use git-stein
python launcher_gitrepoMaker.py -p HBASE -g Apache
python launcher_gitrepoMaker.py -p HIVE -g Apache

# Change the src folder for each version to a method-level repository
python launcher_GitInflator.py

# Link the actual modified method files
python launcher_repoMaker.py
python launcher_DupRepo.py

# Count bugs and files
python Counting.py

# change java version from 11 to 8
update-alternatives --config java
