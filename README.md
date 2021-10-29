<p align="center">
  <p align="center">
    <img src="https://rss3.mypinata.cloud/ipfs/QmUG6H3Z7D5P511shn7sB4CPmpjH5uZWu4m5mWX7U3Gqbu" alt="RSS3" width="300">
  </p>
</p>

> Derived from the best out of RSS, RSS3 is an open protocol designed for content and social networks in the Web 3.0 era.

## Latest draft

- [v0.1.1](https://github.com/NaturalSelectionLabs/RSS3/blob/main/versions/v0.1.1.md)

```typescript
type RSS3ID = string;
type RSS3ItemID = string;
type RSS3ItemsID = string;
type RSS3ListID = string;
type ThirdPartyAddress = string[];

// Common attributes for each files
interface RSS3Base {
    id: RSS3ID | RSS3ItemsID | RSS3ListID;
    "@version": 'rss3.io/version/v0.1.1';
    date_created: string;
    date_updated: string;
}

// Entrance, RSS3 file
interface RSS3 extends RSS3Base {
    id: RSS3ID;
    signature?: string;

    profile: {
        name?: string;
        avatar?: ThirdPartyAddress;
        bio?: string;
        tags?: string[];
        signature?: string;
    };

    items: RSS3Item[];
    items_next?: RSS3ItemsID;

    links?: {
        type: string;
        tags?: string[];
        list: RSS3ID[];
        signature?: string;
    }[];
    "@backlinks"?: {
        type: string;
        list: RSS3ListID;
    }[];

    assets?: {
        type: string;
        tags?: string[];
        content: string;
    }[];
}

// RSS3Items file
interface RSS3Items extends RSS3Base {
    id: RSS3ItemsID;
    signature?: string;

    items: RSS3Item[];
    items_next?: RSS3ItemsID;
}

// RSS3List file
interface RSS3List extends RSS3Base {
    id: RSS3ListID;

    list?: RSS3ID[] | RSS3ItemID[];
    list_next?: RSS3ListID;
}

interface RSS3Item {
    id: RSS3ItemID;
    authors?: RSS3ID[];
    title?: string;
    summary?: string;
    tags?: string[];
    date_published?: string;
    date_modified?: string;

    type?: string;
    upstream?: RSS3ItemID;

    contents?: {
        address: ThirdPartyAddress;
        mime_type: string;
        name?: string;
        tags?: string[];
        size_in_bytes?: string;
        duration_in_seconds?: string;
    }[];

    "@contexts"?: {
        type?: string;
        list?: RSS3ListID;
    }[];

    signature?: string;
}
```

## Historical drafts

- [v0.1.0](https://github.com/NaturalSelectionLabs/RSS3/blob/main/versions/v0.1.0.md)
- [v0.1.0-alpha.0](https://github.com/NaturalSelectionLabs/RSS3/blob/main/versions/v0.1.0-alpha.0.md)

## Contributing

RSS3 is a community-based project, built with an open ecosystem and creative developers, and we thank every one for the participation.

- Report irrationality or request feature in [issues](https://github.com/NaturalSelectionLabs/RSS3/issues)
- Discussion in [discussions](https://github.com/NaturalSelectionLabs/RSS3/discussions)
- Submit your [pull request](https://github.com/NaturalSelectionLabs/RSS3/pulls)

## Contact

[![Twitter][twitter-shield]][twitter-url]
[![Telegram][telegram-shield]][telegram-url]
[![Discord][discord-shield]][discord-url]

RSS3 - [@rss3_](https://twitter.com/rss3_) - contact@rss3.io

Project Link: [https://github.com/NaturalSelectionLabs/RSS3](https://github.com/NaturalSelectionLabs/RSS3)

[twitter-shield]: https://img.shields.io/twitter/follow/RSS3_?style=flat-square&logo=twitter
[twitter-url]: https://twitter.com/rss3_
[telegram-shield]: https://img.shields.io/badge/Telegram-Channel-blue?style=flat-square&logo=telegram
[telegram-url]: https://t.me/joinchat/jhhncmdayvNlMDgx
[discord-shield]: https://img.shields.io/badge/Discord-Server-blueviolet?style=flat-square&logo=discord
[discord-url]: https://bit.ly/3aSYvPA
