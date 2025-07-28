# Fsociety V4 - Advanced Ethical DDoS Testing Suite

![Fsociety](https://i.pinimg.com/736x/30/b9/46/30b94658f685ffd183c8c442d2973d30.jpg)

---

## Overview

Fsociety V4 is a powerful, customizable, and fsociety-themed **ethical DDoS testing toolkit** designed for cybersecurity professionals and researchers. It includes:

- **Controller GUI**: Easy-to-use PyQt5 interface with dark/red terminal aesthetics and embedded fsociety background.
- **Bot**: Multi-mode flood bot supporting TCP, UDP, and HTTP GET floods.
- **Distributed**: Supports launching attacks from multiple bots simultaneously for true distributed stress testing.
- **Advanced Features**: Attack IDs, configurable duration, threads, and attack types. Basic User-Agent rotation and rate-limit avoidance techniques.

---

## Features

- Multi-protocol flood: TCP, UDP, HTTP-GET
- Command format: `ID|TYPE|TARGET|PORT|DURATION|THREADS`
- Multithreaded and async attacks for speed and efficiency
- Fscoiety GUI with embedded background image URL and custom fonts
- Command logging with attack ID tracking
- Basic protection against rate limiting via User-Agent rotation and randomized delays
- Easy to deploy on multiple machines for distributed testing

---

## ⚠️ Disclaimer

**ONLY use this toolkit on targets you own or have explicit permission to test.** Unauthorized use of DDoS tools is illegal and unethical.

This toolkit is intended **for educational and authorized cybersecurity testing purposes only.**

---

## Installation

### Requirements

- Python 3.7+
- `PyQt5`
- `requests`
- `aiohttp`

Install dependencies:

```bash
pip install PyQt5 requests aiohttp
