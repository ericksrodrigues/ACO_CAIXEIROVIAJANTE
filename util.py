import random

def generateCities(totalCities):

    cities = []
    roads = []
    #Setar redes virtuais
    for i in range(0,totalCities):
        cities.append({
            "id": i,
            "target_cities": []
        })
    #Garantir conectividade da rede
    connecteds = []

    while len(connecteds) < totalCities or random.random() < 0.85:
        maxDistanceCity = 5

        idcity = random.randrange(0,totalCities)
        if len(connecteds) < totalCities:
            if len(connecteds) == 0:
                connecteds.append(idcity)

            elif idcity not in connecteds:
                targetcity = connecteds[random.randrange(0,len(connecteds))]
                cities[idcity]['target_cities'].append(targetcity)
                cities[targetcity]['target_cities'].append(idcity)
                connecteds.append(idcity)
                roads.append({"source": idcity,"target": targetcity, "distance": random.randint(1,maxDistanceCity), "pheromone": 0} if idcity < targetcity else {"source": targetcity,"target": idcity, "distance": random.randint(1,maxDistanceCity),"pheromone": 0})
        else:
            #Gerar algumas aleatorias conexoes
            targetcity = connecteds[random.randrange(0,len(connecteds))]
            if(targetcity not in cities[idcity]['target_cities'] and idcity != targetcity):
                cities[idcity]['target_cities'].append(targetcity)
                cities[targetcity]['target_cities'].append(idcity)
                roads.append({"source": idcity,"target": targetcity, "distance": random.randint(1,maxDistanceCity), "pheromone": 0} if idcity < targetcity else {"source": targetcity,"target": idcity, "distance": random.randint(1,maxDistanceCity),"pheromone": 0})

    return {
        "cities": cities,
        "roads": roads
    }