# Traveling Salesman Problem (TSP) — Heuristic Pipeline (Nearest Neighbor + Multi-Start + 2-Opt)

This repository contains my ISEN 320 (Operations Research I) final project implementation for solving a large Traveling Salesman Problem (TSP) instance using a scalable heuristic pipeline:

1) **Nearest Neighbor (NN)** tour construction  
2) **Multi-start initialization** to reduce dependence on starting city  
3) **2-opt (best-improvement)** local search applied to top NN tours with a pass cap to control runtime  

The full report is included in `docs/ISEN_320_Final_Project_Report.pdf`.

## Repo Structure
src/ Python source code
data/ Input dataset(s)
results/ Output files (tours, best tour, etc.)
docs/ Project report PDF

## Quick Start

### Run the full pipeline (recommended)
From the repository root:
python src/run_pipeline.py

### Run steps manually (optional)
python src/nearest_neighbor.py
python src/two_opt.py

## Inputs / Outputs

### Input
data/usa13509.tsp — 13,509-city coordinate dataset

### Outputs
results/nearest_neighbor_tours.txt — NN tours generated from multiple starting cities with their total lengths
results/best_tour_found.txt — best tour found after applying 2-opt to selected NN tours

## Algorithm Overview

### Nearest Neighbor (NN)
Starting from a chosen city, repeatedly visit the nearest unvisited city until all cities are visited, then return to the start.

### Multi-Start Strategy
To avoid a single-start bias without running NN from every city, the pipeline uses a diverse set of starting cities (described in the report).

### 2-Opt (Best Improvement)
2-opt iteratively improves a tour by swapping two edges (reversing a segment) when it reduces total distance. A maximum number of passes is used to keep runtime manageable on large instances.

## Report
See `docs/ISEN_320_Final_Project_Report.pdf` for:

TSP formulation as a Binary Integer Program (decision variables, constraints, subtour elimination)
Branch-and-bound (exact approach overview)
Heuristic design rationale and complexity discussion
Implementation details and results

