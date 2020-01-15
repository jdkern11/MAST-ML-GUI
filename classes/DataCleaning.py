class DataCleaning:

    def __init__(self): 
        # Cleaning methods variables
        self.cleaning_methods = ['remove', 'imputation', 'ppca']
        self.imputation_strategy = ['mean','median']
        
        self.vars = {"cleaning_method": None, "imputation_strategy": None}
        