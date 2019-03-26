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

pinnacle =  
  odds[Bookmaker=="Pinnacle",list(matchid,TieProb,AwayProb,HomeProb,TieOdd,HomeOdd,AwayOdd)]
betssons =
  odds[Bookmaker=="Betsson",list(matchid,TieProb,AwayProb,HomeProb,TieOdd,HomeOdd,
                                 AwayOdd)]
Betfair =
  odds[Bookmaker=="Betfair",list(matchid,TieProb,AwayProb,HomeProb,TieOdd,HomeOdd,
                                 AwayOdd)]
bwin =
  odds[Bookmaker=="bwin",list(matchid,TieProb,AwayProb,HomeProb,TieOdd,HomeOdd,
                              AwayOdd)]
bet365 =
  odds[Bookmaker=="bet365",list(matchid,TieProb,AwayProb,HomeProb,TieOdd,HomeOdd,
                                AwayOdd)]

dt = merge(games,pinnacle,all=TRUE)
dt = merge(dt,betssons,suffixes=c(".1",".2"),all=TRUE)
dt = merge(dt,Betfair,suffixes=c(".2",".3"),all=TRUE)
dt = merge(dt,bwin,suffixes=c(".3",".4"),all=TRUE)
dt = merge(dt,bet365,suffixes=c(".4",".5"),all=TRUE)
dt = dt[,Match_Date:=as.Date(dt[,Match_Date], "%Y-%m-%d")]
dt[,Home_Win := as.numeric(Home_Score>Away_Score)]
dt[,Away_Win:=as.numeric(Away_Score>Home_Score)]
dt[,Res_Tie:=as.numeric(Away_Score==Home_Score)]
dt[,Target:=Home_Score-Away_Score]
#Matches are ordered by date for further use for cumulative functions.
setorder(dt,Match_Date)
dt[,avgHOdd:=(HomeOdd.1+HomeOdd.2+HomeOdd.4+HomeOdd)/4]


dt[,avgAOdd:=(AwayOdd.1+AwayOdd.2+AwayOdd.4+AwayOdd)/4]
dt[,avgTOdd:=(TieOdd.1+TieOdd.2+TieOdd.4+TieOdd)/4]
#Adding 1 column for utility.
dt = dt[,ones:=rep(1,length(dt))]
#Added opposition ID
dt[,oppId:= paste(Home,Away)]

#We will use average of probabilities.
dt[,avgHome:=(HomeProb.1+HomeProb.2+HomeProb.4+HomeProb)/4]
dt[,avgAway:=(AwayProb.1+AwayProb.2+AwayProb.4+AwayProb)/4]
dt[,avgTie:=(TieProb.1+TieProb.2+TieProb.4+TieProb)/4]
#Creating features for probabilities.
#1-Adding Non-Linear Terms
#Polynomial of prob, prob^2
dt[,sqHome:=(avgHome)**2]
dt[,sqAway:=(avgAway)**2]
dt[,sqTie:=(avgTie)**2]
#Exponential of prob, exp(prob)
dt[,expHome:=exp(avgHome)]
dt[,expAway:=exp(avgAway)]
dt[,expTie:=exp(avgTie)]
#Reciprocal of prob, 1/prob.
dt[,recHome:=1/(avgHome)]
dt[,recAway:=1/(avgAway)]


dt[,recTie:=1/(avgTie)]
#Hyperbolic Functions of Prob
dt[,hypHome:=avgHome/(1+avgHome)]
dt[,hypAway:=avgAway/(1+avgAway)]
dt[,hypTie:=avgTie/(1+avgTie)]
#Logarithm of prob
dt[,logHome:=log(avgHOdd)]
dt[,logAway:=log(avgAOdd)]
dt[,logTie:=log(avgTOdd)]

dt[,HomeProb.3:=NULL]
dt[,AwayProb.3:=NULL]
dt[,TieProb.3:=NULL]
dt[,TieOdd.3:=NULL]
dt[,AwayOdd.3:=NULL]
dt[,HomeOdd.3:=NULL]

#2-Adding other meaningful features
#2.A Home Goals per match for Home Team So Far in the Season
dt[,HomeScores:=ifelse(cumsum(ones)==1,0,(cumsum(Home_Score)-
                                            Home_Score)/(cumsum(ones)-1)),by=list(Home,season)]
#2.B Goal Difference per match For Home Team(as a Home Team) So Far in The Season
dt[,DiffSeason:=ifelse(cumsum(ones)==1,0,(cumsum(Home_Score-Away_Score)-
                                            Home_Score+Away_Score)/(cumsum(ones)-1)),by=list(Home,season)]
#2.C Away Goals per match for Away Team So Far in the Season


dt[,AwayScores:=ifelse(cumsum(ones)==1,0,(cumsum(Away_Score)-
                                            Away_Score)/(cumsum(ones)-1)),by=list(Away,season)]
#2.D Goal Difference per match For Away Team(as an Away Team) So Far in The Season
dt[,ADiffSeason:=ifelse(cumsum(ones)==1,0,(cumsum(Home_Score-Away_Score)-
                                             Home_Score+Away_Score)/(cumsum(ones)-1)),by=list(Away,season)]
#2.E Home Team Win Ratio(All Time)
dt[,HomeRatio:=ifelse(cumsum(ones)==1,0.5,(cumsum(Home_Win)-
                                             Home_Win)/(cumsum(ones)-1)),by=list(Home)]
#2.E Average Goal Difference Per Match-up
dt[,MatchupScore:=ifelse(cumsum(ones)==1,0,(cumsum(Home_Score-Away_Score)-
                                              Home_Score+Away_Score)/(cumsum(ones)-1)),by=list(oppId)]
#2.F Historical goals per match for home team
dt[,HistHomeScores:=ifelse(cumsum(ones)==1,0,(cumsum(Home_Score)-
                                                Home_Score)/(cumsum(ones)-1)),by=list(Home)]
#2.G Historical goals per match for home team
dt[,HistAwayScores:=ifelse(cumsum(ones)==1,0,(cumsum(Away_Score)-
                                                Away_Score)/(cumsum(ones)-1)),by=list(Away)]
#2.H Big 4
dt[,Big4 :=
     ifelse(Home=="fenerbahce",1,ifelse(Home=="galatasaray",1,
                                        ifelse(Home=="besiktas",1,
                                               ifelse(Home=="trabzonspor",1,0))))]
dt[,MatchupScore:=NULL]
missing = dt[!complete.cases(dt)]
noMissing = dt[complete.cases(dt)]
noMissing = noMissing[!1795]
noMissing = noMissing[!68]
noMissing = noMissing[!1798]
train = noMissing[season<2017]


model1 =
  lm(Target~HistHomeScores+HistAwayScores+HomeRatio+ADiffSeason+AwayScores+DiffSeason+
       HomeScores+logHome+logAway+logTie+hypAway+hypTie+Big4+HomeProb+HomeProb.1+
       HomeProb.2+HomeProb.4+AwayProb.1+AwayProb.2+AwayProb.4+
       TieProb+TieProb.1+TieProb.2+TieProb.4+recHome+recAway+recTie+expHome+expAway+
       expTie+sqTie+Home+Away,data=train)
stepped = step(model1)
summary(stepped)
#Task 3 - Residuals3
qqnorm(stepped$residuals)
plot(stepped)
predVec = predict(stepped)
train[,pred:=predVec]
library(rpart)
library(rpart.plot)

tr = rpart(Match_Result~pred,data=train,method="class")
prp(tr)
pRes1 = as.matrix(predict(tr))
pRes2 = as.matrix(predict(tr,type="vector"))
train[,predictedTie:=pRes1[,3]]
train[,predictedHome:=pRes1[,2]]
train[,predictedAway:=pRes1[,1]]
train[,predicted:=pRes2]
train[,profit1:=ifelse(Match_Result=="Home"&predicted==2,avgHOdd,
                       ifelse(Match_Result=="Away"&predicted==1,avgAOdd,
                              ifelse(Match_Result=="Tie"&&predicted==3,avgTOdd,0)
))]


train[,profit2:=ifelse(Match_Result=="Home",avgHOdd*predictedHome,
                       ifelse(Match_Result=="Away",avgAOdd*predictedAway,
                              ifelse(Match_Result=="Tie",predictedTie*avgTOdd,0))
)]

train[,profitoT:=(cumsum(profit1))/(cumsum(ones)-1)]
sum(train[,profit1])/length(train[,profit1])
sum(train[,profit2])/length(train[,profit2])
plot(train$profitoT)

test = noMissing[season==2017]
pvec = predict(stepped,newdata=test)
test[,pred:=pvec]
sse = sum(test[,(Target-pred)**2])
sst = sum(test[,(Target-mean(test$Target))**2])
pRes = as.matrix(predict(tr,newdata=test,type="vector"))
test[,prediction:=pRes]
test[,profit:=ifelse(Match_Result=="Home"&pRes==2,avgHOdd,ifelse(Match_Result=="Away"&pRes==1,avgAOdd,0))]
sum(test[,profit])/length(test[,profit])
test[,profitoT:=(cumsum(profit))/(cumsum(ones)-1)]
plot(test$profitoT)