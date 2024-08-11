import os
import subprocess
import glob
import sys
import random

def check_vcpkg(vcpkg_root):
    vcpkg_exe = os.path.join(vcpkg_root, "vcpkg.exe")
    if not os.path.exists(vcpkg_exe):
        print(f"Error: vcpkg not found at {vcpkg_exe}")
        print("Please make sure vcpkg is installed and the path is correct.")
        sys.exit(1)
    return vcpkg_exe

def install_libraries(vcpkg_exe, libraries):
    for lib in libraries:
        try:
            subprocess.run([vcpkg_exe, "install", f"{lib}:x64-windows-static"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error installing {lib}: {e}")
            print("Continuing with the next library...")

def find_lib_files(vcpkg_root):
    lib_dir = os.path.join(vcpkg_root, "installed", "x64-windows-static", "lib")
    return glob.glob(os.path.join(lib_dir, "*.lib"))

def check_flair_tools(flair_path):
    tools = ["pcf.exe", "sigmake.exe"]
    for tool in tools:
        if not os.path.exists(os.path.join(flair_path, tool)):
            print(f"Error: {tool} not found in {flair_path}")
            print("Please make sure FLAIR tools are installed and the path is correct.")
            sys.exit(1)

def parse_address(line):
    match = re.search(r'\b([0-9A-Fa-f]{2}\s){5,}', line)
    return match.group(0).strip() if match else None

def auto_resolve_collisions(exc_file):
    if not os.path.exists(exc_file):
        print(f"Warning: Expected collision file {exc_file} not found.")
        return

    with open(exc_file, 'r') as f:
        lines = f.readlines()

    resolved_lines = []
    current_collision = []
    address_set = set()

    for line in lines:
        if line.startswith(';'):
            continue
        elif line.strip() == '':
            if current_collision:
                for collision in current_collision:
                    address = parse_address(collision)
                    if address and address not in address_set:
                        resolved_lines.append(collision)
                        address_set.add(address)
                        break
                current_collision = []
            resolved_lines.append(line)
        else:
            current_collision.append(line.strip())

    if current_collision:
        for collision in current_collision:
            address = parse_address(collision)
            if address and address not in address_set:
                resolved_lines.append('+' + collision)
                address_set.add(address)
                break

    with open(exc_file, 'w') as f:
        f.writelines(line + '\n' for line in resolved_lines)

def create_signatures(lib_files, flair_path):
    for lib_file in lib_files:
        base_name = os.path.basename(lib_file)
        pat_file = f"{base_name}.pat"
        sig_file = f"{base_name}.sig"
        exc_file = f"{base_name}.exc"
        
        try:
            print(f"Creating PAT file for {base_name}...")
            subprocess.run([os.path.join(flair_path, "pcf"), lib_file, pat_file], check=True)
            
            if not os.path.exists(pat_file):
                print(f"Error: PAT file {pat_file} was not created.")
                continue

            print(f"Creating SIG file for {base_name}...")
            result = subprocess.run([os.path.join(flair_path, "sigmake"), pat_file, sig_file], capture_output=True, text=True, check=False)
            
            print(f"sigmake output for {base_name}:")
            print(result.stdout)
            
            if result.returncode != 0:
                print(f"sigmake error output for {base_name}:")
                print(result.stderr)
                
                if "COLLISIONS DETECTED" in result.stdout or os.path.exists(exc_file):
                    print(f"Collisions detected for {base_name}. Resolving automatically...")
                    auto_resolve_collisions(exc_file)
                    
                    if os.path.exists(exc_file):
                        print(f"Re-running sigmake for {base_name} with resolved collisions...")
                        result = subprocess.run([os.path.join(flair_path, "sigmake"), pat_file, sig_file], capture_output=True, text=True, check=False)
                        
                        print(f"Final sigmake output for {base_name}:")
                        print(result.stdout)
                        if result.returncode != 0:
                            print(f"Final sigmake error output for {base_name}:")
                            print(result.stderr)
                    else:
                        print(f"Warning: Expected collision file {exc_file} not found after resolution attempt.")
                else:
                    print(f"Unexpected error creating signature for {base_name}. Check the error output above.")
            
            if os.path.exists(sig_file):
                print(f"Successfully created signature for {base_name}")
                
                if not os.path.exists("signatures"):
                    os.makedirs("signatures")

                if os.path.exists(os.path.join("signatures", sig_file)):
                    os.remove(os.path.join("signatures", sig_file))

                os.rename(sig_file, os.path.join("signatures", sig_file))

            else:
                print(f"Failed to create signature for {base_name}")
            
        except subprocess.CalledProcessError as e:
            print(f"Error processing {base_name}: {e}")
        
        print("\n" + "="*50 + "\n") 

def main():
    # Configuration
    vcpkg_root = r"C:\Users\sasaz\Downloads\mylibs\vcpkg"
    flair_path = r"C:\Users\sasaz\Downloads\flair90\bin\x64win"
    
    # Check vcpkg and FLAIR tools
    vcpkg_exe = check_vcpkg(vcpkg_root)
    check_flair_tools(flair_path)
    
    # Расширенный список библиотек
    libraries = [
        "curl", "imgui", 
        "boost", "openssl", "nlohmann-json", "spdlog",
        "rapidjson", "protobuf", "opencv", "directxtk",
        "glfw3", "sdl2", "sfml", "asio", "websocketpp",
        "zlib", "lz4", "bzip2", "sqlite3", "poco",
        "eigen", "fftw3", "libsodium", "minizip", "fmt",
        "vulkan", "opencv", "libuv", "tbb", "cereal",
        "capstone", "detours", "directxmesh", "directxtex",
        "mimalloc", "xxhash", "cpr", "toml11", "magic-enum",
        "breakpad", "dirent", "minhook", "hopscotch-map",
        "tracy", "libusb", "libpcap", "dxsdk-d3dx"
    ]
    
    # Install libraries
    install_libraries(vcpkg_exe, libraries)
    
    # Find installed .lib files
    lib_files = find_lib_files(vcpkg_root)
    
    # Create signatures
    create_signatures(lib_files, flair_path)

if __name__ == "__main__":
    main()