import os

def create_config_file():
    sig_files = [f for f in os.listdir('.') if f.endswith('.sig')]
    sig_files.sort()

    with open('sig.cfg', 'w') as config_file:
        for sig_file in sig_files:
            print("[*] Adding", sig_file)

            base_name = sig_file.rsplit('.', 1)[0]
            config_file.write(f'{base_name}\n')

    print("[+] Configuration file 'sig.cfg' has been created.")

if __name__ == "__main__":
    create_config_file()