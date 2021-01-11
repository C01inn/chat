<template>
    <div class="card-0 rounded-2xl">
        <div class="card-1 w-auto widget py-1 px-3 rounded-2xl bg-white border border-gray-300 dark:bg-gray-900 dark:border-gray-800">
            <div class="flex flex-row items-center justify-between w-auto">
                <div class="card-3 flex flex-col w-auto">
                    <div class="tim text-xs uppercase font-light text-gray-500">
                        {{datetime}}
                    </div>
                    <div class="mes w-auto">
                        {{message}}
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import $ from 'jquery'
export default {
    name: "Card",
    props: {
        datetime: String,
        message: String,
        user: Boolean
    },
    mounted() {
        this.$nextTick(() => {
            // if this is the users messahe then make it blue
            if(this.user) {
                $(".card-1").css("background", "#00bfff")
            }
        })
    }
}
</script>
<style scoped>


.card-3 {
    text-align: left;
    word-wrap: break-word;
    overflow-x: auto;
    width: auto;
}
.card-0 {
    max-width: 75%;
    width: fit-content;
}


.tim {
    font-size: .9em;
}

.mes {
    font-size: 18px;
    text-align: left;
    font-weight: 600;
    font-family: -apple-system,BlinkMacSystemFont,"Segoe UI","Roboto","Oxygen","Ubuntu","Cantarell","Fira Sans","Droid Sans","Helvetica Neue",sans-serif;
    position: relative;
}

@media screen and (max-width: 900px) {
    .mes {
        font-size: 15px;
        text-align: left;
        font-weight: 600;
        font-family: -apple-system,BlinkMacSystemFont,"Segoe UI","Roboto","Oxygen","Ubuntu","Cantarell","Fira Sans","Droid Sans","Helvetica Neue",sans-serif;
        position: relative;
    }
} 


</style>