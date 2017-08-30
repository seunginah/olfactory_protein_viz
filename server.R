# Server for Olfactory Protein Viz project -------------------------------------
# Define server logic
server <- function(input, output) {
  # main data table
  output$main_table = renderDataTable({
    datatable(data,
              colnames = c('Protein', 'Zone', 'Segment', 'Area (microns)', 'Std Dev',
                           'Std Error', 'Avg Pixel Intensity', 'Num Pixels', 'Freq_1',
                           'Freq_255'),
              rownames = FALSE
    ) # end datatable
  }) # end renderDataTable
  
}