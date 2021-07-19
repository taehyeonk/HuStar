setwd("D:/BigData/Day5_hw5")

library(dplyr)

Tesla <- read.csv("TSLA.csv", stringsAsFactors = TRUE)

# (i)
Tesla$Date

# (ii)
attach(Tesla)
# 시가
Tesla %>% 
  select(Date, Open, Volume) %>%
  arrange(desc(Open)) %>%
  head(1)
# 종가
Tesla %>% 
  select(Date, Close, Volume) %>%
  arrange(desc(Close)) %>%
  head(1)
# 수정종가
Tesla %>% 
  select(Date, Adj.Close, Volume) %>%
  arrange(desc(Adj.Close)) %>%
  head(1)
# 최대가
Tesla %>% 
  select(Date, High, Volume) %>%
  arrange(desc(High)) %>%
  head(1)

# (iii)
# 중복되는 값이나 NA값 확인
Tesla[duplicated(Tesla),]
sum(is.na(Tesla))

# 상관분석
library(corrplot)
str(Tesla)
data <- Tesla[,2:7]
data_cor <- cor(data, method="pearson")
round(data_cor, 3)
corrplot(data_cor,method="number", order="hclust")
pairs(Tesla[, 2:7], col=Tesla$Date)


# 그래프
library(ggplot2)
Tesla$Date = as.Date(Tesla$Date)
ggplot(data=Tesla, aes(x=Date)) + ylab("가격") +
  geom_line(aes(y=High, color="High")) +
  geom_line(aes(y=Low, color="Low"))

Tesla_add <- Tesla %>%
  mutate(High_Low = High - Low) %>%
  mutate(Close_Open = Close - Open)

ggplot(data=Tesla_add, aes(x=Date, y=High_Low)) + geom_point()

ggplot(data=Tesla_add, aes(x=Date, y=Close_Open)) + geom_line()

ggplot(data=Tesla_add, aes(x=Date)) + ylab("금액 변동폭") +
  geom_point(aes(y=High_Low, color="최대가 - 최소가")) +
  geom_line(aes(y=Close_Open, color="종가 - 시가"))

# 시간에 따른 거래량
ggplot(data=Tesla, aes(x=Date, y=Volume)) + geom_line()
