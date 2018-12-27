A tool to export the snapshot of an ERC20 token at the target height.

### Setup

install the `curl` command line tool

install python 2.7

pip install requests

### Usage

Use the following command to extract the balance of all the ERC20 token holders. Here `genesis_height` is the height (i.e. block number) of the genesis transaction of the ERC20smart contract. `target_height` is the height to export the snapshot. The result will be written into the file specified by `balance_file_path`.

```
python run.py <ethereum_rpc_url> <smart_contract_address> <genesis_height> <target_height> <balance_file_path>
```

### Examples

On any machine, run the following command to extract the balance of all the Theta ERC20 token holders at block height 6958428.
```
python run.py https://mainnet.infura.io 0x3883f5e181fccaf8410fa61e12b59bad963fb645 4728491 6958428 balance.json
```

On a machine with a fully-synced Geth node, run the following command to extract the balance of all the Theta ERC20 token holders at block height 6958428.

```
python run.py http://localhost:8545 0x3883f5e181fccaf8410fa61e12b59bad963fb645 4728491 6958428 balance.json
```
