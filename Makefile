.PHONY: benchmark benchmark-probes benchmark-validate benchmark-validate-platform verify

benchmark:
	./benchmarks/run.py

benchmark-probes:
	./benchmarks/probes.py

benchmark-validate-platform:
	./benchmarks/validate_results.py \
		benchmarks/results/cp21-probes-macos-arm64-apple-m2.json \
		benchmarks/results/cp21-algorithms-macos-arm64-apple-m2.json

benchmark-validate:
	./benchmarks/validate_tier1_baselines.py

verify:
	./verify.sh
