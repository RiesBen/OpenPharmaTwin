from .compartments import factory
from .process import campaignA
from .simulation import run_campaign_on_factory

import simpy as sim

import pandas as pd



# Run simulation:
dfs_list = []
for i in range(1,6):
    print(i)
    env = sim.Environment()
    env.prod_durations = []

    # Plant Modell
    plant = factory(env=env,
                    num_ferm_stage1=4, num_ferm_stage2=i, num_ferm_stage3=i, num_ferm_stage4=i*2,
                    num_harvester=i)

    # Simulation
    simulation = run_campaign_on_factory(env=env, campaign=campaignA,
                                         plant=plant, num_runs=20)
    env.process(simulation)
    env.run()

    # Results
    df = pd.DataFrame(env.prod_durations)
    df['num_stage3'] = i
    dfs_list.append(df)

dfs=pd.concat(dfs_list, ignore_index=True)