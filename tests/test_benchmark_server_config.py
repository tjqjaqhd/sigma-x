from sigma.server_config import load_server_spec


def test_benchmark_load_server_spec(benchmark):
    result = benchmark(load_server_spec)
    assert result.public_ip
