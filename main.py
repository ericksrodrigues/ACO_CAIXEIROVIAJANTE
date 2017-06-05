import util
import ACO
import random
from pprint import pprint

ambient = util.generateCities(30)
antColony = ACO.antColony(len(ambient['cities']),random.randrange(0,len(ambient['cities'])))

ACO.ACO(antColony,ambient,0.1)