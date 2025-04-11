import pickle


def load_all_jds():
    with open("data/jd_cache.pkl", "rb") as f:
        return pickle.load(f)

def load_jd(role):
    return load_all_jds().get(role, {})