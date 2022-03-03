# RIP-1: Registered Account Platforms

## Abstract

RIP-1 is used to describe and qualify the accounts that can be used for RSS3.

## Motivation

The RSS3 protocol does not restrict what platform accounts can be used, which creates uncertainty in implementation and use.

## Cryptography-based Decentralized Platforms

Cryptography-based decentralized platforms do not require a centralized server, but use a public signature algorithm for authentication.

The accounts of these platforms can be used for both Main Accounts and Connected Accounts.

## Centralized Platforms

Centralized platforms require centralized servers for authentication. The user must put the address or name (Refer to [RIP-2: Registered Name Services](./RIPs/RIP-2.md)) of the Main Accounts into some location in the platform's account configuration to verify ownership.

The accounts of these platforms can only be used for Connected Accounts.

## Account Platform List

| Platform ID | Platform Name | Platform Symbol | Platform Website | Cryptography-based | Example | Generation and Verification |
| -- | -- | -- | -- | -- | -- | -- |
| 1 | Ethereum | ethereum | <https://ethereum.org> | Yes | 0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@ethereum | <https://ethereum.org/en/developers/docs/accounts/> |
| 2 | Solana | solana | <https://solana.com> | Yes | 42jYG1DjDeGq8VgKtah1yR45MXU1uxThFxXukb6QBKMY@solana | <https://docs.solana.com/terminology#account> |
| 3 | Flow | flow | <https://www.onflow.org/> | Yes | 0xff2da663c7033313@flow | <https://docs.onflow.org/cadence/language/crypto/> |
| 4 | Arweave | arweave | <https://www.arweave.org/> | Yes | DMMgLkfQ4faV_igfexJn4aOJY7Drc8PkJBk_K5T3rsM@arweave | <https://docs.arweave.org/developers/server/http-api#key-format> |
| 5 | RSS | rss | <https://validator.w3.org/feed/docs/rss2.html> | No | https%3A%2F%2Fdiygod.me%2Fatom.xml@rss | title, description, generator, webMaster |
| 6 | Twitter | twitter | <https://twitter.com> | No | rss3_@twitter | Username, Name, Bio, Website, Pinned tweet |
| 7 | Misskey | misskey | <https://misskey-hub.net/> | No | Candinya@nya.one@misskey | Name, Bio, Labels, Pinned notes |
| 8 | 即刻 | jike | <https://web.okjike.com/> | No | 3EE02BC9-C5B3-4209-8750-4ED1EE0F67BB@jike | 昵称, 签名 |
| 9 | PlayStation | playstation | <https://www.playstation.com/> | No | DIYgod_@playstation | Online ID, Name, About |
| 10 | GitHub | github | <https://github.com/> | No | DIYgod@github | Name, Bio, Company, Website |
