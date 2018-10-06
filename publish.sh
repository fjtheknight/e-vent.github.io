#!/bin/bash

# Script for owner to publish to master and not forget to switch back
git checkout master && git reset --hard dev && git push; git checkout dev
