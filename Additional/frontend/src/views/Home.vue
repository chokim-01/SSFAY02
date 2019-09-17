<template>
<div class="app">
  <v-layout>
    <v-flex xs12 sm12 my-5>
      <div class="header">

        <img src="@/assets/logo.png" class="logo" />
        <title>맥 짚는 AI</title>

        <div class="navi">
          <div class="text-xs-center">
            <v-btn color="secondary" @click="MovePage('NewsList')"> News </v-btn>
            <v-btn color="secondary" @click="MovePage('Search')"> Search </v-btn>
            <v-btn color="secondary" @click="MovePage('AboutUs')"> About Us </v-btn>
          </div>
        </div>
      </div>
    </v-flex>
  </v-layout>

  <NewsList v-if="NowPage==='NewsList'" />
  <Search v-if="NowPage==='Search'" />
  <AboutUs v-if="NowPage==='AboutUs'" />

</div>
</template>

<script>
import NewsList from '@/components/NewsList.vue'
import Search from '@/components/Search.vue'
import AboutUs from '@/components/AboutUs.vue'

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
    }
  },

  methods: {
    MovePage(location) {
      this.NowPage = location;
      console.log(this.NowPage)
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
    padding: 12px 0;
}

</style>
