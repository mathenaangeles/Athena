<template>
    <div id="chat">
        <el-row v-for="(message, index) in messages" :key="index">
            <el-col :span="24">
                <el-card :class="['chat-card', message.user === 'User' ? 'user-message' : 'bot-message']">
                    <div class="chat-message">
                        <strong>{{ message.user }}:</strong> {{ message.text }}
                    </div>
                </el-card>
            </el-col>
        </el-row>
        <el-row id="input-query" type="flex" justify="center">
            <el-col :span="20">
            <el-input
                id="message-input"
                v-model="query"
                placeholder="Type your message here..."
                @keyup.enter="sendMessage">
                <template #prepend>
                    <el-icon><ChatRound /></el-icon>
                </template>
                <template #append>
                    <el-button @click="sendMessage">
                    Send
                    </el-button>
                </template>
            </el-input>
            </el-col>
        </el-row>
    </div>
</template>
  
<script>
  import { mapGetters } from "vuex";
  export default {
    name: "Chat",
    data() {
      return {
        query: '',
        messages: [
        ]
      };
    },
    computed: {
        ...mapGetters(['response']),
    },
    methods: {
        sendMessage() {
            if (this.query.trim() === '') return;
            const user = {
                user: 'User',
                text: this.query,
                timestamp: new Date().toLocaleString()
            };
            this.messages.push(user);
            this.$store
                .dispatch("getResponse", this.query)
                .then(() => {
                    const bot = {
                        user: 'Bot',
                        text: this.response,
                        timestamp: new Date().toLocaleString()
                    };
                    this.messages.push(bot);
                    this.query=""
                })
                .catch((err) => {
                    const bot = {
                        user: 'Bot',
                        text: err,
                        timestamp: new Date().toLocaleString()
                    };
                    this.messages.push(bot);
                    this.query=""
                });
        },
    },
  };
</script>
  
<style scoped>
#chat {
    height: 100%;
}
#input-query {
    position:fixed;
    bottom: 0;
    width: 100%;
}
.chat-card {
  max-width: 70%;
  word-break: break-word;
  margin: 20px;
}
.user-message {
  margin-left: auto;
  background-color: #409EFF
;
}
.bot-message {
  margin-right: auto;
;
}
.chat-body {
    margin-bottom:30px;
}
</style>
  
  