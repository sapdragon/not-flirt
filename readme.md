# FLIRT Signatures Repository

This repository contains FLIRT (Fast Library Identification and Recognition Technology) signatures for various libraries commonly used in Windows software development. These signatures can be used for reverse engineering and binary analysis purposes.

## Contents

- `scripts/`: Contains Python scripts used to generate signatures and create configuration files.
  - `generate_signatures.py`: Script to download libraries via vcpkg and generate FLIRT signatures.
  - `create_config.py`: Script to create the `sig.cfg` configuration file ( to expand autoexec )
- `signatures/`: Contains the generated FLIRT signature files (.sig).
- `configs/`: Contains configuration files for IDA Pro.
  - `sig.cfg`: Configuration file mapping signature files to type libraries.

## Prerequisites

- Python 3.7+
- vcpkg
- IDA Pro with FLAIR tools

## Usage

### Using Pre-generated Signatures

1. Clone or download this repository:
   ```
   git clone https://github.com/sapdragon/not-flirt.git
   ```

2. Copy the contents of the `signatures/` directory to your IDA Pro signatures folder:
   - `IDA Pro\sig\pc\`

3. (OPTIONAL) To enable auto-loading of signatures:
   - Append the content of `configs/sig.cfg` from this repository to the end of `autoload.cfg`.

4. Restart IDA Pro if it's already running.

5. The new signatures will now be available for use in your IDA Pro projects.

### Generating Your Own Signatures

If you want to generate your own signatures:

1. Ensure you have the prerequisites installed (Python 3.7+, vcpkg, IDA Pro with FLAIR tools).

2. Update the paths in `scripts/generate_signatures.py` to match your vcpkg and FLAIR tools installation.

3. Run the signature generation script:
   ```
   python scripts/generate_signatures.py
   ```

4. Create the configuration file:
   ```
   python scripts/create_config.py
   ```

5. The generated signatures will be in the `signatures/` directory, and the configuration file will be in `configs/sig.cfg`.

6. Follow steps 2-5 from the "Using Pre-generated Signatures" section to use your newly generated signatures in IDA Pro.


## Included Libraries

This repository contains FLIRT signatures for the following libraries:

1. curl
2. imgui
3. boost
4. openssl
5. nlohmann-json
6. spdlog
7. rapidjson
8. protobuf
9. opencv
10. directxtk
11. glfw3
12. sdl2
13. sfml
14. asio
15. websocketpp
16. zlib
17. lz4
18. bzip2
19. sqlite3
20. poco
21. eigen
22. fftw3
23. libsodium
24. minizip
25. fmt
26. vulkan
27. libuv
28. tbb
29. cereal
30. capstone
31. detours
32. directxmesh
33. directxtex
34. mimalloc
35. xxhash
36. cpr
37. toml11
38. magic-enum
39. breakpad
40. dirent
41. minhook
42. hopscotch-map
43. tracy
44. libusb
45. libpcap
46. dxsdk-d3dx

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

