#!/usr/bin/env Rscript

# ADS Assignment_3

matches <- read.csv("data/match-data-full.csv")
balls <- read.csv("data/ball-data-full.csv")

# Year used in several questions:
matches$Year <- as.integer(substr(matches$Date, 1, 4))
balls <- merge(balls, matches[,c("ID", "Year")], all.x=T, all.y=F, by.x="GID", by.y="ID")

# Question 1
print("What are the most common types of wickets and how many times do they occur?")

tbl <- sort(table(balls$WicketType, useNA="no", exclude = c("0")), decreasing = T)
writeLines(sprintf("%18s: %3d", names(tbl), tbl))

# Question 2
### PER MATCH?
print("How many runs did Australia, England, India and South Africa average per match in each year 2013, 2014, 2015 and 2016?")

years <- 2013:2016
for (year in years)
{
  for (country in c("Australia", "England", "India", "South Africa"))
  {
    matches_this <- matches[matches$Year %in% years,]
    matches_this <- matches_this[matches_this$Team1==country | matches_this$Team2==country,]
    gids <- matches_this$ID

    balls_this <- balls[balls$GID %in% gids,]
    runs <- sum(balls_this$TotalRuns[balls_this$Batting==country])
    runs_per_match <- runs / length(gids)
    writeLines(sprintf("%d: %14s: matches: %d ; total runs: %d ; avg runs per match: %.1f", year, country, length(gids), runs, runs_per_match))
  }
}

# Question 3
print("How many wins did the West Indies and Sri Lanka each have in 2010 and 2014?")

for (year in c(2010, 2014))
{
  for (country in c("West Indies", "Sri Lanka"))
  {
    matches_this <- matches[matches$Year %in% years,]
    matches_this <- matches_this[matches_this$Winner==country,]
    writeLines(sprintf("%d: %14s: wins: %d", year, country, nrow(matches_this)))
  }
}

# Question 4
print("Which three batsmen scored the most(batter runs) between 2013 and 2015 (inclusive) and what were the trends in their performance?")

years <- 2013:2015
batters <- data.frame(Batsman = unique(balls$Batsman),
                      BatterRuns2013 = NA,
                      BatterRuns2014 = NA,
                      BatterRuns2015 = NA,
                      BatterRunsTotal = NA)
for (batter in batters$Batsman)
{
  balls_this <- balls[balls$Batsman==batter, ]
  for (year in years)
  {
    bruns <- sum(balls_this$BatterRuns[balls_this$Year==year])
    batters[[sprintf("BatterRuns%d", year)]][batters$Batsman==batter] <- bruns
  }
}
batters$BatterRunsTotal <- batters$BatterRuns2013 + batters$BatterRuns2014 + batters$BatterRuns2015
batters <- batters[order(-batters$BatterRunsTotal),]
rownames(batters) <- NULL
#Trend metric: avg % change per year
batters$avg_pct_change <- (
  (batters$BatterRuns2015 - batters$BatterRuns2014) / batters$BatterRuns2014
  + (batters$BatterRuns2014 - batters$BatterRuns2013) / batters$BatterRuns2013
    ) / 2 * 100

print(batters[1:3,])

# Question 5
print("Which five bowlers bowled out the most batsmen between 2010 and 2013 (inclusive) and how many overs did each bowl? Use just the ”bowled” type.")

years <- 2010:2013
bowlers <- data.frame(Bowler = unique(balls$Bowler), Outs = NA, Overs = NA)
for (bowler in bowlers$Bowler)
{
  balls_this <- balls[balls$Bowler==bowler & balls$Year %in% years,]
  n_outs <- nrow(balls_this[balls_this$WicketType=="bowled", ])
  n_overs <- max(balls_this$Over, na.rm=T) # Correct?
  bowlers$Outs[bowlers$Bowler==bowler] <- n_outs
  bowlers$Overs[bowlers$Bowler==bowler] <- n_overs
}
bowlers <- bowlers[order(-bowlers$Outs),]
rownames(bowlers) <- NULL
print(bowlers[1:5,])
