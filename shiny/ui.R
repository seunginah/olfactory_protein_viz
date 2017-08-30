#
# 
# http://shiny.rstudio.com/articles/layout-guide.html

shinyUI(
  dashboardPage(
    dashboardHeader(title = 'Olfactory Protein Visualization', titleWidth = '300px'),
    dashboardSidebar(width = '300px',
                     actionButton('login', label = 'Log In', align = 'center', width = '85px'),
                     h4(),
                     h4(textOutput('login_info'), align = 'center')),
    dashboardBody(
      ) # end dashboardBody
    ) # end dashboardPage
  )