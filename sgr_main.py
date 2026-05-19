from sgr_config import SGRConfig
from experiments.exp_walker import WalkerExperiment

import os 
import sys 


def main() : 
    local_dir = os.path.dirname(os.path.abspath(__file__))

    if len(sys.argv) > 1 : 
        sgr_config_path = os.path.join(local_dir, sys.argv[1])
    else : 
        sgr_config_path = os.path.join(local_dir, "configs/settings/configs.json")

    print(f'config : {sgr_config_path}')

    sgr_config = SGRConfig(sgr_config_path, local_dir)

    exp = WalkerExperiment(sgr_config)

    exp.run(sgr_config.gens)

if __name__ == "__main__" : 
    main()



