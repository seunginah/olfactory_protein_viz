# Global script for Olfactory Protein Viz project ------------------------------
library(shiny)
library(DT)

# Load toy dataset - reads from location of global
data <- read.csv2('data/toy_dataset.csv', header = TRUE, sep = ",")
