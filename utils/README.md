# Run Iroha in one node
Is possible to run Iroha in a single node. You can use this approach If you want to do tests before 
running Iroha in four nodes
```bash
irohad --config configSingle/config.sample --genesis_block configSingle/genesis.block --keypair_name configSingle/node0
```

## Additional Commands
If you like to clean and start fresh
```bash
irohad --config configSingle/config.sample --genesis_block configSingle/genesis.block --keypair_name  configSingle/node0 --overwrite_ledger
```

# Run Iroha in four nodes
On each machine do the following:

Open the [genesis.block](genesis.block) file and update the 'address' entry to correspond the ip of each machine.
 For example, the entry:
```json
{
   "peer":{
      "address":"99.230.31.239:10001",
      "peerKey":"bddd58404d1315e0eb27902c5d7c8eb0602c16238f005773df406bc191308929"
   }
}                            
``` 
will correspond to node0. Inspect the file [node0.pub](node0.pub) and see that `peerkey` is the same key written 
in [node0.pub](node0.pub) file. Update all `peer` entries with the corresponding ip address and 'nodeN.pub' key

One each machine create the folder `config` and copy the [genesis.block](genesis.block) and the 
[config.sample](config.sample)

On each machine run (change 'node0' to make it correspond with the machine, i.e., machine 2 is node1, 
machine 3 is node2 and so on)
```bash
irohad --config config/config.sample --genesis_block config/genesis.block --keypair_name config/node0
```

## Additional Commands
If you like to clean and start fresh
```bash
irohad --config config/config.sample --genesis_block config/genesis.block --keypair_name config/node0 --overwrite_ledger
```
