#!/usr/bin/env bash

uvicorn main:app --reload
python3 consumer.py