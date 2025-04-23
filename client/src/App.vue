<template>
  <div id="app">
    <!-- main card -->
    <div
      id="main"
      class="mx-auto w-3/4 h-auto rounded-lg"
    >
      <div class="messages" id="messages">
        <div v-for="message in messages" :key="message">
          <!--show card v-if message.messageId is found in clients local storage 
          otherwise show the v-else card -->
          <card
            v-if="usersMessage(message.messageId)"
            :user="true"
            class="ml-2 mt-2 mb-2 shadow-xl border"
            :datetime="message.time"
            :message="message.message"
          ></card>
          <card 
            v-else
            :user="false"
            class="ml-2 mt-2 mb-2 shadow-xl border"
            :datetime="message.time"
            :message="message.message"
          ></card>
        </div>
      </div>
      <form @submit.prevent="sendMessage()" class="form-1 flex items-center" id="message-form">
        <input
          id="message-in"
          class="mx-auto shadow-xl appearance-none border w-full py-2 px-3 text-grey-darker leading-tight focus:outline-none focus:shadow-outline"
          type="text"
          placeholder="Message"
        />
        <button
          type="submit"
          class="ml-2 bg-blue-500 hover:bg-blue-700 text-white font-bold py-6 px-5 rounded focus:outline-none focus:shadow-outline"
          aria-label="Send"
        >
        Send
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import * as io from '@/assets/socketio.min.js';
import $ from "jquery";
import card from "@/components/card.vue";

export default {
  name: "App",
  components: {
    card,
  },
  data() {
    return {
      apiUrl: "https://chatserver-ptntfzmvra-uk.a.run.app",
      socketUrl: 'https://chatserver-ptntfzmvra-uk.a.run.app',
      socket: null,
      messages: []
    };
  },
  async created() {
    // set local storage if not already
    let item = window.localStorage.getItem("messages")
    if (item === null) {
      window.localStorage.setItem("messages", "")
    }

    //////////////////////

    let windowHeight = $(window).height();
    
    fetch(this.apiUrl + "/last/" + parseInt(windowHeight / 50), {mode: 'cors'})
      .then((data) => data.json())
      .then((data) => {
        this.messages = data;
        this.messages.forEach((msg, idx) => {
          msg.time = this.unixToString(msg.time)
          this.messages[idx].time = msg.time;
        });
      });
  },
  mounted() {
    this.socket = io.connect(this.socketUrl);
    // recieved message
    this.socket.on("messageResp", (msg) => {
      // format datetime
      msg.time = this.unixToString(msg.time)
      let mainDivHeight = $("#main").height();
      let windowHeight = $(window).height();
      // add to messages array
      if (windowHeight < mainDivHeight + 150) {
        this.messages.shift();
        this.messages.push(msg);
      } else {
        this.messages.push(msg);
      }
    });
    this.$nextTick(() => {
      $("#message-in").focus();
    })
  },
  methods: {
    createMessageId() {
      let id = (new Date()).getTime() + '';
      id += Math.random().toString(16).replace('.', '');
      return id;
    },
    sendMessage() {
      let messageContent = $("#message-in").val();

      // dont allow user to send blank messages
      if (messageContent.replace(" ", "") === "") {
        return;
      }

      // reset text box
      $("#message-in").val("");
      
      let id = this.createMessageId()

      // add message id to local storage
      let oldLocalStorage = localStorage.getItem("messages")
      localStorage.setItem("messages", oldLocalStorage + "," + id)

      //send message to server via websocket
      let messageData = {
        message: messageContent,
        messageId: id
      }
      this.socket.emit("message", messageData);
    },
    // convert the timestamp to a readable format
    unixToString(unixTimestamp) {
      const seconds = Math.floor((Date.now() / 1000) - unixTimestamp);
      const intervals = [
          { label: 'year', seconds: 31536000 },
          { label: 'month', seconds: 2592000 },
          { label: 'week', seconds: 604800 },
          { label: 'day', seconds: 86400 },
          { label: 'hour', seconds: 3600 },
          { label: 'minute', seconds: 60 },
          { label: 'second', seconds: 1 }
      ];

      for (const interval of intervals) {
          const count = Math.floor(seconds / interval.seconds);
          if (count >= 1) {
              return `${count} ${interval.label}${count > 1 ? 's' : ''} ago`;
          }
      }
      return 'Just now';
    },
    // returns true if the message was sent by the current user
    usersMessage(id) {
      return localStorage.getItem("messages").includes(id)
    }
  },
};
</script>

<style>

#messages {
  overflow-y: hidden;
}


#main {
  z-index: 2;
  position: absolute;
  bottom: 7rem;
  left: 50%;
  transform: translateX(-50%);
  overflow: hidden;
  height: auto;
}
@media screen and (max-height: 500px) {
  #main {
    position: absolute;
    bottom: 0.5rem;
    left: 50%;
    transform: translateX(-50%);
  }
}
.form-1 {
  border-top: 1px solid black;
}
#message-in {
  height: 100%;
  position: relative;
  bottom: 0;
  font-size: 44px;
  background: rgba(255, 255, 255, .67);
  padding: 1rem;
  color: rgba(0, 0, 0, 0.75);
}

@media screen and (max-width: 900px) {
  #message-in {
    height: 100%;
    position: relative;
    bottom: 0;
    font-size: 33px;
    background: #fff;
    padding: 1rem;
  }
}

#message-in::placeholder {
  color: rgba(62, 130, 209, .75);
  color: rgba(0, 0, 0, 0.75);

}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
html {
  background: rgb(255, 255, 255);
}

</style>
