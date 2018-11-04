###10/28/18 
#clustering team possessions over 2015-16 season using play-by-play data
#based on teams' shot type, distance, possession time, and whether the shot
#was assisted or block or not 

import pandas as pd 
import numpy as np 
import sklearn 
from sklearn.cluster import KMeans

shot_att=pd.read_csv("shot_att_16.csv")

#score differential 
shot_att['score_diff']=shot_att['home_score']-shot_att['away_score']
#shot types 
shot_att.type= pd.Categorical(shot_att.type)
shot_att.type=shot_att.type.cat.codes
shot_att['type']=shot_att['type'].astype(str)

#subset for clustering 
cluster_sub=shot_att[["team","type","shot_distance","assists","block","poss_time"]]
cluster_sub.info()

#count shots by teams
team_shots=cluster_sub.groupby('team').value_counts() 
team_shots.reset_index(level=0,inplace=True)
team_shots=team_shots.iloc[:,0:2]
team_shots.sort_values(ascending=False,by="type")

#team shot time possession 
team_clock=cluster_sub.groupby('team')['poss_time'].mean()
team_clock=pd.DataFrame(team_clock) 
team_clock.reset_index(level=0,inplace=True)

#team assists
team_ast=cluster_sub.groupby('team')['assists'].value_counts() 
team_ast=pd.DataFrame(team_ast)
team_ast.reset_index(level=0,inplace=True)

#team block shots (against)
team_blks=cluster_sub.groupby('team')['block'].value_counts()
team_blks=pd.DataFrame(team_blks)
team_blks.reset_index(level=0,inplace=True)

#merge dataframes 
teams=pd.merge(team_clock,team_ast,on="team")
teams=pd.merge(teams,team_blks,on="team")

teams.shape #120,4
teams1=teams.values 
teams2=teams1.reshape((30,16))
teams2=pd.DataFrame(teams2)

teams2.columns=['team','poss_time','ast_no','blk_no','x',
'x','x','blk_yes','x','x','ast_yes','x','x','x','x','x']
teams2=teams2[["team","poss_time","ast_no","blk_no",
"blk_yes","ast_yes"]]
teams2['shot_att']=teams2['ast_no']+teams2['ast_yes']
teams2['pct_ast']=teams2['ast_yes']/teams2['shot_att']
teams2['pct_blk']=teams2['blk_yes']/teams2['shot_att']

#summary stats 
teams2.sort_values(ascending=False,by="pct_ast")['team']
teams2.sort_values('pct_ast',ascending=False) #gsw, atl, dal
teams2.sort_values('pct_blk',ascending=False) #mem (0.049), chi, and mil


#kmeans clustering 
cluster_sub1=cluster_sub.iloc[:,1:cluster_sub.shape[1]]
cluster_sub1=cluster_sub1.fillna(cluster_sub1.mean())
kmeans=KMeans(n_clusters=3)
kmeans.fit(cluster_sub1)
results=kmeans.labels_
results=pd.DataFrame(results,columns=['group'])

#concat with original dataframe
final_results=pd.concat([cluster_sub,results],axis=1)

#how is each group characterized?
group_metrics=final_results.groupby('group')[['shot_distance','poss_time','assists','block']].mean() 

#count teams by group 
team_groups=final_results.groupby('team')['group'].value_counts() 
team_groups=pd.DataFrame(team_groups)
team_groups.reset_index(level=0,inplace=True)
team_groups1=team_groups.values 
team_groups1=team_groups1.reshape(30,6)

team=team_groups1[:,0]
g1=team_groups1[:,1]
g2=team_groups1[:,3]
g3=team_groups1[:,5]
final_groups=np.column_stack((team,g1,g2,g3))

final_groups1=pd.DataFrame(final_groups)
final_groups1.columns=['team','g1','g2','g3']
final_groups1['total']=final_groups1['g1']+final_groups1['g2']+final_groups1['g3']
final_groups1['pct_g1']=final_groups1['g1']/final_groups1['total']
final_groups1['pct_g2']=final_groups1['g2']/final_groups1['total']
final_groups1['pct_g3']=final_groups1['g3']/final_groups1['total']

final_groups1['pct_g1']=final_groups1['pct_g1'].astype(float)
final_groups1['pct_g2']=final_groups1['pct_g2'].astype(float)
final_groups1['pct_g3']=final_groups1['pct_g3'].astype(float)

g1=final_groups1[final_groups1['pct_g1']>0.489]['team']
g2=final_groups1[final_groups1['pct_g2']>0.371]['team']
g3=final_groups1[final_groups1['pct_g3']>0.189]['team']