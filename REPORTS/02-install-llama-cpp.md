# Phase 2: Install llama.cpp

## Date
2025-04-06

## Objective
Install llama.cpp with native Windows build (no WSL) and low-RAM optimizations.

## Actions Taken

### 1. Prerequisites Check
- ✅ Git: v2.46.2 (available)
- ❌ CMake: not installed (not needed for pre-built binary)
- ❌ MSBuild: not installed (not needed for pre-built binary)
- ✅ Winget: v1.28.220 (available)

### 2. Download Pre-built Binary
- Release: b4773
- Build: `llama-b4773-bin-win-avx-x64.zip`
- URL: https://github.com/ggerganov/llama.cpp/releases/download/b4773/llama-b4773-bin-win-avx-x64.zip
- Size: ~16MB download

### 3. Installation
- Extracted to: `C:\dev\ai_setup_llama_cpp\llama-cpp\`
- Verified: `llama-cli.exe --help` works correctly
- Removed zip file to save disk space

### 4. Available Tools
- `llama-cli.exe` - Main CLI for text generation and chat
- `llama-server.exe` - HTTP server for API access
- `llama-quantize.exe` - Model quantization tool
- `llama-bench.exe` - Benchmark tool
- `llama-embedding.exe` - Embeddings
- And 50+ other utilities

### 5. Disk Space
- Binaries: ~57MB
- No WSL overhead
- No build toolchain overhead

## Notes
- Used pre-built binary to avoid installing Visual Studio Build Tools (~5GB+)
- AVX x64 build for compatibility with most modern CPUs
- Native Windows, no WSL dependency

## Next Phase
Phase 3: Setup Gemma 4 (detect RAM, select quantization, download model)
