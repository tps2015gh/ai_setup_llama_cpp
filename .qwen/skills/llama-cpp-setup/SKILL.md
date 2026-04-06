# SKILL: llama-cpp-setup

## Description
Setup and configure llama.cpp for local LLM inference on Windows (native, no WSL).

## When to Use
- User wants to install llama.cpp
- User needs to optimize for low-RAM systems (≤8GB)
- User wants native Windows performance

## Quick Reference

### Installation Path
```
C:\dev\ai_setup_llama_cpp\llama-cpp\
```

### Key Binaries
- `llama-cli.exe` - Main CLI (chat & text generation)
- `llama-server.exe` - HTTP API server
- `llama-quantize.exe` - Quantize models
- `llama-bench.exe` - Benchmark

### Models Path
```
C:\dev\ai_setup_llama_cpp\llama-cpp\models\
```

### Basic Usage

#### Chat Mode
```bash
llama-cli.exe -m models\<model>.gguf -cnv
```

#### Text Generation
```bash
llama-cli.exe -m models\<model>.gguf -p "Your prompt" -n 128
```

#### Low-RAM Optimization
```bash
llama-cli.exe -m models\<model>.gguf -cnv -c 2048 -ngl 0 --memory-f32
```

### Parameters
- `-m` : Model path
- `-cnv` : Conversation mode
- `-n` : Tokens to generate
- `-c` : Context size (default 4096, use 2048 for low RAM)
- `-ngl` : GPU layers (0 = CPU only)
- `-t` : Threads (default: auto)

### Troubleshooting
- **Out of memory**: Reduce `-c` to 1024 or 2048
- **Slow inference**: Use `-t <cores>` to match CPU cores
- **Model not found**: Verify path is absolute or relative to llama-cpp\

## Source
Installed from: https://github.com/ggerganov/llama.cpp/releases
Build: b4773, win-avx-x64
