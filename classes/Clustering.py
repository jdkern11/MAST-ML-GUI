class Clustering:
    def __init__(self):
           
        # make a separate list of cluster variables
        # TODO find what other strings possible
        self.vars = {"AffinityPropagation": {'damping': 0.5, 'max_iter': 200, 'convergence_iter': 15, 'affinityCB': 'euclidean'}, 
                      "AgglomerativeClustering": {'n_clusters': 2, 'affinityCB': 'euclidean', 'compute_full_treeCB': 'auto', 'linkageCB': 'ward'},
                      "Birch": {'threshold': 0.5, 'branching_factor': 50, 'n_clusters': 3}, 
                      "DBSCAN": {'eps': 0.5, 'min_samples':5, 'metricCB': 'euclidean', 'algorithmCB': 'auto', 'leaf_size': 30}, 
                      "KMeans": {'n_clusters': 8, 'n_init': 10, 'max_iter': 300, 'tol': 0.0001},
                      "MiniBatchKMeans": {'n_clusters': 8, 'max_iter': 100, 'batch_size': 100}, 
                      "MeanShift": None,
                      "SpectralClustering": {'n_clusters': 8, 'n_init': 10, 'gamma': 1.0, 'affinityCB': 'rbf'}}
                      
        # create list of possible values string choices in clustering
        self.affinity_propagation_affinity = ['euclidean','precomputed']
        # if ward, must be euclidean
        self.agglomerative_clustering_affinity = ['euclidean', 'l1', 'l2', 'manhattan', 'cosine', 'precomputed']
        self.compute_full_tree = ['auto', 'True', 'False']
        self.linkage = ['ward', 'complete', 'average', 'single']
        # TODO, add options for this. There are so thinks to note for it
        self.DBSCAN_metric = ['euclidean']
        self.DBSCAN_algorithm = ['auto','ball_tree','kd_tree','brute']
        # TODO there may be other pairwise kernels that can be added
        self.spectral_clustering_affinity = ['rbf','nearest_neighbors','precomputed','precomputed_nearest_neighbors']
        
        self.combobox_options ={"AffinityPropagationaffinityCB":self.affinity_propagation_affinity,
                                "AgglomerativeClusteringaffinityCB":self.agglomerative_clustering_affinity,
                                "AgglomerativeClusteringcompute_full_treeCB":self.compute_full_tree,
                                "AgglomerativeClusteringlinkageCB":self.linkage,
                                "DBSCANmetricCB":self.DBSCAN_metric,
                                "DBSCANalgorithmCB":self.DBSCAN_algorithm,
                                "SpectralClusteringaffinityCB":self.spectral_clustering_affinity}