<template>
  <div>
    <v-layout v-if="this.$store.state.searchCheck">
      <v-flex class="text-xs-right">{{ findKey }}</v-flex>
    </v-layout>
    <v-layout class="content" row wrap>
      <v-flex class="collumn" v-for="newsOne in newsList" :key="newsOne.news_num" @click="moveDetail(newsOne)">
        <div class="head">
          <span class="headline hl3">
          </span>
          <p><span class="headline hl4">{{newsOne.news_title}}</span></p>
        </div>
        <div class="newsContent" v-html="newsOne.news_context"></div>
      </v-flex>
    </v-layout>
    <div class="text-xs-center">
      <div>
        <v-btn color="primary" @click="movePage('back')" fab small dark>
            <v-icon>fas fa-chevron-left</v-icon>
        </v-btn>
        <v-btn color="primary"  style="width:88px;" round dark>
          <span v-if="isSearchPage" @click="checkSearchPage = !checkSearchPage">{{page}} / {{totalPage}}</span>
          <input v-else type="number" v-model="pageNum" @keyup.enter="getNewsList('page')" style="width:70px;">
        </v-btn>
        <v-btn color="primary" @click="movePage('next')" fab small dark>
            <v-icon>fas fa-chevron-right</v-icon>
        </v-btn>
      </div>
    </div>
  </div>
</template>

<script>
import Server from "../server.js"
import {store} from "../store.js"

import NewsDetail from "@/components/NewsDetail.vue"

export default {
  name: 'NewsList',
  data() {
    return {
      page: 1,
      totalPage: 99,
      searchPage: 1,
      pageNum: "",
      newsList: [{news_context:"", news_date:"", news_num:"", news_title:""}],
      checkSearchPage: true,
      searchKey: this.$store.state.searchKey,
      searchCategory: this.$store.state.searchCategory,
      directPage: {"back": -1, "next": 1},
      loadCount: 3
    }
  },
  components: {
    NewsDetail
  },
  mounted() {
    this.getNewsList();
    this.$store.state.searchCheck = false;
  },
  computed: {
    findKey() {
      if(this.searchKey != this.$store.state.searchKey) {
        this.searchKey = this.$store.state.searchKey;
        this.searchCategory = this.$store.state.searchCategory;
        this.getNewsList();
      }

      if(this.searchCategory == "all")
        var str = "["+this.$store.state.searchLabel[0][this.searchCategory]+"] 검색한 결과입니다." ;
      else
        var str = "["+this.$store.state.searchLabel[0][this.searchCategory]+"] ' "+this.searchKey+" '(으)로 검색한 결과입니다." ;
      return str;
    },
    isSearchPage() {
      return this.checkSearchPage;
    }
  },
  methods: {
    getNewsList(opt) {
      if(this.$store.state.searchCategory=='' || this.$store.state.searchCategory=='all'){
        // 전체 리스트 가져오기
        var today = new Date();
        var yesterday = today.getTime() - (1 * 24 * 60 * 60 * 1000); // 어제 기사 가져오기
        today.setTime(yesterday);
        var day = today.getDate();
        var month = today.getMonth() + 1;
        var year = today.getFullYear();
        if(month < 10)
          month = "0" + month;
        if(day < 10)
          day = "0" + day;
        if(opt == "page") {
          this.page = this.pageNum;
        }
        else {
          this.page = 1;
        }

        let formData = new FormData();
        formData.append("page", this.page);

        formData.append("date", year+""+month+""+day);
        Server(this.$store.state.SERVER_URL).post("/api/get/news", formData)
          .then(res => {
            this.newsList = res.data;
          })

        Server(this.$store.state.SERVER_URL).post("/api/get/news_count", formData)
          .then(res => {
            this.totalPage = Math.floor(res.data[0]["count(*)"]/this.loadCount);
            if(res.data[0]["count(*)"]%this.loadCount!=0){
              this.totalPage += 1;
            }
            if(this.checkSearchPage == false) {
              this.checkSearchPage = true;
            }
          })
      }
      else {
        // 검색 리스트 가져오기
        if(opt == "page"){
          this.page = this.pageNum;
        }
        else {
          this.page = 1;
        }
        let formData = new FormData();
        formData.append("searchCategory", this.searchCategory);
        formData.append("searchKey", this.searchKey);
        formData.append("page", this.page);
        Server(this.$store.state.SERVER_URL).post("/api/get/search", formData)
          .then(res => {
            this.newsList = res.data;
        })
        Server(this.$store.state.SERVER_URL).post("/api/get/search_count", formData)
          .then(res => {
            this.totalPage = Math.floor(res.data[0]["count(*)"]/this.loadCount);
            if(res.data[0]["count(*)"]%this.loadCount!=0){
              this.totalPage += 1;
            }
            if(this.checkSearchPage == false) {
              this.checkSearchPage = true;
            }
        })
      }
    },
    moveDetail(newsObj) {
      this.$store.state.oneNewsInfo = newsObj;
      this.$router.push({path: "NewsDetail"});
    },
    movePage(dir) {
      if(this.page==1 && dir=="back")
        alert("첫 페이지입니다.");
      else if(this.page==this.totalPage && dir=="next")
        alert("마지막 페이지입니다.");
      else {
        this.pageNum = parseInt(this.page) + parseInt(this.directPage[dir]);
        this.getNewsList("page");
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.content {
    font-family: 'Droid Serif', serif;
    font-size: 14px;
    line-height: 0;
    display: inline-block;
    margin-left: 3%;
    box-sizing: content-box !important;
}

.collumn {
    text-decoration: none;
    color: black;
    font-size: 14px;
    line-height: 20px;
    width: 30.5%;
    display: inline-block;
    padding: 0 1%;
    vertical-align: top;
    margin-bottom: 20px;
    transition: all 0.7s;
}

.collumn:hover{
  box-shadow: 4px 4px 10px 4px gray;
  cursor: pointer;
}

.collumn + .collumn {
    border-left: 1px solid #2f2f2f;
}

.collumn .headline {
    text-align: center;
    line-height: normal;
    font-family: 'Playfair Display', serif;
    display: block;
    margin: 0 auto;
}

.collumn .headline.hl1 {
    font-weight: 700;
    font-size: 30px;
    text-transform: uppercase;
    padding: 10px 0;
}

.collumn .headline.hl2 {
    font-weight: 400;
    font-style: italic;
    font-size: 24px;
    box-sizing: border-box;
    padding: 10px 0;
}

.collumn .headline.hl2:before {
    border-top: 1px solid #2f2f2f;
    content: '';
    width: 100px;
    height: 7px;
    display: block;
    margin: 0 auto;
}

.collumn .headline.hl2:after {
    border-bottom: 1px solid #2f2f2f;
    content: '';
    width: 100px;
    height: 13px;
    display: block;
    margin: 0 auto;
}

.collumn .headline.hl3 {
    font-weight: 400;
    font-style: italic;
    font-size: 36px;
    box-sizing: border-box;
    padding: 10px 0;
}

.collumn .headline.hl4 {
    font-weight: 700;
    font-size: 12px;
    box-sizing: border-box;
    padding: 10px 0;
}

.collumn .headline.hl4:before {
    border-top: 1px solid #2f2f2f;
    content: '';
    width: 100px;
    height: 7px;
    display: block;
    margin: 0 auto;
}

.collumn .headline.hl4:after {
    border-bottom: 1px solid #2f2f2f;
    content: '';
    width: 100px;
    height: 10px;
    display: block;
    margin: 0 auto;
}

.collumn .headline.hl5 {
    font-weight: 400;
    font-size: 42px;
    text-transform: uppercase;
    font-style: italic;
    box-sizing: border-box;
    padding: 10px 0;
}

.collumn .headline.hl6 {
    font-weight: 400;
    font-size: 18px;
    box-sizing: border-box;
    padding: 10px 0;
}

.collumn .headline.hl6:before {
    border-top: 1px solid #2f2f2f;
    content: '';
    width: 100px;
    height: 7px;
    display: block;
    margin: 0 auto;
}

.collumn .headline.hl6:after {
    border-bottom: 1px solid #2f2f2f;
    content: '';
    width: 100px;
    height: 10px;
    display: block;
    margin: 0 auto;
}

.collumn .headline.hl7 {
    font-weight: 700;
    font-size: 12px;
    box-sizing: border-box;
    display: block;
    padding: 10px 0;
}

.collumn .headline.hl8 {
    font-weight: 700;
    font-size: 12px;
    box-sizing: border-box;
    padding: 10px 0;
}

.collumn .headline.hl9 {
    font-weight: 700;
    font-size: 12px;
    box-sizing: border-box;
    padding: 10px 0;
}

.collumn .headline.hl10 {
    font-weight: 700;
    font-size: 12px;
    box-sizing: border-box;
    padding: 10px 0;
}

.collumn .citation {
    font-family: 'Playfair Display', serif;
    font-size: 36px;
    line-height: 44px;
    text-align: center;
    font-weight: 400;
    display: block;
    margin: 40px 0;
    font-feature-settings: "liga", "dlig";
}
.collumn .citation:before {
    border-top: 1px solid #2f2f2f;
    content: '';
    width: 100px;
    height: 16px;
    display: block;
    margin: 0 auto;
}

.collumn .citation:after {
    border-bottom: 1px solid #2f2f2f;
    content: '';
    width: 100px;
    height: 16px;
    display: block;
    margin: 0 auto;
}

.collumn .figure {
    margin: 0 0 20px;
}

.collumn .figcaption {
    font-style: italic;
    font-size: 12px;
}

.media {
    -webkit-filter: sepia(80%) contrast(1) opacity(0.8);
    filter: sepia(80%) grayscale(1) contrast(1) opacity(0.8);
    mix-blend-mode: multiply;
    width: 100%;
}

.head {
  height: 170px;
}

@media only all and (max-width: 1300px) {
    .weatherforcastbox {
        display: none;
    }

    .head {
      height: 170px;
    }
}

@media only all and (max-width: 1200px) {
    .collumn {
        width: 31%;
    }

    .head {
      height: 180px;
    }
}

@media only all and (max-width: 900px) {
    .collumn {
        width: 47%;
    }

    .head {
      height: 170px;
    }
}

@media only all and (max-width: 600px) {
    .collumn {
        width: 98%;
    }

    .collumn + .collumn {
        border-left: none;
        border-bottom: 1px solid #2f2f2f;
    }

    header {
        max-width: 320px;
        font-size: 60px;
        line-height: 54px;
        overflow: hidden;
    }

    .head {
      height: 160px;
    }
}
</style>


<style>
.v-responsive {
  height: auto !important;
}

.v-window {
  height: auto !important;
}

.v-carousel__next .v-btn,
.v-carousel__prev .v-btn {
  color: black !important;
}

.newsContent {
  font-family: "Noto Serif KR", serif;
  font-size: 16px;
  line-height: 1.5em;
  white-space: pre-wrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  height: 37.5em;
  -webkit-line-clamp: 25;
  -webkit-box-orient: vertical;
  word-wrap: break-word;
}
</style>
