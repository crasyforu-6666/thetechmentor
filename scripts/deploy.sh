#!/usr/bin/env bash
# Deploy the static site to Vercel production
set -e

VERCEL_BIN="/Users/anshumanbehuria/.npm/_npx/69f9afb961c37556/node_modules/@vercel/vc-native-darwin-arm64/bin/vercel"

if [ -f "$VERCEL_BIN" ]; then
  "$VERCEL_BIN" deploy --prod --yes
else
  npx vercel deploy --prod --yes
fi
