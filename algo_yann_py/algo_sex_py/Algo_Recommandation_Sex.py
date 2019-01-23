# In[24]:
#import matrice
import pandas as pd
data=pd.read_excel("Donnees_Algo_Sex.xls",header=0,parse_cols=None)
#matrice(clients, produits, bool), matrice définie sur une période de 6 mois


# In[25]:

#remplacer les nan par des zero
donnees_algo_sex=data.fillna(0)
#print('le nbre darticles achetés par le client i:\n',z1)
donnees_algo_sex.head(4)


# In[26]:


#le nbre de produit acheté par le client i
donnees1=donnees_algo_sex.drop(['id_gender'], axis=1)
z1=donnees1.astype(bool).sum(axis=1)



# In[27]:


#le nbre de fois qu'un produit j a été acheté par les clients
z2=donnees1.astype(bool).sum(axis=0)



# In[28]:


#quantité des articles vendus
qty=donnees1.sum(axis=0)
qty


# In[32]:


################statistique sexe masculin##########################
g = donnees_algo_sex.groupby('id_gender')
#calculer la moyenne de chaque produit achetée par les hommes
Moy_M=g.get_group('M')[:].mean()
Pourc_M=g.get_group('M')[:].mean()*100
Sum_M=g.get_group('M')[:].sum()[0:donnees_algo_sex.shape[1]-1]
Moy_Pourc_M = pd.concat([Sum_M,Moy_M,Pourc_M],axis=1)
#renommer la colonne 0 comme cluster (car par défaut c'est 0 comme nom de la colonne)
Moy_Pourc_M=Moy_Pourc_M.rename(columns={0:'Number of sales (M)',1: 'Means of men',2: '% of men'},inplace=False) 
print('le nbre,la moyenne et le pourcentage des produits achetés par les hommes\n',Moy_Pourc_M)


# In[34]:


################statistique sexe féminin##########################

Moy_F=g.get_group('F')[:].mean()
Pourc_F=g.get_group('F')[:].mean()*100
Sum_F=g.get_group('F')[:].sum()[0:donnees_algo_sex.shape[1]-1]
Moy_Pourc_F = pd.concat([Sum_F,Moy_F,Pourc_F],axis=1)
#renommer la colonne 0 comme cluster (car par défaut c'est 0 comme nom de la colonne)
Moy_Pourc_F=Moy_Pourc_F.rename(columns={0:'Number of sales (F)',1: 'Means of womens',2: '% of womens'},inplace=False) 
print('la moyenne et le pourcentage des produits achetés par les femmes \n',Moy_Pourc_F)


# In[35]:


#comparaison pourcentage entre femmes et hommes
comparaison = pd.concat([Moy_Pourc_M['% of men'], Moy_Pourc_F['% of womens']],axis=1)
comparaison


# In[36]:


#########recommandation produits pour femme##################
#récuperer les produits qui ont été acheté  par plus 10% de femmes
produit_F_seuil=Moy_Pourc_F[Moy_Pourc_F['% of womens'] >= 10].sort_values(by = '% of womens', ascending = False) 
produit_F_seuil

#récuperer les produits qui ont été acheté  par plus 10% de hommes
produit_M_seuil=Moy_Pourc_M[Moy_Pourc_M['% of men'] >= 10].sort_values(by = '% of men', ascending = False) 
produit_M_seuil


# In[38]:


#preparer une table complete pour déterminer les produits de plus de 10% a shooter aux femmes 
Customers_F= pd.DataFrame()
Shooter_Products_F= pd.DataFrame()
z3=donnees_algo_sex.loc[donnees_algo_sex['id_gender']=="F",:]
Y3=z3.iloc[:,0:z3.shape[1]-1].T
w3= pd.concat([Y3,comparaison],axis=1)
#déterminer les femmes (qui n'ont jamais acheté ce produit) auquelles il faut leur envoyer des produits les plus achetés >50%
for j in w3.columns:
    for i in w3.index:
        if (w3[j][i] == 0) and (w3['% of womens'][i] >=10) and (j != "% of men"):
             Customers_F = Customers_F.append([j]) #matrice clients
             Shooter_Products_F = Shooter_Products_F.append([i]) #matrice produits

Customers_F=Customers_F.rename(columns={0:'Customers (F)'},inplace=False)     
Shooter_Products_F=Shooter_Products_F.rename(columns={0: 'Shooter products (F)'},inplace=False)     
Womens_Recommandation= pd.concat([Customers_F,Shooter_Products_F],axis=1)
Womens_Recommandation


# In[39]:


#preparer une table complete pour déterminer les produits de plus de 50% a shooter aux hommes 
Customers_M= pd.DataFrame()
Shooter_Products_M= pd.DataFrame()
z4=donnees_algo_sex.loc[donnees_algo_sex['id_gender']=="M",:]
Y4=z4.iloc[:,0:z4.shape[1]-1].T
w4= pd.concat([Y4,comparaison],axis=1)
#déterminer les hommes(qui n'ont jamais acheté ce produit) auquelles il faut leur envoyer des produits les plus achetés >50%
for j in w4.columns:
    for i in w4.index:
        if ((w4[j][i] == 0) and (w4['% of men'][i] >=10) and (j != "% of womens")):
              Customers_M = Customers_M.append([j]) #matrice clients
              Shooter_Products_M = Shooter_Products_M.append([i]) #matrice produits
Customers_M =Customers_M.rename(columns={0:'Customers (M)'},inplace=False)     
Shooter_Products_M=Shooter_Products_M.rename(columns={0: 'Shooter products (M)'},inplace=False)     
Men_Recommendation= pd.concat([Customers_M,Shooter_Products_M],axis=1)
Men_Recommendation


# In[40]:


Men_Recommendation.to_csv('Men_Recommendation.xls', sep = '\t') 
Womens_Recommandation.to_csv('Womens_Recommandation.xls', sep = '\t')  
import shutil
Output_algo_sex = open("Output_algo_sex.xls", "w")
list_fichier =['Men_Recommendation.xls','Womens_Recommandation.xls']
for i in list_fichier:
          shutil.copyfileobj(open(i, 'r'), Output_algo_sex)
Output_algo_sex.close()

