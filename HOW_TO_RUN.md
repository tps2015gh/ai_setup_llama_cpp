# How to Run llama.cpp with Gemma 4

## Version
- **llama.cpp:** b8676 (supports Gemma 4)
- **Model:** Gemma 4 E2B Q4_K_M (3.46GB)

## Quick Setup (Automated)
```
python setup.py
```
Then select option **6** to install everything at once.

## Manual Setup

### 1. Install llama.cpp
```
python setup.py
# Select option 1
```

### 2. Download Gemma 4 Model
```
python setup.py
# Select option 2
```

## Run Gemma 4

### Chat Mode
```
llama-cpp\llama-cli.exe -m llama-cpp\models\google_gemma-4-E2B-it-Q4_K_M.gguf -cnv
```

### One-Time Response
```
llama-cpp\llama-cli.exe -m llama-cpp\models\google_gemma-4-E2B-it-Q4_K_M.gguf -p "Your question here" -n 128
```

## Low RAM (8GB)
```
llama-cpp\llama-cli.exe -m llama-cpp\models\google_gemma-4-E2B-it-Q4_K_M.gguf -cnv -c 2048
```

## Parameters
| Flag | Meaning | Example |
|------|---------|---------|
| `-m` | Model path | `-m models\gemma.gguf` |
| `-cnv` | Chat mode | |
| `-p` | Prompt | `-p "Hello"` |
| `-n` | Tokens to generate | `-n 256` |
| `-c` | Context size | `-c 2048` (lower = less RAM) |
| `-t` | CPU threads | `-t 4` |

## HTTP Server (API)
```
llama-cpp\llama-server.exe -m llama-cpp\models\google_gemma-4-E2B-it-Q4_K_M.gguf -c 2048
```
Then open: http://localhost:8080

## Exit
Type `exit` or press `Ctrl+C`
