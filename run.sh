
container=Pingator
img=tomkat/pingator

docker build -t $img .


docker container stop $container
docker container rm $container

#ports - host:container
docker run -d  -p 8083:80 \
    --restart always \
    --name $container \
    -v pingator_config:/mnt/config/ \
    -e TZ=Europe/Kiev \
    $img