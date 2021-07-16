setwd("D:/BigData/Day4_hw4")

library(dplyr)

# 실습 1
# A
SAT <- read.csv("SAT_2010.csv")
SAT[duplicated(SAT),]

# B
str(SAT)

# C
sum(is.na(SAT))

# D
SAT <- read.csv("SAT_2010.csv", stringsAsFactors = TRUE)
attach(SAT)
pairs(SAT)

cor(read, expenditure)
cor(read, pupil_teacher_ratio)
cor(read, salary)
cor(read, math)
cor(read, write)
cor(read, total)
cor(read, sat_pct)

cor(math, expenditure)
cor(math, pupil_teacher_ratio)
cor(math, salary)
cor(math, read)
cor(math, write)
cor(math, total)
cor(math, sat_pct)


# 실습 2
Happy <- read.csv("happy2020.csv", stringsAsFactors = TRUE)
attach(Happy)

# A
sum(is.na(Happy))

# B
install.packages("corrplot")
library(corrplot)
str(Happy)
data <- Happy[,c(3, 4,5,6,7, 8, 9, 10)] 
data_cor <- cor(data)
corrplot(data_cor,method="number",type="lower",order="hclust")

pairs(Happy[, c(3, 5, 6, 7)], col=Happy$Ladder.score)

# C
Happy %>%
  select(c(Country.name, Ladder.score)) %>%
  arrange(desc(Ladder.score)) %>%
  head()

Happy %>%
  select(c(Country.name, Ladder.score)) %>%
  arrange(Ladder.score) %>%
  head()

# D

# E
plot(Logged.GDP.per.capita, Ladder.score, col=as.integer(Country.name), pch=19)
abline(lm(Ladder.score~Logged.GDP.per.capita), col="red", lwd=2, lty=1)
r <- lm(Ladder.score~Logged.GDP.per.capita, Happy)
summary(r)

plot(Social.support, Ladder.score, col=as.integer(Country.name), pch=19)
abline(lm(Ladder.score~Social.support), col="red", lwd=2, lty=1)
r <- lm(Ladder.score~Social.support, Happy)
summary(r)

plot(Healthy.life.expectancy, Ladder.score, col=as.integer(Country.name), pch=19)
abline(lm(Ladder.score~Healthy.life.expectancy), col="red", lwd=2, lty=1)
r <- lm(Ladder.score~Healthy.life.expectancy, Happy)
summary(r)

# 실습 3(추가문제)
filePath <- "http://www.sthda.com/sthda/RDoc/example-files/martin-luther-king-i-have-a-dream-speech.txt"
text <- readLines(filePath)

install.packages("RColorBrewer")
install.packages('NLP')
install.packages('tm')
install.packages('wordcloud')
library('NLP')
library('tm')
library('wordcloud')
library('RColorBrewer')


docs <- Corpus(VectorSource(text))

inspect(docs)

t1<-tm_map(docs,removePunctuation)
t2<-tm_map(t1,stripWhitespace)
t3<-tm_map(t2,function(x) removeWords(x,stopwords()))
tdm<-TermDocumentMatrix(t3)
m<-as.matrix(tdm)
v<-sort(rowSums(m),decreasing = TRUE)
d<-data.frame(word=names(v),freq=v)
head(d)
par(mfrow=c(1,1))
wordcloud(d$word,d$freq,c(8,.5),2,,FALSE,.1)
inspect(t3)