import simpy as sim
from .equipment_module import Vessel

class UpstreamUnit(object):  # Equipment
    def __init__(self, env, num_ferm_stage1=4, num_ferm_stage2=2,
                 num_ferm_stage3=2, num_ferm_stage4=6, num_harvester=1):
        self.env = env
        self.stats = None

        #Upstream
        self.ferm_stage1 = sim.Resource(env, capacity=num_ferm_stage1)
        stage1_vessel =lambda : Vessel("Vessel_S1", env, init=0, capacity=60, resource=self.ferm_stage1)
        self.ferm_stage1.vessels = [stage1_vessel() for i in range(num_ferm_stage1)]

        self.ferm_stage1.get_vessel = stage1_vessel

        self.ferm_stage2 = sim.Resource(env, capacity=num_ferm_stage2)
        self.ferm_stage2.get_vessel = lambda : Vessel("Vessel_S2", env, init=0, capacity=250, resource=self.ferm_stage2)
        self.ferm_stage3 = sim.Resource(env, capacity=num_ferm_stage3)
        self.ferm_stage3.get_vessel = lambda : Vessel("Vessel_S3",env, init=0, capacity=3000, resource=self.ferm_stage3)
        self.ferm_stage4 = sim.Resource(env, capacity=num_ferm_stage4)
        self.ferm_stage4.get_vessel = lambda : Vessel("Vessel_S4",env, init=0, capacity=14000, resource=self.ferm_stage4)
        self.harvester = sim.Resource(env, capacity=num_harvester)
        self.harvester.get_vessel = lambda : Vessel("harvester",env, init=0, capacity=500, resource=self.harvester)

class downstream_unit():
    def __init__(self, env, ):
        self.env=env
