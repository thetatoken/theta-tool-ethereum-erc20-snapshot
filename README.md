A tool to export the snapshot of an ERC20 token at the target height.

### Setup

install the `curl` command line tool

install python 2.7

pip install requests

### Usage

Use the following command to extract the balance of all the ERC20 token holders. `config_file_path` points to the config file (see examples below). `target_height` is the height to export the snapshot. The result will be written into the file specified by `balance_file_path`.

```
python run.py <config_file_path> <target_height> <balance_file_path>
```

### Examples

Here is an example of the config file `config.json`. The fields are self-explanatory. For example, `genesis_height` is the height (i.e. block number) of the block that contains the genesis transaction of the ERC20 smart contract. 
```
{
  "ethereum_rpc_url" : "http://localhost:8545",
  "smart_contract_address" : "0x3883f5e181fccaf8410fa61e12b59bad963fb645",
  "genesis_height" : 4728491,
  "expected_total_supply" : 1000000000000000000000000000
}
```

On a machine with a fully-synced Geth node, run the following command to extract the balance of all the ERC20 token holders at block height 6958428, and save the result to `./balance.json`

```
python run.py config.json 6958428 balance.json
```

