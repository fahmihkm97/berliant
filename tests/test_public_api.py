import berliant


def test_public_version() -> None:
    assert berliant.__version__ == "0.1.0"


def test_scif_is_current_public_implementation() -> None:
    assert berliant.SCIF is berliant.SCIFDiscoveryV4


def test_core_objects_are_available_from_package_root() -> None:
    expected = {
        "ExecutionResult",
        "FailureClass",
        "InteractionFault",
        "KeyedSimulator",
        "ResidualRiskReport",
        "SCIF",
        "SCIFDiscoveryV4",
        "SCIFV4Report",
        "Scenario",
        "Simulator",
        "load_scenario",
    }

    assert expected.issubset(set(berliant.__all__))

    for name in expected:
        assert hasattr(berliant, name)


def test_validated_scif_uses_evaluated_thresholds() -> None:
    def invoke(_capabilities):
        return berliant.ExecutionResult(
            success=True,
            failure_class=None,
            active_capabilities=frozenset(),
        )

    scif = berliant.validated_scif(
        invoke=invoke,
        capabilities=("a", "b", "c"),
    )

    assert scif.pairwise_discovery.min_joint_failure == 0.15
    assert scif.pairwise_discovery.min_jri == 0.10
    assert scif.residual_trials == 1000
    assert scif.min_residual_failure == 0.15
    assert scif.min_residual_increment == 0.10
