from classes import Predictor
from loaders import MovieLensLoader

class MovieLensEvaluator(object):
	def __init__(self):
		pass

	def run_predictions(self, path, dataset = "u1"):
		loader = MovieLensLoader(path, "\\" + dataset + ".base")
		users = loader.users
		items = loader.items
		predictor = Predictor(users, items)

		count, wrong, right, difference = 0.0, 0.0, 0.0, 0.0

		print "Starting test"

		with open(path + "\\" + dataset + ".test") as f, open(path + "\\" + dataset + ".res", "w") as y:
			for line in f:
				data = line.split("\t")
				userid = int(data[0])
				itemid = int(data[1])
				rating = float(data[2])
				new_rating = round(predictor.predict_rating(users[userid], items[itemid]))

				if rating == new_rating:
					right += 1  
				else: 
					wrong += 1
				difference += abs(rating-new_rating)
				count += 1

				y.write(str(userid) + "\t" + str(itemid) + "\t" + str(int(new_rating)) + "\n")

				if count % 100 == 0:
					print "Running test: " + str(count)

		print "Done. Result written to result.txt"
		
		self.__write_result(path, dataset, count, right, wrong, difference)

	def __write_result(self, path, dataset, count, right, wrong, difference):
		with open(path + "\\" + "result.txt", "a") as f:
			f.write("\nDataset: {}\nRight: {} / {}\nWrong: {} / {}\nPercentage: {}\nDifference: {} / {}\n".format(
			dataset, str(right), str(count), str(wrong), str(count), str(right/count*100), str(difference), str(count*4)))