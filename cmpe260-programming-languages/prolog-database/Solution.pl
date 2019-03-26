%Mert Yüksekgönül 2016402147 Project1


%generic list operations are defined below.
%predicates below are used in the implementation.

%Reversing operation.

reverseL([],Z,Z).

reverseL([H|T],Z,Acc) :- 
		reverseL(T,Z,[H|Acc]).


%Merging operation for two lists.				
merge_list([],L,L ).
merge_list([H|T],L,[H|M]):-
		merge_list(T,L,M).		


%Sorting operation for a list.
%Insertion sort algorithm is used. 		
i_sort([],Acc,Acc,W).
i_sort([H|T],Acc,Sorted,W):-
		insert(H,Acc,NAcc,W),i_sort(T,NAcc,Sorted,W).

insert(X,[Y|T],[Y|NT],W):-
		average(X,W,AX),
		average(Y,W,AY),
		AX=<AY,
		insert(X,T,NT,W).

insert(X,[Y|T],[X,Y|T],W):-
		average(X,W,AX),
		average(Y,W,AY),
		AY<AX.

insert(X,[],[X],W).
	

isReversePerm(List1,List2):-
			reverseL(List1,ListRev,[]),
			permutation(ListRev,PermList),
			reverseL(PermList,List2,[]).
		

%Compares 2 lists and returns true if the second list contains all elements of the second list.
isAllIn([],TeamList).

isAllIn([Head|Tail],TeamList):-
			member(Head,TeamList),
			isAllIn(Tail,TeamList).
						
%0.1 allTeams predicate

%returns true if a given list L is the full list of teams with team number N.
allTeams(L,N):-
		findall(T,team(T,_), TeamList),
		isAllIn(L,TeamList),
		isAllIn(TeamList,L),
		length(L,N).

allTeams(L,N):-
		findall(T,team(T,_), TeamList),
		isReversePerm(TeamList,L),
		length(L,N).

			
awayWins(T,W,L):- 
					match(We,L,HomeScore,T,AwayScore),
					AwayScore@>HomeScore,
					We@=<W.

homeWins(T,W,L):- 
					match(We,T,HomeScore,L,AwayScore),
					AwayScore@<HomeScore,
					We@=<W.

drawHMatch(T,W,L):-
					match(We,T,HomeScore,L,AwayScore),
					AwayScore == HomeScore,
					We@=<W.
drawAMatch(T,W,L):-
					match(We,L,HomeScore,T,AwayScore),
					AwayScore == HomeScore,
					We@=<W.
					
wins(T,W,L,N):-
					findall(Hloser,homeWins(T,W,Hloser),Hlist),
					findall(Aloser,awayWins(T,W,Aloser),Alist),
					merge_list(Hlist,Alist,L),
					length(L,N).
					
draws(T,W,L,N):-
					findall(Dhteam,drawHMatch(T,W,Dhteam),Hlist),
					findall(Dateam,drawAMatch(T,W,Dateam),Alist),
					merge_list(Hlist,Alist,L),
					length(L,N).
		
losses(T,W,L,N):-
					findall(Hloser,homeWins(Hloser,W,T),Hlist),
					findall(Aloser,awayWins(Aloser,W,T),Alist),
					merge_list(Hlist,Alist,L),
					length(L,N).					


cumsum([Head], Head).

cumsum([Head1,Head2 | Tail],Total):-
					Head3 is Head1+Head2,
					cumsum([Head3|Tail],Total).
					
					
homeGoals(T,W,S):-
					match(We,T,S,L,AwayScore),
					We@=<W.

awayGoals(T,W,S):- 	match(We,L,HomeScore,T,S),
					We@=<W.

homeConc(T,W,S):-
					match(We,T,TScore,L,S),
					We@=<W.

awayConc(T,W,S):- 	match(We,L,S,T,TScore),
					We@=<W.
					
scored(T,W,S):-	  findall(Score1,homeGoals(T,W,Score1),Hlist),
				  findall(Score2,awayGoals(T,W,Score2),Alist),
				  merge_list(Hlist,Alist,Goals),
				  cumsum(Goals,S).

conceded(T,W,S):- findall(Score1,homeConc(T,W,Score1),Hlist),
				  findall(Score2,awayConc(T,W,Score2),Alist),
				  merge_list(Hlist,Alist,Goals),
				  cumsum(Goals,S).	

average(T,W,A):-  scored(T,W,S),
				  conceded(T,W,C),
				  A is (S-C).
				  
week(W) :-    match(W,A,B,C,D).	
			  
ass(W,W1) :-  ass(W1,W1).

order(L,W1):-  setof(We,week(We),WList),
			  member(W1,WList),
			  ordered(L2,W1),
			  L == L2.

order(L,W) :- ordered(L,W).

ordered(L,W) :- findall(T,team(T,_),TList),
				sortTeams(TList,L,W).

						 

topThree([T1,T2,T3],W) :- order([T1,T2,T3|R],W).

				 
sortTeams(TList,SortedList,W):-
							 i_sort(TList,[],SortedList,W).

	
	

	