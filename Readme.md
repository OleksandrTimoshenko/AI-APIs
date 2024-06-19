docker build -t gpt_api ./

docker run -it -v ./trainingData:/trainingData gpt_api bash
or
docker run -v ./trainingData:/trainingData gpt_api python /app.py