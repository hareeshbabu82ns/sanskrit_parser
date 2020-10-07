#!/bin/bash
build_docker(){
  echo "building docker image locally"
  docker build -f Dockerfile.api -t $image_title:$image_version .   
}

deploy_docker(){
  echo "deploying docker image $deploy_location, version $image_version, title $image_title"
  if [ $deploy_location = "local" ]; then
    # docker stop "$image_title"
    echo "stopping and removing container $image_title"
    docker rm "$image_title"  -f
    echo "deploying new container $image_title"
    docker run -p $port:9000 -d --name $image_title $image_title:$image_version
  else
    echo "saving docker image"
    docker save -o "$image_title.tar" $image_title:$image_version
    echo "copying image to remote"
    scp "$image_title.tar" $remote_user@$remote_ip:$remote_tmp
    echo "loading image on remote"
    ssh $remote_user@$remote_ip docker load -i "$remote_tmp/$image_title.tar"
    echo "stopping and removing existing container $image_title"
    ssh $remote_user@$remote_ip docker rm "$image_title" -f
    echo "deploying new container $image_title on remote"
    ssh $remote_user@$remote_ip docker run -d -p "$port:9000/tcp" --name $image_title --net="proxynet" $image_title:$image_version
  fi
}

usage(){
  echo "$> deploy_api.sh [-t <image_title>] -v <image_version> [-l <location>] [-p <port>] [-h]"
  echo "ex: $> sh deploy_api.sh -t sanskrit_parser -v 1.0 -p 9000"
  echo "ex: $> sh deploy_api.sh -v 1.2 -p 28374 -l remote -r 192.168.0.2"
}

##### Main

image_title=sanskrit_parser
image_version=
deploy_location="local"
port=9000
remote_ip=
remote_user="root"
remote_tmp="/mnt/cache/tmp"

while [ "$1" != "" ]; do
    case $1 in
        -t | --title )           shift
                                image_title=$1
                                ;;
        -v | --version )        shift
                                image_version="v$1"
                                ;;
        -r | --remote )         shift
                                remote_ip=$1
                                ;;    
        -u | --user )           shift
                                remote_user=$1
                                ;;                                                            
        -l | --location )       shift
                                deploy_location=$1
                                ;;         
        -p | --port )           shift
                                port=$1
                                ;;                                                        
        -h | --help )           usage
                                exit
                                ;;
        * )                     usage
                                exit 1
    esac
    shift
done

if [ "$image_version" == "" ]; then
  echo "Image Version (-v) is required"
  usage
  exit 1
fi

if [ $deploy_location != "local" ] && [ "$remote_user" == "" ]; then
  echo "Remote User (-u) is required"
  usage
  exit 1
fi

if [ $deploy_location != "local" ] && [ "$remote_ip" == "" ]; then
  echo "Remote IP (-r) is required"
  usage
  exit 1
fi

build_docker

deploy_docker

echo "done"