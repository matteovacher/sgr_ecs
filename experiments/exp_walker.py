from world import World 
from systems.build_system import BuildSystem
from systems.speciation_system import SpeciationSystem
from systems.eval_system import EvaluationSystem

from tools.hyperneat_base.morpho_genome import MorphoAwareGenome

import neat 

class WalkerExperiment : 

    def __init__(self, sgr_config) : 
        self.world = World()
        # config here is what is obtained from the json file so hyperparameters 
        self.config = self._create_config(sgr_config)

        MorphoAwareGenome.configure(self.config, 
                                    sgr_config.robot_size, 
                                    sgr_config.spec_genotype_weight, 
                                    sgr_config.spec_phenotype_weight)
        
        self.world.add_system(BuildSystem(self.config, sgr_config.robot_size, sgr_config.env, sgr_config.steps))
        self.world.add_system(SpeciationSystem())
        self.world.add_system(EvaluationSystem(sgr_config.env, sgr_config.steps, sgr_config.cpus))

        self.pop = neat.Population(self.config)

    def _create_config(self, sgr_config) :
        config = neat.Config(MorphoAwareGenome, 
                            neat.DefaultReproduction, 
                            neat.DefaultSpeciesSet, 
                            neat.DefaultStagnation, 
                            sgr_config.config_path)
        
        # overwritting 
        config.pop_size = sgr_config.pop_size

        # overwritting the size of entry, outputs...
        size_of_input_of_cppn = sgr_config.substrate_dimension * 2 + 1 
        config.genome_config.num_inputs = size_of_input_of_cppn
        self.genome_config.input_keys = [-1*i for i in range(1, size_of_input_of_cppn+1)]

        config.genome_config.num_outputs = 2
        config.genome_config.output_keys = [1, 2]

        return config





    
    
