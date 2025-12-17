import simpy as sim

class biomanufacturing_plant():
    def __init__(self, upstream, downstream=None):
        self.upstream =upstream
        self.downstream = downstream
