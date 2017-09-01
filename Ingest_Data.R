library(gdata)
# CHANGE THE LOCATION OR USERNAME!!
setwd("/Users/mm22140/Box Sync/Sales-and-Marketing-Domain/datadays_olfactory/data")



read_sheet <- function(protein, sheet_name) {
  # Importing the sheet_name sheet of protein file
  print(paste("Reading the sheet", sheet_name))
  protein_file <- paste(protein, "xlsx", sep=".")
  d <- read.xls(protein_file,sheet= sheet_name,head=F, stringsAsFactors=FALSE, blank.lines.skip=F)
  return(d)
}

make_sheet_zone_data <- function(protein, sheet_data, sheet_name, zone) {
  # Taking the zone part of the sheet_name sheet of protein file
  print(paste("Reading the zone", zone))
  if (zone == "VZ") {
    data <- sheet_data[5:267,]
  } else if (zone == "IZ") {
    data <- sheet_data[269:531,]
  } else if (zone == "DZ") {
    data <- sheet_data[533:795,]
  } else {
    print("Zone should be 'VZ', 'IZ', or 'DZ'")
    return(NULL)
  }
  # Removing all empty columns
  data[data == ""] <- NA
  data <- data[,colSums(is.na(data))<nrow(data)]
  # Return NULL if the data set is empty
  if (dim(data)[2]==0) {
    print("Data is absent for the indicated sheet and zone")
    return(NULL)
  }
  # Counting the number of segments
  K <- dim(data)[2]
  # Copying segment names
  for (i in seq(1,K,2)) {
    data[1,i+1] <- as.character(data[1,i])
  }
  # Setting the segment variable name
  data[1,1] <- "Segment"
  # Dropping the repeated names
  todrop <- seq(3,K,2)
  data <-  data[-todrop]
  # Transposing the data frame and setting the correct column names
  n <- data$V1
  data <- as.data.frame(t(data[,-1]))
  colnames(data) <- n
  rownames(data) <- NULL
  # Adding zone name to the table
  zon <- data.frame(zon = rep_len(zone, K/2))
  data <- cbind(zon, data)
  # Adding image (sheet) name to the table
  imag <- data.frame(imag = rep_len(sheet_name, K/2))
  data <- cbind(imag, data)
  # Adding the protein name to the table
  prot <- data.frame(prot = rep_len(protein, K/2))
  data <- cbind(prot, data)
  # Dropping useless variable
  data$'value (0 to 255)' <- NULL
  # Renaming variables
  temp <- c("protein", "image", "zone", "segment", "area",	"std_dev", "std_error", "avg_pix_intensity",	"num_pix")
  for (i in 0:255) {
    temp <- c(temp, paste("freq",i,sep="_"))
  }
  colnames(data) <- temp
  return(data)
}

make_protein_data <- function(protein) {
  print(paste("Reading the protein", protein))
  output <- NULL
  sheets <- sheetNames(paste(protein, "xlsx", sep="."))
  zones <- c('VZ','IZ','DZ')
  for (s in sheets) {
    the_sheet <- read_sheet(protein,s)
    for (z in zones) {
      piece_of_data <- make_sheet_zone_data(protein, the_sheet, s, z)
      output <- rbind(output, piece_of_data)
    }
  }
  return(output)
}

proteins <- c('Bmpr2', 'Cdh5')

make_data <- function() {
  output <- NULL
  for (p in proteins) {
    output <- rbind(output, make_protein_data(p))
  }
  return(output)
} 

reshape_wide_to_long <- function(ready_data) {
fin <- cbind(id=rownames(ready_data),ready_data)
columns_to_long <- c('freq_0')
for (i in 1:255) {
  columns_to_long <- c(columns_to_long, paste("freq",i,sep="_"))
}
reshaped <- reshape(fin, direction="long", idvar="id",
              varying = columns_to_long, v.names='pix_freq',
              timevar="pix_value", times=0:255)
reshaped <- reshaped[order(reshaped$id),]
rownames(reshaped) <- NULL
return(reshaped)
}


# Execute this
final <- make_data()
final_dataset <- reshape_wide_to_long(final)
write.csv(final_dataset, file = "Final_dataset.csv")