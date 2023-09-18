from rmshared.content.taxonomy.core.protocols.abc import IValues


class Values(IValues[str | int | float]):
    types = tuple({str, int, float})

    def make_value(self, data):
        if isinstance(data, self.types):
            return data
        else:
            raise ValueError(f'Expected one of {self.types}, got {data}')

    def jsonify_value(self, value):
        return value
