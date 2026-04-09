import os
import subprocess
import sys

BASE_DIR = "clinical_rag"

# -----------------------------
# 1. CREATE FOLDER STRUCTURE
# -----------------------------

folders = [
    f"{BASE_DIR}/data/raw",
    f"{BASE_DIR}/data/processed",
    f"{BASE_DIR}/models",
    f"{BASE_DIR}/src/ingestion",
    f"{BASE_DIR}/src/indexing",
    f"{BASE_DIR}/src/retrieval",
    f"{BASE_DIR}/src/generation",
    f"{BASE_DIR}/src/voice",
    f"{BASE_DIR}/api",
    f"{BASE_DIR}/evaluation",
    f"{BASE_DIR}/config"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

# create __init__.py for modular imports
for folder in folders:
    if "src" in folder:
        init_file = os.path.join(folder, "__init__.py")
        open(init_file, "a").close()

print("✅ Folder structure created")

# -----------------------------
# 2. CREATE REQUIREMENTS.TXT
# -----------------------------

requirements = """faiss-cpu==1.7.4
sentence-transformers==2.7.0
torch==2.2.2
transformers==4.41.2

fastapi==0.110.0
uvicorn==0.29.0

pypdf==4.2.0
numpy==1.26.4
scikit-learn==1.4.2
tqdm==4.66.4

openai==1.30.1

gTTS==2.5.1

SpeechRecognition==3.10.0
pyaudio==0.2.14
"""

req_path = os.path.join(BASE_DIR, "requirements.txt")

with open(req_path, "w") as f:
    f.write(requirements)

print("✅ requirements.txt created")

# -----------------------------
# 3. CREATE VIRTUAL ENV
# -----------------------------

venv_path = os.path.join(BASE_DIR, "venv")

print("⚙️ Creating virtual environment...")
result = subprocess.run([sys.executable, "-m", "venv", venv_path])

if result.returncode != 0:
    print("❌ Failed to create virtual environment")
    sys.exit(1)

print("✅ Virtual environment created")

# -----------------------------
# 4. INSTALL DEPENDENCIES
# -----------------------------

if os.name == "nt":
    pip_path = os.path.join(venv_path, "Scripts", "pip")
    python_path = os.path.join(venv_path, "Scripts", "python")
else:
    pip_path = os.path.join(venv_path, "bin", "pip")
    python_path = os.path.join(venv_path, "bin", "python")

print("⬆️ Upgrading pip...")
subprocess.run([python_path, "-m", "pip", "install", "--upgrade", "pip"])

print("📦 Installing dependencies...")
install_result = subprocess.run([pip_path, "install", "-r", req_path])

if install_result.returncode != 0:
    print("❌ Dependency installation failed!")
    print("👉 Try manually installing PyAudio:")
    print("   pip install pipwin")
    print("   pipwin install pyaudio")
    sys.exit(1)

print("✅ Dependencies installed")

# -----------------------------
# 5. FINAL OUTPUT
# -----------------------------

print("\n🎯 SETUP COMPLETE!")

if os.name == "nt":
    print("\n👉 Activate environment:")
    print(f"{BASE_DIR}\\venv\\Scripts\\activate")
else:
    print("\n👉 Activate environment:")
    print(f"source {BASE_DIR}/venv/bin/activate")

print("\n👉 Verify setup:")
print("pip list")
print("python -c \"import faiss, torch, speech_recognition\"")