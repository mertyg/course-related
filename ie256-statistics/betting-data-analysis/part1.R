games =fread("matches.csv",header=TRUE)
odds =fread("odds.csv",header=TRUE)


#plots the Home Goals Histogram with associated Poisson Distribution
hist(games[,Home_Score],ylab="Number of Games",xlab="Home Goals",main="Task 1 Home Goals")
xfit = seq(0,max(games[,Home_Score]),1)
yfit = dpois(xfit,lambda=mean(games[,Home_Score]))
lines(xfit,yfit*length(games[,Home_Score]),col="blue",lty=6)

#Plots the Quantiles of associated Poisson ditribution
firstQ = qpois(.25,lambda=mean(games[,Home_Score]))
secondQ = qpois(.5,lambda=mean(games[,Home_Score]))
thirdQ=qpois(.75,lambda=mean(games[,Home_Score]))
abline(v=firstQ,col="green",lwd=4,lty=4)
abline(v=secondQ,col="green",lwd=4,lty=4)
abline(v=thirdQ,col="green",lwd=4,lty=4)

#adds the explanations, with output of actual quantiles of data.table.
text(firstQ,735,"1st and 2nd Quantile")
text(thirdQ,635,"3rd Quantile")
text(5,400,"Given matches data have the following quantiles: ")
strQuants1 = capture.output(quantile(games[,Home_Score],probs=c(.25,.5,.75)))
text(5,300,paste(strQuants1[1],"\n",strQuants1[2]))
legend(5, 650, legend=c("Home Goals", "Poisson pmf","Quantiles of Poisson"),col=c("black", "blue","green"), lty=c(1,6,4), cex=0.8)

#plots the histogram of away goals with associated poisson distribution
hist(games[,Away_Score],ylab="Number of Games",xlab="Away Goals",main="Task 1 Away Goals")
xfit = seq(0,max(games[,Away_Score]),1)
yfit = dpois(xfit,lambda=mean(games[,Away_Score]))
lines(xfit,yfit*length(games[,Away_Score]),col="blue",lty=6)

#Plots the Quantiles of associated Poisson distribution
firstQ = qpois(.25,lambda=mean(games[,Away_Score]))
secondQ = qpois(.5,lambda=mean(games[,Away_Score]))
thirdQ=qpois(.75,lambda=mean(games[,Away_Score]))
abline(v=firstQ,col="green",lwd=4,lty=4)
abline(v=secondQ,col="green",lwd=4,lty=4)
abline(v=thirdQ,col="green",lwd=4,lty=4)

#adds the explanations, with output of actual quantiles of data.table.
text(firstQ+.3,738,"1st Quantile")
text(secondQ,790,"2nd Quantile")
text(thirdQ,635,"3rd Quantile")
text(5,400,"Given matches data have the following quantiles: ")
strQuants1 = capture.output(quantile(games[,Away_Score],probs=c(.25,.5,.75)))
text(5,300,paste(strQuants1[1],"\n",strQuants1[2]))
legend(5, 750, legend=c("Away Goals", "Poisson pmf","Quantiles of Poisson"),col=c("black", "blue","green"), lty=c(1,6,4), cex=0.8)


#Plots the away goals histogram with associated Skellam Distribution
#i.e. Skellam is the difference of 2 Poisson distributions
hist(games[,Home_Score-Away_Score],ylab="Number of Games",xlab="Home Goals-Away Goals",main="Task 1 Goals Difference")
xfit = seq(-6,6,0.1)
yfit = dskellam(xfit,lambda1=mean(games[,Home_Score]),lambda2=mean(games[,Away_Score]))
lines(xfit,yfit*length(games[,Home_Score]),col="blue",lty=3)
text(-4.5,400,"Blue line is pmf of Skellam distribution \n with Home Score and Away Score means")
legend(-6.5, 600, legend=c("Goals Difference", "Skellam pmf"),col=c("black", "blue"), lty=c(1,3), cex=0.8)


#setting the key for merge operations
#creating related probability vectors with normalization
setkey(odds,matchid)
setkey(games,matchid)
odds = odds[,SumProb := (1/TieOdd)+(1/AwayOdd)+(1/HomeOdd)]
odds = odds[,TieProb := 1/(TieOdd*SumProb)]
odds = odds[,AwayProb := 1/(AwayOdd*SumProb)]
odds = odds[,HomeProb := 1/(HomeOdd*SumProb)]
gameswOdds = merge(games,odds[,list(matchid,HomeProb,AwayProb,TieProb,Bookmaker)])


betssons = gameswOdds[Bookmaker=="Betsson"]
betssons[,buckets:=cut(betssons[,HomeProb-AwayProb],c(-25:25)/25)]
betssons[,RealResult:=mean(Match_Result=="Tie"),by=buckets]
plot(y=betssons[,RealResult],x=betssons[,HomeProb-AwayProb],col="Red",main="Betsson",xlab="P(Home)-P(Away)"
     ,ylab="P(Draw)",pch=17,ylim=c(0,0.5))
points(y=betssons[,TieProb],x=betssons[,HomeProb-AwayProb])
legend(0.36, 0.5, legend=c("Company's Probability", "Actual Results in the related bucket"),col=c("black", "red"), pch=c(1,17), cex=0.8)


pinnacle = gameswOdds[Bookmaker=="Pinnacle"]
pinnacle[,buckets:=cut(pinnacle[,HomeProb-AwayProb],c(-20:20)/20)]
pinnacle[,RealResult:=mean(Match_Result=="Tie"),by=buckets]
plot(y=pinnacle[,RealResult],x=pinnacle[,HomeProb-AwayProb],col="Red",main="Pinnacle",xlab="P(Home)-P(Away)"
     ,ylab="P(Draw)",pch=17,ylim=c(0,0.5))
points(y=pinnacle[,TieProb],x=pinnacle[,HomeProb-AwayProb])
legend(0.36, 0.5, legend=c("Company's Probability", "Actual Results in the related bucket"),col=c("black", "red"), pch=c(1,17), cex=0.8)


Betfair = gameswOdds[Bookmaker=="Betfair"]
Betfair[,buckets:=cut(Betfair[,HomeProb-AwayProb],c(-20:20)/20)]
Betfair[,RealResult:=mean(Match_Result=="Tie"),by=buckets]
plot(y=Betfair[,RealResult],x=Betfair[,HomeProb-AwayProb],col="Red",main="Betfair",xlab="P(Home)-P(Away)"
     ,ylab="P(Draw)",pch=17,ylim=c(0,0.5))
points(y=Betfair[,TieProb],x=Betfair[,HomeProb-AwayProb])
legend(0.36, 0.5, legend=c("Company's Probability", "Actual Results in the related bucket"),col=c("black", "red"), pch=c(1,17), cex=0.8)



bwin = gameswOdds[Bookmaker=="bwin"]
bwin[,buckets:=cut(bwin[,HomeProb-AwayProb],c(-20:20)/20)]
bwin[,RealResult:=mean(Match_Result=="Tie"),by=buckets]
plot(y=bwin[,RealResult],x=bwin[,HomeProb-AwayProb],col="Red",main="bwin",xlab="P(Home)-P(Away)"
     ,ylab="P(Draw)",pch=17,ylim=c(0,0.5))
points(y=bwin[,TieProb],x=bwin[,HomeProb-AwayProb])
legend(0.36, 0.5, legend=c("Company's Probability", "Actual Results in the related bucket"),col=c("black", "red"), pch=c(1,17), cex=0.8)



bet365 = gameswOdds[Bookmaker=="bet365"]
bet365[,buckets:=cut(bet365[,HomeProb-AwayProb],c(-20:20)/20)]
bet365[,RealResult:=mean(Match_Result=="Tie"),by=buckets]
plot(y=bet365[,RealResult],x=bet365[,HomeProb-AwayProb],col="Red",main="bet365",xlab="P(Home)-P(Away)"
     ,ylab="P(Draw)",pch=17,ylim=c(0,0.5))
points(y=bet365[,TieProb],x=bet365[,HomeProb-AwayProb])
legend(0.36, 0.5, legend=c("Company's Probability", "Actual Results in the related bucket"),col=c("black", "red"), pch=c(1,17), cex=0.8)


#For grid tables
library(grid.table)
grid.table(betssons[order(buckets),list(ActualResult=mean(Match_Result=="Tie"),P_Draw = mean(TieProb),Earn_Ratio = mean(Match_Result=="Tie")-mean(TieProb)
                                        ,Count_Matches = .N),by=buckets])

