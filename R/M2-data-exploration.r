#setwd("~/Documents/ADS-SU17/")
matches <- read.csv("data/match-data-full.csv")
balls <- read.csv("data/ball-data-full.csv")

str(matches)
str(balls)

par(mar=c(10,10,4,2))

hist(matches$WinBy,col="darkred")
barplot(table(matches$Winner),cex.lab=.75,las=1,col="darkred",horiz = T)
boxplot(matches$WinBy~matches$Winner,cex.lab=.5,las=3,col="darkred",mar=c(3,1,1,1))

barplot(sort(table(matches$PlayerOfMatch),decreasing =T)[seq(1,6)],
        cex.lab=.75,las=1,col="darkred",horiz = T)
barplot(
  sort(sort(table(balls$Bowler[balls$WicketType!=0]),decreasing = T)[seq(1,10)]),
  cex.lab=.75,las=1,col="darkred",horiz=T
  )

summary(matches)
summary(balls)

par(mar=c(10,10,4,2))
total.matches <- table(as.factor(c(as.character(matches$Team1),as.character(matches$Team2))))
barplot(sort(total.matches),cex.lab=.75,las=1,col="darkred",horiz=T)

