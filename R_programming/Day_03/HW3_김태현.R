setwd("D:/BigData/Day3_hw3")

library(dplyr)

# 실습 1
# Step 1
NSC2_M40 <- read.csv("NSC2_M40_1000.csv",stringsAsFactors = TRUE)
t <- NSC2_M40 %>%
  filter(STD_YYYY >= 2002 & STD_YYYY <= 2008) %>%
  group_by(RN_INDI, STD_YYYY) %>%
  summarise(number = n())

# Step 2
NSC2_BNC <- read.csv("NSC2_BNC_1000.csv",stringsAsFactors = TRUE)
temp_data <- inner_join(NSC2_BNC, t, by.x="STD_YYYY", by.y="RN_INDI")

# Step 3
temp_data %>%
  select(c(RN_INDI, STD_YYYY, number)) %>%
  arrange(desc(number))

# 실습 2
# A
SAT <- read.csv("SAT_2010.csv",stringsAsFactors = TRUE)
var(SAT$total)
mean(SAT$total)
median(SAT$total)

# B
m <- mean(SAT$total)
s <- sd(SAT$total)

SAT %>%
  filter(total >= m-s & total <= m+s) %>%
  summarise(number = n())

# C
m <- mean(SAT$total)
SAT %>% 
  mutate(total_dist = abs(total-m)) %>%
  select(c(state, total, total_dist)) %>%
  arrange(desc(total_dist))

# D
library(ggplot2)
SAT %>%
  filter(salary >= 50000) %>%
  ggplot(aes(x=total, y=sat_pct)) +
  geom_point(alpha=0.6) +
  scale_x_continuous(limits = c(1350, 1800)) +
  scale_y_continuous(limits = c(0, 100))

SAT %>%
  filter(salary < 50000) %>%
  ggplot(aes(x=total, y=sat_pct)) +
  geom_point(alpha=0.6) +
  scale_x_continuous(limits = c(1350, 1800)) +
  scale_y_continuous(limits = c(0, 100))

# E
qqnorm(SAT$total)
qqline(SAT$total, col=2, cex=7)

shapiro.test(SAT$total)


# 실습 3
# 3
# 1.1
pizzar <- read.csv("pizzar.csv",stringsAsFactors = TRUE)
attach(pizzar)
boxplot(Delivery~Bread, boxwex=0.5)

# 1.2
t.test(Delivery~Bread, data = pizzar)
