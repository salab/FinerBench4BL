#! /bin/bash
# use git-stein
python launcher_gitrepoMaker.py -p CODEC -g Commons
python launcher_gitrepoMaker.py -p COLLECTIONS -g Commons
python launcher_gitrepoMaker.py -p COMPRESS -g Commons
python launcher_gitrepoMaker.py -p CONFIGURATION -g Commons
python launcher_gitrepoMaker.py -p CRYPTO -g Commons
python launcher_gitrepoMaker.py -p CSV -g Commons
python launcher_gitrepoMaker.py -p IO -g Commons
python launcher_gitrepoMaker.py -p LANG -g Commons
python launcher_gitrepoMaker.py -p WEAVER -g Commons
# add digest option
python launcher_gitrepoMaker.py -p MATH -g Commons -d

# Change the src folder for each version to a method-level repository
python launcher_GitInflator.py

# Link the actual modified method files
python launcher_repoMaker.py
python launcher_DupRepo.py

# Count bugs and files
python Counting.py

# change java version from 11 to 8
update-alternatives --config java
