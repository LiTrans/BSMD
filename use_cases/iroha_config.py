#!/usr/bin/env python3

from iroha import IrohaCrypto

# chief node
######################
chief_private_key = '054e294d86bedf9a43cf20542cade6e57addfd4294a276042be4ba83c73f8d9e'
chief_public_key = IrohaCrypto.derive_public_key(chief_private_key)
chief_name = 'chief'
# worker1 node
######################
worker1_private_key = '7a3a8efe3fbfac57af55e8d2a4b20e27b19444c4d240924dd1bd57701a5a0731'
worker1_public_key = IrohaCrypto.derive_public_key(worker1_private_key)
worker1_name = 'worker1'
# worker2 node
######################
worker2_private_key = '94ba95a4520107a8a9abc864db900b5c00660c48bbb0333edaa5ab081f52e2ed'
worker2_public_key = IrohaCrypto.derive_public_key(worker2_private_key)
worker2_name = 'worker2'
# worker3 node
######################
worker3_private_key = '8c578c774f553b99ebbaf89d9314f8ceaf6b4e93119c2550e10cf0de8ee93b51'
worker3_public_key = IrohaCrypto.derive_public_key(worker3_private_key)
worker3_name = 'worker3'
# worker4 node
######################
worker4_private_key = 'afa0c9cd046cbf7cb8998761c28a3dbfd8537de02d078657dcce25614a34b2d9'
worker4_public_key = IrohaCrypto.derive_public_key(worker4_private_key)
worker4_name = 'worker4'
# worker5 node
######################
worker5_private_key = '333611dc29d0ed8c1ed9de9eb629280f8fc745aecbed5c7b80d2c024a088a2a8'
worker5_public_key = IrohaCrypto.derive_public_key(worker5_private_key)
worker5_name = 'worker5'
# worker6 node
######################
worker6_private_key = '116737445ed840fef349d6e61bd5fe3762e153ceb4042b2045d5bb7bcc149b43'
worker6_public_key = IrohaCrypto.derive_public_key(worker6_private_key)
worker6_name = 'worker6'
# worker7 node
######################
worker7_private_key = '303db8234e576a9f158d7e909dda6b560a95520182c9bc069fdeaed330e33e15'
worker7_public_key = IrohaCrypto.derive_public_key(worker7_private_key)
worker7_name = 'worker7'
# worker8 node
######################
worker8_private_key = '3c08c360f0d69eff638c50609d11c57cd9aeaaca9f55e6808f5e008fdcd3788e'
worker8_public_key = IrohaCrypto.derive_public_key(worker8_private_key)
worker8_name = 'worker8'
# worker9 node
######################
worker9_private_key = '3587faf346d017b6e103332f681a9a109bb599ed7ee52c6441e2afe78b2fab40'
worker9_public_key = IrohaCrypto.derive_public_key(worker9_private_key)
worker9_name = 'worker9'
# To create private and public keys for nodes use
# user_p_key = IrohaCrypto.private_key()
# print('private: ', user_p_key)
# print('public: ', IrohaCrypto.derive_public_key('f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70'))
