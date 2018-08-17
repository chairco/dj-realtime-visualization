#-*- coding: utf-8 -*-

class ChartFactory:
    def __init__(self):
        self._func = {}
        self._charts = {}

    def collect(self, name):
        def _inject(func):
            self._func[name] = func
            return func

        return _inject

    def create(self, name, **kwargs):
        num = kwargs.get('num')
        if name in self._func:
            chart = self._func[name](num)
            return chart
        else:
            raise ValueError(f'No Chart build for {name}')