from TextSimilar import cosine_sim
from numpy import argmax
import json

with open('../data_processing/scrape_store.json') as json_file:
  textArr = json.load(json_file)

testList = []
for article in textArr:
  testList.append(article['textData']);
  # print(article['title']);

similarityMatrix = cosine_sim(*testList).tolist()
topicsList = []
masterList = []
delCount = 0

for simList in similarityMatrix:
  topic = []
  selfIndex = simList.index(max(simList))
  # DEBUG LINE
  # topic.append(textArr[selfIndex]['title'])
  topic.append(textArr[selfIndex]);
  for simIndex in range(selfIndex + 1, len(simList)):
    if (simList[simIndex] < 0.95 and simList[simIndex] > 0.4 and simIndex not in masterList): #refine later
      #DEBUG LINE
      # topic.append(textArr[simIndex]['title']) 
      topic.append(textArr[selfIndex])
      delCount = sum(num < simIndex for num in masterList)
      del similarityMatrix[simIndex - delCount]
      masterList.append(simIndex)
  topicsList.append(topic)

return topicsList