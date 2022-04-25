<template>
    <v-card flat tile>
        <v-toolbar height="32" dense flat>
            <v-toolbar-items class="align-center mr-1 text-caption font-weight-light">
                json raw
            </v-toolbar-items>
            <v-toolbar-items>
                <v-switch
                    v-model="isPretty"
                    height="32"
                    >
                    <template #label>
                        <span class="text-caption">json pretty</span>
                    </template>
                </v-switch>
            </v-toolbar-items>
            <v-spacer />
            <v-toolbar-items>
                <ita-btn-copy-clipboard
                    x-small
                    :text="jsonText"
                    label="Copiar JSON"
                    title="Copiar código JSON al portapapeles"
                />
            </v-toolbar-items>
        </v-toolbar>
        <v-card-text>
            <vue-json-pretty 
                v-if="isPretty"
                :data="json"
                show-length
                highlight-mouseover-node
                :show-double-quotes="false"
                style="word-break:break-all"
            />
            <code 
                v-else
                class="ita-code-json"
                >
                <pre>{{ jsonText }}</pre>
            </code>
        </v-card-text>
    </v-card>
    
</template>

<script>
    import VueJsonPretty from 'vue-json-pretty';
    
    export default {
        components: {
            VueJsonPretty,
        },
        props: {
            json: {
                type: [Object, Array],
                default: () => {}
            }
        },
        data () {
            return {
                isPretty: true,
            }
        },
        computed: {
            jsonText () {
                return JSON.stringify(this.json, null, 4)
            }
        },
    }
</script>

<style>
    .ita-code-json {
        display: block;
    }
    .ita-code-json pre {
        word-break: break-word;
        white-space: pre-wrap
    }
</style>
