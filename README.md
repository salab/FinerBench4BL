## Environment

`Docker 20.10.8 (Client), 20.20.12 (Server)`

## Environment in Docker

- `Python 2.7`
- `Java JDK1.8` ← to run IRBL techniques
- `Java JDK11` ← to run git-stein

### Directory

- /Docker
  - Generate Docker containers for each project
- /Docker/newscripts
  - There are modified evaluation scripts and startup shell scripts
- /scripts
  - Bench4BL's evaluation scripts
- /techniques
  - IRBL techniques' jar file
  - /techniques/method_jar
    - Method level IRBL techniques' jar file
  - /techniques/file_jar
    - Fixed file level jar file provided in Bench4BL's IRBL techniques

## Preparation

### Convert the file level repository to the method level

1. Clone this repository
2. Make docker containers. The Docker directory has been divided into groups of experimental targets (46 projects in Bench4BL), so move to the directory of the group you want to experiment with.
   `Apache/CAMEL`
   `Apache/HBASE_HIVE`
   `Commons`
   `JBoss`
   `Wildfly`
   `Spring`
   `Spring_SPR`
3. Run build.sh. At this point, the container name and image name can be set freely.

```
$ chmod +x build.sh
$ ./build.sh -c {container-name} -i {image-name}
```

For example, when creating a container for `Commons`

```
$ cd /Docker/Commons
$ ./build.sh -c commons-container -i commons-image
```

4. Enter the container you have built.
5. In contaner, run `launcher.sh`. `launcher.sh` is in `Bench4BL/scripts/`. In this scripts, Historinc, which is the repository transformation tool, is executed. And in this process, oracles at the method level are generated.

```
$ cd scripts/
$ chmod +x launcher.sh
$ ./launcher.sh
```

6. At the end of launcher.sh, you are asked what version of Java you want to use, so select JDK1.8.

## Experiments

Run `launcher_Tool.py`.

```
$ cd /Bench4BL/scripts
$ timeout -sKILL 40000 python launcher_Tool.py -w {output-directory-name} -g {group} -p {project}
```

options

- `-w` specifies the output directory name
- `-g` is the group to be experimented with
- `-p` is the project to be experimented with
- `-t` selects the IRBL tool to experiment

If `-g`, `-p` are not specified IRBL techniques will be run for all projects.
If `-t` is not specified, all IRBL techniques will be run.

## Analysis

Change name="test" in line 449 of `XLSResultsAll.py` to the name of the output file

```
e.g.) Outputting results of ExpCommons
name = "ExpCommons".
```

Generate an xlsx file for analysis.

```
$ python XLSResultsAll.py
```

An xlsx file for analysis is generated in /expresults with a name like Result_ExpCommons.xlsx.

---

# DockerFile set

Run build.sh and build the container.

```
$ ./build.sh -c {container-name} -i {image-name}
```

What `copy.sh` copies are all the files in the newscripts.
Copy the modified scripts you want to put into the container

## shell scripts

- build.sh
  - script to launch Docker containers.
- copy.sh
  - Script to copy here what is needed to build the container and run the techniques.
  - Called within build.sh.
- download.sh, launcher.sh, Subjects.py
  - Scripts are executed in each container—scripts are different for each project.
