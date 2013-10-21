from loaders import EachMovieLoader, MovieLensLoader
from classes import Predictor
from evaluators import MovieLensEvaluator

#Loading data
path = "\MovieLens\ml-100k\ml-100k" #Path to MovieLens dir.
dataset = "u.data" #Name of dataset.
loader = MovieLensLoader("D:\Dropbox\Data Sets\MovieLens\ml-100k\ml-100k", dataset)
users, items = loader.users, loader.items

#Making predictions
predictor = Predictor(users, items)
print predictor.predict_rating(users[1], items[100]) #Predicted rating for user 1 on item 100.

#Running evaluation of a test-set.
#Outputs predicted ratings to dataset.res and statistics to result.txt
#evaluator = MovieLensEvaluator()
#evaluator.run_predictions("D:\Dropbox\Data Sets\MovieLens\ml-100k\ml-100k", "u1")