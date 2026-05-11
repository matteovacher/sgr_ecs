from ecs.tools.hyperneat_base.robot_simulator import RobotSimulator

from pathos.multiprocessing import ProcessPool
import dill 
import numpy as np 
import math
import errno 
import multiprocess 



class EvaluationSystem : 
    def __init__(self, env_name, n_steps, cpus) : 
        self.env_name = env_name
        self.n_steps = n_steps
        self.cpus = cpus
        self.simulator = RobotSimulator(env_name, n_steps)

    def process(self, registry) : 

        if self.cpus > 1 : 
            self._process_parallel(registry)
        elif self.cpus == 1 : 
            self._process_sequential(registry)


    def _process_sequential(self, registry) : 
        entity_ids = [entity_id for entity_id in registry.get_all_id_with_body() if registry.has_controller_network(entity_id)]
        for entity_id in entity_ids :
            body = registry.get_body(entity_id).body 
            controller_network = registry.get_controller_network(entity_id).controller_network 

            fitness, finished = self.simulator.simulate(body, controller_network)
            registry.add_fitness(entity_id, fitness, finished)

    def _process_parallel(self, registry) :
        entity_ids = [entity_id for entity_id in registry.get_all_id_with_body() if registry.has_controller_network(entity_id)]
        bodies = [registry.get_body(entity_id).body for entity_id in entity_ids]
        controller_networks = [registry.get_controller_network(entity_id).controller_network for entity_id in entity_ids]
        chunk = list(zip(entity_ids, bodies, controller_networks))
        chunks = self._cut_chunk(chunk)
        try : 
            pool = ProcessPool(nodes = self.cpus)
            results_map = pool.amap(
                self._process_worker,
                chunks
            )
            results = results_map.get(timeout=60*10)

            for result_dictionary in results : 
                for entity_id, (fitness, finished) in result_dictionary.items() :
                    registry.add_fitness(entity_id, fitness, finished)

        except IOError as e : 
            if e.errno == errno.EPIPE : 
                print("Problem with broken pipe")
            else : 
                raise(IOError)
        except multiprocess.context.TimeoutError as e:
            print("Deu timeout!!!!!!")
            for entity_id in entity_ids : 
                if not registry.has_fitness(entity_id) :
                    registry.add_fitness(entity_id, -10000, False)

        finally : 
            pool.terminate()
            pool.clear()


    def _process_worker(self, chunk) : 
        results_dict = {}
        for entity_id, body, controller_network in chunk : 
            fitness, finished = self.simulator.simulate(body, controller_network)
            results_dict[entity_id] = (fitness, finished)  
        return results_dict 
        
    def _cut_chunk(self, chunk) : 
        chunks =[]
        length = len(chunk)
        size_of_chunk = math.ceil(length / self.cpus)
        for i in range(0, length, size_of_chunk) :
            chunks.append(chunk[i:i+size_of_chunk])
        return chunks 


        

