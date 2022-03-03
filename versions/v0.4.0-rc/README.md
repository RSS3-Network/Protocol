# RSS3 Protocol v0.4.0-rc

## 1. Abstract

The right to create, disseminate and distribute information should not be in the hands of centralized governing. It is the basic right of cyber lives.

Gradually over the past two decades, several data superpowers have controlled contents and links to create a toxic centralized atmosphere, where privacy and freedom are sacrificed for profits. This atmosphere further hinders innovations: No matter how well you design and engineer your application, there is no way to compete with the data monopolies.

The world has been eager for a new way of information syndication. RSS used to be the pioneer of its time, now it’s time for us to pick up the baton and carry on.

Derived from the best out of RSS, RSS3 is an open information syndication protocol that aims to support efficient and decentralized information distribution in Web3.

This document defines the aggregation format and communication of information for cryptographically based decentralized accounts.

## 2. Status of This Document

This version is a beta version, although this protocol is well established in theory, it still needs to be tested in practice, so it is not guaranteed to be compatible with subsequent versions, but breaking updates will be kept to a minimum.

## 3. Dependencies

- [RFC 3986 - Uniform Resource Identifier (URI): Generic Syntax](https://datatracker.ietf.org/doc/html/rfc3986): The protocol uses a large number of RFC 3986 Uniform Resource Identifiers to identify things in RSS3.
- [RFC 3339 - Date and Time on the Internet: Timestamps](https://datatracker.ietf.org/doc/html/rfc3339): All times appearing in the protocol use the RFC 3339 standard.
- [RFC 6838 - Media Type Specifications and Registration Procedures](https://datatracker.ietf.org/doc/html/rfc6838): The value of the item.attachment.mime_type field in the protocol uses the RFC 6838 standard.
- [RFC 4122 - A Universally Unique IDentifier (UUID) URN Namespace](https://datatracker.ietf.org/doc/html/rfc4122): UUID is used to uniquely identify items.
- [JSON Schema: A Media Type for Describing JSON Documents](https://datatracker.ietf.org/doc/html/draft-bhutton-json-schema-00): The protocol provides the user with a series of JSON Schema to do format validation.

## 4. Main Concepts

### 4.1. File

The implementing program returns data and the user submits data in the form of RSS3-compliant JSON files. There are two types of files, Index File and their attached List File, of which you can get an overview by browsing through the [Use Cases](#_6-use-cases).

The mine_type of RSS3 file is `application/rss3+json`, it is recommended to include `content-type: application/rss3+json; charset=utf-8` in the Response Headers of RSS3 file.

#### 4.1.1. File Base

Each file has some basic properties.

```ts
type FileBase = {
    version: 'v0.4.0';
    identifier: InstanceURI | CustomItemListURI | AggregatedItemListURI | CustomLinkListURI | AggregatedLinkListURI | BacklinkListURI;
    date_created: string;
    date_updated: string;
} & (SignedBase | UnsignedBase);
```

##### 4.1.1.1. `version`

Version of the protocol, the current is `v0.4.0`.

##### 4.1.1.2. `identifier`

The URI of the current file, which should also contain the query if there is one.

##### 4.1.1.3. `date_created` and `date_updated`

The creation time and update time of the file, in the format RFC 3339.

##### 4.1.1.4. SignedBase and UnsignedBase

See [Authentication](#_4-8-authentication).

#### 4.1.2. Index File

The Index file is the main entry point for the instance and holds general information about the instance, including the details of [profile](#_4-7-profile) and URIs of the [links](#_4-6-link) or [items](#_4-5-item) list, etc.

```ts
type IndexFile = FileBase & {
    profile?: Profile;
    links: LinksSet;
    items: ItemsSet;
}
```

##### 4.1.2.1. `profile` and `links` and `items`

- [Profile](#_4-7-profile)
- [Link](#_4-6-link)
- [Item](#_4-5-item)

#### 4.1.3. List File

The list file is used to store the list data, including various item lists and link lists.

| Type | Signed | URI | List Element |
| --- | --- | --- | --- |
| Custom Item List | true | `CustomItemListURI` | `Item` |
| Aggregated Item List | false | `AggregatedItemListURI` | `Item` |
| Custom Link List | true | `CustomLinkListURI` | `InstanceURI` or `ItemURI` |
| Aggregated Link List | false | `AggregatedLinkListURI` | `InstanceURI` or `ItemURI` |
| Backlink List | false | `BacklinkListURI` | `InstanceURI` or `ItemURI` |

```ts
type ListFile<URIType, ElementType> = FileBase & {
    identifier: URIType;
    identifier_next?: URIType;

    total: number;
    list?: ElementType[];
}

// for items
type CustomItemList = SignedBase & ListBase<CustomItemListURI, Item>;
type AggregatedItemList = UnsignedBase & ListBase<AggregatedItemListURI, Item>;

// for links
type CustomLinkList = SignedBase & ListBase<CustomLinkListURI, InstanceURI | ItemURI>;
type AggregatedLinkList = UnsignedBase & ListBase<AggregatedLinkListURI, InstanceURI | ItemURI>;
type BacklinkList = UnsignedBase & ListBase<BacklinkListURI, InstanceURI | ItemURI>;
```

##### 4.1.3.1. `list`

List element, depending on the type of the list file, may be item, link, backlink, etc.

##### 4.1.3.2. `identifier_next`

The URI used to identify the next page. If not specified, the current page is the last one by default.

For example:

```json
{
    "identifier":      "rss3://account:0xtest@ethereum/list/notes/1",
    "identifier_next": "rss3://account:0xtest@ethereum/list/notes/0"
}
{
    "identifier":      "rss3://account:0xtest@ethereum/list/notes?limit=5",
    "identifier_next": "rss3://account:0xtest@ethereum/list/notes?limit=5&last_time=2022-01-01T00:00:00Z"
}
```

##### 4.1.3.3. `total`

Total number of elements in this page and its next pages.

### 4.2. Account

In order to remain open and compatible, the protocol does not create a new account system. Instead, it is compatible with existing account systems of other platforms, including accounts of cryptography-based decentralized and centralized platforms.

There are two types of accounts

- Main Account: the account in the instance URI, which represents the owner and signer of the file and can only be of a decentralized platform.

- Connected Accounts: accounts in the `profile.account` field, which represents other accounts belonging to the instance.

An account consists of two pieces of information: the account ID and the platform to which the account belongs.

```xsl
Account = <identity>@<account_platform>
```

- `identity` is the unique account ID within the platform;
- `account_platform` is defined by [RIP-1: Registered Account Platforms](./RIPs/RIP-1.md).

For example,

- An EVM account can be represented as `0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@ethereum`.

- A Twitter account can be represented as `DIYgod@twitter`.

### 4.3. Instance

An instance is an RSS3 interactive object, an RSS3 presence unit that contains an RSS3 Index file and its attached list files.

```xsl
Instance = <prefix>:<identity>@<platform>
```

- `prefix` is one constant of `account`, `asset`, `note`;
- `platform` is the platform to which the instance belongs. The platform of account is defined by [RIP-1: Registered Account Platforms](./RIPs/RIP-1.md), and the platform of item is defined by [RIP-3: Registered Item Networks](./RIPs/RIP-3.md) and [RIP-4: Registered Indexed Items](./RIPs/RIP-4.md);
- `identity` is the unique ID of the instance on this platform.

#### 4.3.1. Account Instance

An Account Instance is an instance created with an account, which may be automatically generated on registration or added with a user signature when changing the profile.

```xsl
AccountInstance = account:<identity>@<account_platform>
```

For example,

- `account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@ethereum`
- `account:DIYgod@twitter`

#### 4.3.2. Item Instance

An Item Instance is an automatically generated Instance for Item. They can be used for links in many scenarios, such as where an NFT asset is displayed and commented on in an NFT marketplace.

```xsl
ItemInstance = {asset|note}:<metadata_proof_or_uuid>@<item_network>
```

For example,

- `asset:0xacbe98efe2d4d103e221e04c76d7c55db15c8e89-5@ethereum_mainnet`

### 4.4. Identifier

The protocol uses a number of Uniform Resource Identifiers (URIs) that conform to the [RFC 3986](https://datatracker.ietf.org/doc/html/rfc3986) standard to identify things in RSS3, such as instance identifiers, item identifiers, and list identifiers. The RSS3 URI can be used by users to access the items it represents or as the target of a link.

#### 4.4.1. Scheme

The scheme is `rss3`. I.e. RSS3 URI starts with `rss3://`.

#### 4.4.2. Authority

The protocol uses [Instance](#_4-3-instance) as an authority.

#### 4.4.3. URI

The below illustrates the component of each URI.

##### 4.4.3.1. Instance URI

```xsl
InstanceURI = rss3://<Instance>
```

E.g.

- Account Instance URI

    ```text
    rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@ethereum
    ```

- Asset Instance URI

    ```text
    rss3://asset:0xb9619cf4f875cdf0e3ce48b28a1c725bc4f6c0fb-1024@ethereum_mainnet
    ```

- Note Instance URI

    ```text
    rss3://note:https%3A%2F%2Ftwitter.com%2FDIYgod%2Fstatus%2F1483972580616949762@twitter
    ```

##### 4.4.3.2. Item URI

> Please refer to [Item](#_4-5-item) for more about Item.

An `ItemURI` is:

```xsl
ItemURI = rss3://<Instance>/{notes|assets}/<item_uuid>
```

E.g.,

- A Note Item URI of an Instance:

    ```text
    rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@ethereum/notes/5591079b-1f5b-4ae9-8209-51b18f0d3be0
    ```

##### 4.4.3.3. Item List URI

```xsl
CustomItemListURI     = rss3://<Instance>/list/{notes|assets}/<page_index>
AggregatedItemListURI = rss3://<Instance>/list/{notes|assets}[?<query_string>]
```

If `page_index` exists, then the list is a custom item list and uses it for pagination. The starting index `page_index` is `0`.

If `page_index` does not exist, then the list is an aggregated item list, which may include custom items and auto items indexed from other platforms.

> Please refer to [Item](#_4-5-item) to know more.

Available queries:

| Key | Usage |
| --- | --- |
| limit | Used for pagination, limiting the count of the returning items. There should be a maximum and minimal value when implementing. |
| last_time | Used for pagination. An RFC 3339 time. If specified, returning only items before this time. |
| link_type | If specified, returning only the corresponding link type of items. |
| filter_tags | If specified, returning only items of the corresponding tags (filtered using the `tags` attribute of items). Multiple values are separated by commas. |
| filter_auto | If true, returning only items with `auto` field set to true. If false, the opposite. If not available, no filter on this effect will be applied. |
| filter_network | If specified, returning only items with `metadata.network` field in the filter list. Multiple values are separated by commas. |
| filter_mime_types | If specified, returning only items with `attachments.mime_type` field containing the corresponding values. Multiple values are separated by commas. |

E.g.,

- The custom note list in the second list page:

    ```text
    rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@ethereum/list/notes/1
    ```

- The list of the first 5 notes (including custom and auto):

    ```text
    rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@ethereum/list/notes?limit=5
    ```

- The note list from the instance's following instances:

    ```text
    rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@ethereum/list/notes?link_type=following
    ```

##### 4.4.3.4. Link List URI

```xsl
CustomLinkListURI     = rss3://<Instance>/list/links/<link_type>/<page_index>
AggregatedLinkListURI = rss3://<Instance>/list/links/<link_type>[?<query_string>]
```

`link_type` is defined by [RIP-5: Registered Link Types](./RIPs/RIP-5.md).

Available queries:

| Key | Usage |
| --- | --- |
| limit | Used for pagination, limiting the count of the returning items. There should be a maximum and minimal value when implementing. |
| last_instance | Used for pagination. If specified, returning the instances after this instance. |
| instance | If specified, returning only the list containing this instance. If specified but no list satisfies, returning null. |

E.g.

- The following link list in the second list page:

    ```text
    rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@ethereum/list/links/following/1
    ```

- The following link list of the first 5 instances:

    ```text
    rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@ethereum/list/links/following?limit=5
    ```

- Query if an instance is followed by another instance:

    ```text
    rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@ethereum/list/links/following?instance=0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944
    ```

##### 4.4.3.5. Backlink List URI

```xsl
BacklinkListURI = rss3://<Instance>/list/backlinks[?<query_string>]
```

Available queries:

| Key | Usage |
| --- | --- |
| type | Returning only backlinks of this type. |
| limit | Used for pagination, limiting the count of the returning items. There should be a maximum and minimal value when implementing. |
| last_instance | Used for pagination. If specified, returning the instances after this instance. |
| instance | If specified, returning only the list containing this instance. If specified but no list satisfies, returning null. |

E.g.

- The following list of the first 5 instances:

    ```text
    rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@ethereum/list/backlinks?type=following&limit=5
    ```

- Query if an instance is following another instance:

    ```text
    rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@ethereum/list/backlinks?type=following&instance=0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944
    ```

- A note’s comments:

    ```text
    rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@ethereum/notes/5591079b-1f5b-4ae9-8209-51b18f0d3be0/list/backlinks/comment
    ```

### 4.5. Item

Item is an action or good that is automatically or passively generated by an instance. The protocol cannot predict what types of content there will be, so the protocol strives to define it more generically and unrestricted. It may be a blog post, an NFT, or a commodity, a game activity, etc. The content of a user's custom item is not restricted. The content of an automatically indexed item is restricted in [RIP-4: Registered Indexed Items](./RIPs/RIP-4.md).

#### 4.5.1. Item Overall

The structure of Items could be seen in an index file:

```ts
type ItemsSet = {
    notes: {
        identifier_custom?: CustomItemListURI;
        identifier: AggregatedItemListURI;
        filters?: Filters;
    };
    assets: {
        identifier_custom?: CustomItemListURI;
        identifier: AggregatedItemListURI;
        filters?: Filters;
    };
};
```

##### 4.5.1.1. `items.assets`

`assets` are the items owned by instances, which can also be extended and interpreted as any fixed display content according to different usage scenarios, such as an NFT, a game achievement, a physical figure, a commodity for sale, etc.

##### 4.5.1.2. `items.notes`

`notes` are the actions or events generated by the instance, which can also be extended and interpreted as any stream content according to different usage scenarios, such as writing a blog post, getting a NFT dynamic, writing a forum post, posting a reply to other items, etc.

##### 4.5.1.3. `items.x.identifier_custom`

`identifier_custom` records the URI of the custom item list on the last page, and the list element is the item submitted by the user himself.

When there is only one page of content, the value of `identifier_custom` is `rss3://<Instance>/list/{notes|assets}/0` till the content exceeds the file size limit specified by the implementation program. Then the new item is recorded in a new file whose URI is `rss3://<Instance>/list/{notes|assets}/1`, and the `identifier_custom` field is changed to `rss3://<Instance>/list/{notes|assets}/1`.

##### 4.5.1.4. `items.x.identifier`

`identifier` is the URI of the automatically aggregated item list, which contains not only the custom items submitted by the user but also the automatically indexed items, sorted by `date_created`, the newest at the top. It supports some queries.

##### 4.5.1.5. `items.x.filters`

`filters` are used to filter the automatically indexed items returned by `identifier` to meet the needs of the user's selective display.

It filters on `item.tags` and `item.metadata.network`.

```ts
type Filters = {
    blocklist?: string[];
    allowlist?: string[];
}
```

###### 4.5.1.5.1. `items.x.filters.blocklist`

Prevent items or backlinks containing fields in this list from being returned, e.g. `blocklist: ["twitter"]`, in which case, items with `item.tags` and `item.metadata.network` value of `twitter` will not be returned by AggregatedItemListURI.

###### 4.5.1.5.2. `items.x.filters.allowlist`

Only items or backlinks that contain fields in this list are allowed to be returned. If there is an allowlist, the blocklist will be invalid. For example, if `allowlist: ["twitter"]`, then only items with `item.tags` and `item.metadata.network` value of `twitter` will be returned by AggregatedItemListURI.

#### 4.5.2. Item Details

```ts
type Item = {
    identifier: ItemURI;
    date_created: string;
    date_updated: string;

    auto?: true;
    identifier_instance?: InstanceURI;

    links: LinksSet;

    tags?: (AutoAssetType | AutoNoteType | string)[];
    authors: Account[];
    title?: string;
    summary?: string;
    attachments?: Attachment[];

    metadata?: {
        network: NetworkName;
        proof: string;

        [key: string]?: any;
    };
};
```

##### 4.5.2.1. `item.date_created`

The time when the action or item was generated, in the format of [RFC 3339](https://datatracker.ietf.org/doc/html/rfc3339), such as the time when the article was published, the time when the NFT was mint, the time when the product was put on the shelf, the time when the NFT was obtained (in the note, it indicates the time when the action was generated), etc.

##### 4.5.2.2. `item.date_updated`

The time of an action or item change, in the format of [RFC 3339](https://datatracker.ietf.org/doc/html/rfc3339), such as article modification time, acquisition time of NFT (in the asset, indicating the time of the item change), etc.

##### 4.5.2.3. `item.auto`

If true, it means this is an automatically indexer-generated item rather than an action or item submitted by the user himself.

##### 4.5.2.4. `item.identifier` and `item.identifier_instance`

`identifier` is the address of an item in its current instance. See [Item URI](#_4-4-3-2-item-uri).

`identifier_instance` is the address of the item as a standalone instance. See [Instance URI](#_4-4-3-1-instance-uri).

That's right. The same item can be accessed through two different URIs. If you want to comment on this item belonging to its instance, like saying "your NFT is so beautiful", then you should use `identifier`(, the possible application scenarios are personal homepage, etc.); if you just want to comment on the item itself, like saying "this NFT is so beautiful" , that has nothing to do with which instance this item belongs to, then you should use `identifier_instance`(, the possible application scenarios include NFT market, etc).

##### 4.5.2.5. `item.links`

See [Link](#_4-6-link).

##### 4.5.2.6. `item.tags`

`tags` is an array of strings. Similar to the concept of tags commonly used in personal blogs, you can add multiple tags to an article; the automatically indexed item will also have tags, indicating the type of the item, and the specific value is limited in [RIP-4: Registered Indexed Items](./RIPs/RIP-4.md).

##### 4.5.2.7. `item.authors`

`authors` is an array of Accounts, indicating the accounts who have produced this item, such as the author of the article, the seller of the product, etc. It can be omitted if it is the current instance address.

If the item is an indexed item and the author is a Connected Account, it will additionally contain the Main Account.

##### 4.5.2.8. `item.title` and `item.summary`

The content of a `summary` cannot be too long, and the implementation program should set a maximum length.

If it is a short content, then it is likely to only have a `summary` without a `title`, such as a Tweet from Twitter.

If it is a long article and its word count exceeds the size limit, then its `summary` should only be a summary or truncation of the article, and the complete content should be placed in `attachments`.

##### 4.5.2.9. `item.attachments`

`attachments` records the attachments of this item, such as images of the article, etc. If it is a long article, it may also contain the full text of the article.

It is an array of attachment. Each element's structure is:

```ts
type Attachment = {
    type?: string;
    content?: string;
    address?: URI;
    mime_type: string;
    size_in_bytes?: number;
}
```

###### 4.5.2.9.1. `item.attachments[i].type`

The type of attachment, indicating the function or classification of this attachment, such as thumbnail, detailed description, etc.

This value can be any string.

###### 4.5.2.9.2. `item.attachments[i].content` and `item.attachments[i].address`

`content` is the actual content of the attachment, such as the full body of the article or the base64 string of an image. The content of this field may be very long, but the implementation program should also be limited to the maximum length of the content to avoid affecting the storage efficiency of the entire network. Content that exceeds the maximum length limit should be placed in the address field using third-party storage.

`address` is the URI of this attachment pointing to a third-party address, such as a markdown file address or an image address.

`content` and `address` are mutually exclusive, one attachment can only have one and only one of them.

###### 4.5.2.9.3. `item.attachments[i].mime_type`

This records the media type of this attachment. The format must conform to the RFC 6838 standard, such as `image/png`, `text/markdown`, etc. This is an important but easily overlooked field from an application presentation point of view, so the protocol specifies it as a required field.

###### 4.5.2.9.4. `item.attachments[i].size_in_bytes`

This records the size of this attachment in bytes. It is useful for displaying large files such as videos and audios. It is also a field that is easily overlooked. The protocol recommends that the existence and accuracy of this field be ensured as much as possible.

##### 4.5.2.10. `item.metadata`

This records metadata for automatically indexed items, with specific values defined in [RIP-4: Registered Indexed Items](./RIPs/RIP-4.md).

###### 4.5.2.10.1. `item.metadata.network`

The network where this item is stored.

Its value is defined by [RIP-3: Registered Item Networks](./RIPs/RIP-3.md).

###### 4.5.2.10.2. `item.metadata.proof`

This records the credentials for indexing this item, such as transaction hash and the address of a centralized platform.

### 4.6. Link

This describes the relationship between two instances or items in RSS3.

#### 4.6.1. Link Overall

Link exists in two places, Instance and Item, both of which have a `links` field. In the content:

```ts
interface LinksSet {
    identifiers?: {
        type: LinkType;
        identifier_custom: CustomLinkListURI;
        identifier: AggregatedLinkListURI;
    }[];
    identifier_back: BacklinkListURI;
}
```

##### 4.6.1.1. `links.identifiers.type`

The type of relationship, such as the following relationship of Instance, the comment relationship of Item, etc. The specific value is restricted in [RIP-5: Registered Link Types](./RIPs/RIP-5.md).

##### 4.6.1.2. `links.identifiers.identifier_custom`

This records the URI of the custom link list on the last page, and the content of the list is the URI submitted by the user himself

When there is only one page of content, the value of `identifier_custom` is `rss3://<Instance>/list/link/0`, until the content exceeds the file size limit specified by the implementation program, then the new link is recorded in a new file whose URI is `rss3://<Instance>/list/link/1`, and changes the `identifier_custom` field to `rss3://<Instance>/list/link/1`.

##### 4.6.1.3. `links.identifiers.identifier`

This is the URI of the automatically aggregated link list, which supports some queries.

##### 4.6.1.4. `links.identifier_back`

This records the reverse relationship of this link. For example, if A records a following relationship to B, then the `identifier_back` of B will automatically record a reverse-following (i.e., followed-by) relationship of A.

#### 4.6.2. Link Details

```ts
type Link = {
    identifier_target: InstanceURI | ItemURI;
    type: LinkType;

    auto?: true;
    metadata?: Metadata;
};
```

##### 4.6.2.1. `link.identifier_target`

The link target is an RSS3 URI, which can be an Instance URI or an Item URI. It means that the user can follow an RSS3 account, and comments on an RSS3 asset or an RSS3 note.

##### 4.6.2.2. `link.type`

See [links.identifier_back](#_4-6-1-1-links-identifiers-type).

### 4.7. Profile

Profile is located in the `profile` field of an Index File, which records the basic information of the instance, including the name, avatar, profile, etc.

```ts
type Profile = {
    name?: string;
    avatars?: URI[];
    bio?: string;
    attachments?: Attachment[];

    accounts?: Accounts;

    tags?: (AutoAssetType | AutoNoteType | string)[];
    metadata?: Metadata;
};
```

#### 4.7.1. `profile.name`

The name of the instance, such as the user's screen name, the asset's title.

#### 4.7.2. `profile.avatars`

Instance icons, such as the user's avatar and asset images, can be set multiple at the same time, and applications should generally choose the first to display.

#### 4.7.3. `profile.bio`

Textual introduction to the instance.

#### 4.7.4. `profile.attachments`

When used for Item Instance, same as [item.attachments](#_4-5-2-9-item-attachments).

When used for Account Instance, `profile` is a very flexible and diverse information. The protocol cannot predict all requirements, so only a few of the most commonly used information are defined, and it is expected to use the `attachments` field to record the profile information that is not clearly defined, such as `websites`, `banner`.

For example:

```json
{
    "attachments": [
        {
            "type": "websites",
            "content": "https://rss3.io\nhttps://diygod.me",
            "mime_type": "text/uri-list",
        },
        {
            "type": "banner",
            "content": "ipfs://QmT1zZNHvXxdTzHesfEdvFjMPvw536Ltbup7B4ijGVib7t",
            "mime_type": "image/jpeg",
        }
    ]
}
```

#### 4.7.5. `profile.accounts`

This is the other [accounts](#_4-2-account) used to record instance bindings, including accounts of cryptography-based decentralized and centralized platforms.

```ts
type Accounts = {
    identifier: AccountInstanceURI;
    signature?: string;
}[];
```

##### 4.7.5.1. `profile.accounts[i].identifier`

The URI of the account. If it is a decentralized account based on cryptography, use `profile.accounts[i].signature` to verify ownership. If it is a centralized account that cannot be signed, the user must put the address or name (Refer to [RIP-2: Registered Name Services](./RIPs/RIP-2.md)) of the Main Account into some location in the platform's account configuration to verify ownership, as specified by [RIP-1: Registered Account Platforms](./RIPs/RIP-1.md).

#### 4.7.6. `profile.accounts[i].signature`

This is used to verify the ownership of the bound account, signed by the bound account instead of the Main Account.

```ts
profile.accounts[i].signature = sign(`[RSS3] I am adding account ${profile.accounts[i].identifier} to my RSS3 Instance ${InstanceURI}`);
```

#### 4.7.7. `profile.tags` and `profile.metadata`

For Item Instance, same as [item.tags](#_4-5-2-6-item-tags) and [item.metadata](#_4-5-2-10-item-metadata).

### 4.8. Authentication

This set of verification mechanisms is used to verify the legitimacy of files. It covers the verification of user-submitted files by implementation programs, the synchronizing files between nodes in a decentralized implementation, and returned files by the implementation program on the client side.

#### 4.8.1. SignedBase and UnsignedBase

The files are divided into signed files and unsigned files. Each file contains a field of either `SignedBase` or `UnsignedBase`, which is used to record the authentication method of the file.

```ts
type SignedBase = {
    signature: string;
    agents?: {
        pubkey: string;
        signature: string;
        authorization: string;
        app: string;
        date_expired: string;
    }[];
    controller?: string;
}

type UnsignedBase = {
    auto: true;
}
```

- The signed file uses the `SignedBase` type, which is used to save the data of the user's signature authentication. The client can perform signature verification. Signed files include the Index files of Account Instance and the custom item/link list files.
- The unsigned file uses the `UnsignedBase` type to save the data automatically generated by the implementation program. The client needs to verify it according to the relevant signed file or `metadata.proof` field. Unsigned files include automatically aggregated item/link list files, and reverse relation list files.

#### 4.8.2. `signature`

This is located in the root path of a signed file, signed by Instance's private key. The signature message is the file's JSON string sorted by key alphabetically. The signature algorithm may vary depending on the platform. Which algorithm to use is defined in [RIP-1: Registered Account Platforms](./RIPs/RIP-1.md).

When verifying the signature and calculating the signed message, note that the existing `signature` field must be removed first.

```ts
signatrue = sign(`[RSS3] I am confirming the results of changes to my file ${identifier}: ${SortedStringify(file)}`);
```

For example, a file like:

```json
{
    "version": "v0.4.0",
    "identifier": "rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@ethereum",
    "signatrue": "This should not be included",

    "items": {
        "notes": 1,
        "assets": 2
    }
}
```

Its signature is: `[RSS3] I am confirming the results of changes to my file rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@ethereum: {"items":{"assets":2,"notes":1},"version":"v0.4.0"}`

#### 4.8.3. `agents`

::: danger
This is a feature that may reduce security significantly. The protocol will remove it or make significant changes in future versions depending on actual usage.
:::

It is located in the root path of a signed file. This is a function similar to remember me in Web2. You can use the signature of the Main Account to authorize a randomly local-generated proxy signature account. When modifying the file, use the proxy account for signature authorization to reduce the number of signatures of the Main Account and the cost of use.

This also means that if the private key of the proxy account is leaked or the application chooses to do evil, the file will lose its security completely. End users will have to reauthorize this feature with full trust in the application.

The encryption algorithm uses Ed25519.

##### 4.8.3.1. `agents[i].pubkey`

The base64 of the public key of the proxy account, generated by the client.

##### 4.8.3.2. `agents[i].signature`

The base64 of the private key of the proxy account. The signed message is the same as the `signature`.

##### 4.8.3.3. `agents[i].authorization`

The authorized signature of the Main Account to the proxy account.

```ts
agents.signatrue = sign(`[RSS3] I am well aware that this APP (name: ${app}) can use the following agent instead of me (${InstanceURI}) to modify my files and I would like to authorize this agent (${pubkey})`);
```

##### 4.8.3.4. `agents[i].app`

The application name used to distinguish different proxy accounts.

##### 4.8.3.5. `agents[i].date_expired`

The expiration time of the proxy account, the implementation program should limit the maximum value. After expiration, the proxy account should be deleted.

#### 4.8.4. `controller`

Reserved field, used to define the control of the file, not used for now.

The current plan is to use a contract to control the controller of the file for scenarios, such as forums that require multiple people to modify the same file together.

## 5. Validation

### 5.1. TypeScript

```ts
// Instance
type AccountInstance = string;
type ItemInstance = string;

type Instance = AccountInstance | ItemInstance;

// URI
type InstanceURI = string;

type ItemURI = string;

type CustomItemListURI = string;
type AggregatedItemListURI = string;

type CustomLinkListURI = string;
type AggregatedLinkListURI = string;
type BacklinkListURI = string;

type URI = string;

// Common attributes for each files
interface Base {
    version: 'v0.4.0';
    identifier: InstanceURI | CustomItemListURI | AggregatedItemListURI | CustomLinkListURI | AggregatedLinkListURI | BacklinkListURI;
    date_created: string;
    date_updated: string;
}

interface SignedBase extends Base {
    signature: string;
    agents?: {
        pubkey: string;
        signature: string;
        authorization: string;
        app: string;
        date_expired: string;
    }[];
    controller?: string;
}

interface UnsignedBase extends Base {
    auto: true;
}

// Base types
interface Attachment {
    type?: string;
    content?: string;
    address?: URI;
    mime_type: string;
    size_in_bytes?: number;
}

interface Metadata {
    network?: NetworkName;
    proof: string;

    [key: string]: any;
}

interface Filters {
    blocklist?: string[];
    allowlist?: string[];
}

interface LinksSet {
    identifiers?: {
        type: LinkType;
        identifier_custom: CustomLinkListURI;
        identifier: AggregatedLinkListURI;
    }[];
    identifier_back: BacklinkListURI;
}

// RSS3 index files, main entrance for a instance
interface Index extends SignedBase, UnsignedBase {
    identifier: InstanceURI;

    profile?: {
        name?: string;
        avatars?: URI[];
        bio?: string;
        attachments?: Attachment[];

        accounts?: {
            identifier: InstanceURI;
            signature?: string;
        }[];

        tags?: (AutoAssetType | AutoNoteType | string)[];
        metadata?: Metadata;
    };

    links: LinksSet;

    items: {
        notes: {
            identifier_custom?: CustomItemListURI;
            identifier: AggregatedItemListURI;
            filters?: Filters;
        };
        assets: {
            identifier_custom?: CustomItemListURI;
            identifier: AggregatedItemListURI;
            filters?: Filters;
        };
    };
}

// items
type Item = {
    identifier: ItemURI;
    date_created: string;
    date_updated: string;

    auto?: true;
    identifier_instance?: InstanceURI;

    links: LinksSet;

    tags?: (AutoAssetType | AutoNoteType | string)[];
    authors: Account[];
    title?: string;
    summary?: string;
    attachments?: Attachment[];

    metadata?: Metadata;
};

type Link = {
    identifier_target: InstanceURI | ItemURI;
    type: LinkType;

    auto?: true;
    metadata?: Metadata;
};

// RSS3 list files
type ListBase<URIType, ElementType> = {
    identifier: URIType;
    identifier_next?: URIType;

    total: number;
    list?: ElementType[];
}

type CustomItemList = SignedBase & ListBase<CustomItemListURI, Item>;
type AggregatedItemList = UnsignedBase & ListBase<AggregatedItemListURI, Item>;

type CustomLinkList = SignedBase & ListBase<CustomLinkListURI, Link>;
type AggregatedLinkList = UnsignedBase & ListBase<AggregatedLinkListURI, Link>;
type BacklinkList = UnsignedBase & ListBase<BacklinkListURI, Link>;
```

### 5.2. JSON Schema

TODO

## 6. Use Cases

### 6.1. Index File Demo

URI `rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@ethereum`

```json
{
    "version": "v0.4.0",
    "identifier": "rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@ethereum",
    "date_created": "2021-08-17T14:36:00.676Z",
    "date_updated": "2022-02-10T22:50:53.132Z",

    "signature": "0x85d66b17df7343364c6b89ede6ff15279505abfdfa7b8c70590d53a3a10db97a504b8a2536a7dcc12527af42f28f643a258d48f395b8fa5917336f06d8972be41c",
    "agents": [
        {
            "pubkey": "rrqJ2xn7oUd4wGW8VbsZk9XeacYMap4/jprIA5b35ns=",
            "signature": "PObUwUA+BEStJZJoY4xBsOkQujsRAZ4yULZIu0orDHCID2ezI5/eD8EskIK+RFNvSCp9tKTSYqurEFa2egW6Dg==",
            "authorization": "",
            "app": "Revery",
            "date_expired": "2023-02-10T22:50:53.132Z"
        }
    ],

    "profile": {
        "name": "DIYgod",
        "avatars": [
            "ipfs://QmT1zZNHvXxdTzHesfEdvFjMPvw536Ltbup7B4ijGVib7t"
        ],
        "bio": "Cofounder of RSS3.",
        "attachments": [
            {
                "type": "websites",
                "content": "https://rss3.io\nhttps://diygod.me",
                "mime_type": "text/uri-list",
            },
            {
                "type": "banner",
                "content": "ipfs://QmT1zZNHvXxdTzHesfEdvFjMPvw536Ltbup7B4ijGVib7t",
                "mime_type": "image/jpeg",
            }
        ],

        "accounts": [
            {
                "identifier": "rss3://account:0x8768515270aA67C624d3EA3B98CA464672C50183@ethereum",
                "signature": "0x4828da56a162b9504dca6009864a90ed0ca3e56256d8458af451874ad7dd9cb26be4f399a56a8b69a881297ba6b6434a7f2f4a4f3557890d1efa8490769187be1b"
            },
            {
                "identifier": "rss3://account:DIYgod@twitter"
            }
        ]
    },

    "links": {
        "identifiers": [
            {
                "type": "following",
                "identifier_custom": "rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@ethereum/list/links/following/1",
                "identifier": "rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@ethereum/list/links/following"
            },
        ],
        "identifier_back": "rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@ethereum/list/backlinks"
    },

    "items": {
        "notes": {
            "identifier_custom": "rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@ethereum/list/notes/0",
            "identifier": "rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@ethereum/list/notes",
            "filters": {
                "blocklist": [
                    "Twitter"
                ]
            }
        },
        "assets": {
            "identifier_custom": "rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@ethereum/list/assets/0",
            "identifier": "rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@ethereum/list/assets",
            "filters": {
                "allowlist": [
                    "Polygon"
                ]
            }
        }
    }
}
```

### 6.2. Link List File Demo

URI `rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@ethereum/list/links/following/1`

```json
{
    "version": "v0.4.0",
    "identifier": "rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@ethereum/list/links/following/1",
    "identifier_next": "rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@ethereum/list/links/following/0",
    "date_created": "2021-08-17T14:36:00.676Z",
    "date_updated": "2022-02-10T22:50:53.132Z",

    "signature": "0x5b2387a7e1b2ceb1a1b0c177294ca480ec1f43a21ad627476951b0c69baece500bde043d6f3a8ff1a8e248e3216517316b397806f6a6e721df50ed43479d65651c",

    "total": 8,
    "list": [
        {
            "identifier_target": "rss3://account:0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045@ethereum",
            "type": "following"
        },
        {
            "identifier_target": "rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@ethereum/asset/1B599C2B-4153-4DFC-8909-25AE1D51E801",
            "type": "following"
        },
        {
            "identifier_target": "rss3://note:https%3A%2F%2Ftwitter.com%2FDIYgod%2Fstatus%2F1483972580616949762@twitter",
            "type": "following"
        },
        {
            "identifier_target": "rss3://asset:0xacbe98efe2d4d103e221e04c76d7c55db15c8e89-5@ethereum_mainnet",
            "type": "following"
        }
    ]
}
```

### 6.3. Asset List File Demo

URI `rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@ethereum/list/assets/0`

```json
{
    "version": "v0.4.0",
    "identifier": "rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@ethereum/list/assets/0",
    "date_created": "2021-08-17T14:36:00.676Z",
    "date_updated": "2022-02-10T22:50:53.132Z",

    "signature": "0x5b2387a7e1b2ceb1a1b0c177294ca480ec1f43a21ad627476951b0c69baece500bde043d6f3a8ff1a8e248e3216517316b397806f6a6e721df50ed43479d65651c",

    "total": 1,
    "list": [
        {
            "identifier": "rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@ethereum/asset/D52DCF9F-7FF0-400A-9562-66C87DB3A866",
            "date_created": "2021-08-17T14:36:00.676Z",
            "date_updated": "2022-02-10T22:50:53.132Z",

            "links": {
                "identifier_back": "rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@ethereum/asset/D52DCF9F-7FF0-400A-9562-66C87DB3A866/list/backlinks"
            },
        
            "tags": [
                "Garage Kit"
            ],
            "authors": [
                "0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@ethereum"
            ],
            "summary": "My Garage Kit - 2233",
            "attachments": [
                {
                    "address": "ipfs://QmT1zZNHvXxdTzHesfEdvFjMPvw536Ltbup7B4ijGVib7t",
                    "mime_type": "image/jpg",
                    "size_in_bytes": 1024
                }
            ]
        }
    ]
}
```

### 6.4. Note List File Demo

URI `rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@ethereum/list/notes/0`

```json
{
    "version": "v0.4.0",
    "identifier": "rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@ethereum/list/notes/0",
    "date_created": "2021-08-17T14:36:00.676Z",
    "date_updated": "2022-02-10T22:50:53.132Z",

    "signature": "0x5b2387a7e1b2ceb1a1b0c177294ca480ec1f43a21ad627476951b0c69baece500bde043d6f3a8ff1a8e248e3216517316b397806f6a6e721df50ed43479d65651c",

    "total": 1,
    "list": [
        {
            "identifier": "rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@ethereum/note/D52DCF9F-7FF0-400A-9562-66C87DB3A866",
            "date_created": "2021-08-17T14:36:00.676Z",
            "date_updated": "2022-02-10T22:50:53.132Z",

            "links": {
                "identifiers": [
                    {
                        "type": "comment",
                        "identifier_custom": "rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@ethereum/note/D52DCF9F-7FF0-400A-9562-66C87DB3A866/list/links/comment/0",
                        "identifier": "rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@ethereum/note/D52DCF9F-7FF0-400A-9562-66C87DB3A866/list/links/comment"
                    },
                ],
                "identifier_back": "rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@ethereum/note/D52DCF9F-7FF0-400A-9562-66C87DB3A866/list/backlinks"
            },

            "authors": [
                "0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@ethereum",
                "0x09D9719d01f48304993b35c5b5c813DdCD622362@ethereum"
            ],
            "title": "RSS3 is born",
            "summary": "RSS3 is a next-generation feed standard that aims to support efficient and decentralized information distribution.",
            "attachments": [
                {
                    "content": "# I include a markdown",
                    "mime_type": "text/markdown"
                }, {
                    "address": "ipfs://QmT1zZNHvXxdTzHesfEdvFjMPvw536Ltbup7B4ijGVib7t",
                    "mime_type": "image/jpg",
                    "size_in_bytes": 1024
                }
            ]
        }
    ]
}
```
