# UI for Olfactory Protein Viz Project -----------------------------------------

ui <- fluidPage(
  titlePanel("Olfactory Protein Visualization"),
  
  sidebarLayout(
    sidebarPanel(
      
      checkboxGroupInput("zone", "Choose a zone:",
                  choices = c("VZ", "IZ", "DZ")),
      checkboxGroupInput("segment", "Choose a segment:",
                  choices = c("1", "2", "3", "10", "12")),
      checkboxGroupInput("protein", "Choose a protein", 
                  choices = c("Protein A", "Protein B"))
    ), # end sidebarPanel
    
    mainPanel(
      tabsetPanel(
        tabPanel("Data Selection"),
        tabPanel("Visualization")
      ) # end tabset panel
    ), # end mainPanel
    position = "left"
  ) # end sidebarLayout
  
)