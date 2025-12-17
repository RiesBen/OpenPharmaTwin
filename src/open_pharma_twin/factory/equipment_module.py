import simpy as sim

class Vessel(sim.Container):
    def __init__(self, name, env, init=0, capacity=250, resource=None):
        super().__init__(env=env, init=init, capacity=capacity)
        self.name= name
        self.env = env
        self.request = None
        self.resource = resource
        self.in_use = False

    def produce(self, incubation_time=20):
        yield self.env.timeout(incubation_time)

    # Reserve Ressource
    def activate_resource(self):
        self.request = self.resource.request()
        self.in_use = True
        return self.request

    def release_resource(self):
        if self.level != 0:
            raise ValueError("The Resource cannot be released, if not empty")
        self.resource.release(self.request)
        self.in_use = False

    # Move Content
    def fill(self, dv=1):
        if dv > self.capacity-self.level:
            raise ValueError("Full")
        self.put(dv)

    def remove(self, dv=-1):
        if self.level == 0:
            raise ValueError("Empty")
        elif dv < 0:
            self.get(self.level)
        elif self.level < dv:
            raise ValueError("Not Enough")
        else:
            self.get(dv)

    def transfer(self, target_vessel, dv=-1):
        if self.level == 0:
            raise ValueError("Empty")
        elif self.level < dv:
            raise ValueError("Not Enough")
        if dv < 0:
            tv = self.level
        else:
            tv = dv
        self.get(tv)
        target_vessel.fill(tv)
