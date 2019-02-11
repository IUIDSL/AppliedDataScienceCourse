library(readr)
library(RJSONIO)
library(RSQLite)

hc_csv <- read_csv("data/HateCrimes_csv_v2.csv")

fin <- file("data/HateCrimes_json_v2.json")
x <- fromJSON(fin)
close(fin)

hcj <- data.frame(x[[1]])
for (i in 2:length(x))
{
  hcj <- rbind(hcj, data.frame(x[[i]]))
}

con <- dbConnect(RSQLite::SQLite(), "data/hatecrimes_v2.db")
dbListTables(con)
hc_db <- dbGetQuery(con, "SELECT * FROM hatecrimes")
dbDisconnect(con)
