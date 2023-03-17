#! /bin/bash
# use git-stein
python launcher_gitrepoMaker.py -p ANDROID -g Spring
python launcher_gitrepoMaker.py -p BATCH -g Spring
python launcher_gitrepoMaker.py -p BATCHADM -g Spring
python launcher_gitrepoMaker.py -p DATACMNS -g Spring
python launcher_gitrepoMaker.py -p DATAGRAPH -g Spring
python launcher_gitrepoMaker.py -p DATAJPA -g Spring
python launcher_gitrepoMaker.py -p DATAMONGO -g Spring
python launcher_gitrepoMaker.py -p DATAREDIS -g Spring
python launcher_gitrepoMaker.py -p LDAP -g Spring
python launcher_gitrepoMaker.py -p MOBILE -g Spring
python launcher_gitrepoMaker.py -p SEC -g Spring
python launcher_gitrepoMaker.py -p SECOAUTH -g Spring
python launcher_gitrepoMaker.py -p SGF -g Spring
python launcher_gitrepoMaker.py -p SHDP -g Spring
python launcher_gitrepoMaker.py -p SHL -g Spring
python launcher_gitrepoMaker.py -p SOCIAL -g Spring
python launcher_gitrepoMaker.py -p SOCIALFB -g Spring
python launcher_gitrepoMaker.py -p SOCIALLI -g Spring
python launcher_gitrepoMaker.py -p SOCIALTW -g Spring
python launcher_gitrepoMaker.py -p SWF -g Spring
python launcher_gitrepoMaker.py -p SWS -g Spring
# add digest option
python launcher_gitrepoMaker.py -p AMQP -g Spring -d
python launcher_gitrepoMaker.py -p DATAREST -g Spring -d
python launcher_gitrepoMaker.py -p ROO -g Spring -d

# Change the src folder for each version to a method-level repository
python launcher_GitInflator.py

# Link the actual modified method files
python launcher_repoMaker.py
python launcher_DupRepo.py

# Count bugs and files
python Counting.py

# change java version from 11 to 8
update-alternatives --config java
