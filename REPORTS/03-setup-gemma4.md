# Phase 3: Setup Gemma 4

## Date
2025-04-06

## Objective
Download and configure Gemma 4 model appropriate for 8GB RAM system.

## System Detection

### RAM
- **Total RAM: 8GB** (8589934592 bytes)
- Single RAM module detected

### Disk Space
- **Before download:** ~15.6GB free
- **After download:** ~12GB free

## Model Selection

### Available Gemma 4 Variants
- Gemma 4 E2B (2B parameters) - **Selected for 8GB RAM**
- Gemma 4 E4B (4B parameters) - Too large for 8GB
- Gemma 4 26B-A4B - Too large
- Gemma 4 31B - Too large

### Quantization Choice: Q4_K_M
- **File:** `google_gemma-4-E2B-it-Q4_K_M.gguf`
- **Size:** 3.46GB
- **Quality:** Good balance of quality and size
- **RAM Usage:** ~4GB total (model + context + OS overhead)

### Why Q4_K_M?
- Fits comfortably in 8GB RAM
- Good quality for most tasks
- Leaves room for OS and other processes
- Smaller quantizations (Q2, Q3) sacrifice too much quality

## Actions Taken

### 1. Created Models Directory
- `llama-cpp\models\`

### 2. Downloaded Model
- Source: HuggingFace (bartowski/google_gemma-4-E2B-it-GGUF)
- URL: `https://huggingface.co/bartowski/google_gemma-4-E2B-it-GGUF/resolve/main/google_gemma-4-E2B-it-Q4_K_M.gguf`
- Size: 3,462,673,376 bytes (3.46GB)
- Download time: ~7 minutes

### 3. Verified Download
- File size confirmed: 3.46GB
- Removed invalid test file from earlier attempt

## Model Location
```
C:\dev\ai_setup_llama_cpp\llama-cpp\models\google_gemma-4-E2B-it-Q4_K_M.gguf
```

## Usage Example
```bash
llama-cpp\llama-cli.exe -m llama-cpp\models\google_gemma-4-E2B-it-Q4_K_M.gguf -p "Hello, how are you?" -n 128
```

## Next Phase
Phase 4: Create Skills & Agents
