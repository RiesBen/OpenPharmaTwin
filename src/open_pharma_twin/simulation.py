import pandas as pd

from .factory.plant import biomanufacturing_plant



def run_campaign_on_factory(env, campaign, plant:biomanufacturing_plant, monitor, num_runs=10): #Simulation Control
    for run in range(num_runs):
        env.process(campaign(env, run, plant, monitor))
        yield env.timeout(0)  # Wait a bit before generating a new person

class Monitor:
    def __init__(self, env):
        self.env = env
        self._equippment_monitor = []
        self._process_monitor = []
        self._campaign_monitor = []
        self._ressource_monitor = []

    @property
    def equippment_monitor(self):
        return pd.DataFrame(self._equippment_monitor)

    @property
    def process_monitor(self):
        return pd.DataFrame(self._process_monitor)

    @property
    def campaign_monitor(self):
        return pd.DataFrame(self._campaign_monitor)

    @property
    def ressource_monitor(self):
        return pd.DataFrame(self._ressource_monitor)

    def record_vessel(self, campaignID, vessel, action):
        equippment_usage = {"name": vessel.name, "Campaign_ID": campaignID, "time": self.env.now, "level": vessel.level, "action": action}
        self._equippment_monitor.append(equippment_usage)

    def record_process(self, campaignID, process, action):
        process_monitor = {"name": process, "Campaign_ID": campaignID, "time": self.env.now, "action": action}
        self._process_monitor.append(process_monitor)

    def record_campaign(self, campaignID, action):
        product_monitor = {"name": campaignID, "time": self.env.now, "action": action}
        self._campaign_monitor.append(product_monitor)

    def record_ressource(self, campaignID, process, ressource, requires):
        ressource_monitor = {"campaign": campaignID, "process":process, "ressource":ressource, "time": self.env.now, "requires": requires}
        self._ressource_monitor.append(ressource_monitor)
