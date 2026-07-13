class SceneDetector:

    def __init__(self, settings):

        self.settings = settings

    def analyze(self, frame):

        return {

            "brightness": frame.mean()

        }