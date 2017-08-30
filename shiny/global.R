library(shiny)
library(shinydashboard)
# db / data manipulation
library(D3TableFilter)
library(dplyr)
library(tidyr)
library(lubridate)
library(stringr)
# graphing
library(pROC)
library(ggplot2)
library(scales)


# options(java.parameters = "-Xmx12000m") # more java heap space for big queries
# options(warning.length = 8170) # to print out Teradata errors in full

# function to remove line breaks in the query string, or Teradata doesn't like it--------
# cq <- function(x) gsub("[[:space:]]+", " ", x)
# q <- "SELECT "
# q <- sprintf(q, start_date, end_date)
# 
# # pull the data
# data_raw <- tdQuery(cq(q))
