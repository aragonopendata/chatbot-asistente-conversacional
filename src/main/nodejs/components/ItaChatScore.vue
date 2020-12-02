<template>
    <v-chip-group
        :value="score"
        active-class="black--text"
        @change.once="submitScore($event)"
        >
        <v-chip 
            v-for="({ label, value, icon, color}, index) in items"
            :key="index"
            pill 
            small
            :value="value" 
            :disabled="disabled" 
            :color="color" 
            >
            <v-icon left>{{ icon }}</v-icon>
            {{ label }}
        </v-chip>
    </v-chip-group>
</template>

<script>
    export default {
        props: {
            score: {
                type: Number,
                default: null
            }
        },
        data () {
            return {
                disabled: false,
                scoreSelected: null,
                scores: [
                    {
                        label: "Mala",
                        value: -10,
                        icon: "mdi-emoticon-sad-outline",
                        color: "error lighten-2"
                    },
                    {
                        label: "Normal",
                        value: 0,
                        icon: "mdi-emoticon-neutral-outline",
                        color: "warning lighten-2"
                    },
                    {
                        label: "Buena",
                        value: 10,
                        icon: "mdi-emoticon-happy-outline",
                        color: "success lighten-2"
                    }
                ]
            }
        },
        computed: {
            items () {
                return this.disabled 
                    ? this.scores.filter(o => o.value === this.scoreSelected)
                    : this.scores
                    ;
            }
        },
        methods: {
            submitScore (score) {
                this.disabled = true;
                this.scoreSelected = score;
                this.$emit('change', score)
            }
        }
    }
</script>
