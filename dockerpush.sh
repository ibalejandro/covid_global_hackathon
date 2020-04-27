#!/bin/sh
docker build -t 5vid-telemetry .
aws ecr get-login-password --region us-west-2 --profile=5vid-admin | docker login --username AWS --password-stdin 240851575709.dkr.ecr.us-west-2.amazonaws.com/5vid-telemetry
docker tag 5vid-telemetry:latest 240851575709.dkr.ecr.us-west-2.amazonaws.com/5vid-telemetry:latest
docker push 240851575709.dkr.ecr.us-west-2.amazonaws.com/5vid-telemetry:latest