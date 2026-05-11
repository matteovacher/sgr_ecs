from entity_manager import EntityManager
from registry import ComponentRegistry

class World : 

    def __init__(self) :
        self.entities = EntityManager()
        self.registry = ComponentRegistry()
        self._systems = []

    def add_system(self, system) : 
        self._systems.append(system)

    def reset(self) : 
        self.registry.clear_all_except_genome()

    def step(self) : 
        for system in self._systems : 
            system.process(self.registry)



