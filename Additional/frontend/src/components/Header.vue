<template>
<div>
  <v-layout class="app">
    <v-flex class="header" xs12 my-5 >
        <v-layout row wrap>
          <v-flex xs12 sm8>
            <router-link to="/"><img src="@/assets/logo.png" class="logo"/></router-link>
            <title>맥 짚는 AI</title>
          </v-flex>
          <v-flex class="searchPart"xs12 sm4>
            <v-text-field
                style="width: 90%; margin: 0 auto;"
                placeholder="검색어를 입력하세요."
                append-outer-icon="fas fa-search"
                v-model="searchKey"
                @click:append-outer="SearchNews()"
              ></v-text-field>
          </v-flex>
        </v-layout>
        <v-layout class="navi" row wrap>
            <v-flex xs12 sm4>
              <v-btn class="headerBtn" to="/" flat> News </v-btn>
              <v-btn class="headerBtn" to="AboutUs" flat> About Us </v-btn>
              <v-icon class="chatbotIcon" @click.stop="menu = !menu">far fa-comment-dots</v-icon>
              <v-menu class="chat" v-model="menu" :close-on-content-click="false" :nudge-width="200" offset-y>
                <template v-slot:activator="{ on }"></template>

                <v-card>
                  <v-flex class="chatbox"></v-flex>
                  <textarea class="chattext" v-model="text" @keyup.enter="enter" name="content" rows="2" placeholder="입력하세요."></textarea>
                </v-card>
              </v-menu>
            </v-flex>
            <v-flex hidden-xs-only sm5></v-flex>
            <v-flex xs12 sm3 id="realNewsTitle">
                <vue-swimlane :words="newsTitle" :scale="1.3" :pauseOnHover="true"></vue-swimlane>
            </v-flex>
        </v-layout>
    </v-flex>
  </v-layout>
</div>
</template>

<script>
import axios from "axios";

export default {
  name: 'Header',
  components: {
  },
  data() {
    return {
      NowPage: "AboutUs",
      newsTitle : ["1. 나는 사람이다.", "2. 자소서 쓰기 싫어요!", "3. 오늘은 9월 16일", "4. 가나다라가나다라가나다라가나다라가나다라가나다라가나다라"],
      searchKey : "",
      menu: false,
      text: "",
    }
  },

  methods: {
    MovePage(location) {
      this.NowPage = location;
    },

    SearchNews() {
      console.log(this.searchKey);
      this.searchKey = "";
    },

    enter(){
      if(this.check){
        this.check = !this.check
        return ;
      }

      this.check = !this.check

      // user comment
      var select = document.querySelector('.chatbox')
      select.innerHTML += "<p class='arrow_box_right'>"+ this.text +"</p></br>"

      // form data
      var form = new FormData()
      form.append('msg', this.text)

      // chatbot comment
      axios.post("http://localhost:5000/api/chat", form)
          .then(res => {

            select.innerHTML += "<p class='arrow_box_left'>" + JSON.stringify(res.data[0]["value"]) + "</p>"
          }).catch(error => {
            console.log(error)
          }).then(()=>{
            select.scrollTop = select.scrollHeight
            document.querySelector('.chattext').value = ''
          })

      this.text = ""
    }
  }

}
</script>


<style lang="scss" scoped>
.header {
    position: relative;

    .logo {
        width: 80px;
        height: 80px;
    }

    title {
        font-family: 'Droid Serif', serif;
        font-weight: 900;
        font-size: 4rem;
        display: inline-block;
        margin-left: 10px;
    }
}

.app {
    font-size: 14px;
    color: #2f2f2f;
}

.navi {
    border-bottom: 2px solid #2f2f2f;
    border-top: 2px solid #2f2f2f;
    text-align: left !important;
}

.headerBtn {
  background: #00000000 !important;
}

#realNewsTitle {
  font-family: 'Noto Serif KR', serif;
  overflow: hidden;
  text-overflow: ellipsis;
  padding: 10px 0;
}

@media (min-width : 600px) {
  .header
  title {
    font-size: 5rem;
  }
  .searchPart {
    padding-top: 40px;
  }
}

.v-btn--active:before, .v-btn:focus:before, .v-btn:hover:before {
    background-color: #00000000;
}

.chatbotIcon {
  margin-left: 10px;
  font-size: 30px;
}

.chatbox {
  height: 350px;
  border: 1px solid black;
  overflow-y:scroll;
}

.chat {
  width: 15%;
  margin: auto;
}

.chattext {
  width: 80%;
  border: 0;
  outline: 0;
}

</style>
