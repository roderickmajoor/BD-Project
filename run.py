from Pipelines.PipelineModuleFactory import PipelineModuleFactory
import yaml

import yaml
import importlib

def load_yaml_file(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def initialize_classes(config):
    modules = []
    # If config is a list, iterate through each item
    if isinstance(config, list):
        for item in config:
            modules.extend(initialize_classes(item))  # Aggregate results from recursive calls

    # If config is a dictionary, check for "module"
    elif isinstance(config, dict):
        if "module" in config and "config" in config:
            module_name = config["module"]
            config = config["config"]
            print(module_name, config)
            # although we could use importlib, we will use a factory pattern instead
            # because python relative imports are a just a pain.
            module = PipelineModuleFactory.create_module(module_name, config)
            modules.append(module)
        else:
            # Recursively search for nested configurations
            for key in config:
                modules.extend(initialize_classes(config[key]))
                
    return modules

if __name__ == "__main__":
    # Assuming your YAML file path is 'path/to/your/config.yaml'
    config = load_yaml_file('config.yaml')
    modules = initialize_classes(config)
    data_loader = modules[0]
    rest = modules[1:]
    df = data_loader.collect_data()
    for module in rest:
        df = module.process(df)
    print(df.show())
    
    
    

        
        
        
        
            
            
            
        
    
    
    