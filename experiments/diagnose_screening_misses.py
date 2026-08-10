from berliant.bsib import Simulator, load_scenario
from berliant.discovery import SCIFDiscoveryV2

SCENARIO_PATH = "benchmarks/bsib_01/easy/BSIB-PAIR-002.yaml"

TARGET_PAIR = tuple(
    sorted(
        (
            "tools",
            "streaming",
        )
    )
)

SEEDS = (13, 21)


def main() -> None:
    scenario = load_scenario(SCENARIO_PATH)

    print()
    print("SCIF V2 SCREENING-MISS DIAGNOSTIC")
    print("=" * 72)

    for seed in SEEDS:
        simulator = Simulator(
            scenario,
            seed=seed,
        )

        engine = SCIFDiscoveryV2(
            invoke=simulator.invoke,
            capabilities=scenario.capabilities,
            initial_trials=100,
            confirm_trials=1500,
            subset_confirm_trials=1000,
            min_joint_failure=0.15,
            min_jri=0.10,
            confidence_threshold=0.95,
            seed=20260810 + seed,
        )

        report = engine.discover()

        baseline = report.stats[()]
        tools = report.stats[("tools",)]
        streaming = report.stats[("streaming",)]
        pair = report.stats[TARGET_PAIR]

        max_subset_rate = max(
            baseline.failure_rate,
            tools.failure_rate,
            streaming.failure_rate,
        )

        screening_jri = pair.failure_rate - max_subset_rate

        joint_threshold = engine.min_joint_failure * 0.75

        jri_threshold = engine.min_jri * 0.67

        print()
        print(f"SEED {seed}")
        print("-" * 72)

        print(
            f"baseline rate       : "
            f"{baseline.failure_rate:.3f} "
            f"({baseline.failures}/{baseline.trials})"
        )

        print(
            f"tools rate          : "
            f"{tools.failure_rate:.3f} "
            f"({tools.failures}/{tools.trials})"
        )

        print(
            f"streaming rate      : "
            f"{streaming.failure_rate:.3f} "
            f"({streaming.failures}/{streaming.trials})"
        )

        print(
            f"pair rate           : "
            f"{pair.failure_rate:.3f} "
            f"({pair.failures}/{pair.trials})"
        )

        print(f"max subset rate     : {max_subset_rate:.3f}")

        print(f"screening JRI       : {screening_jri:+.3f}")

        print()
        print(f"joint threshold     : {joint_threshold:.3f}")

        print(f"JRI threshold       : {jri_threshold:.3f}")

        joint_pass = pair.failure_rate >= joint_threshold

        jri_pass = screening_jri >= jri_threshold

        print()
        print(f"joint gate          : {'PASS' if joint_pass else 'FAIL'}")

        print(f"JRI gate            : {'PASS' if jri_pass else 'FAIL'}")


if __name__ == "__main__":
    main()
