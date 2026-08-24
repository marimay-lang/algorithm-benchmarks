.PHONY: benchmark benchmark-probes benchmark-features benchmark-validate
.PHONY: benchmark-validate-public-alpha benchmark-validate-platform verify

benchmark:
	./benchmarks/run.py

benchmark-probes:
	./benchmarks/probes.py

benchmark-features:
	./benchmarks/feature_probes.py

benchmark-validate-platform:
	./benchmarks/validate_results.py \
		benchmarks/results/cp21-probes-linux-x86_64.json \
		benchmarks/results/cp21-algorithms-linux-x86_64.json

benchmark-validate:
	./benchmarks/validate_tier1_baselines.py --gate checkpoint-21

benchmark-validate-public-alpha:
	./benchmarks/validate_tier1_baselines.py --gate public-alpha

verify:
	./verify.sh
