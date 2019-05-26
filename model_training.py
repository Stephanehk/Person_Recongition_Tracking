from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
import pickle


def train_face_recognizer():
    embeddings = "/Users/2020shatgiskessell/Desktop/Missing_Child_Recognition/output/embeddings.pickle"
    recongizer_o = "/Users/2020shatgiskessell/Desktop/Missing_Child_Recognition/output/recognizer.pickle"
    le_o = "/Users/2020shatgiskessell/Desktop/Missing_Child_Recognition/output/le.pickle"

    #load face knownEmbeddings
    data = pickle.loads(open(embeddings, "rb").read())
    #label encodings
    le = LabelEncoder()
    labels = le.fit_transform(data["names"])

    #train
    print("[INFO] training model...")
    recognizer = SVC(C=1.0, kernel="linear", probability=True)
    recognizer.fit(data["embeddings"], labels)

    # write the actual face recognition model to disk
    f = open(recongizer_o, "wb")
    f.write(pickle.dumps(recognizer))
    f.close()

    # write the label encoder to disk
    f = open(le_o, "wb")
    f.write(pickle.dumps(le))
    f.close()
