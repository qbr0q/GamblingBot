class FixesList(list):
    def __init__(self, maxlen=3, *args):
        super().__init__(args)
        self.maxlen = maxlen

    def append(self, item):
        super().append(item)
        if len(self) > self.maxlen:
            self.pop(0)
