# ItaTraining

## Props

<!-- @vuese:ItaTraining:props:start -->
|Name|Description|Type|Required|Default|
|---|---|---|---|---|
|toolbarColor|-|`String`|`false`|""|
|toolbarIcon|-|`String`|`false`|""|
|title|-|`String`|`false`|""|
|storeItems|-|`String`|`false`|''|
|intents|-|`Array`|`false`||
|names|-|`Array`|`false`|item,items|
|empty|-|`Boolean`|`false`|false|
|disabled|-|`Boolean`|`false`|false|

<!-- @vuese:ItaTraining:props:end -->


## Events

<!-- @vuese:ItaTraining:events:start -->
|Event Name|Description|Parameters|
|---|---|---|
|onItemDeleted|-|-|
|onError|-|-|
|onItemChanged|await this.recommendIntents(key);|-|
|select_intentId|filter INTENTS to recommended & show its TEMPLATES|-|

<!-- @vuese:ItaTraining:events:end -->


