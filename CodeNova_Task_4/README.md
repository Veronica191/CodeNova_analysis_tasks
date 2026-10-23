# Customer Segmentation Using RFM Analysis and K-Means Clustering

## 1. Project Overview

This project applies customer segmentation techniques to a Superstore sales dataset. The objective is to group customers according to their purchasing behaviour using Recency, Frequency, and Monetary (RFM) analysis and K-Means clustering.

The resulting customer segments help identify high-value customers, regular customers, and customers who may need re-engagement.

## 2. Objectives

- Calculate customer-level RFM features.
- Scale the features before clustering.
- Evaluate potential cluster counts using the Elbow Method and Silhouette Score.
- Apply K-Means clustering.
- Visualize customer segments using Principal Component Analysis (PCA).
- Interpret the clusters and recommend appropriate business strategies.

## 3. Tools and Libraries

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Jupyter Notebook

## 4. Methodology

### Data Preparation

The sales dataset was loaded and its date fields were converted to datetime format. For this analysis, records dated after the analysis date were excluded. The original dataset was retained separately.

### RFM Feature Engineering

Customer behaviour was summarized using three features:

- **Recency:** Number of days since the customer's most recent purchase.
- **Frequency:** Number of distinct orders placed by the customer.
- **Monetary:** Total sales value attributed to the customer.

### Feature Scaling

StandardScaler was used to standardize the RFM features before applying K-Means.

### Cluster Selection

The Elbow Method and Silhouette Score were used to compare possible cluster counts. The three-cluster model achieved a Silhouette Score of approximately 0.3402, compared with 0.3375 for the four-cluster model. Three clusters were selected based on the evaluation results and the interpretability of the resulting customer groups.

### Clustering and Visualization

K-Means was applied with three clusters. PCA was used to project the scaled RFM data into two dimensions for visualization. The first two principal components explained approximately 84.57% of the variance.

## 5. Customer Segmentation Results

The analysis identified 803 customers across three segments.

| Customer Segment | Customers | Average Recency (Days) | Average Frequency | Average Monetary (Sales) |
|---|---:|---:|---:|---:|
| High-Value Loyal Customers | 252 | 93.98 | 8.38 | 4,997.89 |
| Regular Customers | 415 | 120.43 | 4.88 | 1,603.73 |
| At-Risk Customers | 136 | 551.85 | 3.34 | 1,399.03 |

### High-Value Loyal Customers

This segment has the highest average purchase frequency and monetary value.

**Recommendation:** Encourage retention through loyalty initiatives, personalized offers, and relevant product recommendations.

### Regular Customers

This is the largest segment, representing customers with moderate purchase frequency and spending.

**Recommendation:** Encourage repeat purchases through targeted promotions and relevant recommendations.

### At-Risk Customers

These customers have the longest average time since their last purchase and the lowest average purchase frequency.

**Recommendation:** Consider re-engagement campaigns to encourage customers to return.

## 6. Key Findings

- High-Value Loyal Customers have the highest average sales value and purchase frequency.
- Regular Customers make up approximately 51.7% of the customer base.
- At-Risk Customers have an average recency of approximately 552 days.
- Three clusters produced a slightly higher Silhouette Score than four clusters in the models compared.

## 7. Limitations

- Monetary value represents sales, not profit.
- Cluster personas are interpretations of average RFM values and may not describe every customer in a segment.
- The analysis excludes orders dated after the chosen analysis date.
- The clustering results depend on the dataset, feature choices, and model configuration.

## 8. Project Outputs

- Jupyter Notebook containing the analysis and visualizations.
- `output/customer_persona_summary.csv`
- `output/cluster_evaluation_results.csv`

## 9. Conclusion

RFM analysis and K-Means clustering provided a practical way to group customers according to purchasing behaviour. The resulting segments can help a business prioritize customer retention, repeat-purchase strategies, and re-engagement efforts.
