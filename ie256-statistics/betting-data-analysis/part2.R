library(data.table)
games =fread("matches.csv",header=TRUE)
odds =fread("odds.csv",header=TRUE)

#Probabilities are normalized and evaluated here.
setkey(odds,matchid)
setkey(games,matchid)
odds = odds[,SumProb := (1/TieOdd)+(1/AwayOdd)+(1/HomeOdd)]
odds = odds[,TieProb := 1/(TieOdd*SumProb)]
odds = odds[,AwayProb := 1/(AwayOdd*SumProb)]
odds = odds[,HomeProb := 1/(HomeOdd*SumProb)]
gameswOdds = merge(games,odds[,list(matchid,HomeProb,AwayProb,TieProb,Bookmaker)])

betssons = gameswOdds[Bookmaker=="Betsson"]
pinnacle = gameswOdds[Bookmaker=="Pinnacle"]
Betfair = gameswOdds[Bookmaker=="Betfair"]
bwin = gameswOdds[Bookmaker=="bwin"]
bet365 = gameswOdds[Bookmaker=="bet365"]


#Task 1
#Null hypothesis: Home Goals follow Poisson Distribution.
#Alternative hypothesis: Home Goals do not follow Poisson Distribution.
#Our significance level is 0.01.

#We obtain the frequencies related to number of goals. 
#For 8 goals which were never scored in reality, we added zero.
#The reason for this is, expected distribution have some considerable probability for this number(0.07).
#After than this, we performed chi squared goodness of fit test.
homeFreq = as.vector(table(games[,Home_Score]))
homeFreq = c(homeFreq,0)
awayFreq = as.vector(table(games[,Away_Score]))
awayFreq = c(awayFreq,0)
homeExp = length(games[,Home_Score])*dpois(c(0:8),lambda=games[,mean(Home_Score)])
awayExp = length(games[,Away_Score])*dpois(c(0:8),lambda=games[,mean(Away_Score)])

homeChi = sum(((homeFreq-homeExp)**2)/homeExp)
awayChi = sum(((awayFreq-awayExp)**2)/awayExp)
pchisq(homeChi,df=7)
pchisq(awayChi,df=7)

#For home goals, the test returned a p-value of 0.84. Since this value is in 0.99 interval, we fail to reject.
#For away goals, the test returned a p-value of 0.95. Since this value is in 0.99 interval, we fail to reject.


#By using simulation and a builtin function, we can also do the hypothesis testing
#First parameter is observed values.
#Second parameter is expected values, a vector of values generated by R, following Poisson Distribution.
chisq.test(games[,Home_Score],rpois(length(games[,Home_Score]),lambda=games[,mean(Home_Score)]))


#Task 2
#Null Hypothesis: Mean Goal Difference = 0
#Alternative Hypothesis: Mean Goal Difference > 0 (one sided)
#Used test statistic : Paired T-Statistic
#Since differences follow a normal distribution, we will use t-statistic to test its mean.

differenceMeans = c()
pvalues = c()
for(i in c(2011:2017)){
  vec=games[season==i,Home_Score-Away_Score]
  differenceMeans = c(differenceMeans,mean(vec))
  samplesd = sd(vec)
  tval= differenceMeans[i-2010]/(samplesd/sqrt(length(vec)))
  print(tval)
  pvalues = c(pvalues,pt(tval,df=length(vec)-1))
  }

pvalues

# P Values related to each year is like the following:
# 0.9998611 0.9998661 0.9999781 0.9966476 0.9999531 0.9987388 0.9999426
# Since all of the pvalues are less than 0.01, we reject the null hypothesis.
#This means that goals difference in greater than zero for each season.



#Task 3
#We do not know if variances are equal to each other or not.
#Hence we will do the hypothesis testing assuming that sd1 is not equal to sd2.
#Null Hypothesis : Difference = 0
#Alternative Hypothesis : Difference <> 0.
#Used test-statistic: T-statistic since we are examining differences of means.
pvalues = c()

betssonsHome2010 = betssons[season==2010,HomeProb]
betssonsHome2016 = betssons[season==2016,HomeProb]
betssonsAway2016 = betssons[season==2016,AwayProb]
betssonsAway2010 = betssons[season==2010,AwayProb]
var1 = sd(betssonsHome2010)**2
var2 = sd(betssonsHome2016)**2
n1 = length(betssonsHome2010)
n2 = length(betssonsHome2016)

tval = (mean(betssonsHome2010)-mean(betssonsHome2016))/sqrt((var1/n1)+(var2/n2))
df = ceiling((((var1/n1)+(var2/n2))**2)/(((var1/n1)**2)/(n1-1)+((var2/n2)**2)/(n2-1)))
pvalues = c(pvalues,pt(tval,df))


pinnacleHome2010 = pinnacle[season==2010,HomeProb]
pinnacleHome2016 = pinnacle[season==2016,HomeProb]
pinnacleAway2016 = pinnacle[season==2016,AwayProb]
pinnacleAway2010 = pinnacle[season==2010,AwayProb]
var1 = sd(pinnacleHome2010)**2
var2 = sd(pinnacleHome2016)**2
n1 = length(pinnacleHome2010)
n2 = length(pinnacleHome2016)

tval = (mean(pinnacleHome2010)-mean(pinnacleHome2016))/sqrt((var1/n1)+(var2/n2))
df = ceiling((((var1/n1)+(var2/n2))**2)/(((var1/n1)**2)/(n1-1)+((var2/n2)**2)/(n2-1)))
pvalues = c(pvalues,pt(tval,df))

BetfairHome2010 = Betfair[season==2010,HomeProb]
BetfairHome2016 = Betfair[season==2016,HomeProb]
BetfairAway2016 = Betfair[season==2016,AwayProb]
BetfairAway2010 = Betfair[season==2010,AwayProb]
var1 = sd(BetfairHome2010)**2
var2 = sd(BetfairHome2016)**2
n1 = length(BetfairHome2010)
n2 = length(BetfairHome2016)

tval = (mean(BetfairHome2010)-mean(BetfairHome2016))/sqrt((var1/n1)+(var2/n2))
df = ceiling((((var1/n1)+(var2/n2))**2)/(((var1/n1)**2)/(n1-1)+((var2/n2)**2)/(n2-1)))
pvalues = c(pvalues,pt(tval,df))


BwinHome2010 = bwin[season==2010,HomeProb]
BwinHome2016 = bwin[season==2016,HomeProb]
BwinAway2016 = bwin[season==2016,AwayProb]
BwinAway2010 = bwin[season==2010,AwayProb]
var1 = sd(BwinHome2010)**2
var2 = sd(BwinHome2016)**2
n1 = length(BwinHome2010)
n2 = length(BwinHome2016)

tval = (mean(BwinHome2010)-mean(BwinHome2016))/sqrt((var1/n1)+(var2/n2))
df = ceiling((((var1/n1)+(var2/n2))**2)/(((var1/n1)**2)/(n1-1)+((var2/n2)**2)/(n2-1)))
pvalues = c(pvalues,pt(tval,df))

Bet365Home2010 = bet365[season==2010,HomeProb]
Bet365Home2016 = bet365[season==2016,HomeProb]
Bet365Away2016 = bet365[season==2016,AwayProb]
Bet365Away2010 = bet365[season==2010,AwayProb]
var1 = sd(Bet365Home2010)**2
var2 = sd(Bet365Home2016)**2
n1 = length(Bet365Home2010)
n2 = length(Bet365Home2016)

tval = (mean(Bet365Home2010)-mean(Bet365Home2016))/sqrt((var1/n1)+(var2/n2))
df = ceiling((((var1/n1)+(var2/n2))**2)/(((var1/n1)**2)/(n1-1)+((var2/n2)**2)/(n2-1)))
pvalues = c(pvalues,pt(tval,df))


#Result:

pvalues

#We do not have data for 2010 season of Betfair. Hence we were not able to calculate the p value.
#In other bookmakers, the p value is around 0.3-0.4 . Hence, we fail to reject the null hypothesis with 0.05 significance.
#Thus, we can say that means are the same for those 2 seasons.

#Task 4

#Null Hypothesis: Ratio of variances is 1.
#Alternative Hypothesis: Ratio of variances is not 1.
#Used test statistic: F-statistic, since it lets us make calculations about ratio of variances.
away2011 = games[season==2011,Away_Score]
away2015 = games[season==2015,Away_Score]
fval = (sd(away2011)**2)/(sd(away2015)**2)
pf(fval,df1 = length(away2011),df2=length(away2015))
#We are using p value approach. P-Value is found to be 0.52. 
#Which means we are not in the critical region for both of the significance levels, 0.1 and 0.01.
#Hence we fail to rejet for both significance levels.



  