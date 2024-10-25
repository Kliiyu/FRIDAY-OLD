# Installation

## **Prerequisites**

### Recommended System Requirements

#### Llama 3.1 (Better results, slower)

- **Operating System**: Windows 10 or later, macOS 11 or later, Linux
- **Processor**: Intel i7 or equivalent
- **Memory**: 16 GB RAM
- **Storage**: 10 GB available space

#### Llama 3.2:1b (Worse results, faster)

- **Operating System**: Windows 10 or later, macOS 11 or later, Linux
- **Processor**: Intel i5 or equivalent
- **Memory**: 8 GB RAM
- **Storage**: 6 GB available space

## Installing Python

### Installation Steps

#### Windows

1. Download the installer from the [official Python website](https://www.python.org/downloads/windows/).
2. Run the installer and ensure you check the box "Add Python to PATH".
3. Follow the on-screen instructions to complete the installation.
4. Verify the installation by running `python --version` in Command Prompt.

#### macOS

1. Download the installer from the [official Python website](https://www.python.org/downloads/mac-osx/).
2. Open the downloaded `.pkg` file and follow the on-screen instructions.
3. Verify the installation by running `python3 --version` in Terminal.

#### Linux

1. Open your terminal.
2. Use the package manager for your distribution to install Python. For example, on Debian-based systems:

```
sudo apt update
sudo apt install python3
```

Verify the installation by running `python3 --version` in Terminal.

## Installing Llama 3.1 or 3.2:1b

### Installation Steps

#### Windows

1. Download the installer from the [official website](https://ollama.com/download/windows).
2. Run the installer and follow the on-screen instructions.
3. Verify the installation by running `ollama --version` in Command Prompt.

#### macOS

1. Download the installer from the [official website](https://ollama.com/download/mac).
2. Double click the downloaded `Ollama.app` file and add it to the applications folder.
3. Follow the on-screen instructions, verify the installation by running `ollama --version` in Terminal.

#### Linux

1. Install ollama by running the following command: (or [manual installation](https://github.com/ollama/ollama/blob/main/docs/linux.md))

```
curl -fsSL https://ollama.com/install.sh | sh
```

Verify the installation by running `ollama --version` in Terminal.

### Download the preferred model

#### Llama3.1

1. Go to your terminal and use the command

```
ollama pull llama3.1
```

#### Llama3.2:1b

1. Go to your terminal and use the command

```
ollama pull llama3.2:1b
```

## **Setting up the project**

### Downloading

#### Using git

1. Run git clone in your terminal

```
git clone https://github.com/Kliiyu/FRIDAY.git
```

#### Using github

1. Open the repository on [Github](https://github.com/Kliiyu/FRIDAY)
2. Download the zip file or open the project with [Github Desktop](https://desktop.github.com/download/)

### Setup

#### Project initialization

1. Open terminal in the folder created
2. Make a Python Virtual Environment and activate it with

```
python -m venv .venv 
.venv/scripts/activate
```

Install required dependencies using

```
python -m pip install --upgrade pip
pip install -r ./config/requirements.txt
```

#### Setting up the .env file

1. Go to the config folder and rename `.env.example` to `.env`
2. Fill in the field in the file with your personal API keys/secrets

## **Next Steps**

You have completed the installation. To learn how to run FRIDAY, please refer to the [How to run FRIDAY Guide](running.md "Running FRIDAY").
