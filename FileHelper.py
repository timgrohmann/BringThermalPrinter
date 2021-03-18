import pickle
import warnings

class FileHelper():
    @staticmethod
    def load_file(name):
        try:
            return pickle.load(open(f"store/{name}.pkl", "rb"))
        except:
            warnings.warn(f"Could not locate file named {name}")
            return None

    @staticmethod
    def save_file(name, doc):
        with open(f'store/{name}.pkl', 'wb') as f:
            pickle.dump(doc, f)

    @staticmethod
    def load_or_lamda(name, func, force_load: bool = False):
        f = FileHelper.load_file(name)
        if f is None or force_load:
            f = func()
            FileHelper.save_file(name, f)
        return f