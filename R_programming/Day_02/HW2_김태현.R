library(dplyr)

# set working directory
setwd("D:/BigData/Day2_hw2")

## SAT_2010 Data ------------------------------------------------------
SAT_2010<-read.csv(file="SAT_2010.csv", stringsAsFactors = TRUE)

# 실습 1
  # A
attach(SAT_2010)
par(mfrow=c(2, 2))
m <-matrix(c(1,1,2,3), ncol=2, byrow=T)
layout(m)
boxplot(write, math, names=c("write","math"))
hist(write)
hist(math)

  # B
pairs(SAT_2010, col=SAT_2010$total)
pairs(SAT_2010[,5:9], col=SAT_2010$total)

  # C
par(mfrow=c(2, 2))
plot(total, read)
abline(lm(read~total), col="red", lwd=2, lty=1)
lines(lowess(total, read), col="blue", lwd=2, lty=2)
plot(total, math)
abline(lm(math~total), col="red", lwd=2, lty=1)
lines(lowess(total, math), col="blue", lwd=2, lty=2)
plot(total, write)
abline(lm(write~total), col="red", lwd=2, lty=1)
lines(lowess(total, write), col="blue", lwd=2, lty=2)
plot(total, sat_pct)
abline(lm(sat_pct~total), col="red", lwd=2, lty=1)
lines(lowess(total, sat_pct), col="blue", lwd=2, lty=2)
# ---------------------------------------------------------------------

## serach Data --------------------------------------------------------
# 실습 2
  # A
Search <- read.csv(file="search.csv", stringsAsFactors = TRUE)
Search_gender <- read.csv(file="search_gender.csv", stringsAsFactors = TRUE)
Search_age <- read.csv(file="search_age.csv", stringsAsFactors = TRUE)
Search_local <- read.csv(file="search_local.csv", stringsAsFactors = TRUE)
str(Search)
Search$일 = as.Date(Search$일)
str(Search)

  # B
library(ggplot2)
attach(Search)
p <- ggplot(Search, aes(x=일)) + ylab("검색량") +
  geom_line(aes(y=라면, color="라면")) +
  geom_line(aes(y=zoom, color="zoom")) +
  geom_line(aes(y=코로나, color="코로나")) +
  geom_line(aes(y=BTS, color="BTS"))
p

  # C
p <- ggplot(Search_gender, aes(x=품목, y=count, fill=성별)) +
  geom_bar(stat='identity', width=.5)
p

p <- ggplot(Search_gender, aes(x=성별, y=count, fill=품목)) +
  geom_bar(stat='identity', position='dodge')
p

  # D
p <- ggplot(Search_age, aes(x=연령)) + ylab("검색량") +
  geom_point(aes(y=라면, color="라면")) +
  geom_point(aes(y=zoom, color="zoom")) +
  geom_point(aes(y=코로나, color="코로나")) +
  geom_point(aes(y=BTS, color="BTS")) +
  theme(panel.background = element_rect(fill = 'white', colour = "gray"),
        panel.grid.major = element_line(color = "gray"),
        legend.key = element_rect(fill = 'white'))
p

  # E
p <- ggplot(Search_local, aes(x=지역, fill=검색어)) +
  geom_histogram(stat="count")
p

