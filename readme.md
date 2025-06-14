# Good Luck, Have Fun!

`docker pull coriscope/ghlf:v0.1.0-alpha`

`docker run -p 1337:1337 coriscope/ghlf:v0.1.0-alpha`

`http://localhost:1337`



docker build -t glhf:local .

docker run --rm \
  --name glhf-test \
  -p 1337:1337 \
  glhf:local

  docker exec -it glhf-test sh