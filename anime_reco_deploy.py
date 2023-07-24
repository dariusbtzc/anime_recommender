# -*- coding: utf-8 -*-
"""anime_reco_deploy.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ryBHG6eWKeqdjCvf02vAdVP1q_oRoU6b
"""

import cornac
import cloudpickle
import pandas as pd
import streamlit as st

st.title("Anime Recommender")


# Load the required datasets and models
try:
    # User ratings data - users that have completely watched the anime and given a non-zero score
    ratings = pd.read_csv('rating_complete.csv')

    # Anime metadata
    anime = pd.read_csv('anime.csv', usecols = ['MAL_ID', 'Name', 'Genres'])
    anime.rename(columns = {'MAL_ID': 'anime_id'}, inplace = True)
    anime.columns = map(str.lower, anime.columns)

    # MostPop model
    with open('mostpop.pkl', 'rb') as f:
      most_pop = cloudpickle.load(f)

    # CTR model
    with open('ctr.pkl', 'rb') as f:
      ctr = cloudpickle.load(f)

except FileNotFoundError as e:
    st.error(f"File not found: {e}")
    st.stop()


# User and item mappings for both models
ctr_user_id2idx = list(ctr.train_set.uid_map)
ctr_item_idx2id = list(ctr.train_set.item_ids)

most_pop_user_id2idx = list(most_pop.train_set.uid_map)
most_pop_item_idx2id = list(most_pop.train_set.item_ids)


# For entering the user ID and number of recommendations
user_id_input = st.text_input('Enter your user ID:')
if user_id_input:
    try:
        user_id = int(user_id_input)

        # Ensures that the user ID is not less than 0
        if user_id < 0:
            st.error('Invalid user ID. Please enter a different user ID.')
            st.stop()

    # Ensures that the user ID input is an integer
    except ValueError:
        st.error('User ID must be an integer.')

TOPK = st.number_input('Enter the number of recommendations:', min_value = 1, max_value = 50, value = 10, step = 1)


# Generate the top recommendations
if st.button('Generate'):

  if user_id:

    # Run CTR - for current users
    if user_id in ctr_user_id2idx:
      user_idx = ctr_user_id2idx.index(user_id)
      recommendations_idx, scores = ctr.rank(user_idx)

      # Exclude previously rated items
      rated_items = set(ratings.loc[ratings['user_id'] == user_id, 'anime_id'])
      top_recommendations_idx = [item_idx for item_idx in recommendations_idx if ctr_item_idx2id[item_idx] not in rated_items][:TOPK]

      # Get the item IDs
      top_recommendations_ids = [ctr_item_idx2id[item_idx] for item_idx in top_recommendations_idx]
      recommended_animes = anime[anime['anime_id'].isin(top_recommendations_ids)].reset_index(drop = True)
      recommended_animes.rename(columns = {'anime_id': 'Anime ID', 'name': 'Title', 'genres': 'Genres'}, inplace = True)

      st.write(recommended_animes)

    # Run MostPop - for new users
    else:
      st.write('Welcome new user! Here are some popular animes to get you started:')

      user_idx = most_pop_user_id2idx.index(189037)
      recommendations_idx, scores = most_pop.rank(user_idx)
      top_recommendations_idx = recommendations_idx[:TOPK]

      # Get the item IDs
      top_recommendations_ids = [most_pop_item_idx2id[item_idx] for item_idx in top_recommendations_idx]
      recommended_animes = anime[anime['anime_id'].isin(top_recommendations_ids)].reset_index(drop = True)
      recommended_animes.rename(columns = {'anime_id': 'Anime ID', 'name': 'Title', 'genres': 'Genres'}, inplace = True)

      st.write(recommended_animes)