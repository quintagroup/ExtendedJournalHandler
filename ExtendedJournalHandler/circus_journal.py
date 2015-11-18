from systemd import journal

class JournalStream(object):
    def __init__(self, **kwargs):
        self.kwargs = dict([(item.upper(), kwargs[item],) for item in kwargs])

    def __call__(self, data):
        journal.send(
            data['data'],
            CIRCUS_STREAM=data['name'],
            **self.kwargs
        )


    def close(self):
        pass
