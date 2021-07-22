setwd("D:/BigData/Day1_hw1")
install.packages("dplyr")
library(dplyr)

###########################################################
# 실습 1
# A
autompg = read.csv("autompg.csv")
attach(autompg)
subdata1 <- subset(autompg, cyl==8)
subdata2 <- subset(autompg, cyl==4)
detach(autompg)
attach(subdata1)
mean(hp)
detach(subdata1)
attach(subdata2)
mean(hp)
detach(subdata2)

# B
subdata3 <- subset(autompg, grepl("chevrolet",carname))
dim(subdata3)

###########################################################
# 실습 2
hitter = read.csv("Hitters.csv")
head(hitter)

# A
attach(hitter)
hitter <- hitter %>%
  mutate(Bat_Avg = Hits/AtBat)
head(hitter)

# B
hitter <- hitter %>%
  mutate(OnBase_perc = (Hits + Walks)/(AtBat + Walks))
head(hitter)

# C
hitter %>%
  summarize(mean(Bat_Avg), mean(OnBase_perc), median(Bat_Avg), median(OnBase_perc))

# D
attach(hitter)
Bat_Avg_mean <- mean(Bat_Avg)
onBase_perc_mean <- mean(OnBase_perc)
subdata4 <- filter(hitter, Bat_Avg > Bat_Avg_mean & OnBase_perc > onBase_perc_mean)
nrow(subdata4) / nrow(hitter) * 100

# E
Chitter <- hitter %>%
  select(CAtBat, CHits, CHmRun, CRuns, CRBI, CWalks)
head(Chitter)

# F
max_min = function(n) {
  return (max(n) - min(n))
}

  # t()를 이용해서 전치시킨 후 cbind
r1 <- t(select(Chitter, 1:6) %>% summarize_all(mean))
r2 <- t(select(Chitter, 1:6) %>% summarize_all(min))
r3 <- t(select(Chitter, 1:6) %>% summarize_all(max))
r4 <- t(select(Chitter, 1:6) %>% summarize_all(max_min))
table <- cbind(r1, r2, r3, r4)
colnames(table) <- c("mean", "min", "max", "max-min")
table
