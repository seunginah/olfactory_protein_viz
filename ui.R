# UI for Olfactory Protein Viz Project -----------------------------------------

ui <- fluidPage(
  titlePanel("Olfactory Protein Visualization"),
  
  sidebarLayout(
    sidebarPanel(
      checkboxGroupInput("zone", "Choose a zone:",
                  choices = c("VZ", "IZ", "DZ"),
                  selected = "VZ"),
      checkboxGroupInput("segment", "Choose a segment:",
                  choices = c("1", "2", "10", "11", "12"),
                  selected = "1"),
      checkboxGroupInput("protein", "Choose a protein", 
                  choices = c("Bmpr2", "Cdh5"),
                  selected = "Bmpr2")
    ), # end sidebarPanel
    
    mainPanel(
      tabsetPanel(
        tabPanel("Data Selection",
                 DT::dataTableOutput("main_table")),
        tabPanel("Visualization")
      ) # end tabset panel
    ), # end mainPanel
    position = "left"
  ) # end sidebarLayout
  
)