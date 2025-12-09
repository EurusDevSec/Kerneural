# Kerneural: Automated Purple Teaming with eBPF & LLMs

<div align="center">

![Kerneural Logo](logo.jpg)

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![Falco](https://img.shields.io/badge/Security-Falco-00A3E0.svg?style=flat&logo=falco&logoColor=white)](https://falco.org/)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

**From Static Defense to Digital Immune System.**

[Key Features](#key-features) •
[Architecture](#system-architecture) •
[Getting Started](#getting-started) •
[Usage](#usage) •
[Roadmap](#roadmap) •
[Contributing](#contributing)

</div>

---

## 📖 Overview

**Kerneural** (Kernel + Neural) is a research project designed to build an **Automated Purple Teaming** system. It shifts the security paradigm from "Static Rules" to a "Digital Immune System" capable of self-learning and self-healing in runtime.

By combining **eBPF (Falco)** for deep kernel-level visibility and **LLM-driven Agents (Google Gemini)** for intelligent analysis, Kerneural creates a closed-loop control system that detects attacks, analyzes them, and automatically generates and applies blocking rules without human intervention.

## ✨ Key Features

- **👁️ Deep Visibility**: Monitors 100% of system calls using **Falco** (eBPF) at the kernel level.
- **🧠 Neural Core**: Powered by **Google Gemini 1.5 Flash** to analyze security logs and understand attacker intent.
- **🛡️ Auto-Healing**: Automatically generates and applies Falco rules to block active threats in real-time.
- **⚔️ Automated Red Teaming**: Integrated **Atomic Red Team** scenarios to simulate realistic attacks (MITRE ATT&CK).
- **📊 Rich Dashboard**: A beautiful, hacker-style TUI (Terminal User Interface) for real-time monitoring.

## 🏗️ System Architecture

The system operates as a closed-loop feedback mechanism:

1.  **The Battlefield (Victim)**: A vulnerable container (Nginx/App) exposed to attacks.
2.  **Blue Agent (The Sensor)**: Falco hooks into the kernel to detect anomalous behavior and generates logs.
3.  **Neural Core (The Brain)**:
    - Ingests Falco logs.
    - Uses Gemini to analyze the attack pattern.
    - Generates a precise Falco rule (YAML) to mitigate the threat.
4.  **Red Agent (The Stimulus)**: Executes attack scripts (e.g., Reverse Shell, Credential Dumping) to test the defense.

## 🚀 Getting Started

### Prerequisites

- **OS**: Linux (Ubuntu 22.04 LTS recommended) or **Windows via WSL2**.
- **Docker** & **Docker Compose**.
- **Python 3.10+**.
- **Google Gemini API Key**.

### Installation

1.  **Clone the repository**

    ```bash
    git clone https://github.com/EurusDevSec/kerneural.git
    cd kerneural
    ```

2.  **Set up the environment**

    ```bash
    # Create a virtual environment
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

    # Install dependencies
    pip install -r requirements.txt
    ```

3.  **Configure Secrets**
    Create a `.env` file (or set environment variables) with your Gemini API key:
    ```bash
    export GEMINI_API_KEY="your_api_key_here"
    ```

## 🕹️ Usage

### 1. Start the Infrastructure

Launch the victim container and the Falco sensor:

```bash
docker-compose up -d
```

### 2. Run the Neural Dashboard

Start the main controller which listens for logs and manages the AI agents:

```bash
python run.py
```

### 3. Launch Attacks (Simulation)

In a separate terminal, run the automated attack scenarios to test the system:

```bash
bash demo_attacks.sh
```

_Watch the dashboard as the system detects the attack, analyzes it, and automatically deploys a counter-measure rule._

## 🗺️ Roadmap

- [x] **Sprint 1: Infrastructure**: Docker & Falco setup with basic visibility.
- [x] **Sprint 2: Weaponization**: Red Agent with Atomic Red Team integration.
- [x] **Sprint 3: Neural Integration**: Gemini API connection for log analysis.
- [x] **Sprint 4: The Feedback Loop**: Full automation of rule generation and hot-reloading.
- [ ] **Future**: Support for multi-node Kubernetes clusters.

## 🤝 Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## 📜 License

Distributed under the Apache 2.0 License. See `LICENSE` for more information.

## 📞 Contact

**EurusDevSec** - [Project Link](https://github.com/EurusDevSec/kerneural)

---

<div align="center">
  <sub>Built with ❤️ by the Kerneural Team</sub>
</div>
