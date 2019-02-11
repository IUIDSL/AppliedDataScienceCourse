#Set up and exploration
#setwd("~/Documents/R-AlgorithmsI-Tutorial/")
auto <- read.table("data/auto-mpg.data",col.names = c("MPG","cylinders","displacement","horsepower",
                                                 "weight","acceleration","year","origin","name"))
str(auto)
summary(auto)
auto$horsepower <- as.integer(auto$horsepower)

fe <- function(x){if(x>30){T}else{F}}
auto$fuelEfficient<-sapply(X=with(auto, MPG),FUN=fe)

#Setting up train/test
set.seed(31052017)
smp_size <- floor(.8 * nrow(auto))
ti <- sample(seq_len(nrow(auto)),size=smp_size) 
train.auto <- auto[ti,]
test.auto <- auto[-ti,]
str(train.auto)
str(test.auto)

# Linear Model
mylm <- with(train.auto, lm(MPG~weight+year+horsepower))
res <- predict.lm(mylm,test.auto)
summary(abs(res - test.auto$MPG))

# K-Means Clustering
mykm <- kmeans(auto[c("weight","year")],2)
plot(auto[c("weight","year")],col=mykm$cluster,pch=as.integer(auto$fuelEfficient))
mykm <- data.frame(auto,mykm$cluster)
with(mykm, table(fuelEfficient,mykm.cluster))

# K-NN for 1 and 3 neighbors
library('class')
k1.pred <- knn(train.auto[c(seq(2,8),10)],test.auto[c(seq(2,8),10)],cl=train.auto$fuelEfficient,k=1)
k3.pred <- knn(train.auto[c(seq(2,8),10)],test.auto[c(seq(2,8),10)],cl=train.auto$fuelEfficient,k=3)
kpred <- data.frame(test.auto,k1.pred,k3.pred)
with(kpred, table(fuelEfficient, k1.pred))
with(kpred, table(fuelEfficient, k3.pred))

library("rpart")

# Classification Tree
ctree <- rpart(fuelEfficient ~ cylinders+horsepower+weight+acceleration+year,
              data=train.auto,
              method = 'class')
ctree.test <- data.frame(test.auto,predict(ctree,test.auto))
summary(ctree.test[which(ctree.test$fuelEfficient==T),c(10,11,12)])
summary(ctree.test[which(ctree.test$fuelEfficient==F),c(10,11,12)])

# Regression Tree
rtree <- rpart(MPG ~ cylinders+horsepower+weight+acceleration+year,
              data=train.auto,
              method = 'anova')
rtree.test <- data.frame(test.auto,predict(rtree,test.auto))
summary(abs(rtree.test[1]-rtree.test[11]))

