from sigma.core.ml_module import MLModule


def test_ml_module_init():
    ml = MLModule()
    assert hasattr(ml, "predict")
