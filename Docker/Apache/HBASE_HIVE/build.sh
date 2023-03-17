#!/bin/bash

# set args as container and image name
while getopts c:i: OPT
do
  case $OPT in
    "c" ) FLG_C="TRUE" ; CONTAINER="$OPTARG" ;;
    "i" ) FLG_I="TRUE" ; IMAGE="$OPTARG" ;;
    * ) echo "Usage: $CMDNAME [-c container name] [-i image name]" 1>&2
        exit 1 ;;
  esac
done

# オプションなしで実行させない
if [ ! "$FLG_C" = "TRUE" ] && [ ! "$FLG_I" = "TRUE" ]; then
  echo "Usage: $CMDNAME [-c container name] [-i image name]"
  exit 1
fi

if [ "$FLG_C" = "TRUE" ]; then
  echo "conitaner name is : $CONTAINER"
fi

if [ "$FLG_I" = "TRUE" ]; then
  echo "image name is : $IMAGE"
fi

# execute copy.sh
MSG=`./copy.sh`
echo $MSG

# build docker
docker build -t $IMAGE --force-rm .
docker run -it --name $CONTAINER $IMAGE /bin/bash
