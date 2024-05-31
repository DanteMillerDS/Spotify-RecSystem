import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

class MusicRecommender:
    "A class to recommend artists to users based on their listening history."
    def __init__(self, data):
        self.sample_data = data
        self.user_artists = {}
        self.all_artists = []
        self.user_vectors = None
        self.similarity_matrix = None

    def find_all_users_artists(self):
        """
        Extracts all unique artists for each user.
        :return: None.
        """
        user_artists = {}
        for user, data in tqdm(self.sample_data.items(), desc="Processing users"):
            artists = set()
            for artist_name in data:
                artists.add(artist_name)
            user_artists[user] = artists
        self.user_artists = user_artists

    def find_all_unique_artists(self):
        """Finds all unique artists in the dataset.
        :return: None.
        """
        all_artists = set()
        for artists in tqdm(self.user_artists.values(), desc="Processing artists"):
            all_artists.update(artists)
        self.all_artists = list(all_artists)

    def create_user_artist_matrix(self):
        """
        Creates a matrix of users and artists.
        :return: None.
        """
        self.user_vectors = pd.DataFrame(0, index=self.user_artists.keys(), columns=self.all_artists)
        for user, artists in tqdm(self.user_artists.items(), desc="Processing users and artist"):
            self.user_vectors.loc[user, list(artists)] = 1

    def calculate_similarity_matrix(self):
        """
        Calculates the similarity matrix between users.
        :return: None.
        """
        self.similarity_matrix = pd.DataFrame(cosine_similarity(self.user_vectors), index=self.user_vectors.index, columns=self.user_vectors.index)

    def suggest_artists_current_user(self):
        """
        Suggests artists to a user based on their listening history.
        :return: None.
        """
        while True:
            print("Available users:", ", ".join(self.similarity_matrix.index))
            current_user = input("Enter the current user (or type 'quit' to exit): ")
            if current_user == 'quit':
                return
            if current_user not in self.similarity_matrix.index:
                print(f"User {current_user} not found. Please try again.")
                continue
            
            while True:
                try:
                    top_n = int(input("Enter the number of similar users to be used in suggesting new artists: "))
                    break
                except ValueError:
                    print("Please enter a valid number.")
            
            while True:
                try:
                    suggestion_number = int(input("Enter the number of artists to suggest: "))
                    break
                except ValueError:
                    print("Please enter a valid number.")
            
            similar_users = self.similarity_matrix[current_user].sort_values(ascending=False).index[1:top_n+1]
            recommendations = {}
            for similar_user in similar_users:
                similarity_score = self.similarity_matrix.at[current_user, similar_user]
                for artist in self.user_artists[similar_user]:
                    if artist not in self.user_artists[current_user]:
                        if artist not in recommendations:
                            recommendations[artist] = 0
                        recommendations[artist] += similarity_score
            
            sorted_recommendations = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)
            top_recommendations = [artist for artist, score in sorted_recommendations]
            print(f"Artists to recommend to {current_user}: {top_recommendations[0:suggestion_number]}")
            break

    def suggest_artists_new_user(self):
        """
        Suggests artists to a new user based on their listening history.
        :return: None.
        """
        while True:
            new_user = input("Enter the new user's name (or type 'quit' to exit): ")
            if new_user == 'quit':
                return
            if not new_user:
                print("User name cannot be empty. Please try again.")
                continue
            break

        while True:
            try:
                top_n = int(input("Enter the number of similar users to be used in suggesting new artists: "))
                break
            except ValueError:
                print("Please enter a valid number.")

        while True:
            try:
                suggestion_number = int(input("Enter the number of artists to suggest: "))
                break
            except ValueError:
                print("Please enter a valid number.")
        
        available_artists = set(self.all_artists)
        new_user_artists = set()
        
        while True:
            print("You can filter available artists by entering a keyword. Type 'done' to finish.")
            keyword = input("Enter a keyword to filter artists: ").lower()
            if keyword == 'done':
                break
            filtered_artists = [artist for artist in available_artists if keyword in artist.lower()]
            if not filtered_artists:
                print("No artists found with that keyword. Please try again.")
            else:
                print("Filtered artists:", ", ".join(filtered_artists))

            while True:
                artist = input("Enter an artist name from the filtered list (or type 'done' to finish): ")
                if artist == 'done':
                    break
                if artist not in available_artists:
                    print(f"Artist {artist} not found in the database. Please try again.")
                    continue
                new_user_artists.add(artist)
        
        self.user_artists[new_user] = new_user_artists
        self.find_all_unique_artists()
        self.create_user_artist_matrix()
        self.calculate_similarity_matrix()
        
        similar_users = self.similarity_matrix[new_user].sort_values(ascending=False).index[1:top_n+1]
        recommendations = {}
        for similar_user in similar_users:
            similarity_score = self.similarity_matrix.at[new_user, similar_user]
            for artist in self.user_artists[similar_user]:
                if artist not in self.user_artists[new_user]:
                    if artist not in recommendations:
                        recommendations[artist] = 0
                    recommendations[artist] += similarity_score
        
        sorted_recommendations = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)
        top_recommendations = [artist for artist, score in sorted_recommendations]
        print(f"Artists to recommend to {new_user}: {top_recommendations[0:suggestion_number]}")
