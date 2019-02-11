#setwd("~/Downloads/")
lbr <- read.csv("data/low_birth_rate_full.csv")

byage <- with(lbr,table(LOW,AGE))
barplot(byage,
        main="Low Birth Weight Births by Age of Mother",
        xlab = "Age of Mother",
        col = c("blue","red"),
        legend = c("normal","low"))

