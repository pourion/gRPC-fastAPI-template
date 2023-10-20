#!/usr/bin/env bash

uvicorn main:app --reload --port=8008
python3 consumer.py