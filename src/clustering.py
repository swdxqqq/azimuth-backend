from typing import Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import data_analysis as da

def prepare_clustering_data(year: int) -> Tuple[pd.DataFrame, np.ndarray]:
    """Prepare data for clustering for the specific year"""
    # Load normilized dataframe
    df_normalized = da.normalize_data("standard")
    
    # Filter for the year
    df_year = df_normalized[df_normalized['Year'] == year].copy()
    
    # Find numeric columns for featuring
    feature_cols = [col for col in df_year.select_dtypes(include=['number']).columns
                    if col != 'Year']
    
    X = df_year[feature_cols].values
    
    return df_year, X


def find_optimal_k(X: np.ndarray, max_k: int = 10) -> None:
    """Build Elbow Method plot to find optimal K-value"""
    inertias = []
    silhouette_scores = []
    k_range = range(2, max_k + 1)
    
    for k in k_range:
        kmeans = KMeans(n_clusters=k, init="k-means++", random_state=42, n_init=20)
        kmeans.fit(X)
        
        inertias.append(kmeans.inertia_)
        silhouette_scores.append(silhouette_score(X, kmeans.labels_))
    
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(k_range, inertias, marker="o")
    plt.xlabel("Number of clusters (K)")
    plt.ylabel("Inertia")
    plt.title("Elbow Method")
    plt.grid(True)
    
    plt.subplot(1, 2, 2)
    plt.plot(k_range, silhouette_scores, marker="o")
    plt.xlabel("Number of clusters (K)")
    plt.ylabel("Silhouette score")
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()
    
    print("\nK | Inertia | Silhouette Score")
    for k, inertia, sil in zip(k_range, inertias, silhouette_scores):
        print(f"{k} | {inertia:.2f} | {sil:.2f}")
        
        
def main():
    df_year, X = prepare_clustering_data(2025)
    find_optimal_k(X)  
        
if __name__ == '__main__':
    main()