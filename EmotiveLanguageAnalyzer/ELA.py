import AInvestor.EmotiveLanguageAnalyzer.ELAWebCrawler as ELAWebCrawler

class EmotiveLanguageAnalyser:

    def __init__(self):
        self.state = 0
        self.status = 'Idle'
        self.website_dict = {}
        self.emotive_words = {}


class Website:

    def __init__(self, name: str, address: str, data: dict):
        self.name = name
        self.address = address
        self.data = data