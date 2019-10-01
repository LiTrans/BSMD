.. BSMD documentation master file, created by
   sphinx-quickstart on Thu Sep 26 13:20:53 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

A multi-layered blockchain framework for smart mobility data-markets
====================================================================
Blockchain has the potential to render the transaction of information more secure and transparent. Nowadays,
transportation data are shared across multiple entities using heterogeneous mediums, from paper collected data
to smartphone. Most of this data are stored in central servers that are susceptible to hacks. In some cases shady actors
who may have access to such sources, share the mobility data with unwanted third parties. A multi-layered Blockchain
framework for Smart Mobility Data-market (BSMD) is presented for addressing the associated privacy, security,
management, and scalability challenges.

Each participant shares their encrypted data to the blockchain network and can transact information with other
participants as long as both parties agree to the transaction rules issued by the owner of the data.
Data ownership, transparency, auditability and access control are the core principles of the proposed blockchain
for smart mobility data-market. For a description of the framework read the paper_.

Prerequisite
------------
To start using the BSMD you must have at least one *Iroha* node running. *Hyperledger Iroha* is a straightforward
distributed ledger technology (DLT), inspired by Japanese Kaizen principle — eliminate excessiveness (muri).
Iroha has essential functionality for your asset, information and identity management needs, at the same time being an
efficient and trustworthy crash fault-tolerant tool for your enterprise needs [#]_. Click here_ to build and install an
Iroha network

.. toctree::
   :maxdepth: 2
   :caption: Layers:

   contract
   communication
   identification
   incentives

.. toctree::
   :maxdepth: 2
   :caption: Utils:

   utils
   administrator



.. _paper: https://arxiv.org/pdf/1906.06435.pdf
.. [#] https://github.com/hyperledger/iroha.
.. _here: https://iroha.readthedocs.io/en/latest/build/index.html#
