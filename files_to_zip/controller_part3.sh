#!/bin/bash



kubectl create -f parsec-benchmarks/part2a/parsec-ferret.yaml
kubectl create -f parsec-benchmarks/part2a/parsec-freqmine.yaml
kubectl create -f parsec-benchmarks/part2a/parsec-blackscholes.yaml
kubectl create -f parsec-benchmarks/part2a/parsec-canneal.yaml
kubectl create -f parsec-benchmarks/part2a/parsec-fft.yaml
kubectl create -f parsec-benchmarks/part2a/parsec-dedup.yaml


