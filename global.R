# Global script for Olfactory Protein Viz project ------------------------------
library(shiny)
library(DT)
library(dplyr)

# Load toy dataset - reads from location of global -----------------------------
data <- read.csv2('data/toy_dataset.csv', header = TRUE, sep = ",")

# Functions --------------------------------------------------------------------
filter_data <- function(zone_input, segment_input, protein_input) {
  print(zone_input)
  print(segment_input)
  print(protein_input)
  if (!is.null(zone_input)) {
    data <- data[data$zone == zone_input, ]
  }
  if (!is.null(segment_input)) {
    data <- data[data$segment == segment_input, ]
  }
  if (!is.null(protein_input)) {
    data <- data[data$protein == protein_input, ]
  }
  return(data)
}
