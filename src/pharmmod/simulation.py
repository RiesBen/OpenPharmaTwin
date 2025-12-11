
from .compartments import factory
def run_campaign_on_factory(env, campaign, plant:factory, num_runs=10): #Simulation Control
    for run in range(num_runs):
        env.process(campaign(env, run, plant))
        yield env.timeout(0)  # Wait a bit before generating a new person
