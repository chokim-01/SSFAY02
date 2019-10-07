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
            <v-flex xs12 sm7 lg4>
              <v-btn class="headerButton" to="/" flat> News </v-btn>
              <v-btn class="headerButton" to="AboutUs" flat> About Us </v-btn>

              <!-- chatbot1 -->
              <v-icon class="chatbotIcon" @click.stop="check_bot_view = !check_bot_view">far fa-comment-dots</v-icon>

              <!-- chat search -->
              <v-icon class="chatIcon" @click.stop="check_chatsearch_view = !check_chatsearch_view">far fa-comments</v-icon>

              <v-menu class="chat" v-model="check_bot_view" :close-on-content-click="false" :nudge-width="200" offset-y>
                <template v-slot:activator="{ on }"></template>

                <v-card>
                  <v-flex>
                    <div class="chatHeader"> 심심이</div>
                    <div class='chatbox'>
                      <div class='botTalk'>
                        <v-layout v-for="(responseItem, index) in chatResponeseItems" :key="responseItem+index" row wrap mt-5>
                          <v-flex xs1>
                            <div class="botCharacter">
                              <img class="botImage" src="@/assets/chick.png">

                            </div>
                          </v-flex>
                          <v-flex xs10>
                            <p class='arrow_box_left' v-html="responseItem" />
                          </v-flex>
                        </v-layout>
                      </div>
                      <div class='loadIcon'>
                        <div class="loader" v-if="load">
                         <div class="circle"></div>
                         <div class="circle"></div>
                         <div class="circle"></div>
                         <div class="circle"></div>
                         <div class="circle"></div>
                        </div>
                      </div>
                    </div>
                  </v-flex>
                  <textarea class="chattext" v-model="text" @keyup.13="enterBot" name="content" rows="2" placeholder="입력하세요."></textarea>
                  <i class="send far fa-paper-plane" @click="enterBot"></i>
                </v-card>
              </v-menu>

              <v-menu class="chat" v-model="check_chatsearch_view" :close-on-content-click="false" :nudge-width="200" offset-y>
                <template v-slot:activator="{ on }"></template>

                <v-card>
                  <v-flex>
                    <div class="chatHeader">뉴스 검색 도우미</div>
                    <div class='chatbox'>
                      <div class='chatSearch'  @click="chatToDetail()" >
                        <v-layout v-for="(chatItem, index) in chatSearchItems" :key="chatItem+chatItem.newsNum" row wrap mt-5>
                          <v-flex xs1>
                            <div class="botCharacter">
                              <img class="botImage" src="@/assets/chick.png">

                            </div>
                          </v-flex>
                          <v-flex xs10>
                            <p class='arrow_box_left' v-html="chatItem.msg" />
                            <p v-if="chatItem.newsNum!=null" class='arrow_box_left'>
                              <span v-bind:value="chatItem.newsNum" class="clickTitle">
                                {{chatItem.newsTitle}}
                              </span>
                              <br><br>
                              <span v-html="chatItem.newsTags" />
                            </p>
                          </v-flex>
                        </v-layout>
                      </div>
                    </div>
                  </v-flex>
                  <textarea class="chattextSearch" v-model="textSearch" @keyup.13="enterChat" name="content" rows="2" placeholder="입력하세요."></textarea>
                  <i class="send far fa-paper-plane" @click="enterChat"></i>
                </v-card>
              </v-menu>
            </v-flex>

            <v-flex hidden-sm-only lg4></v-flex>
            <v-flex id="realNewsTitle" xs12 sm5 lg4>
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
      check_bot_view: false,
      check_chatsearch_view: false,
      text: "",
      textSearch: "",
      load: false,
      chatSearchItems: [],
      chatResponeseItems: []
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
      // 전체 리스트 가져오기
        var today = new Date();
        var yesterday = today.getTime() - (1 * 24 * 60 * 60 * 1000); // 어제 기사 가져오기
        today.setTime(yesterday);
        var day = today.getDate();
        var month = today.getMonth() + 1;
        var year = today.getFullYear();
        if(month<10) month = "0" + month;
        if(day<10) day = "0" + day;

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

    enterBot(){
      // user comment
      this.load = true;
      var select = document.querySelector('.botTalk');

      select.innerHTML += "<p class='arrow_box_right'>"+ this.text +"</p></br>";
      document.querySelector('.chattext').value = '';

      // form data
      var form = new FormData();
      form.append('msg', this.text);

      // chatbot comment
      Server(this.$store.state.SERVER_URL).post("/api/chat", form).then(res => {
        this.chatResponeseItems.push(JSON.stringify(res.data));
      }).catch(error => {

      }).then(()=>{
        this.load = false;
        select.scrollTop = select.scrollHeight;
      })

      this.text = null;
    },

    enterChat(){

      var arrowLeft = "<p class='arrow_box_left'>";
      var arrowRight = "<p class='arrow_box_right'>";
      var arrowEnd = "</p></br>";
      var notFound = "찾으시는 기사가 없어요 ㅠㅠ";
      var catchFound = "이 기사를 찾으셨나요?";
      var select = document.querySelector('.chatSearch');

      select.innerHTML += arrowRight + this.textSearch + arrowEnd;
      document.querySelector('.chattextSearch').value = '';

      // form data
      var form = new FormData()
      form.append('msg', this.textSearch);

      // chatbot search
      Server(this.$store.state.SERVER_URL).post("/api/get/chat", form).then(res => {
        if(res.data == "False"){
          let chatSearchOne = {
            msg : notFound,
            newsTitle : null,
            newsNum: null,
            newsTags : null
          };

          this.chatSearchItems.push(chatSearchOne);

          return;
        }

        let tags = "태그 : "
        for(let data of res.data){
          tags += "<span style='border-radius: 20px; background-color:white; margin: 0px 5px; border: 1px dotted gray; padding: 0px 5px 0px 2px;'> #"+data["newstag_name"] + "</span>";
        }

        let chatSearchOne = {
          msg : catchFound,
          newsTitle : "제목 : " + JSON.stringify(res.data[0]["news_title"]),
          newsNum: res.data[0]["news_num"],
          newsTags : tags
        };

        this.chatSearchItems.push(chatSearchOne);

      }).catch(error => {

      }).then(()=>{
        select.scrollTop = select.scrollHeight
      })

      this.textSearch = null
    },

    moveDetailPage() {
      var e = window.event;
      var titleClick = e.target || e.srcElement;
      var eventNum = parseInt(titleClick.innerHTML.substring(0,1));

      this.$store.state.oneNewsInfo = this.newsAllInfo[eventNum-1];

      if(window.location.pathname != "/NewsDetail") {
        this.$router.push({path: "NewsDetail"});
      }
    },

    chatToDetail() {
      var e = window.event;
      var titleClick = e.target || e.srcElement;

      // 뉴스 가져와서 store에 저장
      var form = new FormData();
      form.append('news_num', titleClick.getAttribute("value"));

      Server(this.$store.state.SERVER_URL).post("/api/get/one_news", form).then(res => {
        this.$store.state.oneNewsInfo = res.data[0];
      }).catch(error => {

      }).then(()=>{
        this.check_chatsearch_view = !this.check_chatsearch_view;
      })

      setTimeout(() => {
        if(window.location.pathname != "/NewsDetail") {
          this.$router.push({path: "NewsDetail"});
        }
      }, 400);
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
        font-weight: 400;
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
  cursor: pointer;
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
  margin-right: 14px;
}

.chatIcon {
  line-height: 15px;
  margin-left: 10px;
  font-size: 30px;
}

.chatbox {
  padding: 10px;
  height: 350px;
  background-color: #F2F2F2;
}

.botTalk {
  width:100%;
  max-height: 300px;
  overflow-y:scroll;
  overflow-x:hidden;
}

.chatSearch {
  width:100%;
  max-height: 300px;
  overflow-y:scroll;
  overflow-x:hidden;
}

.botCharacter {
  margin: 0 auto;
  margin-top: 5px;
  border-radius: 50%;
  background-color: #F2F5A9;
  width:40px;
  height:40px;
}

.botImage {
  width:inherit;
  height:inherit;
}

.chatHeader {
  color: #084B8A;
  font-size:20px;
  text-align: center;
}

.chat {
  width: 70%;
  height: auto;
  margin: auto;
  border-radius: 10%;
}

.chattext {
  width: 88%;
}

.chattextSearch {
  width: 88%;
}

.clickTitle {
  font-weight: bold;
}

.clickTitle:hover {
  text-decoration : underline;
  cursor: pointer;
}

.send {
  float: right;
  font-size: 30px;
  margin-top: 5px;
  margin-right: 15px;
}

.loader {
   width: 50px;
   height: 50px;
   margin: auto;
   float: left;
   clear: both;
   margin-left: 30px;
   margin-bottom: -10px;
}

.loader .circle {
   position: absolute;
   width: 20px;
   height: 20px;
   opacity: 0;
   transform: rotate(225deg);
   animation-iteration-count: infinite;
   animation-name: orbit;
   animation-duration: 4s;
}

.loader .circle:after {
   content: "";
   position: absolute;
   width: 4px;
   height: 4px;
   border-radius: 5px;
   background: #828282;
   box-shadow: 0 0 9px rgba(255, 255, 255, 0.7);
}

.loader .circle:nth-child(2) {
   animation-delay: 240ms;
}

.loader .circle:nth-child(3) {
   animation-delay: 480ms;
}

.loader .circle:nth-child(4) {
   animation-delay: 720ms;
}

.loader .circle:nth-child(5) {
   animation-delay: 960ms;
}

@keyframes orbit {
   0% {
       transform: rotate(225deg);
       opacity: 1;
       animation-timing-function: ease-out;
   }
   7% {
       transform: rotate(345deg);
       animation-timing-function: linear;
   }
   30% {
       transform: rotate(455deg);
       animation-timing-function: ease-in-out;
   }
   39% {
       transform: rotate(690deg);
       animation-timing-function: linear;
   }
   70% {
       transform: rotate(815deg);
       opacity: 1;
       animation-timing-function: ease-out;
   }
   75% {
       transform: rotate(945deg);
       animation-timing-function: ease-out;
   }
   76% {
       transform: rotate(945deg);
       opacity: 0;
   }
   100% {
       transform: rotate(945deg);
       opacity: 0;
   }
}

@media (max-width : 600px) {
  .v-menu__content {
    width: 80% !important;
    min-width: 0px !important;
  }

  .send {
    margin-right: 7px;
    transform: scale(0.7);
  }

  .chatbox {
    font-size: 12px;
  }

  .chattextSearch, .chattext {
    width: 80%;
  }
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
