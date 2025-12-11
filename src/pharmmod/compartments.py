import simpy as sim
import numpy as np
import pandas as pd


class Vessel(sim.Container):
    def __init__(self, env, init=0, capacity=250, incubation_time=19, resource=None):
        super().__init__(env=env, init=init, capacity=capacity)
        self.incubation_time = incubation_time
        self.env = env
        self.request = None
        self.resource = resource
        self.in_use = False

    def activate_resource(self):
        self.request = self.resource.request()
        self.in_use = True
        return self.request

    def release_resource(self):
        self.resource.release(self.request)
        self.in_use = False

    def produce(self, runID=None):
        yield self.env.timeout(self.incubation_time)

    def transfer(self, target_vessel, dv=-1):
        if dv < 0:
            tv = self.level
        else:
            tv = dv
        self.get(tv)
        target_vessel.put(tv)


class factory(object):  # Equipment
    def __init__(self, env, num_ferm_stage1=4, num_ferm_stage2=2,
                 num_ferm_stage3=2, num_ferm_stage4=6, num_harvester=1):
        self.env = env
        self.ferm_stage1 = sim.Resource(env, capacity=num_ferm_stage1)
        self.ferm_stage1.get_vessel = lambda : Vessel(env, init=0, capacity=60, incubation_time=20, resource=self.ferm_stage1)
        self.ferm_stage2 = sim.Resource(env, capacity=num_ferm_stage2)
        self.ferm_stage2.get_vessel = lambda : Vessel(env, init=0, capacity=250, incubation_time=120, resource=self.ferm_stage2)
        self.ferm_stage3 = sim.Resource(env, capacity=num_ferm_stage3)
        self.ferm_stage3.get_vessel = lambda : Vessel(env, init=0, capacity=3000, incubation_time=240, resource=self.ferm_stage3)
        self.ferm_stage4 = sim.Resource(env, capacity=num_ferm_stage4)
        self.ferm_stage4.get_vessel = lambda : Vessel(env, init=0, capacity=14000, incubation_time=1000, resource=self.ferm_stage4)
        self.harvester = sim.Resource(env, capacity=num_harvester)
        self.harvester.get_vessel = lambda : Vessel(env, init=0, capacity=500, incubation_time=100, resource=self.harvester)
        self.stats = None


def run_campaign_on_factory(env, campaign, plant:factory, num_runs=10): #Simulation Control
    for run in range(num_runs):
        env.process(campaign(env, run, plant))
        yield env.timeout(0)  # Wait a bit before generating a new person
