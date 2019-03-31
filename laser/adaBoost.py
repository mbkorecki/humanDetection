import cPickle
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier

class AdaBoost:
    def __init__(self):
        with open('adaboost_model', 'rb') as fid:
            self.model = cPickle.load(fid)

    def performBoost(self, X, y, mode):
        # if (mode == "init"):
        #     model = AdaBoostClassifier(DecisionTreeClassifier(max_depth = 1), algorithm = "SAMME", n_estimators = 200)
        #     with open('adaboost_model', 'wb') as fid:
        #         cPickle.dump(model, fid)
        #
        # if (mode == "train"):
        #     with open('adaboost_model', 'rb') as fid:
        #         model = cPickle.load(fid)
        #     model.fit(X, y)
        #     with open('adaboost_model', 'wb') as fid:
        #         cPickle.dump(model, fid)

        if (mode == "test"):
            prediction = self.model.predict(X)
            # print y, ",", prediction
            return prediction
