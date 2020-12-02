#!/bin/bash



sessionTeruel=$(curl  -sc - 'localhost:5000/' | grep session | cut -f7)

sessionZaragoza=$(curl  -sc - 'localhost:5000/' | grep session | cut -f7)

zaragoza() {
curl -s   http://localhost:5000/chat  -H "Cookie:session=$sessionZaragoza;"   -d '{"text":"Quien es el alcalde de Zaragoza","timeout":false}'    -H 'content-type:application/json' -H 'Accept: application/json' | jq '  .answer[1]== "El alcalde de Zaragoza es Jorge Antonio Azcon Navarro"'&
}

teruel(){
curl -s   http://localhost:5000/chat  -H "Cookie:session=$sessionTeruel;"   -d '{"text":"Quien es el alcalde de Teruel","timeout":false}'    -H 'content-type:application/json' -H 'Accept: application/json' | jq '  .answer[1]== "El alcalde de Teruel es Emma Buj Sánchez"'&
}


huesca(){
sessionHuesca=$(curl  -sc - 'localhost:5000/' | grep session | cut -f7)
curl -s   http://localhost:5000/chat  -H "Cookie:session=$sessionHuesca;"   -d '{"text":"Quien es el alcalde de Huesca","timeout":false}'    -H 'content-type:application/json' -H 'Accept: application/json' | jq '  .answer[1]== "El alcalde de Huesca es Luis Eliseo Felipe Serrate"'&
}


for i in {1..10}
do 
  zaragoza
  teruel
  huesca
done


