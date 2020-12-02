<template>
    <v-row no-gutters class="fill-height">
        <v-col cols="12">    
            <iframe :src="src" style="height:100%;width:100%;border:0" />
        </v-col>
    </v-row>
</template>
<script>
    const IFRAMES = process.env.iframes // nuxt.config.js => env

    export default {
        validate ({ params }) {
            // compruebo que el "/path" coincide con algún "package.iframes.path"
            return Object.keys(IFRAMES).includes(`/${params.iframe}`)
        },
        data () {
            return {
                src: IFRAMES[this.$route.path]
            }
        }
    }
</script>
