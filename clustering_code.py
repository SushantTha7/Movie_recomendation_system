import pre_processing
from sklearn.cluster import  KMeans

def clustered_final_df(df):
    df['Cluster_Id']=None

    #modify the n_clustervalue to get the more detailed clustering.
    kmeans = KMeans(n_clusters = 200)

    features = df[['P_Genre','S_Genre','T_Genre']]
    kmeans.fit(features)
    df['Cluster_Id'] =kmeans.predict(features)
    return df

def cluster_everything(input_movie):
    df = pre_processing.pre_process_all()
    df = clustered_final_df(df)
    df.to_csv('Dataset_to_plot.csv')

    #check if the movie is present or not
    input_movie = input_movie.lower()
    # try:
    movie_not_found=df.loc[~df['Movie'].str.contains(input_movie)]
    if len(movie_not_found)==0:
        print('movie not found')
        return 0 
    get_cluster = df['Cluster_Id'].loc[df['Movie'].str.contains(input_movie)].values[0]
    similar_movies_list = df['Movie'].loc[df['Cluster_Id']== get_cluster].values
    return similar_movies_list
    # except:
        # print('movie not found')
        # return 0



# test = cluster_everything(input_movie)









