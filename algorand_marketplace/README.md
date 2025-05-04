# Algorand Marketplace Smart Contract

This project contains a basic marketplace smart contract written in PyTeal for the Algorand blockchain.

## Features

- Seller can list an item (ASA) with a fixed price.
- Buyer can purchase the item by sending Algos.
- Seller confirms and completes the delivery manually.

## Usage

1. Deploy the contract with the item price and asset ID.
2. Buyer calls the `buy` method with payment.
3. Seller calls `claim` to complete the transaction.

## Requirements

- Python
- PyTeal
