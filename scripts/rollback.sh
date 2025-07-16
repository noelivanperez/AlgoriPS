#!/bin/bash
# Roll back deployment to a previous tag
tag=$1
if [ -z "$tag" ]; then
  echo "Usage: $0 <tag>"
  exit 1
fi
kubectl set image deployment/algorips core=algorips/core:$tag && \
  kubectl rollout status deployment/algorips
