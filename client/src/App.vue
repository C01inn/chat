<template>
  <div id="app">
    <!-- main card -->
    <div
      id="main"
      class="mx-auto w-3/4 h-auto rounded-lg"
    >
      <div class="messages" id="messages">
        <div v-for="message in messages" :key="message">
          <card
            v-if="message.ip === ip"
            :user="true"
            class="ml-2 mt-2 mb-2 shadow-xl border user-message"
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
      <form @submit.prevent="sendMessage()" class="form-1" id="message-form">
        <input
          id="message-in"
          class="mx-auto shadow-xl appearance-none solid w-full py-2 px-3 text-grey-darker leading-tight focus:outline-none focus:shadow-outline"
          type="text"
          placeholder="Message"
        />
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
      apiUrl: "https://apichatroom.herokuapp.com",
      //apiUrl: "http://127.0.0.1:999",
      socket: null,
      messages: [],
      ip: ''
    };
  },
  async created() {
    this.ip = await this.getIp()
    // get users ip address
    let windowHeight = $(window).height();
    fetch(this.apiUrl + "/last/" + parseInt(windowHeight / 50))
      .then((data) => data.json())
      .then((data) => {
        this.messages = data;
        this.messages.forEach((msg, idx) => {
          msg.time = new Date(msg.time * 1000);
          msg.time = this.formatedDate(msg.time);
          this.messages[idx].time = msg.time;
        });
      });
  },
  mounted() {
    this.socket = io.connect(this.apiUrl);
    // recieved message
    this.socket.on("messageResp", (msg) => {
      // format datetime
      msg.time = new Date(msg.time * 1000);
      msg.time = this.formatedDate(msg.time);
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
    sendMessage() {
      let messageContent = $("#message-in").val();
      $("#message-in").val("");

      this.socket.emit("message", {
        message: messageContent,
      });
    },
    militaryToStandard(hour, minute) {
      if (minute < 10) {
        minute = "0" + minute;
      }
      if (hour > 13) {
        hour = 24 - hour;
        hour = 12- hour;
        return hour + ":" + minute + " PM";
      }
      return hour + ":" + minute + "AM";
    },
    formatedDate(previous) {
      const monthNames = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
      ];
    
      var currentTime = new Date();
      let month = monthNames[previous.getMonth()];
      let day = previous.getDay().toString();
      let year = previous.getFullYear();
      let hour = parseInt(previous.getHours().toString());
      let minute = parseInt(previous.getMinutes().toString());
      let timee = this.militaryToStandard(hour, minute);
      let finalDate = `${timee} ${month}, ${day} ${year}`;
      return finalDate;
    },
    async getIp() {
      const resp = await fetch(this.apiUrl + '/myip');
      let data = await resp.json()
      return data.ip
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
  color: blue;
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
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
html {
  background: gray;
}

</style>
