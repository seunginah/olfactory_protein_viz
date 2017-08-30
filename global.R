# Global script for Olfactory Protein Viz project ------------------------------
library(shiny)

# Load toy dataset
data <- read.csv2('../data/toy_dataset.csv', header = TRUE, sep = ",")
