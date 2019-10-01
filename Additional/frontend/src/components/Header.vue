<template>
<div>
  <v-layout class="app">
    <v-flex class="header" xs12 my-5 >
        <v-layout row wrap>
          <v-flex xs12 sm8>
            <router-link to="/">
              <img src="@/assets/logo.png" class="logo"/>
              <title>俟翍日報</title>
            </router-link>
          </v-flex>
          <v-flex class="searchPart1" xs4 sm1>
            <v-select
              v-model="searchCategory"
              :items="selectCategory"
              item-text="label"
              item-value="value"
              label="검색 옵션"
              append-icon="fas fa-caret-down"
            >
            </v-select>
          </v-flex>
          <v-flex class="searchPart2" v-if="searchCategory=='date'" xs8 sm3>
            <v-text-field
            v-model="searchKey"
            class="posAuto90"
            append-outer-icon="fas fa-search"
            @click:append-outer="SearchNews()"
            @click.stop="menu = !menu"
            readonly
            ></v-text-field>
            <v-menu
            v-model="menu"
            min-width="290px"
            offset-y
            >
              <template v-slot:activator="{ on }"></template>
              <v-date-picker
              v-model="searchKey"
              prev-icon="fas fa-chevron-left"
              next-icon="fas fa-chevron-right"
              no-title scrollable>
                <v-spacer></v-spacer>
                <v-btn color="primary" @click="menu = false" flat>Cancel</v-btn>
                <v-btn color="primary" @click="$refs.menu.save(date)" flat>OK</v-btn>
              </v-date-picker>
            </v-menu>
          </v-flex>
          <v-flex class="searchPart2" v-else xs8 sm3>
            <v-text-field
            v-model="searchKey"
            class="posAuto90"
            placeholder="검색어를 입력하세요."
            append-outer-icon="fas fa-search"
            @click:append-outer="SearchNews()"
            ></v-text-field>
          </v-flex>
        </v-layout>
        <v-layout class="navi" row wrap>
            <v-flex xs12 sm4>
              <v-btn class="headerButton" to="/" flat> News </v-btn>
              <v-btn class="headerButton" to="AboutUs" flat> About Us </v-btn>

              <!-- chatbot -->
              <v-icon class="chatbotIcon" @click.stop="check_view = !check_view">far fa-comment-dots</v-icon>
              <v-menu class="chat" v-model="check_view" :close-on-content-click="false" :nudge-width="200" offset-y>
                <template v-slot:activator="{ on }"></template>

                <v-card>
                  <v-flex class="chatbox"></v-flex>
                  <textarea class="chattext" v-model="text" @keyup.enter="enter" name="content" rows="2" placeholder="입력하세요."></textarea>
                </v-card>
              </v-menu>

            </v-flex>
            <v-flex hidden-xs-only sm4></v-flex>
            <v-flex xs12 sm4 id="realNewsTitle" >
              <div @click="moveDetailPage()">
                <vue-swimlane :words="newsTitle" :scale="1" :pauseOnHover="true" ></vue-swimlane>
              </div>
            </v-flex>
        </v-layout>
    </v-flex>
  </v-layout>
</div>
</template>

<script>
import Server from "../server.js"
import {store} from "../store.js"

export default {
  name: 'Header',
  store,
  components: {
  },
  data() {
    return {
      NowPage: "AboutUs",
      newsTitle : [""],
      newsAllInfo: [],
      searchKey : "",
      searchCategory: "All",
      selectCategory: [
        {label: "전체", value: "all"},
        {label: "제목", value: "title"},
        {label: "태그", value: "tag"},
        {label: "날짜", value: "date"}
      ],
      menu: false,
      check_view: false,
      text: ""
    }
  },
  mounted() {
      // news title가져와서 실시간 보여주기
      this.getNewsTitle();
  },
  methods: {
    MovePage(location) {
      this.NowPage = location;
    },

    SearchNews() {
      if(this.searchCategory == "all"){
        this.$store.state.searchCategory = this.searchCategory;
        this.$store.state.searchKey = "nullValue";
        this.$store.state.searchCheck = true;
        this.searchKey = "";
        this.searchCategory = "";
      }
      else {
        if(this.searchKey == "" ) {
          alert("검색어를 입력하세요.");
          return false;
        }
        else {
          if(this.searchCategory=="date") {
            this.searchKey = this.searchKey.substring(0,4) + this.searchKey.substring(5,7) + this.searchKey.substring(8,10)
          }
          this.$store.state.searchKey = this.searchKey;
          this.$store.state.searchCategory = this.searchCategory;
          this.$store.state.searchCheck = true;
          this.searchKey = "";
          this.searchCategory = "";
        }
      }
      if(location.pathname != "/"){
        this.$router.push({path: "/"});
      }
    },
    getNewsTitle() {
      const axios = require("axios");
      var today = new Date();
      var day = today.getDate() - 1; // 어제 기사 가져오기
      var month = today.getMonth() + 1;
      var year = today.getFullYear();

      if(month<10) month = "0" + month;

      /* 나중에 삭제해야함 */
          year = "2019";
          month = "09";
          day = "22";
      /* */

      let formData = new FormData();
      formData.append("page", 10);
      formData.append("date", year+""+month+""+day);
      Server(this.$store.state.SERVER_URL).post("/api/get/head_news", formData)
        .then(res => {
          this.newsTitle = [];
          for(var newsIdx in res.data) {
            this.newsTitle.push((parseInt(newsIdx)+1)+". "+res.data[newsIdx].news_title);
          }
          this.newsAllInfo = res.data;
        })
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
      Server(this.$store.state.SERVER_URL).post("/api/chat", form).then(res => {
        select.innerHTML += "<p class='arrow_box_left'>" + JSON.stringify(res.data) + "</p>"
      }).catch(error => {
        console.log(error)
      }).then(()=>{
        select.scrollTop = select.scrollHeight
        document.querySelector('.chattext').value = ''
      })

      this.text = ""
    },
    moveDetailPage() {
      var e = window.event;
      var titleClick = e.target || e.srcElement;
      var eventNum = parseInt(titleClick.innerHTML.substring(0,1));

      this.$store.state.oneNewsInfo = this.newsAllInfo[eventNum-1];

      if(window.location.pathname != "/NewsDetail") {
        this.$router.push({path: "NewsDetail"});
      }
    }
  }
}
</script>


<style lang="scss" scoped>
@import url('https://fonts.googleapis.com/css?family=Ma+Shan+Zheng&display=swap');

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
        color: black;
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

.headerButton {
  background: #00000000 !important;
}

#realNewsTitle {
  font-family: 'Noto Serif KR', serif;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-top: 10px;
  padding-right: 2%;
}

.searchPart1 {
  padding-left: 15px;
  padding-bottom: 5px;
}

.searchPart2 {
  padding-top: 4px;
}

.posAuto90 {
  width: 90%;
  margin: 0 auto;
}

.v-btn--active:before, .v-btn:focus:before, .v-btn:hover:before {
    background-color: #00000000;
}

.chatbotIcon {
  line-height: 15px;
  margin-left: 10px;
  font-size: 30px;
}

.chatbox {
  padding: 10px;
  height: 350px;
  overflow-y:scroll;
  background-color: #F2F2F2;
}

.chat {
  width: 70%;
  margin: auto;
  border-radius: 10%;
}

.chattext {
  width: 100%;
  padding: 10px;
}

@media (min-width : 600px) {
  .header
  title {
    font-size: 5rem;
  }
  .searchPart1 {
    padding: 0 5px;
    padding-top: 36px !important;
  }
  .searchPart2 {
    padding-top: 40px;
  }
}

@media (max-width : 375px) {
  .chat {
    float: left;
    width: 40%;
  }
}
</style>

<style>

.vue-swimlane ul {
  padding-left: 0px !important;
}

#realNewsTitle li {
  width:100%;
  white-space: nowrap;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
  text-align: left;
}
</style>
