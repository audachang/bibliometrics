import pandas as pd
import numpy as np
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

# Function to perform dimension reduction and create a 2D scatter plot
def plot_countries_2d(X, method_name='PCA', title='2D Projection', country_names=None):
    # Dimension reduction
    if method_name == 'PCA':
        model = PCA(n_components=2)
    elif method_name == 't-SNE':
        model = TSNE(n_components=2, learning_rate='auto', init='random')
    else:
        raise ValueError("Unsupported dimension reduction method: {}".format(method_name))

    X_reduced = model.fit_transform(X)

    # Scatter plot
    plt.figure(figsize=(8, 6))
    for i, country in enumerate(country_names):
        plt.scatter(X_reduced[i, 0], X_reduced[i, 1], label=country)
        plt.text(X_reduced[i, 0], X_reduced[i, 1], country)
    
    plt.title(title)
    plt.xlabel('Component 1')
    plt.ylabel('Component 2')
    plt.grid(True)
    plt.show()


def safe_pearsonr(x, y):
    finite_mask = np.isfinite(x) & np.isfinite(y)
    if finite_mask.sum() > 1:  # Ensure there are at least two finite values
        return pearsonr(x[finite_mask], y[finite_mask])
    else:
        return np.nan, np.nan


def adjust_rankings_to_target_correlation(base_rankings, target_corr, max_iterations=1000, tolerance=0.01):
    """
    Adjust rankings to achieve a target correlation with the base rankings.
    This is a simple heuristic approach and may not achieve the exact target in all cases.
    """
    adjusted_rankings = base_rankings.copy()
    current_corr, _ = pearsonr(base_rankings, adjusted_rankings)
    iteration = 0

    while abs(current_corr - target_corr) > tolerance and iteration < max_iterations:
        # Introduce random swaps in the adjusted rankings
        swap_indices = np.random.choice(len(base_rankings), 2, replace=False)
        adjusted_rankings[swap_indices] = adjusted_rankings[swap_indices[::-1]]
        new_corr, _ = pearsonr(base_rankings, adjusted_rankings)
        
        # If the new correlation is closer to the target, update the current correlation; else, undo the swap
        if abs(new_corr - target_corr) < abs(current_corr - target_corr):
            current_corr = new_corr
        else:
            # Undo the swap
            adjusted_rankings[swap_indices] = adjusted_rankings[swap_indices[::-1]]

        iteration += 1

    return adjusted_rankings

def create_correlated_rankings(unique_keywords, country_names, 
    high_corr_pair=('USA', 'Taiwan'), desired_correlation=0.75):
    period_a_df = pd.DataFrame(index=unique_keywords, columns=country_names)
    period_b_df = pd.DataFrame(index=unique_keywords, columns=country_names)

    # Initial random permutation for all countries
    for country in country_names:
        period_a_df[country] = np.random.permutation(len(unique_keywords))
        period_b_df[country] = np.random.permutation(len(unique_keywords))

    # Adjust Taiwan's rankings to approximate the desired correlation with the USA
    for period_df in [period_a_df, period_b_df]:
        usa_rankings = period_df[high_corr_pair[0]].values
        taiwan_rankings = adjust_rankings_to_target_correlation(usa_rankings, desired_correlation)
        period_df[high_corr_pair[1]] = taiwan_rankings

    return period_a_df, period_b_df

# Rest of the code for RSA analysis, visualization, and saving results remains the same.


def calculate_similarity_matrix(df):
    countries = df.columns
    similarity_matrix = pd.DataFrame(index=countries, columns=countries)
    for country1 in countries:
        for country2 in countries:
            corr, _ = safe_pearsonr(df[country1], df[country2])
            similarity_matrix.loc[country1, country2] = corr
    return similarity_matrix.astype(float)

def between_period_rsa(df_a, df_b):
    rsa_values = {}
    for country in df_a.columns:
        corr, _ = safe_pearsonr(df_a[country], df_b[country])
        rsa_values[country] = corr
    return rsa_values

unique_keywords = [
    'Assessment', 'Game', 'Mobile', 'Scaffolding', 'Mooc', 'Collaborative learning', 'STEM',
    'Self-efficacy', 'Language learning', 'Cognitive Load', 'Self-Regulated Learning',
    'Digital Games', 'Mobile Learning', 'Online Assessment', 'Adaptive Learning', 'Self Regulated Learning',
    'Learning analytics', 'COVID', 'EFL', 'Adaptive'
]

country_names = ['USA', 'Taiwan', 'China', 'Korea', 'Netherlands', 'Others']

period_a_df, period_b_df = create_correlated_rankings(unique_keywords, country_names)

similarity_matrix_a = calculate_similarity_matrix(period_a_df)
similarity_matrix_b = calculate_similarity_matrix(period_b_df)

# Saving to Excel is handled as before
period_a_df.to_excel('period_a_rankings.xlsx')
period_b_df.to_excel('period_b_rankings.xlsx')




# Visualize the similarity matrices
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
sns.heatmap(similarity_matrix_a, annot=True, cmap='coolwarm')
plt.title('Time Period A Similarity Matrix')
plt.subplot(1, 2, 2)
sns.heatmap(similarity_matrix_b, annot=True, cmap='coolwarm')
plt.title('Time Period B Similarity Matrix')
plt.tight_layout()
plt.show()

# Between period RSA
rsa_values = between_period_rsa(period_a_df, period_b_df)
plt.figure(figsize=(10, 5))
pd.Series(rsa_values).plot(kind='bar', color='skyblue')
plt.title('Between Time Period RSA for Each Country')
plt.ylabel('RSA Value')
plt.xlabel('Country')
plt.show()




# Apply dimension reduction and visualize for Time Period A
print("PCA - Time Period A")
plot_countries_2d(similarity_matrix_a, method_name='PCA', title='PCA - Time Period A', country_names=similarity_matrix_a.columns)
print("t-SNE - Time Period A")
plot_countries_2d(similarity_matrix_a, method_name='t-SNE', title='t-SNE - Time Period A', country_names=similarity_matrix_a.columns)

# Apply dimension reduction and visualize for Time Period B
print("PCA - Time Period B")
plot_countries_2d(similarity_matrix_b, method_name='PCA', title='PCA - Time Period B', country_names=similarity_matrix_b.columns)
print("t-SNE - Time Period B")
plot_countries_2d(similarity_matrix_b, method_name='t-SNE', title='t-SNE - Time Period B', country_names=similarity_matrix_b.columns)
