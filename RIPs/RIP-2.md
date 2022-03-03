# RIP-2: Registered Name Services

## Abstract

RIP-2 is used to describe and qualify name services that can be used for authentication of RSS3 Connected Accounts.

## Motivation

The RSS3 protocol does not restrict what name services can be used, which creates uncertainty in implementation and use.

## Dependencies

- [RFC 1035 - Domain names - implementation and specification](https://datatracker.ietf.org/doc/html/rfc1035)
- [RFC 1464 - Using the Domain Name System To Store Arbitrary String Attributes](https://datatracker.ietf.org/doc/html/rfc1464)

## Name Service List

| Registry | Top-level domains | Website |
| -- | -- | -- |
| Domain Name System (DNS) | <https://data.iana.org/TLD/tlds-alpha-by-domain.txt> | <https://www.iana.org/> |
| Ethereum Name Service (ENS) | .eth | <https://ens.domains/> |
| Decentralized Account Systems (DAS) | .bit | <https://da.systems/> |
| Flowns | .fn | <https://www.flowns.org/> |

### Using DNS to resolve RSS3 accounts

A TXT record (short for text record) is a type of resource record in the Domain name system (DNS) used to provide the ability to associate arbitrary text with a host or other name, such as human readable information about a server, network, data center, or other accounting information. ([TXT record - Wikipedia](https://en.wikipedia.org/wiki/TXT_record))

This proposal specifies using the TXT field of DNS to resolve accounts, with the string content conforming to the RFC 1464 standard.

TXT record name:

```text
_rns
```

TXT record value: 

```xsl
<account_platform>=<identity>[; <account_platform>=<identity>; ...]
```

For example:

```text
ethereum=0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944; solana=42jYG1DjDeGq8VgKtah1yR45MXU1uxThFxXukb6QBKMY
```
