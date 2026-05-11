from registry import ComponentRegistry

class SpeciationSystem : 
    def __init__(self) : 
        pass

    def process(self, registry) : 

        # for each robot in the registry that posses a body, we write its body in the genome, so that it can calculate de distance function 

        for entity_id in list(registry.get_all_id_with_body()) : 
            body = registry.get_body(entity_id).body 
            genome_component = registry.get_genome(entity_id)
            genome_component.genome.robot = body 


