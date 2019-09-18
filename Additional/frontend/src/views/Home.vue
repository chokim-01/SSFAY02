<template>
<div class="app">
  <v-layout>
    <v-flex xs12 sm12 my-5>
      <div class="header">

        <img src="@/assets/logo.png" class="logo" @click="MovePage('AboutUs')"/>
        <title>맥 짚는 AI</title>

        <v-layout class="navi">
            <v-flex xs12 sm6>
              <v-btn class="headerBtn" @click="MovePage('NewsList')" flat> News </v-btn>
              <v-btn class="headerBtn" @click="MovePage('Search')" flat> Search </v-btn>
              <v-btn class="headerBtn" @click="MovePage('AboutUs')" flat> About Us </v-btn>
            </v-flex>
            <v-flex hidden-xs-only sm3></v-flex>
            <v-flex xs12 sm3 id="realNewsTitle">
                <vue-swimlane :words="newsTitle" :scale="1.3" :pauseOnHover="true"></vue-swimlane>
            </v-flex>
        </v-layout>
      </div>
    </v-flex>
  </v-layout>

  <NewsList v-if="NowPage==='NewsList'" />
  <Search v-if="NowPage==='Search'" />
  <AboutUs v-if="NowPage==='AboutUs'" />

</div>
</template>

<script>
import NewsList from "@/components/NewsList.vue"
import Search from "@/components/Search.vue"
import AboutUs from "@/components/AboutUs.vue"

export default {
  name: 'home',
  components: {
    NewsList,
    Search,
    AboutUs,
  },
  data() {
    return {
      NowPage: "AboutUs",
      newsTitle : ["1. 나는 사람이다.", "2. 자소서 쓰기 싫어요!", "3. 오늘은 9월 16일", "4. 가나다라가나다라가나다라가나다라가나다라가나다라가나다라"]
    }
  },

  methods: {
    MovePage(location) {
      this.NowPage = location;
    }
  }

}
</script>


<style lang="scss" scoped>
.header {
    text-align: center;
    position: relative;

    .logo {
        width: 80px;
        height: 80px;
    }

    title {
        font-family: 'Droid Serif', serif;
        font-weight: 900;
        font-size: 5rem;
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
</style>
