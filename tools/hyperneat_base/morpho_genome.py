import neat 


class MorphoAwareGenome(neat.DefaultGenome) :
    neat_config = None

    def __init__(self, key) : 
        super().__init__(key)
        self.body = None # will be written outside 
        if MorphoAwareGenome.config is None :
            raise RuntimeError("Please set the neat_config attribute of MorphoAwareGenome before creating any instance of it.")

    @classmethod
    def configure(myclass, config, robot_size, spec_genotype_weight, spec_phenotype_weight) : 
        myclass.config = config
        myclass.robot_size = robot_size
        myclass.spec_genotype_weight = spec_genotype_weight
        myclass.spec_phenotype_weight = spec_phenotype_weight
         

    def distance(self, other, _) : 

        genotype_distance = super().distance(other, MorphoAwareGenome.config.genome_config)
        
        if self.body is None or other.body is None : 
            return self.spec_genotype_weight*genotype_distance
    
        difference = 0 
        for i in range(self.robot_size) : 
            for j in range(self.robot_size) : 
                if (self.body[i][j] == 0 and other.body[i][j] != 0) or (self.robot[i][j] != 0 and other.robot[i][j] == 0) : 
                    difference += 1
                elif self.body[i][j] != other.body[i][j] : 
                    difference += 0.75

        phenotype_distance = difference/(self.robot_size**2) # Normalizing between 0 and 1        
        return self.spec_genotype_weight*genotype_distance + self.spec_phenotype_weight*phenotype_distance

