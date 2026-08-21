.PHONY: benchmark benchmark-probes benchmark-validate verify

benchmark:
	./benchmarks/run.py

benchmark-probes:
	./benchmarks/probes.py

benchmark-validate:
	./benchmarks/validate_results.py \
		benchmarks/results/cp21-probes-macos-arm64-apple-m2.json \
		benchmarks/results/cp21-algorithms-macos-arm64-apple-m2.json

verify:
	./verify.sh
