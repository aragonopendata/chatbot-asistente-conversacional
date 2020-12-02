<template>
    <div>
        <span>{{ maxIdleTime - idleTime }}</span>
        <v-icon 
            :title="title" 
            :class="{flash: iconTimerNum === 8}"
            >
            {{ idleTime ? `mdi-circle-slice-${iconTimerNum}` : 'mdi-circle-outline' }}
        </v-icon>  
    </div>   
</template>

<script>
export default {
    props: {
        title: {
            type: String,
            default: ''
        },
        maxIdleTime: {
            type: Number,
            default: 300 // 10seg | 60 = 1min | 300 = 5 min
        }
    },
    data () {
        return {
            idleTime: 0
        }
    },
    computed: {
        iconTimerNum () {
            return Math.max(1, Math.min(8, Math.round((this.idleTime/ this.maxIdleTime) * 10)))
        }
    },
    destroyed () {
        this.endTimer();
    },
    methods: {
        startTimer () {
            this.endTimer();
            this.$options._TIMER = setInterval(() => {
                this.idleTime += 1;
                if (this.idleTime >= this.maxIdleTime){
                    this.$emit('onEnd')
                }
            }, 1000)
            // console.warn('startTimer', this.$options._TIMER);
        },
        endTimer () {
            if (this.$options._TIMER) {
                // console.warn('endTimer', this.$options._TIMER);
                this.idleTime = 0;
                clearInterval(this.$options._TIMER);
                this.$options._TIMER = null;
            }
        },
        hasTimer () {
            return this.$options._TIMER
        }
    }
}
</script>

<style>
    @keyframes idletimer_flash {
        from,
        50%,
        to {  opacity: 1; }

        25%,
        75% { opacity: 0; }
    }

    .flash {
        animation-name: idletimer_flash;
        animation-duration: 0.75s;
        animation-iteration-count: infinite;
    }
</style>
