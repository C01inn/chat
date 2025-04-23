<template>
<div
    :class="['message-bubble', user ? 'float-right' : 'float-left', 'max-w-xs', 'lg:max-w-md', 'mx-4', 'my-2', 'p-3', 'rounded-lg', 'shadow-md', 'bg-white', 'dark:bg-gray-800']">
    <div class="message-content">
    <div class="message-time text-xs font-light mb-1">
        {{ datetime }}
    </div>
    <div class="message-text text-base font-medium text-gray-900 dark:text-gray-100">
        {{ message }}
    </div>
    </div>
</div>
</template>

<script>
export default {
name: "Card",
props: {
    datetime: String,
    message: String,
    user: Boolean
},
mounted() {
    this.$nextTick(() => {
    if (this.user) {
        this.$el.style.backgroundColor = '#90D5FF';
    }
    });
}
};
</script>

<style scoped>
.message-bubble {
    max-width: 75%;
    width: fit-content;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border-radius: 1rem;
    clear: both;
}

.float-right {
    margin-left: auto;
}

.float-left {
    margin-right: auto;
}

.message-content {
    display: flex;
    flex-direction: column;
    word-wrap: break-word;
    overflow-wrap: break-word;
}

.message-time {
    font-size: 0.9rem;
    color: #000000;
    text-shadow: 1px 1px 2px lightgray;
}

.message-text {
    font-size: 1.15rem;
    line-height: 1.5;
    color: #1f2937;
    text-align: left;
}

@media (max-width: 900px) {
    .message-text {
        font-size: 0.875rem;
    }
}
</style>
