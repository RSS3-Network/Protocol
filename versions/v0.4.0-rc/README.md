# RSS3 Protocol v0.4.0-rc

## Abstract

The right to create, disseminate and distribute information should not be in the hands of centralized governing. It is the basic right of cyber lives.

Gradually over the past two decades, contents and links have been controlled by several data superpowers, who then eats all the profits, privacy and freedom. This centralization also resulted in a terrible environment of user experience innovations: No matter how well your design and engineer your application, there is no way to compete with the data monopolies.

The world has been eager for a new way of information syndication. RSS used to be the pioneer of its time, now it’s time for us to pick up the baton and carry on.

Derived from the best out of RSS, RSS3 is an open information syndication protocol that aims to support efficient and decentralized information distribution in Web3.

This document defines the aggregation format and communication of information for cryptographically based decentralized accounts.

## Status of This Document

This version is a beta version, although this protocol is well established in theory, it still needs to be tested in practice, so it is not guaranteed to be compatible with subsequent versions, but breaking updates will be kept to a minimum.

## Dependencies

- [RFC 3986 - Uniform Resource Identifier (URI): Generic Syntax](https://datatracker.ietf.org/doc/html/rfc3986): The protocol uses a large number of RFC 3986 Uniform Resource Identifiers to identify things in RSS3.
- [RFC 3339 - Date and Time on the Internet: Timestamps](https://datatracker.ietf.org/doc/html/rfc3339): All times appearing in the protocol use the RFC 3339 standard.
- [RFC 6838 - Media Type Specifications and Registration Procedures](https://datatracker.ietf.org/doc/html/rfc6838): The value of the item.attachment.mime_type field in the protocol uses the RFC 6838 standard.
- [JSON Schema: A Media Type for Describing JSON Documents](https://datatracker.ietf.org/doc/html/draft-bhutton-json-schema-00): The protocol provides the user with a series of JSON Schema to do format validation.

## Main Concepts

### File

The implementing program returns data and the user submits data in the form of RSS3-compliant JSON files. There are two types of files, Index File and their attached List File, which you can get an overview of by browsing through the [Use Cases](#use-cases).

The mine_type of RSS3 file is `application/rss3+json`, it is recommended to include `content-type: application/rss3+json; charset=utf-8` in the Response Headers of RSS3 file.

#### File Base

Each file has some basic properties.

```ts
type FileBase = {
    version: 'v0.4.0';
    identifier: InstanceURI | CustomItemListURI | AggregatedItemListURI | CustomLinkListURI | AggregatedLinkListURI | BacklinkListURI;
    date_created: string;
    date_updated: string;
} & (SignedBase | UnsignedBase);
```

##### `version`

Version of the protocol, the current version is `v0.4.0`.

##### `identifier`

The URI of the current file, which should also contain the query if there is one.

##### `date_created` and `date_updated`

The creation time and update time of the file, in the format RFC 3339.

##### SignedBase and UnsignedBase

See [Authentication](#authentication).

#### Index File

The Index file is the main entry point for the instance and holds general information about the instance, including the details of [profile](#profile) and URIs of the [links](#link) or [items](#item) list, etc.

```ts
type IndexFile = FileBase & {
    profile?: Profile;
    links: LinksSet;
    items: ItemsSet;
}
```

##### `profile` and `links` and `items`

- [Profile](#profile)
- [Link](#link)
- [Item](#item)

#### List File

The list file is used to store the list data, including various item lists, link lists.

| Type | Signed | URI | List Element |
| --- | --- | --- | --- |
| Custom Item List | true | `CustomItemListURI` | `Item` |
| Aggregated Item List | false | `AggregatedItemListURI` | `Item` |
| Custom Link List | true | `CustomLinkListURI` | `InstanceURI` or `ItemURI` |
| Aggregated Link List | false | `AggregatedLinkListURI` | `InstanceURI` or `ItemURI` |
| Backlinks List | false | `BacklinkListURI` | `InstanceURI` or `ItemURI` |

```ts
type ListFile<URIType, ElementType> = FileBase & {
    identifier: URIType;
    identifier_next?: URIType;
    list?: ElementType[];
}

// for items
type CustomItemList = SignedBase & ListBase<CustomItemListURI, Item>;
type AggregatedItemList = UnsignedBase & ListBase<AggregatedItemListURI, Item>;

// for links
type CustomLinkList = SignedBase & ListBase<CustomLinkListURI, InstanceURI | ItemURI>;
type AggregatedLinkList = UnsignedBase & ListBase<AggregatedLinkListURI, InstanceURI | ItemURI>;
type BacklinksList = UnsignedBase & ListBase<BacklinkListURI, InstanceURI | ItemURI>;
```

##### `list`

List element, depending on the type of list file, may be item, link, backlink, etc.

##### `identifier_next`

The URI used to identify the next page. If not present, the current page is the last.

For example:

```json
{
    "identifier":      "rss3://account:0xtest@evm/list/notes/1",
    "identifier_next": "rss3://account:0xtest@evm/list/notes/0"
}
{
    "identifier":      "rss3://account:0xtest@evm/list/notes?limit=5",
    "identifier_next": "rss3://account:0xtest@evm/list/notes?limit=5&last_time=2022-01-01T00:00:00Z"
}
```

### Account

In order to remain open and compatible, the protocol does not create a new account system, but is compatible with existing account systems of other platforms, including accounts of cryptography-based decentralized and centralized platforms.

The account may appear in two places, 1) the instance account in the instance URI, which represents the owner and signer of the file and can only be of a decentralized platform; 2) the `account` field in the `profile` field, which represents other accounts belonging to the instance. 

An account consists of two pieces of information: the account ID and the platform to which the account belongs.

```xsl
Account = <identity>@<account_platform>
```

- `identity` is the unique account ID within the platform;
- `account_platform` is defined by [RSS3 Improvement Proposals: Registered account platforms](./improvement-proposals/registered-account-platforms.md).

For example,

- An EVM account can be represented as `0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@evm`.

- A Twitter account can be represented as `DIYgod@twitter`.

### Instance

An instance is an RSS3 interactive object, an RSS3 presence unit that contains an RSS3 Index file and its attached list files.

```xsl
Instance = <prefix>:<identity>@<platform>
```

- `prefix` is one constant of `account`, `asset`, `note` and `external`;
- `platform` is the platform to which the instance belongs. The platform of account is defined by [RSS3 Improvement Proposals: Registered account platforms](./improvement-proposals/registered-account-platforms.md), the platform of item is defined by [RSS3 Improvement Proposals: Registered items](./improvement-proposals/registered-items.md);
- `identity` is the unique ID of the instance on this platform.

#### Account Instance

An Account Instance is an instance created with an account, which may be automatically generated when registering or added with a user signature when changing the profile.

```xsl
AccountInstance = account:<identity>@<account_platform>
```

For example,

- `account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@evm`
- `account:DIYgod@twitter`

#### Item Instance

An Item Instance is an automatically generated Instance for Item, they can be used for links, such as scenarios where an NFT asset is displayed and commented on in an NFT marketplace.

```xsl
ItemInstance = {asset|note}:<unique_id>@<item_platform>
```

For example,

- `asset:ethereum-0xacbe98efe2d4d103e221e04c76d7c55db15c8e89-5@evm`

#### External Instance

An External Instance is an automatically generated Instance for external address that can be used for linked objects. For example, if users follow an RSS address, they can see updates of that RSS address.

```xsl
ExternalInstance = external:<authority>@<scheme>
```

For example,

- an instance of an RSS address `https://diygod.me/atom.xml` is `external:diygod.me%2Fatom.xml@https`

### Identifier

The protocol uses a number of Uniform Resource Identifiers (URIs) that conform to the [RFC 3986](https://datatracker.ietf.org/doc/html/rfc3986) standard to identify things in RSS3, such as instance identifiers, item identifiers, and list identifiers. The RSS3 URI can be used by users to access the items it represents or as the target of a link.

#### Scheme

The scheme is `rss3`. I.e. RSS3 URI starts with `rss3://`.

#### Authority

The protocol uses [Instance](#instance) as an authority.

#### URI

The below illustrates the component of each URI.

##### Instance URI

```xsl
InstanceURI = rss3://<Instance>
```

E.g.

- Account Instance URI

    ```text
    rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@evm
    ```

- Asset Instance URI

    ```text
    rss3://asset:0xb9619cf4f875cdf0e3ce48b28a1c725bc4f6c0fb+1024@ethereum
    ```

- Note Instance URI

    ```text
    rss3://note:5591079b-1f5b-4ae9-8209-51b18f0d3be0@twitter
    ```

##### Item URI

> Please refer to [Item](#item) for more about Item.

An `ItemURI` is:

```xsl
ItemURI = rss3://<Instance>/{notes|assets}/<item_uuid>
```

E.g.,

- A Note Item URI of an Instance:

    ```text
    rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@evm/notes/5591079b-1f5b-4ae9-8209-51b18f0d3be0
    ```

- A standalone Note Item URI:

  ```text
  rss3://note:5591079b-1f5b-4ae9-8209-51b18f0d3be0@evm
  ```

##### Item List URI

```xsl
CustomItemListURI     = rss3://<Instance>/list/{notes|assets}/<page_index>
AggregatedItemListURI = rss3://<Instance>/list/{notes|assets}[?<query_string>]
```

If `page_index` is present, the list is a custom item list. It is used for pagination. The starting index `page_index` is `0`.

If `page_index` is not present, the list is a aggregated item list, which may include custom items and auto items indexed from other platforms.

> Please refer to [Item](#item) to know more.

Available queries:

| Key | Usage |
| --- | --- |
| limit | Used for pagination, limiting the count of the returning items. There should be a maximum and minimal value for this when implementing. |
| last_time | Used for pagination. An RFC 3339 time. If avaiable, returning only items before this time. |
| link_type | If available, returning only the corresponding link type of items. |
| filter_tags | If available, returning only the corresponding tags of items (judging from their `tags` attributes). Multiple values is separated by commas. |
| filter_auto | If true, returning only items with `auto` fields set to true. If false, the opposite. If not available, no filter on this effect will be applied. |
| filter_platforms | If available, returning only items with `metadata.platform` fields containing the corresponding values. Multiple values is separated by commas. |
| filter_mime_types | If available, returning only items with `attachments.mime_type` fields containing the corresponding values. Multiple values is separated by commas. |

E.g.,

- The custom note list in the second list page:

    ```text
    rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@evm/list/notes/1
    ```

- The list of the first 5 notes (including custom and auto):

    ```text
    rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@evm/list/notes?limit=5
    ```

- The note list from the instance's following instances:

    ```text
    rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@evm/list/notes?link_type=following
    ```

##### Link List URI

```xsl
CustomLinkListURI     = rss3://<Instance>/list/links/<link_type>/<page_index>
AggregatedLinkListURI = rss3://<Instance>/list/links/<link_type>[?<query_string>]
```

- link_type is defined by [RSS3 Improvement Proposals: Registered link types](./improvement-proposals/registered-link-types.md).

Available queries:

| Key | Usage |
| --- | --- |
| limit | Used for pagination, limiting the count of the returning items. There should be a maximum and minimal value for this when implementing. |
| last_instance | Used for pagination. If available, returning the instances after this instance. |
| instance | If available, returning only the list containing this instance. If available but no list satisfies, returning null. |

E.g.

- The following link list in the second list page:

    ```text
    rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@evm/list/links/following/1
    ```

- The following link list of the first 5 instances:

    ```text
    rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@evm/list/links/following?limit=5
    ```

- Query if an instance is followed by another instance:

    ```text
    rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@evm/list/links/following?instance=0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944
    ```

##### Backlink List URI

```xsl
BacklinkListURI = rss3://<Instance>/list/backlinks[?<query_string>]
```

Available queries:

| Key | Usage |
| --- | --- |
| type | Returning only backlinks of this type. |
| limit | Used for pagination, limiting the count of the returning items. There should be a maximum and minimal value for this when implementing. |
| last_instance | Used for pagination. If available, returning the instances after this instance. |
| instance | If available, returning only the list containing this instance. If available but no list satisfies, returning null. |

E.g.

- The following list of the first 5 instances:

    ```text
    rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@evm/list/backlinks?type=following&limit=5
    ```

- Query if an instance is following another instance:

    ```text
    rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@evm/list/backlinks?type=following&instance=0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944
    ```

- A note’s comments:

    ```text
    rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@evm/notes/5591079b-1f5b-4ae9-8209-51b18f0d3be0/list/backlinks/comment
    ```

### Item

Item is an action or item that is automatically or passively generated by an instance. The protocol cannot predict what types of content there will be, so the protocol strives to define it more generically and unrestricted. It may be a blog post, an NFT, or a commodity, a game activity, etc. The content of a user's custom item is not restricted. The content of an automatically indexed item is restricted in [RSS3 Improvement Proposals: Registered items](./improvement-proposals/registered-items.md).

#### Item Overall

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

##### `items.assets`

`assets` are the items owned by instances, which can also be extended and interpreted as any fixed display content according to different usage scenarios, such as an NFT, a game achievement, a physical figure, a commodity for sale, etc.

##### `items.notes`

`notes` are the actions or events generated by the instance, which can also be extended and interpreted as any stream content according to different usage scenarios, such as writing a blog post, getting a NFT dynamic, writing a forum post, posting a reply to other items, etc.

##### `items.x.identifier_custom`

`identifier_custom` records the URI of the custom item list on the last page, and the list element is the item submitted by the user himself.

When there is only one page of content, the value of `identifier_custom` is `rss3://<Instance>/list/{notes|assets}/0`, until the content exceeds the file size limit specified by the implementation program, then the new item is recorded in a new file whose URI is `rss3://<Instance>/list/{notes|assets}/1`, and changes the `identifier_custom` field to `rss3://<Instance>/list/{notes|assets}/1`.

##### `items.x.identifier`

`identifier` is the URI of the automatically aggregated item list, which contains not only the custom items submitted by the user, but also the automatically indexed items, sorted by `date_created`, the newest at the top. It supports some queries.

##### `items.x.filters`

`filters` are used to filter the aggregated results returned by `identifier`. See [Filter](#filter) for details.

#### Item Details

```ts
type Item = {
    identifier: ItemURI;
    date_created: string;
    date_updated: string;

    auto?: true;
    identifier_instance?: InstanceURI;

    links: LinksSet;

    tags?: (AutoAssetType | AutoNoteType | string)[];
    authors: InstanceURI[];
    title?: string;
    summary?: string;
    attachments?: Attachment[];

    metadata?: {
        proof: string;
        platform: ItemPlatform;
        from?: string;
        to?: string;
        id: string;
    };
};
```

##### `item.date_created`

The time when the action or item was generated, in the format of [RFC 3339](https://datatracker.ietf.org/doc/html/rfc3339), such as the time when the article was published, the time when the NFT was mint, the time when the product was put on the shelf, the time when the NFT was obtained (in the note, it indicates the time when the action was generated), etc.

##### `item.date_updated`

The time of an action or item change, in the format of [RFC 3339](https://datatracker.ietf.org/doc/html/rfc3339), such as article modification time, acquisition time of NFT (in the asset, indicating the time of the item change), etc.

##### `item.auto`

If true, it means this is an automatically indexer-generated item rather than an action or item submitted by the user himself.

##### `item.identifier` and `item.identifier_instance`

`identifier` is the address of an item in its current instance. See [Item URI](#item-uri).

`identifier_instance` is the address of the item as a standalone instance. See [Instance URI](#instance-uri).

That's right. The same item can be accessed through two different URIs. If you want to comment on this item belonging to its instance, like saying "your NFT is so beautiful", then you should use `identifier`(, the possible application scenarios are personal homepage, etc.); if you just want to comment on the item itself, like saying "this NFT is so beautiful" , that has nothing to do with which instance this item belongs to, then you should use `identifier_instance`(, the possible application scenarios include NFT market, etc).

##### `item.links`

See [Link](#link).

##### `item.tags`

`tags` is an array of strings. Similar to the concept of tags commonly used in personal blogs, you can add multiple tags to an article; the automatically indexed item will also have tags, indicating the type of the item, and the specific value is limited in [RSS3 Improvement Proposals: Registered items](./improvement-proposals/registered-items.md).

##### `item.authors`

`authors` is an array of InstanceURIs, indicating the authors who produced this item, such as the author of the article, the seller of the product, etc. It can be omitted if it is the current instance address.

##### `item.title` and `item.summary`

The content of a `summary` cannot be too long, and the implementation program should set a maximum length.

If it is a short content, then it is likely to only have a `summary` without a `title`, such as a Tweet from Twitter.

If it is a long article, its word count exceeds the size limit, then its `summary` should only be a summary or truncation of the article content, and the complete content should be placed in `attachments`.

##### `item.attachments`

`attachments` records the attachments of this item, such as images of the article, etc. If it is a long article, it may also contain the full text of the article.

It's an array of attachment. Each element's structure is:

```ts
type Attachment = {
    type?: string;
    content?: string;
    address?: URI;
    mime_type: string;
    size_in_bytes?: number;
}
```

###### `item.attachments[i].type`

The type of attachment, indicating the function or classification of this attachment, such as thumbnail, detailed description, etc.

This value can be any string.

###### `item.attachments[i].content` and `item.attachments[i].address`

`content` is the actual content of the attachment, such as the full body of the article or the base64 string of an image. The content of this field may be very long, but the implementation program should also limit the maximum length of the content to avoid affecting the storage efficiency of the entire network. Content that exceeds the maximum length limit should be placed in the address field using third-party storage.

`address` is the URI of this attachment pointing to a third-party address, such as a markdown file address or an image address.

`content` and `address` are mutually exclusive, one attachment can only have one and only one of them.

###### `item.attachments[i].mime_type`

This records the media type of this attachment. The format must conform to the RFC 6838 standard, such as `image/png`, `text/markdown`, etc. This is an important but easily overlooked field from an application presentation point of view, so the protocol specifies it as a required field.

###### `item.attachments[i].size_in_bytes`

This records the size of this attachment in bytes. It is useful for displaying large files such as video and audio. It is also a field that is easily overlooked. The protocol recommends that the existence and accuracy of this field be ensured as much as possible.

##### `item.metadata`

This records metadata for automatically indexed items, with specific values defined in [RSS3 Improvement Proposals: Registered items](./improvement-proposals/registered-items.md).

###### `item.metadata.proof`

This records the credentials for indexing this item, such as transaction hash and the address of a centralized platform.

###### `item.metadata.platform`

This records the source platform of this item, such as `ethereum`, `twitter`, etc.

###### `item.metadata.from`

This is for a note that indicates an action. This records a content before this change.

For exmaple, if it is an NFT transferring action, then this field records the account that initiated this transfer.

###### `item.metadata.to`

This is for a note that indicates an action. This records a content after this change.

###### `item.metadata.id`

The unique ID of this item on the platform it belongs to, such as `<token_address>-<token_id>` of an NFT.

### Link

This describes the relationship between two instances or items in RSS3.

#### Link Overall

Link exists in two places, Instance and Item, both of which have a `links` field. In the content:

```ts
interface LinksSet {
    identifiers?: {
        type: LinkType;
        identifier_custom: CustomLinkListURI;
        identifier: AggregatedLinkListURI;
    }[];
    identifier_back: BacklinkListURI;
    filters?: Filters;
}
```

##### `links.identifiers.type`

The type of relationship, such as the following relationship of Instance, the comment relationship of Item, etc. The specific value is restricted in [RSS3 Improvement Proposals: Registered link types](./improvement-proposals/registered-link-types.md).

##### `links.identifiers.identifier_custom`

This records the URI of the custom link list on the last page, and the content of the list is the URI submitted by the user himself

When there is only one page of content, the value of `identifier_custom` is `rss3://<Instance>/list/link/0`, until the content exceeds the file size limit specified by the implementation program, then the new link is recorded in a new file whose URI is `rss3://<Instance>/list/link/1`, and changes the `identifier_custom` field to `rss3://<Instance>/list/link/1`.

##### `links.identifiers.identifier`

This is the URI of the automatically aggregated link list, which supports some queries.

##### `links.identifier_back`

This records the reverse relationship of this link. For example, if A records a following relationship to B, then the `identifier_back` of B will automatically record a reverse-following (i.e., followed-by) relationship of A.

##### `links.filters`

This is used to filter the aggregated results returned by `identifier_back`. See [Filter](#filter) for details.

#### Link Details

```ts
type Link = InstanceURI | ItemURI;
```

A link is represented by an RSS3 URI, which can be an Instance URI or an Item URI, which means that the user can follow an RSS3 account, an external address such as traditional RSS feed, or an RSS3 asset or an RSS3 Example comments.

### Filter

Both `item.x` and `links` have the `filters` field, which is used to filter the automatically indexed items and backlinks to meet the needs of the user's selective display. The implementation program must selectively return data according to the `Filter` configuration.

`items` is a filter for `tags` and `metadata.platforms`, and `backlinks` is a filter for `list`.

```ts
type Filters = {
    blocklist?: string[];
    allowlist?: string[];
}
```

The list elements of `blocklist` and `allowlist` are regular expressions.

#### `filters.blocklist`

Prevent items or backlinks containing fields in this list from being returned, e.g. `blocklist: ["twi.*er"]`, then all tags and items that satisfy `twi.*ter` in `tags` and `metadata.platforms` will not be returned by AggregatedItemListURI.

#### `filters.allowlist`

Only items or backlinks that contain fields in this list are allowed to be returned. If there is an allowlist, the blocklist will be invalid. For example, `allowlist: ["twi.*er"]`, then only items that satisfy `twi.*er` in `tags` and `metadata.platforms` will be returned by AggregatedItemListURI.

### Profile

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

#### `profile.name`

The name of the instance, such as the user's screen name, the asset's title.

#### `profile.avatars`

Instance icons, such as the user's avatar and asset images, can be set multiple at the same time, and applications should generally choose the first to display.

#### `profile.bio`

Textual introduction to the instance.

#### `profile.attachments`

When used for Item Instance, same as [item.attachments](#item-attachments).

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

#### `profile.accounts`

This is the other [accounts](#account) used to record instance bindings, including accounts of cryptography-based decentralized and centralized platforms.

```ts
type Accounts = {
    identifier: AccountInstanceURI;
    signature?: string;
}[];
```

##### `profile.accounts[i].identifier`

The URI of the account. If it is a decentralized account based on cryptography, use `profile.accounts[i].signature` to verify ownership. If it is a centralized account that cannot be signed, the address or name (Refer to [RSS3 Improvement Proposals: Registered name services](./improvement-proposals/registered-name-services.md)) of the main account must be placed somewhere on the platform to verify, as specified by [RSS3 Improvement Proposals: Registered account platforms](./improvement-proposals/registered-account-platforms.md).

#### `profile.accounts[i].signature`

This is used to verify the ownership of the bound account, signed by the bound account instead of the main account.

```ts
profile.accounts[i].signature = sign(`[RSS3] I am adding account ${profile.accounts[i].identifier} to my RSS3 Instance ${InstanceURI}`);
```

#### `profile.tags` and `profile.metadata`

For Item Instance, same as [item.tags](#item-tags) and [item.metadata](#item-metadata).

### Authentication

This set of verification mechanisms is used to verify the legitimacy of files, including the process of implementation programs to verify the legality of files submitted by users, verifying the legality of files when synchronizing files between nodes in a decentralized implementation, and verifying the legality of files returned by the implementation program on the client side.

#### SignedBase and UnsignedBase

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
- The unsigned file uses the `UnsignedBase` type to save the data automatically generated by the implementation program. The client needs to verify it according to the relevant signed file or `metadata.proof` field. Unsigned files include the Index files of Item External Instance, the Index files of External Instance, automatically aggregated item/link list files, and reverse relation list files.

#### `signature`

This is located in the root path of a signed file, signed by Instance's private key. The signature message is the file's JSON string sorted by key alphabet. The signature algorithm may vary depending on the platform. Which algorithm to use is defined in [RSS3 Improvement Proposals: Registered account platforms](./improvement-proposals/registered-account-platforms.md).

When verifying the signature and calculating the signed message, note that the existing `signature` field must be removed first.

```ts
signatrue = sign(`[RSS3] I am confirming the results of changes to my file ${identifier}: ${SortedStringify(file)}`);
```

For example, a file like:

```json
{
    "version": "v0.4.0",
    "identifier": "rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@evm",
    "signatrue": "This should not be included",

    "items": {
        "notes": 1,
        "assets": 2
    }
}
```

Its signature is: `[RSS3] I am confirming the results of changes to my file rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@evm: {"items":{"assets":2,"notes":1},"version":"v0.4.0"}`

#### `agents`

::: danger
This is a feature that may reduce security significantly. The protocol will remove it or make significant changes in future versions depending on actual usage.
:::

It is located in the root path of a signed file. This is a function similar to remember me in Web2. You can use the signature of the main account to authorize a locally randomly generated proxy signature account. When modifying the file, use the proxy account for signature authorization to Reduce the number of signatures of the main account and reduce the cost of use.

This also means that if the private key of the proxy account is leaked or the application chooses to do evil, the file will lose its security completely. End users should reauthorize this feature with full trust in the application.

The encryption algorithm uses Ed25519.

##### `agents[i].pubkey`

The base64 of the public key of the proxy account, generated by the client.

##### `agents[i].signature`

The base64 of the private key of the proxy account. The signed message is the same as the `signature`.

##### `agents[i].authorization`

The authorized signature of the main account to the proxy account.

```ts
agents.signatrue = sign(`[RSS3] I am well aware that this APP (name: ${app}) can use the following agent instead of me (${InstanceURI}) to modify my files and I would like to authorize this agent (${pubkey})`);
```

##### `agents[i].app`

The application name used to distinguish different proxy accounts.

##### `agents[i].date_expired`

The expiration time of the proxy account, the implementation program should limit the maximum value. After expiration, the proxy account should be deleted.

#### `controller`

Reserved field, used to define the control of the file, not used for now.

The current plan is to use a contract to control the controller of the file in the future, for scenarios such as forums that require multiple people to modify the same file together.

## Use Cases

### Index File Demo

URI `rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@evm`

```json
{
    "version": "v0.4.0",
    "identifier": "rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@evm",
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
                "identifier": "rss3://account:0x8768515270aA67C624d3EA3B98CA464672C50183@evm",
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
                "identifier_custom": "rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@evm/list/links/following/1",
                "identifier": "rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@evm/list/links/following"
            },
        ],
        "identifier_back": "rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@evm/list/backlinks",
        "filters": {
            "blocklist": [
                "0x8768515270aA67C624d3EA3B98CA464672C50183"
            ]
        }
    },

    "items": {
        "notes": {
            "identifier_custom": "rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@evm/list/notes/0",
            "identifier": "rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@evm/list/notes",
            "filters": {
                "blocklist": [
                    "Twitter"
                ]
            }
        },
        "assets": {
            "identifier_custom": "rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@evm/list/assets/0",
            "identifier": "rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@evm/list/assets",
            "filters": {
                "allowlist": [
                    "Polygon"
                ]
            }
        }
    }
}
```

### Link List File Demo

URI `rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@evm/list/links/following/1`

```json
{
    "version": "v0.4.0",
    "identifier": "rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@evm/list/links/following/1",
    "identifier_next": "rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@evm/list/links/following/0",
    "date_created": "2021-08-17T14:36:00.676Z",
    "date_updated": "2022-02-10T22:50:53.132Z",

    "signature": "0x5b2387a7e1b2ceb1a1b0c177294ca480ec1f43a21ad627476951b0c69baece500bde043d6f3a8ff1a8e248e3216517316b397806f6a6e721df50ed43479d65651c",

    "list": [
        "rss3://account:0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045@evm",
        "rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@evm/note/D52DCF9F-7FF0-400A-9562-66C87DB3A866",
        "rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@evm/asset/1B599C2B-4153-4DFC-8909-25AE1D51E801",
        "rss3://note:tweet-1473342342765678605@twitter",
        "rss3://asset:ethereum-0xacbe98efe2d4d103e221e04c76d7c55db15c8e89-5@evm",
        "rss3://external:diygod.me%2Fatom.xml@https"
    ]
}
```

### Asset List File Demo

URI `rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@evm/list/assets/0`

```json
{
    "version": "v0.4.0",
    "identifier": "rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@evm/list/assets/0",
    "date_created": "2021-08-17T14:36:00.676Z",
    "date_updated": "2022-02-10T22:50:53.132Z",

    "signature": "0x5b2387a7e1b2ceb1a1b0c177294ca480ec1f43a21ad627476951b0c69baece500bde043d6f3a8ff1a8e248e3216517316b397806f6a6e721df50ed43479d65651c",

    "list": [
        {
            "identifier": "rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@evm/asset/D52DCF9F-7FF0-400A-9562-66C87DB3A866",
            "date_created": "2021-08-17T14:36:00.676Z",
            "date_updated": "2022-02-10T22:50:53.132Z",

            "links": {
                "identifier_back": "rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@evm/asset/D52DCF9F-7FF0-400A-9562-66C87DB3A866/list/backlinks"
            },
        
            "tags": [
                "Garage Kit"
            ],
            "authors": [
                "rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@evm"
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

### Note List File Demo

URI `rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@evm/list/notes/0`

```json
{
    "version": "v0.4.0",
    "identifier": "rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@evm/list/notes/0",
    "date_created": "2021-08-17T14:36:00.676Z",
    "date_updated": "2022-02-10T22:50:53.132Z",

    "signature": "0x5b2387a7e1b2ceb1a1b0c177294ca480ec1f43a21ad627476951b0c69baece500bde043d6f3a8ff1a8e248e3216517316b397806f6a6e721df50ed43479d65651c",

    "list": [
        {
            "identifier": "rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@evm/note/D52DCF9F-7FF0-400A-9562-66C87DB3A866",
            "date_created": "2021-08-17T14:36:00.676Z",
            "date_updated": "2022-02-10T22:50:53.132Z",

            "links": {
                "identifiers": [
                    {
                        "type": "comment",
                        "identifier_custom": "rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@evm/note/D52DCF9F-7FF0-400A-9562-66C87DB3A866/list/links/comment/0",
                        "identifier": "rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@evm/note/D52DCF9F-7FF0-400A-9562-66C87DB3A866/list/links/comment"
                    },
                ],
                "identifier_back": "rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@evm/note/D52DCF9F-7FF0-400A-9562-66C87DB3A866/list/backlinks",
                "filters": {
                    "blocklist": [
                        "0x8768515270aA67C624d3EA3B98CA464672C50183"
                    ]
                }
            },

            "authors": [
                "rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@evm",
                "rss3://account:0x09D9719d01f48304993b35c5b5c813DdCD622362@evm"
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
