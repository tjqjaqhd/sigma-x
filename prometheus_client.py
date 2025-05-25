class Counter:
    def __init__(self, name, doc):
        self.name = name
        self.value = 0
        _registry[name] = self

    def inc(self, amt=1):
        self.value += amt


class Summary:
    def __init__(self, name, doc):
        self.name = name
        self.values = []
        _registry[name] = self

    def observe(self, value):
        self.values.append(value)


class Gauge:
    def __init__(self, name, doc):
        self.name = name
        self.value = 0
        _registry[name] = self

    def set(self, value):
        self.value = value


_registry = {}


def generate_latest():
    lines = []
    for name, metric in _registry.items():
        if isinstance(metric, Counter):
            lines.append(f"# TYPE {name} counter")
            lines.append(f"{name} {metric.value}")
        elif isinstance(metric, Gauge):
            lines.append(f"# TYPE {name} gauge")
            lines.append(f"{name} {metric.value}")
        elif isinstance(metric, Summary):
            avg = sum(metric.values) / len(metric.values) if metric.values else 0.0
            lines.append(f"# TYPE {name} summary")
            lines.append(f"{name} {avg}")
    return "\n".join(lines).encode()
