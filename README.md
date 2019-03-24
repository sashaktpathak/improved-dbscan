# DBSCAN
 density-based clustering algorithm in Python
 
 Works with 2D points.

## Usage
Run with parameters (optional):
* -f filename.csv - path to dataset file with 2D points (default "datasets/annulus.csv", semicolon separated values)
* -eps 5 - epsilon parameter (see more (wiki)[https://en.wikipedia.org/wiki/DBSCAN#Original_Query-based_Algorithm]) (default 5)
* -min 10 - minimum number of points required to form a dense region parameter (default 10)

Example:

```
python dblp.py -f datasets/annulus.csv -eps 5 -min 10
```

## Output
* Silhouette Coefficients
* SSE
* Dunn index
* Size of clusters
* Python plot with points, colored by clusters

## Improvement
* Better CVI Value than Original DBScan
* Introduced Eps' to reduce the area to pick next point
* Core Point searches for next point to pick in region between Eps and Eps'