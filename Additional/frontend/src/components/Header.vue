<template>
<div>
  <v-layout class="app">
    <v-flex class="header" xs12 my-5 >
        <v-layout row wrap>
          <v-flex xs12 sm8>
            <router-link to="/"><img src="@/assets/logo.png" class="logo"/></router-link>
            <title>맥 짚는 AI</title>
          </v-flex>
          <v-flex class="searchPart1" xs4 sm1>
            <v-select
              :items="selectCat"
              label="검색 옵션"
              append-icon="fas fa-caret-down"
              v-model="searchCat"
            >
            </v-select>
          </v-flex>
          <v-flex class="searchPart2" v-if="searchCat=='날짜'" xs8 sm3>
            <v-text-field
            v-model="searchKey"
            readonly
            style="width: 90%; margin: 0 auto;"
            append-outer-icon="fas fa-search"
            @click:append-outer="SearchNews()"
            @click.stop="menu = !menu"
            ></v-text-field>
            <v-menu
            v-model="menu"
            offset-y
            min-width="290px"
            >
              <template v-slot:activator="{ on }"></template>
              <v-date-picker
              v-model="searchKey"
              prev-icon="fas fa-chevron-left"
              next-icon="fas fa-chevron-right"
              no-title scrollable>
                <v-spacer></v-spacer>
                <v-btn flat color="primary" @click="menu = false">Cancel</v-btn>
                <v-btn flat color="primary" @click="$refs.menu.save(date)">OK</v-btn>
              </v-date-picker>
            </v-menu>
          </v-flex>
          <v-flex class="searchPart2" v-else xs8 sm3>
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
            </v-flex>
            <v-flex hidden-xs-only sm3></v-flex>
            <v-flex xs12 sm5 id="realNewsTitle">
                <vue-swimlane :words="newsTitle" :scale="1" :pauseOnHover="true"></vue-swimlane>
            </v-flex>
        </v-layout>
    </v-flex>
  </v-layout>
</div>
</template>

<script>
export default {
  name: 'Header',
  components: {
  },
  data() {
    return {
      NowPage: "AboutUs",
      newsTitle : [""],
      searchKey : "",
      searchCat: "전체",
      selectCat: ['전체', '제목', '태그', '날짜'],
      menu: false,
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
      if(this.searchCat == "전체"){
        this.$store.state.searchCat = this.searchCat;
        this.$store.state.searchKey = "nullValue";
        this.$store.state.searchChk = true;
        this.searchKey = "";
        this.searchCat = "";
        return true;
      }
      else {
        if(this.searchKey == "" ) {
          alert("검색어를 입력하세요.");
          return false;
        }
        else {
          if(this.searchCat=="날짜") {
            this.searchKey = this.searchKey.substring(0,4) + this.searchKey.substring(5,7) + this.searchKey.substring(8,10)
          }
          this.$store.state.searchKey = this.searchKey;
          this.$store.state.searchCat = this.searchCat;
          this.$store.state.searchChk = true;
          this.searchKey = "";
          this.searchCat = "";
        }
      }
    },
    getNewsTitle() {
      const axios = require("axios");
      var today = new Date();
      var day = today.getDate() - 1; // 어제 기사 가져오기
      var month = today.getMonth() + 1;
      var year = today.getFullYear();

      if(month<10) month = "0" + month;

      day-=7; // 나중에 지울것

      let formData = new FormData();
      formData.append("page", 1);
      formData.append("date", year+""+month+""+day);
      axios.post("http://localhost:5000/api/get/news", formData)
        .then(res => {
          for(var newsIdx in res.data) {
            this.newsTitle.push((parseInt(newsIdx)+1)+". "+res.data[newsIdx].news_title);
          }
        })
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
  margin-top: 10px;
}
.searchPart1 {
  padding-left: 15px;
  padding-bottom: 5px;
}
.searchPart2 {
  padding-top: 4px;
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

.v-btn--active:before, .v-btn:focus:before, .v-btn:hover:before {
    background-color: #00000000;
}

</style>
