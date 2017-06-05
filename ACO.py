import random
import matplotlib.pyplot as plt
from pprint import pprint

def ant(original_position):
    ant_return = {
        "memory_cities": [original_position],
        "memory_roads": [],
        "position": original_position,
        "original_position": original_position
    }
    return ant_return

def antColony(size,original_position):
    antColony_return = []
    for i in range(0,size):
        antColony_return.append(ant(original_position))
    return antColony_return

def probability(ambient,antColony,current_ant):
    possible_targets = [ x for x in ambient['cities'][current_ant['position']]['target_cities'] if x not in current_ant['memory_cities']]

    if len(possible_targets) == 0:
        possible_targets = [ x for x in ambient['cities'][current_ant['position']]['target_cities'] ]
    all_values = 0.0
    arr_probability = []
    for target in possible_targets:
        id_road = get_road(current_ant['position'], target,ambient['roads'])
        all_values += ambient['roads'][id_road]['pheromone']*ambient['roads'][id_road]['pheromone']*(1.0/ambient['roads'][id_road]['distance'])
    for target in possible_targets:
        id_road = get_road(current_ant['position'], target, ambient['roads'])
        arr_probability.append({ 
   
            "probability": ambient['roads'][id_road]['pheromone']*ambient['roads'][id_road]['pheromone'] * (1.0/ambient['roads'][id_road]['distance']) / all_values,
            "target": target
            
            })
    return arr_probability

def get_road(position_a,position_b,roads):
    low = position_a
    high = position_b
    if low > high:
        low = high
        high = position_a
    return next(x for x in range(0,len(roads)) if roads[x]['source'] == low and roads[x]['target'] == high)

def move_ant(arr_probability):
    
    randValue = random.uniform(0,1)
    aux = 0.0
    i = 0
    for prob in arr_probability:
        aux += prob["probability"]
        if aux > randValue:
            break
        i += 1
    return arr_probability[i]["target"]

def ACO(ant_colony, ambient, evaporation_coeficient):
    pheromone = []
    for i in range(0,len(ambient['roads'])):
        pheromone.append([])
    flag = True
    while flag:
        for index,ant in enumerate(ant_colony):

            while len(ant['memory_cities']) < len(ambient['cities']):
                #print ant['position']
                arr_probability = probability(ambient,ant_colony, ant)
                new_position = move_ant(arr_probability)
                ant['memory_roads'].append(get_road(new_position,ant['position'],ambient['roads']))
                if new_position not in ant['memory_cities']:
                    ant['memory_cities'].append(new_position)
                ant['position'] = new_position
                if len(ant['memory_cities']) == len(ambient['cities']) and ant['memory_cities'][0] == ant['original_position']:
                    del ant['memory_cities'][0]
                #print ant['memory_cities']
                #print ant['memory_roads']
            ant['memory_cities'] = [ant['original_position']]
            ant_colony[index] = ant
        
        #evaporation
        for index,road in enumerate(ambient['roads']):
            ambient['roads'][index]['pheromone'] = (1 - evaporation_coeficient)*road['pheromone']
            if ambient['roads'][index]['pheromone'] < 1:
                ambient['roads'][index]['pheromone'] = 1
        #update pheromone
        for index,ant in enumerate(ant_colony):
            distance = 0
            for id_road in ant['memory_roads']:
                distance += ambient['roads'][id_road]['distance']
            for id_road in ant['memory_roads']:
                ambient['roads'][id_road]['pheromone'] += (10.0)/distance
        if has_same_routes(ant_colony):
            flag = False
        else:
            for index,ant in enumerate(ant_colony):
                ant_colony[index]['memory_roads'] = []

        for index,road in enumerate(ambient['roads']):
            pheromone[index].append(road['pheromone'])
    
    pprint(ambient)
    distance = 0
    for index,dataroad in enumerate(pheromone):
        plt.plot(range(0,len(dataroad)), dataroad)
    for id_road in ant['memory_roads']:
        distance += ambient['roads'][id_road]['distance']
    pprint(distance)
    plt.show()

    pprint(ant_colony[0]['memory_roads'])
    return ant_colony[0]['memory_roads']
    

  
def has_same_routes(ant_colony):
    ant_roads = ant_colony[0]['memory_roads']
    for ant in ant_colony:
        for road in ant['memory_roads']:
            if road not in ant_roads:
                return False
    return True


    