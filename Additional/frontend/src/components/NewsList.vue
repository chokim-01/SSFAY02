<template>
  <v-container>
    <v-card id="realNewsTitle">
      <vue-swimlane :words="newsTitle" :scale="3"></vue-swimlane>
    </v-card>

    <v-layout row wrap>
      <v-flex xs6>
        <v-text-field
        label="검색어를 입력하세요."
        solo
        ></v-text-field>
      </v-flex>
      <v-btn color="success">Success</v-btn>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  name: "newsList",
  data () {
    return {
      newsTitle : ["1. 나는 사람이다.", "2. 자소서 쓰기 싫어요!", "3. 오늘은 9월 16일", "4. 가나다라가나다라가나다라가나다라가나다라가나다라가나다라"]
    }
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css?family=Noto+Serif+KR&display=swap');

#realNewsTitle {
  font-family: 'Noto Serif KR', serif;
  width: 80%;
  margin: 50px auto;
  overflow: hidden;
  text-overflow: ellipsis;
}

</style>
