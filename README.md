# Anime Recommender
Two major challenges of anime streaming platforms today include:
1. Boosting user engagement and satisfaction
2. Diversifying user interests

This project aims to build a recommender system to address these challenges by offering personalised anime content using historical user rating data and anime metadata from Kaggle's [Anime Recommendation Database 2020](https://www.kaggle.com/datasets/hernan4444/anime-recommendation-database-2020).

In doing so, the recommender can align with **user preferences** and recommend a **diverse range of animes**, including lesser-known titles (i.e., cold-start items).

For this project, the `Cornac` library will be used to develop the anime recommender from pre-processing to deployment. For more information on `Cornac`, please refer to the links below:
* GitHub: [https://github.com/PreferredAI/cornac](https://github.com/PreferredAI/cornac)
* Documentation: [https://cornac.readthedocs.io/en/latest/](https://cornac.readthedocs.io/en/latest/)


# Recommender Demo
The images below show the results of running the anime recommender using the `streamlit` module: 

For the current users, the selected model (i.e., Collaborative Topic Regression) was used to recommend personalised anime titles.

In contrast, for new users, a baseline model (i.e., Most Popular) was used to recommend the most popular anime titles.
