A tool to export the snapshot of an ERC20 token at the given height.

### Setup
install the `curl` command line tool

pip install requests

### Usage
python run.py <ethereum_rpc_url> <smart_contract_address> <start_height> <end_height>

### Examples
python run.py https://mainnet.infura.io 0x3883f5e181fccaf8410fa61e12b59bad963fb645 5728491 5728891

python run.py http://localhost:8545 0x3883f5e181fccaf8410fa61e12b59bad963fb645 5728491 5728991
