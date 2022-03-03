---
sidebarDepth: 2
---

# RIP-4: Registered Indexed Items

## Abstract

RIP-2 is used to describe and qualify indexed assets and notes that can be used for RSS3 items.

## Motivation

The RSS3 protocol does not restrict what assets and notes can be indexed, which creates uncertainty in implementation and use.

## Dependencies

- [RIP-1: Registered Account Platforms](./RIP-1.md): as `<platform_name>`
- [RIP-3: Registered Item Networks](./RIP-3.md): as `<network_name>`

## TypeScript Validation

```ts
type Item = {
    identifier: ItemURI;
    date_created: string;
    date_updated: string;

    auto: true;
    identifier_instance?: InstanceURI;

    tags?: string[];
    authors: Account[];
    title?: string;
    summary?: string;
    attachments?: {
        type?: string;
        content?: string;
        address?: URI;
        mime_type: string;
        size_in_bytes?: number;
    }[];

    metadata?: {
        network: NetworkName;
        proof: string;

        [key: string]: any;
    };
};
```

## Indexed Note Item List

### NFT Activities

NFT activity, including NFT minting, transferring out, transferring in, and burning.

#### `tags`

```json
"tags": [
    "NFT"
]
```

#### `attachments`

```json
"attachments": [
    {
        "type": "name",
        "content": "<name>",
        "mime_type": "text/plain"
    },
    {
        "type": "description",
        "content": "<description>",
        "mime_type": "text/plain"
    },
    {
        "type": "object",
        "address": "<object_address>",
        "mime_type": "<object_mime_type>",
        "size_in_bytes": <object_size_in_bytes>
    },
    {
        "type": "preview",
        "address": "<preview_address>",
        "mime_type": "<preview_mime_type>",
        "size_in_bytes": <preview_size_in_bytes>
    },
    {
        "type": "attributes",
        "content": "{\"<attribute_key>\":\"<attribute_value>\",...}",
        "mime_type": "text/json"
    },
    {
        "type": "external_url",
        "content": "<external_url>",
        "mime_type": "text/uri-list"
    }
]
```

#### `metadata`

```ts
"metadata": {
    "network": "<network_name>",
    "proof": "<transaction_hash>",
    "from": "<transaction_from>",
    "to": "<transaction_to>",

    "token_standard": "<token_standard>",
    "token_id": "<token_id>",
    "token_symbol": "<token_symbol>",

    "collection_address": "<collection_address>",
    "collection_name": "<collection_name>",
}
```

#### Special NFTs

Some NFTs contain special tags.

##### POAP

A set of [POAP](https://poap.xyz/) NFTs centrally issued, distributed and stored data by POAP Inc, which needs to be fetched from POAP Inc's centralized servers, but due to its widespread use, we have to support it specifically.

```json
"tags": [
    "NFT",
    "POAP"
]
```

Condition: `metadata.network` === `Gnosis Mainnet` && `metadata.collection_address` === `0x22C1f6050E56d2876009903609a2cC3fEf83B415`

#### Examples

##### Minting of RSS3 Whitepaper #1800

[Chain Explorer](https://etherscan.io/nft/0xb9619cf4f875cdf0e3ce48b28a1c725bc4f6c0fb/1800)

```json
{
    "identifier": "rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@ethereum/note/D52DCF9F-7FF0-400A-9562-66C87DB3A866",
    "date_created": "2022-01-19T02:06:38.000Z",
    "date_updated": "2022-01-19T02:06:38.000Z",

    "auto": true,
    "identifier_instance": "rss3://note:0x0b97d6caf6ade4cb0ec6f483463371b97d04fb1a74f72bcc411e480572d712af@ethereum_mainnet",

    "tags": [
        "NFT"
    ],
    "authors": [
        "0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@ethereum"
    ],

    "attachments": [
        {
            "type": "name",
            "content": "RSS3 Whitepaper v1.0",
            "mime_type": "text/plain"
        },
        {
            "type": "description",
            "content": "RSS3 Whitepaper v1.0 - Commemorative & Limited Edition",
            "mime_type": "text/plain"
        },
        {
            "type": "object",
            "address": "ipfs://bafybeicij6vw6xcsgwldofnmmh3c3j4w5yiocs6l72yubpbcldxcglkvqe/rss3-whitepaper-no-1800.glb",
            "mime_type": "model/gltf-binary",
            "size_in_bytes": 3983376
        },
        {
            "type": "preview",
            "address": "ipfs://bafybeianto7koyrfwkdjymx7byjrs3hzy7ldipfxc343vra2t7pbd557sy/rss3-whitepaper-no-1800.png",
            "mime_type": "image/png",
            "size_in_bytes": 117310
        },
        {
            "type": "attributes",
            "content": "{\"Author(s)\":\"Natural Selection Labs\",\"Edition\":\"First Edition\",\"Edition Language\":\"English\",\"File Format\":\"PDF\",\"No.\":1800,\"date\":1610323200}",
            "mime_type": "text/json"
        },
        {
            "type": "external_url",
            "content": "https://rss3.io/RSS3-Whitepaper.pdf",
            "mime_type": "text/uri-list"
        }
    ],

    "metadata": {
        "network": "Ethereum Mainnet",
        "proof": "0x0b97d6caf6ade4cb0ec6f483463371b97d04fb1a74f72bcc411e480572d712af",

        "from": "0x0000000000000000000000000000000000000000",
        "to": "0xc8b960d09c0078c18dcbe7eb9ab9d816bcca8944",

        "token_standard": "ERC-721",
        "token_id": "1800",
        "token_symbol": "RWP",

        "collection_address": "0xb9619cf4f875cdf0e3ce48b28a1c725bc4f6c0fb",
        "collection_name": "RSS3 Whitepaper"
    }
}
```

##### Minting of POAP #2444192

[Chain Explorer](https://blockscout.com/xdai/mainnet/tx/0x51de22ba27f05aee163bf01983107b7ddb130d70e1cf9a0ea544392c80580020)

Its data stored by <https://api.poap.xyz/token/2444192>

```json
{
    "identifier": "rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@ethereum/note/C97402DD-87BB-4054-ADD0-39F2C3CC8B0F",
    "date_created": "2021-11-02T03:11:40.000Z",
    "date_updated": "2021-11-02T03:11:40.000Z",

    "auto": true,
    "identifier_instance": "rss3://note:0x51de22ba27f05aee163bf01983107b7ddb130d70e1cf9a0ea544392c80580020@gnosis_mainnet",

    "tags": [
        "NFT",
        "POAP"
    ],
    "authors": [
        "0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@ethereum"
    ],

    "attachments": [
        {
            "type": "name",
            "content": "RSS3 Fully Supports POAP",
            "mime_type": "text/plain"
        },
        {
            "type": "description",
            "content": "This POAP is used to commemorate the RSS3 protocol now fully supports the index of POAPs.",
            "mime_type": "text/plain"
        },
        {
            "type": "object",
            "address": "https://assets.poap.xyz/rss3-fully-support-poap-2021-logo-1635826323177.png",
            "mime_type": "image/png",
            "size_in_bytes": 1264683
        },
        {
            "type": "preview",
            "address": "https://assets.poap.xyz/rss3-fully-support-poap-2021-logo-1635826323177.png",
            "mime_type": "image/png",
            "size_in_bytes": 1264683
        },
        {
            "type": "attributes",
            "content": "{\"id\":12526,\"fancy_id\":\"rss3-fully-support-poap-2021\",\"country\":\"\",\"city\":\"\",\"year\":2021,\"start_date\":\"02-Nov-2021\",\"end_date\":\"02-Nov-2021\",\"expiry_date\":\"02-Dec-2021\"}",
            "mime_type": "text/json"
        },
        {
            "type": "external_url",
            "content": "https://rss3.bio",
            "mime_type": "text/uri-list"
        }
    ],

    "metadata": {
        "network": "Gnosis Mainnet",
        "proof": "0x51de22ba27f05aee163bf01983107b7ddb130d70e1cf9a0ea544392c80580020",

        "from": "0x0000000000000000000000000000000000000000",
        "to": "0xc8b960d09c0078c18dcbe7eb9ab9d816bcca8944",

        "token_standard": "ERC-721",
        "token_id": "2444192",
        "token_symbol": "The Proof of Attendance Protocol",

        "collection_address": "0x22C1f6050E56d2876009903609a2cC3fEf83B415",
        "collection_name": "POAP"
    }
}
```

#### References

- [Specification | Metaplex Docs](https://docs.metaplex.com/token-metadata/specification)
- [EIP-721: Non-Fungible Token Standard](https://eips.ethereum.org/EIPS/eip-721)

### Mirror Entries

Activity of a [Mirror](https://mirror.xyz/) Entry.

Mirror Entry is a kind of JSON file that uses the Ethereum account, but is stored in Arweave Mainnet by a Mirror official account.

It is worth noting that Mirror Entries can be modified by a new transaction.

#### `title`

Title of the Mirror Entry

#### `summary`

Part or all of the Mirror Entry body.

If the body is too long, then only record part of the body, followed by `...` at the end, the length is the maximum summary length set by the implementation program.

#### `tags`

```json
"tags": [
    "Mirror Entry"
]
```

#### `attachments`

```json
"attachments": [
    {
        "type": "body",
        "content": "<body>",
        "mime_type": "text/markdown"
    }
]
```

#### `metadata`

```ts
"metadata": {
    "network": "Arweave Mainnet",
    "proof": "<transaction_hash>"
}
```

#### Example

##### Entry vfTMz8HQa28GNEMfhZLbbAdYQoaY11khOUyXAzBjnX8

[Mirror Address](https://mirror.xyz/0xee8fEeb6D0c2fC02Ef41879514A75d0E791b5061/vfTMz8HQa28GNEMfhZLbbAdYQoaY11khOUyXAzBjnX8)

[Arware Transaction](https://viewblock.io/arweave/tx/9s_R8b4UfSMoP1wIJ7UGUC-fMtR68Z9cZQYplA6nj-k)

[Arware Link](https://63chy34fd5emud6xaie62qmubhzs2r5pdh24mudctfaou6he.arweave.net/9s_R8b4UfSMoP1wIJ7UGUC-fMtR68Z9cZQYplA6nj-k)

```json
{
    "identifier": "rss3://account:0xee8fEeb6D0c2fC02Ef41879514A75d0E791b5061@ethereum/note/1B599C2B-4153-4DFC-8909-25AE1D51E801",
    "date_created": "2021-08-10T05:07:22.000Z",
    "date_updated": "2021-08-10T05:07:22.000Z",

    "auto": true,
    "identifier_instance": "rss3://note:9s_R8b4UfSMoP1wIJ7UGUC-fMtR68Z9cZQYplA6nj-k@arweave_mainnet",

    "tags": [
        "Mirror Entry"
    ],
    "authors": [
        "0xee8fEeb6D0c2fC02Ef41879514A75d0E791b5061@ethereum"
    ],

    "title": "献出心脏 直到高墙倒塌",
    "summary": "> 四千多字的一篇博客居然前前后后写了一个月，倒不是没有思路，就是和自己经历相关的文字，可能会抑制不住的想要反复补充修改，而且常常写着写着会思绪飘移，开始回顾一些其他事情...总之最后终于下定决心无论如何一定要写完了！\n\n标题借用了进击的巨人里的一句经典台词，“献出心脏”。可能有点浮夸（毕竟日语嘛...），但是我想了半天，还是觉得这句话最适合我的心意，献出心脏，为自由，为平等，为Web 3....",

    "attachments": [
        {
            "type": "body",
            "content": "> 四千多字的一篇博客居然前前后后写了一个月，倒不是没有思路，就是和自己经历相关的文字，可能会抑制不住的想要反复补充修改，而且常常写着写着会思绪飘移，开始回顾一些其他事情...总之最后终于下定决心无论如何一定要写完了！\n\n标题借用了进击的巨人里的一句经典台词，“献出心脏”。可能有点浮夸（毕竟日语嘛...），但是我想了半天，还是觉得这句话最适合我的心意，献出心脏，为自由，为平等，为Web 3.0。怀着对未来愉快的勇气，我决定写下这篇博客记录这一路的走走停停。鸡蛋和高墙当然选择站在鸡蛋的一边，我们不会放弃，我们前赴后继。\n\n## 那天我们想起被巨人们支配的恐惧\n\n刚加入RSS3的时候，兔子问我对开源的追求这么纯粹是受过什么人的影响吗。固然天性喜欢合作与分享，讨厌集权和垄断，但是能够有一些具体的想法与实践，确实是很幸运的受到遇到了一些引路人的。当然影响最大的是Aaron Swartz，那个哭着看完[互联网之子](https://movie.douban.com/subject/25785114/)的夜晚我想我会用余生去铭记，我痛恨这个充满谎言的世界，让为众人抱薪者冻毙于风雪；我鼓舞于Aaron炙热的理想主义，为了促进社会公正去无私战斗的勇气；我羡慕他的才华，也心痛他的绝望；我兴奋于这个世界曾经有过这样闪闪发光的人，也悲伤于最后是以他的短暂的一生的纪录片这种方式认识他。\n\n另外一位对我影响很大的人，是我在 [IST](https://tecnico.ulisboa.pt/en/) 做交换生期间的同学。这个世界上总是不缺一些奇怪的人，他绝对是其中之一。他是一个比现在的我对开源的追求还要纯粹的多的人。他不使用Google，Facebook等社交媒体，不使用MacBook，他的笔记本操作系统是Linux，他使用Emacs写presentation，比起Github更倾向使用 Gitlab。最初认识他是因为选的一门课的大作业需要找队友，我就去和看上去形单影只的他搭话。在第一天认识他的时候他和我讲与其说是我们使用 Facebook，不如说是 Facebook 使用我们，然后提出使用 Riot.im（现在叫Element.io）进行团队交流。以当时的我对安全的通信软件的理解，只知道Telegram。然后他告诉我Telegram服务端是不开源的，Telegram不是去中心化的，Riot是去中心化的，Telegram的注册需要手机号，Riot只需要邮箱。虽然我痛恨满口谎言的 Google 说着 don't do evil 却一直在 do evil，但那时的我主力浏览器依然是Chrome。他和我说如果真的不习惯 Firefox，可以使用 [Chromium](https://www.chromium.org/getting-involved/download-chromium)，它可以同步 Google 账号，但是是开源的。（现在我的主力浏览器也是Firefox了，当时有一点 Firefox 很古早很难用的刻板印象，但其实并不会）也是他让我知道了 GenLib，并且给我讲了很多微软/谷歌的版权之恶。可以说是他真正领我进入了开源和去中心化的世界。我很幸运遇见这样的人，也很幸运知道世界上原来有这样的人。\n\n若曾经看过光明，如何能再习惯黑暗。见过那些在黑暗中负重前行，与巨人们作战的同胞，怎么能继续选择装聋作哑。沉默从来不是中立，沉默就是把选票投给了高墙。\n\n## 结束是另一个开始\n\n去中心化所暗示的平等、合作、自治，如同洞穴外的阳光，曾刺痛我的双眼，让当时的我疯狂想要进入区块链的行业，只是因为区块链天然的具有去中心化特性。我参与区块链方向的research，也做区块链方向的intern。算来到现在入行两年多了，但是说实话，到后面我真的已经对区块链非常疲惫了，以致最后full time的求职意向完全不想考虑区块链了。我不是说对区块链技术没有兴趣了，而是说工作不想碰区块链了，因为国内币圈风气太差，加过的所有开发者社群最后都是币价交流社；很多项目方炒作区块链的概念装模作样的解决一些不痛不痒的问题，最后又落脚点在融资；完全的 Defi（去中心化金融）基本不可能真的在国内做下去；一些公司虽然是基于区块链做事，但是要么更注重联盟链，要么就算是基于公链也做的事情和去中心化也关系不大......总之一腔热血横冲直撞，花了很久才醒悟到区块链终究只是术，我想要的道不非在于此。\n\n面对现实的无力感，苍白如烈日当空，让我开始迷惘；社交媒体每日上演的荒谬，让我几乎政治性抑郁；思考到底什么事情是最应该去做的，让我陷入焦虑；那段时间我常常突然对自己每天到底在干什么感到强烈的虚无，常常觉得自己离这个世界太遥远，对这个世界的认知太浅薄而虚幻。\n\n我热爱这个世界，也热爱我的专业——计算机，但是不是因为技术，也不是因为趋势。最开始接触互联网不能完全说是意外，但绝不是兴趣使然的命中注定；审视自身，虽然我确实能够感受到对一些技术的兴趣，但是我完全不是一个能从纯技术中得到获取意义上的满足感的人；对计算机技术所暗示的充满科技感的赛博朋克般的未来世界，我从来没有过期待与痴迷；而所谓为了不被时代潮流抛弃所以要拥抱互联网这种论调，我更是向来不认可，时代，潮流，皆指向虚妄的概念，真实的惟有这世间的人。我热爱计算机，是因为最初的互联网曾经闪耀过的自由的光，是因为那些声明黑客宣言的自由的灵魂们，那些为了夺回用户的隐私和自由和巨头们对抗着的战士们，那些敏锐的察觉到这个世界存在的问题并大胆的用技术去探索实践一个更好的解决方案的骇客们，让我一直以来相信着指尖有改变世界的力量，哪怕是一点点。是靠着那一点点微弱但耀眼的，看到过再也无法忘记的光，我才一直没有转行。\n\n但是那段时间，面对这个世界的极度无力感，真的让我很多次认真地思考换一个能够对世界产生更有意义的影响的行业。\n\n日日夜夜，遥望星辰大海，我思考着，到底想要什么到底应该做什么。\n\n> 如果你能 decentralize 世上一件事物，而且只能是一種，你會選擇甚麼？我很認真地想過，不是因為有燈神幫我實現願望，而是因為力量微薄，即使花上餘生都不一定能成功；既然怎樣努力都不一定能 decentralize 一件事物，就更不可能貪心同時做多種，而必須集中力量到一點。\n\n直到8个月前读到文章[無大台真相：They can't kill us all](https://matters.news/@ckxpress/%E7%84%A1%E5%A4%A7%E5%8F%B0%E7%9C%9F%E7%9B%B8-they-can-t-kill-us-all-bafyreieqqwdavbc5bowq2ogugj6bmzlyscim3bcezsiwaegxoefg2653dy) 里面抛出的这个问题，我感觉我仿佛抓住了什么。作者说金钱不是他的终极关怀，对我而言也是一样啊。尽管最初因为去中心化闯入区块链的世界，但是我渐渐发现，就算是对于Defi（去中心化金融），区块链与去中心化结合的典型应用场景，其实我也没有那么关心。尽管还是会在每个披萨节尽可能的表达一句敬贸易自由，尽管我热烈地期待着一个贸易自由的世界，但是我知道那不是我最想把我的生命投入去实现的愿望。\n\n去中心化于我而言是梦开始的地方，是我想要的道，或者说非常接近我想要的道。到现在也有了一些尽管不算很多的技术积累，到底我还是想去做啊。我知道我很可能做不到，但是说到底做不做得到又有什么关系呢。正确的事情，值得去做的事情，去做了即意义本身，我只是想更强烈的感受到我活着，我真心实意的如此觉得。选择一样事物用一生去努力实现去中心化，要做的只是选择一样东西，然后投入一生去做，不需要去在意能不能做得到，就足够可以活的坚定而踏实了，听起来不是很有诱惑力吗？\n\n那么生命短暂，到底我想要去中心化哪一样事物？\n\n思索良久（一个月），我得出了属于我的答案：阅读。如果有天堂，那一定是图书馆的模样。那里信息自由地流通，书籍自由地出版，人与人自由地讨论。\n\n我真的很喜欢这种看起来和金钱就关系不大而且很偏重人文关怀的去中心化方向。作出这个结论的时候，我对我未来的期待是努力成为一名独立研究者。但是其实具体怎么做我毫无头绪，唯一可以确定的是，我希望从技术方向入手去做这件事，因为我有兴趣这么做。\n\n（为什么是独立研究者而不是独立开发者的原因之一是独立开发者通常要直接和客户打交道，有太多和市场推广和钱有关的麻烦事情......我一度怀疑过像我这么对钱头疼的人，除了啃老还有没有别的出路......）\n\n不过幸得命运女神眷顾，虽然我之前决定努力成为独立研究者，Twitter的bio也都这么写了，但是没想到后来意外的遇见了RSS3。那是又一个辗转反侧无法入眠的夜晚，并没有任何期待的只是抱着单纯聊聊天的想法发送了好友请求，却猝不及防的从凌晨十二点开始通了一个半小时的电话，之后就决定加入RSS3。\n\n在这方面我时常觉得自己是一个幸运的人。我真的原本都做好了哪怕在肯德基蹭网，租城中村廉租房，也要自费独立研究的打算，没想到现在有了一个可以带薪研究和我想独立研究差不算远的内容的机会（约等于带薪独立研究）；原本也完全没想着投入到有着所谓的发展前景的充溢着金钱的领域（没错我就是在说人工智能，proudly I can say 我的 background 和人工智能的关系几乎为零），没想到变幻莫测的社会机遇能让DWeb领域也有不少项目得到投资人的认可；原本也完全没冲着什么好找工作的方向去学习（是的这次我在说SDE），但是反倒是因为一些小众的智能合约相关研究背景也能得到某信息通信大厂某实验室的青睐。\n\n我从不害怕失败，我只害怕有一天我再也不敢去尝试；我从不害怕未来遥不可及，我只害怕有一天我会就此认命。\n\n## 我得到了星星上的金子，却被燃烧殆尽\n\n之前还在芝加哥上学的时候遇到一个读Post Doc的台湾人，他自述过往的求学经历从台南到台北到欧洲到北美，一次比一次离家远。他自嘲自己像一个迷失了的流浪的孩子。当时的我一下子被这句话击中，我也是啊（~~不，我不是Post Doc~~），无可救药地眷恋一个又一个的远方。但是更多时候这种热爱似乎只停留在我的幻想里。年少轻狂，看着天边像在眼前，赴汤蹈火也想走一趟？我也想要拥有这样的意气风发啊，可是我时常觉得我活的过于束手束脚。我明明走的更远的。比如我明明可以更轻松愉快的写下这个小节的，明明把写下这篇文字的力气用在其他事情上。\n\n我不羡慕自由的灵魂，因为我也有，我羡慕那些自由的肉体，因为我时常感觉自己的肉体深陷囹圄。亲情的羁绊与对自己人生的掌握的两难，似乎贯穿我这二十多年的人生。亲情的重量，大概永远是我生命中不能承受之轻。这么多年我感受的到我可以更坚定和自信的和主流价值观对抗，我拥有了更加强大的对真善美的信仰，但是面对以爱之名的束缚时的绝望感，我依然觉得在原地踏步。如果说有什么不同，那就是10年前的我只能选择故意拖慢回家的步伐，而10年后的我可以选择沉迷酒精。我知道他们想要什么，可是我不知道我给不给得了；我理解所有的无可奈何，可是触碰不到的距离我一毫一厘也改变不了；我知道什么样的妥协能让除了我之外的人都高兴，可是我知道我杀不死我自己。\n\n我曾把完整的镜子打碎，我曾把机会就扔在我眼前。他们说我自毁前途（~~这不就是我想要的么~~），大概是吧，对better world的期许指引的人生并不能让我有一个他们眼中的better life。事实上我也不在乎这些，我时常有种想要坠入万丈深渊的感觉，也许我真的，只想活得更强烈一些。\n\n我知道自由是相对的，自由是有界限的，也知道正是因为自由的界限才使自由显得更加珍贵。可是我也知道自由是有代价的，freedom is not free. 人真的有选择吗，如果终有一日“我得到了星星上的金子，却被燃烧殆尽”，是不是最好的结局？\n\n沉默如谜。\n\n## 我也想说下一个十年我们再见\n\n可是总归，我还是不想为了理想去死的。亦余心之所善兮，虽九死其犹未悔，为了理想失去生命丝毫不会令我感到惧怕。但是我想活着，活着继续为了理想努力。黑塞说青年人总是勇于为理想捐躯，老年人虽缺少英雄气概，但懂得自己为了什么备受折磨。勇于为理想捐躯也许很畅快，但那不是勇敢，是对生命的不尊重。尽管我不在乎最终能不能成功，但是显然我不想去以一种一看就不可能成功的方式去实践，我暗自下定决心要做一个知行合一脚踏实地的理想主义者。试图在人间建立天堂，只会致使通往地狱。我明白这其中的道理，我希望我能拥有区分这些细微之处的智慧。\n\n十年前我似乎也想过，努力不让自己被世界改变。可是这滚滚红尘，谁能独善其身。现在的我，更加明白，我不可能不被世界改变，我只能选择去改变世界，在与世界的交互中去为我想要的未来投票。我不想等到我老了，我的孙辈来质问我，互联网变成今天这个样子的时候，你们在做什么。我曾通宵达旦地工作学习过无数个夜晚，不是为了没有选择，而是为了有能力承受选择非主流价值观的那条路的代价，是为了选择我想要的未来。\n\n我也想说，下一个十年，我们再见。那时，再回头看看，我们做到了什么。\n\n听说这是最后一个被辜负的春天，飞鸟将嬉戏云端，古老的诗歌会重新被吟唱。",
            "mime_type": "text/markdown"
        }
    ],

    "metadata": {
        "network": "Arweave Mainnet",
        "proof": "9s_R8b4UfSMoP1wIJ7UGUC-fMtR68Z9cZQYplA6nj-k"
    }
}
```

### Gitcoin Donations

A special transfer activity for making a donation on Gitcoin.

#### `tags`

```json
"tags": [
    "Donation",
    "Gitcoin"
]
```

#### `attachments`

```json
"attachments": [
    {
        "type": "title",
        "content": "<title>",
        "mime_type": "text/plain"
    },
    {
        "type": "description",
        "content": "<description>",
        "mime_type": "text/plain"
    },
    {
        "type": "logo",
        "address": "<logo_address>",
        "mime_type": "<logo_mime_type>",
        "size_in_bytes": <logo_size_in_bytes>
    },
    {
        "type": "gitcoin_url",
        "content": "<gitcoin_url>",
        "mime_type": "text/uri-list"
    }
]
```

#### `metadata`

```ts
"metadata": {
    "network": "<network_name>",
    "proof": "<transaction_hash>",

    "from": "<transaction_from>",
    "to": "<transaction_to>",

    "destination": "<admin_address>",
    "value_amount": <amount>,
    "value_symbol": "<symbol>",
}
```

#### Example

##### Donation 0xa262c71eb905ff5ab6da66134826c5f6d90af8db7b406f84ef4ac725d574749c

[Chain Explorer](https://etherscan.io/tx/0xa262c71eb905ff5ab6da66134826c5f6d90af8db7b406f84ef4ac725d574749c)

[Gitcoin address](https://gitcoin.co/grants/2679/rss3-rss-with-human-curation)

```json
{
    "identifier": "rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@ethereum/note/CEA936A0-9859-4CA7-B5BC-B6D14CBBBCE0",
    "date_created": "2021-10-14T02:42:51.000Z",
    "date_updated": "2021-10-14T02:42:51.000Z",

    "auto": true,
    "identifier_instance": "rss3://note:0xa262c71eb905ff5ab6da66134826c5f6d90af8db7b406f84ef4ac725d574749c@ethereum_mainnet",

    "tags": [
        "Donation",
        "Gitcoin"
    ],
    "authors": [
        "0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@ethereum"
    ],

    "attachments": [
        {
            "type": "title",
            "content": "RSS3 - RSS with human curation",
            "mime_type": "text/plain"
        },
        {
            "type": "description",
            "content": "\nWelcome to the RSS3 GR 12\n\nSupport by Web3 Pass RSS3.bio: If u donations to us on GR12 you will get a $PASS to claim a free testnet RNS. Also, you will get a chance to try out our new product we're about to launch with a testnet RNS\n\n\n\nJoin us on RSS3 community\n\n\nWebsite: https://rss3.io\nDiscord: https://discord.gg/rss3\nTelegram: https://t.me/joinchat/jhhncmdayvNlMDgx\nTwitter: https://twitter.com/rss3_\nReddit: https://reddit.com/r/RSS3/\nQ3 NewsLetter arrived\n\n\n\n\n\n\nUpdate @ July 2\nQ2 NewsLetter arrived\n\n\n\nUpdate @ June 30\n\nIntro\nRSS3 is an open protocol designed for content and social networks in the Web 3 era. We believe the right to create, disseminate and distribute information should not be in the hands of centralized governing. It is the basic right of cyber lives.\n\nTeam\nI first was working on an RSS related app in 2018, which led me to the famous RSS project on Github called RSSHub (https://github.com/DIYgod/RSSHub). I worked on different types of social networks after that and gradually shifted my focus onto decentralized social and content networks. It was not until the second half of 2020, did I suddenly remembered RSSHub and its creator DIYgod (https://diygod.me/). I connected with him and decided that we could carry some of the best from RSS and build something better. Till today five of our talented members are based in Seattle, Shanghai and Auckland. They have created well-known open source projects, RSSHub & DPlayer, or are believers in the open-source community. Some are focused on front-end workflow optimisation, others are pioneers in marketing operations.\n\n\n\n\nThe Ideologies We Carry\nOpen Source\nIt goes without saying that the whole RSS3 project, including the standard and protocol itself and all other supporting layers like hosting and indexing, should be open source. Everyone should have the right to inspect and understand what the code is and how it works. Also, being open-source gives all developers a direct way to contribute to all parts of the project.\nWe will encourage all applications that utilize the protocol to be open-source as well. Otherwise, users won’t be trusting them with their valuable private keys. Chances are that malicious and non-open-source applications will be eliminated by market competition while data monopoly no longer exists.\nRight now, people are forced to trust centralized parties for what an internet service does. There are of course big brands to trust, like Facebook, Google or Amazon. People used to have the idea that “big brands won’t cheat”, but recent incidents have all reminded us that giving anyone the chance to do evil is equally dangerous. We need transparency.\n\nDistributed Control\nThe old RSS was designed to be decentralized but not distributed. And that leads to super sub-centres which still carries too much power similar to centralized architectures. For example, Spotify hosts a great number of long-tail podcasts and, though it still uses RSS for publishing, controls all the RSS files and the audio files.\nThe ultimate distributed control is to have every cyber persona control its data. And this means both indexing files and the content file should be under distributed hosting, and the right to edit the files are determined by their key pairs like in Bitcoin or Ethereum. However, it is important to note that this key pair that controls ownership can also be changed by their key holder, which will result in transferring or trading of a certain persona.\nThat being said, we still need to keep in mind that general users will take a pretty long time to adopt this idea of keeping one's keys and controlling one's data with them. There will likely be a gradual process that involves efforts from multiple parties.\n\nInclusiveness\nRSS3 and its applications are determined to win against the old giants, so it has to be inclusive in two major ways.\nIt starts with the inclusiveness regarding types of applications. Any content or social network is defined by its content form and network structure, where network structure is determined by the type of links and mechanism of discovery. Facebook, Twitter, Instagram, Whatsapp and TikTok are not that different technically. We need the protocol to support very different types of applications so that innovations can continue to happen.\nThen we need the inclusiveness on modules. Whether it is hosting, indexing or monetizing, RSS3 is designed to be extremely open to modules with different functionalities. This gives RSS3 great flexibility and possibility regarding what it can do in the future.\n\nThe Future We Aim\nEmpowered Personas\nCyber personas will truly have full control regarding the data they produce. Any persona can freely express their thoughts and ideas without being censored by any centralized agency. You can go to any application with your own content and relationships. No platform can ever force you to labour for it anymore. You, no longer the platform, will be empowered to create, own and monetize.\n\nPlatformless Medias\nMedias right now are closely bonded with platforms. Each social media platform has its own social graph and primary form of content. The adoption of RSS3 will give media a chance to have the largest unified group of subscribers, an efficient monetization channel without platform commission, and the freedom to generate content of various forms.\n\nInnovative Applications\nInnovations in user experience have slowed down so dramatically as data superpowers continue to grow. We want to rebuild the prosperous ecology of applications for different user experiences to emerge. When users control their data, they can easily choose to move to applications with better design and engineering efforts. Unlike competing for the scale and speed of data monopolizing, now applications will be competing for user experience.\n\nThe Team We Build\nTo achieve what we aimed for, we formed a distributed organization with a high standard. Every member who works on RSS3 comes from his/her/their/its true belief and passion. We share the culture below:\n\nMission\nTo Liberates Contents and Links\n\nVision\nBuild a world where information and its flow are free, secure, efficient and distributed\n\nValue\nNeutrality\nInclusiveness\nEquality\nSecurity\nPrivacy\nMeticulosity\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n",
            "mime_type": "text/plain"
        },
        {
            "type": "logo",
            "address": "https://c.gitcoin.co/grants/546622657b597ce151666ed2e2ecbd92/rss3_square_blue.png",
            "mime_type": "image/png",
            "size_in_bytes": 106964
        },
        {
            "type": "gitcoin_url",
            "content": "https://gitcoin.co/grants/2679/rss3-rss-with-human-curation",
            "mime_type": "text/uri-list"
        }
    ],

    "metadata": {
        "network": "Ethereum Mainnet",
        "proof": "0xa262c71eb905ff5ab6da66134826c5f6d90af8db7b406f84ef4ac725d574749c",

        "from": "0xc8b960d09c0078c18dcbe7eb9ab9d816bcca8944",
        "to": "0x7d655c57f71464b6f83811c55d84009cd9f5221c",

        "destination": "0x8c23B96f2fb77AaE1ac2832debEE30f09da7af3C",
        "value_amount": 0.00029085,
        "value_symbol": "Ether"
    }
}
```

### Tweets

[Tweets](https://help.twitter.com/en/using-twitter/types-of-tweets) on [Twitter](https://twitter.com/).

See the [Twitter API Documentation](https://developer.twitter.com/en/docs/twitter-api/v1/tweets/timelines/overview) to learn more about how to get tweets.

#### `title`

Null

#### `summary`

Tweet text.

#### `tags`

```json
"tags": [
    "Tweet"
]
```

#### `attachments`

```json
"attachments": [
    {
        "type": "media",
        "address": "<media_address>",
        "mime_type": "<media_mime_type>",
        "size_in_bytes": <media_size_in_bytes>
    },
    {
        "type": "quote_address",
        "content": "<quote_address>",
        "mime_type": "text/uri-list"
    },
    {
        "type": "quote_text",
        "content": "<quote_text>",
        "mime_type": "text/plain"
    },
    {
        "type": "quote_media",
        "address": "<quote_media_address>",
        "mime_type": "image/png",
        "size_in_bytes": <quote_media_size_in_bytes>
    },
    ...
]
```

#### `metadata`

```ts
"metadata": {
    "network": "Twitter",
    "proof": "<tweet_address>"
}
```

#### Example

##### Tweet 1483972580616949762

[Tweet address](https://twitter.com/DIYgod/status/1483972580616949762)

<details>
    <summary>Twitter API</summary>

```json
{
    "created_at": "Thu Jan 20 01:20:08 +0000 2022",
    "id_str": "1483972580616949762",
    "text": "YES! https://t.co/OheN2oPAVC https://t.co/gTpAi7Ct5c",
    "entities": {
        "urls": [
            {
                "url": "https://t.co/OheN2oPAVC",
                "expanded_url": "https://twitter.com/rss3_/status/1483803568327262210",
                ...
            }
        ],
        "media": [
            {
                "id_str": "1483972365038067717",
                "media_url_https": "https://pbs.twimg.com/media/FJghAOqXIAUPAqJ.jpg",
                "url": "https://t.co/gTpAi7Ct5c",
                "type": "photo",
                ...
            }
        ]
        ...
    },
    "quoted_status": {
        "user": {
            "screen_name": "rss3_",
            ...
        },
        "created_at": "Wed Jan 19 14:08:33 +0000 2022",
        "id_str": "1483803568327262210",
        "text": "6 mins for all Whitepaper NFTs! Thank you all!",
        ...
    }
    ...
}
```

</details>

```json
{
    "identifier": "rss3://account:0xee8fEeb6D0c2fC02Ef41879514A75d0E791b5061@ethereum/note/1BB1AF27-0046-4436-BDA1-C505AD2E40E7",
    "date_created": "2022-01-20T01:20:08.000Z",
    "date_updated": "2022-01-20T01:20:08.000Z",

    "auto": true,
    "identifier_instance": "rss3://note:https%3A%2F%2Ftwitter.com%2FDIYgod%2Fstatus%2F1483972580616949762@twitter",

    "tags": [
        "Tweet"
    ],
    "authors": [
        "0xee8fEeb6D0c2fC02Ef41879514A75d0E791b5061@ethereum",
        "DIYgod@twitter"
    ],

    "summary": "YES!",

    "attachments": [
        {
            "type": "media",
            "address": "https://pbs.twimg.com/media/FJghAOqXIAUPAqJ.jpg?name=orig",
            "mime_type": "image/png",
            "size_in_bytes": 73876
        },
        {
            "type": "quote_address",
            "content": "https://twitter.com/rss3_/status/1483803568327262210",
            "mime_type": "text/uri-list"
        },
        {
            "type": "quote_text",
            "content": "6 mins for all Whitepaper NFTs! Thank you all!",
            "mime_type": "text/plain"
        }
    ],

    "metadata": {
        "network": "Twitter",
        "proof": "https://twitter.com/DIYgod/status/1483972580616949762"
    }
}
```

### Misskey Notes

[Misskey](https://misskey-hub.net/) [Notes](https://misskey-hub.net/en/docs/features/note.html).

See the [Misskey API Documentation](https://misskey.io/api-doc#operation/users/notes) to learn more about how to get Misskey Notes.

#### `title`

Null

#### `summary`

Note text.

#### `tags`

```json
"tags": [
    "Misskey Note"
]
```

#### `attachments`

```json
"attachments": [
    {
        "type": "emojis",
        "content": "<emojis>",
        "mime_type": "text/json",
    },
    {
        "type": "file",
        "address": "<file_address>",
        "mime_type": "<file_mime_type>",
        "size_in_bytes": <file_size_in_bytes>
    },
    {
        "type": "quote_address",
        "content": "<quote_address>",
        "mime_type": "text/uri-list",
    },
    {
        "type": "quote_text",
        "content": "<quote_text>",
        "mime_type": "text/plain",
    },
    {
        "type": "quote_emojis",
        "content": "<quote_emojis>",
        "mime_type": "text/json",
    },
    {
        "type": "quote_file",
        "content": "<quote_file_address>",
        "mime_type": "<quote_file_mime_type>",
        "size_in_bytes": <quote_file_size_in_bytes>
    },
    ...
]
```

#### `metadata`

```ts
"metadata": {
    "network": "Misskey",
    "proof": "<misskey_address>"
}
```

#### Example

##### Misskey nya.one/notes/8wern2wyun

[Misskey address](https://nya.one/notes/8wern2wyun)

<details>
    <summary>Misskey API</summary>

```json
{
    "id": "8wern2wyun",
    "createdAt": "2022-02-06T11:48:20.482Z",
    "text": "盲 盒（物理x :nacho_nya:",
    "cw": null,
    "emojis": [
        {
            "name": "nacho_nya",
            "url": "https://file.nya.one/misskey/webpublic-cc375802-fe69-4c4c-9e8d-2cddd2505404.png"
        }
    ],
    "renote": {
        "id": "8werm1i8u5",
        "createdAt": "2022-02-06T11:47:32.000Z",
        "text": "？？？\nNFT 是这么卖的？？",
        "cw": null,
        "emojis": [
            {
                "name": "nacho_attention@.",
                "url": "https://file.nya.one/misskey/webpublic-b45483d9-b09b-4b84-a1f2-8fb2595671fa.png"
            }
        ],
        "files": [
            {
                "type": "image/jpeg",
                "md5": "c84435a19d51bb05879e5b2276e71d8a",
                "size": 317909,
                "url": "https://file.nya.one/misskey/52cd5198-bb00-4f8e-b023-9063b2c988f2.jpeg",
                ...
            }
        ],
        "uri": "https://m.uuu.moe/users/yashi/statuses/107750886737259295",
        "url": "https://m.uuu.moe/@yashi/107750886737259295"
        ...
    }
    ...
}
```

</details>

```json
{
    "identifier": "rss3://account:0xee8fEeb6D0c2fC02Ef41879514A75d0E791b5061@ethereum/note/18602E45-F56D-4FB5-A136-238F40893E9C",
    "date_created": "2022-02-06T11:48:20.482Z",
    "date_updated": "2022-02-06T11:48:20.482Z",

    "auto": true,
    "identifier_instance": "rss3://note:https%3A%2F%2Fnya.one%2Fnotes%2F8wern2wyun@misskey",

    "tags": [
        "Misskey Note"
    ],
    "authors": [
        "0xee8fEeb6D0c2fC02Ef41879514A75d0E791b5061@ethereum",
        "Candinya@nya.one@misskey"
    ],

    "summary": "盲 盒（物理x :nacho_nya:",

    "attachments": [
        {
            "type": "emojis",
            "content": "{\"name\":\"nacho_nya\",\"url\":\"https://file.nya.one/misskey/webpublic-cc375802-fe69-4c4c-9e8d-2cddd2505404.png\"}",
            "mime_type": "text/json",
        },
        {
            "type": "quote_address",
            "content": "https://m.uuu.moe/@yashi/107750886737259295",
            "mime_type": "text/uri-list",
        },
        {
            "type": "quote_text",
            "content": "？？？\nNFT 是这么卖的？？",
            "mime_type": "text/plain",
        },
        {
            "type": "quote_file",
            "content": "https://file.nya.one/misskey/52cd5198-bb00-4f8e-b023-9063b2c988f2.jpeg",
            "mime_type": "image/jpeg",
            "size_in_bytes": 317909
        },
    ],

    "metadata": {
        "network": "Misskey",
        "proof": "https://nya.one/notes/8wern2wyun"
    }
}
```

### Jike Posts

[Jike](https://web.okjike.com/) Posts.

#### `title`

Null

#### `summary`

Post text.

#### `tags`

```json
"tags": [
    "Jike Post"
]
```

#### `attachments`

```json
"attachments": [
    {
        "type": "media",
        "address": "<media_address>",
        "mime_type": "<media_mime_type>",
        "size_in_bytes": <media_size_in_bytes>
    },
    {
        "type": "quote_address",
        "content": "<quote_address>",
        "mime_type": "text/uri-list",
    },
    {
        "type": "quote_text",
        "content": "<quote_text>",
        "mime_type": "text/plain",
    },
    {
        "type": "quote_media",
        "address": "<quote_media_address>",
        "mime_type": "<quote_media_mime_type>",
        "size_in_bytes": <quote_media_size_in_bytes>
    },
    ...
]
```

#### `metadata`

```ts
"metadata": {
    "network": "Jike",
    "proof": "<jike_address>"
}
```

#### Example

##### Jike 61dfc33558b7cf00109d11a4

[Jike address](https://web.okjike.com/repost/61dfc33558b7cf00109d11a4)

<details>
    <summary>Jike API</summary>

```json
{
    "id": "61dfc33558b7cf00109d11a4",
    "type": "REPOST",
    "content": "已经确保了",
    "createdAt": "2022-01-13T06:14:13.064Z",
    "__typename": "Repost",
    "target": {
        "id": "61dfb9ce6dcd95001093f964",
        "type": "ORIGINAL_POST",
        "content": "RSS3 与即刻APP达成深度合作，RSS3已支持即刻APP内容索引，在其生态产品 REVERY.so 中可查看即刻APP的内容。\n\n未来，双方将在内容索引、数据支持等方向展开更多合作。同时，即刻与RSS3推出特别纪念NFT，用户在RSS3网络中绑定自己的即刻账号即可满足铸造条件。\n\n确保 Web3 发生在即刻",
        "pictures": [
            {
                "thumbnailUrl": "https://cdn.jellow.site/FpHKp4b_mcsQpC1Jciae7yQjDBDzv2.jpg?imageMogr2/auto-orient/thumbnail/300x2000%3E/quality/70/interlace/1",
                "__typename": "PictureInfo"
            }
        ],
        "topic": {
            "id": "5738965b6628391200809ff1",
            "content": "Web3研究所",
            "__typename": "TopicInfo"
        },
        "__typename": "OriginalPost"
        ...
    },
    "targetType": "ORIGINAL_POST",
    ...
}
```

</details>

```json
{
    "identifier": "rss3://account:0xee8fEeb6D0c2fC02Ef41879514A75d0E791b5061@ethereum/note/1CBC16D3-98C8-4A86-9778-2B5C7697D663",
    "date_created": "2022-01-13T06:14:13.064Z",
    "date_updated": "2022-01-13T06:14:13.064Z",

    "auto": true,
    "identifier_instance": "rss3://note:https%3A%2F%2Fweb.okjike.com%2ForiginalPost%2F5ee1b02380d99c00184c15d0@jike",

    "tags": [
        "Jike Post"
    ],
    "authors": [
        "0xee8fEeb6D0c2fC02Ef41879514A75d0E791b5061@ethereum",
        "3EE02BC9-C5B3-4209-8750-4ED1EE0F67BB@jike"
    ],

    "summary": "已经确保了",

    "attachments": [
        {
            "type": "quote_address",
            "content": "https://web.okjike.com/originalPost/61dfb9ce6dcd95001093f964",
            "mime_type": "text/uri-list",
        },
        {
            "type": "quote_text",
            "content": "RSS3 与即刻APP达成深度合作，RSS3已支持即刻APP内容索引，在其生态产品 REVERY.so 中可查看即刻APP的内容。\n\n未来，双方将在内容索引、数据支持等方向展开更多合作。同时，即刻与RSS3推出特别纪念NFT，用户在RSS3网络中绑定自己的即刻账号即可满足铸造条件。\n\n确保 Web3 发生在即刻",
            "mime_type": "text/plain",
        },
        {
            "type": "quote_media",
            "address": "https://cdn.jellow.site/FpHKp4b_mcsQpC1Jciae7yQjDBDzv2.jpg",
            "mime_type": "image/jpeg",
            "size_in_bytes": 256905
        }
    ],

    "metadata": {
        "network": "Jike",
        "proof": "https://web.okjike.com/originalPost/5ee1b02380d99c00184c15d0"
    }
}
```

## Indexed Asset Item List

### NFT

#### `title`

NFT name.

#### `summary`

NFT description.

#### `tags`

```json
"tags": [
    "NFT"
]
```

#### `attachments`

```json
"attachments": [
    {
        "type": "object",
        "address": "<object_address>",
        "mime_type": "<object_mime_type>",
        "size_in_bytes": <object_size_in_bytes>
    },
    {
        "type": "preview",
        "address": "<preview_address>",
        "mime_type": "<preview_mime_type>",
        "size_in_bytes": <preview_size_in_bytes>
    },
    {
        "type": "attributes",
        "content": "{\"<attribute_key>\":\"<attribute_value>\",...}",
        "mime_type": "text/json"
    },
    {
        "type": "external_url",
        "content": "<external_url>",
        "mime_type": "text/uri-list"
    }
]
```

#### `metadata`

```ts
"metadata": {
    "network": "<network_name>",
    "proof": "<collection_address>-<token_id>",

    "token_standard": "<token_standard>",
    "token_id": "<token_id>",
    "token_symbol": "<token_symbol>",

    "collection_address": "<collection_address>",
    "collection_name": "<collection_name>",
}
```

#### Special NFTs

See [Indexed Note Item List - Special NFTs](#special-nfts)

#### Examples

##### Minting of RSS3 Whitepaper #1800

[Chain Explorer](https://etherscan.io/nft/0xb9619cf4f875cdf0e3ce48b28a1c725bc4f6c0fb/1800)

```json
{
    "identifier": "rss3://account:0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@ethereum/asset/D52DCF9F-7FF0-400A-9562-66C87DB3A866",
    "date_created": "2022-01-19T02:06:38.000Z",
    "date_updated": "2022-01-19T02:06:38.000Z",

    "auto": true,
    "identifier_instance": "rss3://asset:0xb9619cf4f875cdf0e3ce48b28a1c725bc4f6c0fb-1800@ethereum_mainnet",

    "tags": [
        "NFT"
    ],
    "authors": [
        "0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944@ethereum"
    ],

    "title": "RSS3 Whitepaper v1.0",
    "summary": "RSS3 Whitepaper v1.0 - Commemorative & Limited Edition",

    "attachments": [
        {
            "type": "object",
            "address": "ipfs://bafybeicij6vw6xcsgwldofnmmh3c3j4w5yiocs6l72yubpbcldxcglkvqe/rss3-whitepaper-no-1800.glb",
            "mime_type": "model/gltf-binary",
            "size_in_bytes": 3983376
        },
        {
            "type": "preview",
            "address": "ipfs://bafybeianto7koyrfwkdjymx7byjrs3hzy7ldipfxc343vra2t7pbd557sy/rss3-whitepaper-no-1800.png",
            "mime_type": "image/png",
            "size_in_bytes": 117310
        },
        {
            "type": "attributes",
            "content": "{\"Author(s)\":\"Natural Selection Labs\",\"Edition\":\"First Edition\",\"Edition Language\":\"English\",\"File Format\":\"PDF\",\"No.\":1800,\"date\":1610323200}",
            "mime_type": "text/json"
        },
        {
            "type": "external_url",
            "content": "https://rss3.io/RSS3-Whitepaper.pdf",
            "mime_type": "text/uri-list"
        }
    ],

    "metadata": {
        "network": "Ethereum Mainnet",
        "proof": "0xb9619cf4f875cdf0e3ce48b28a1c725bc4f6c0fb-1800",

        "token_standard": "ERC-721",
        "token_id": "1800",
        "token_symbol": "RWP",

        "collection_address": "0xb9619cf4f875cdf0e3ce48b28a1c725bc4f6c0fb",
        "collection_name": "RSS3 Whitepaper"
    }
}
```

### GitHub Achievement

TODO

### PlayStation Network Trophy

TODO
