<template>
<v-layout row wrap>
  <v-flex class="posCenter" xs12 sm8 mb-2>
    <v-layout row wrap pb-4>
      <v-flex id="newspaperTitle" xs12>
        {{ detailTitle }}
      </v-flex>
      <v-flex class="text-xs-center" xs12 mb-4>
        <v-chip v-for="idx in 6" :key="idx" color="red" outline>
          <!--  임시 -->
          # 블라블라
        </v-chip>
      </v-flex>
      <v-flex class="text-xs-right" xs12 px-4>{{dateFormmat}}</v-flex>
      <v-flex id="newspaperContent" xs12 pa-3>
        {{ detailContext }}
      </v-flex>
    </v-layout>
  </v-flex>
  <v-flex id="newspaperGraph" xs12 mb-5 pa-3>
    <v-layout row wrap>
      <v-flex xs12 sm1 />
      <v-flex xs12 sm5>
        <canvas id="PNChart" width="300" height="300" />
      </v-flex>
      <v-flex xs12 sm4 mt-5>
        <canvas id="TimeChart" width="300" height="300" />
      </v-flex>
    </v-layout>
  </v-flex>
  <v-flex class="posCenter" xs12 sm8 mb-5>

    <v-card id="newsComment" flat>

      <v-layout class="mh50" row wrap>
        <v-flex xs3 sm2>
          <h2>댓글 {{commentsCount}}개</h2>
        </v-flex>
        <v-flex xs7 sm9></v-flex>
        <v-flex xs2 sm1>
          <v-btn @click="showLocalFunc()">지역감정보기</v-btn>
        </v-flex>
      </v-layout>

      <v-list id="newsCommentList">
        <template v-for="comment in comments" class="cmtRow" v-if="showLocal">
          <v-layout class="mh50" row wrap>
            <v-flex class="newsCommentRow" xs12 sm2><b>{{comment.comment_time}}</b></v-flex>
            <v-flex class="newsCommentRow" v-text="comment.comment_context" xs10 sm9></v-flex>
            <v-flex xs2 sm1 v-if="comment.label_news == '0'">
              <v-chip id="newsThumbs" text-color="red" label>
                <v-icon right>fas fa-thumbs-down</v-icon>
              </v-chip>
            </v-flex>
            <v-flex xs2 sm1 v-else>
              <v-chip id="newsThumbs" text-color="blue" label>
                <v-icon right>fas fa-thumbs-up</v-icon>
              </v-chip>
            </v-flex>
          </v-layout>
        </template>

        <template v-for="comment in comments" class="cmtRow" v-if="!showLocal && comment.label_local =='0' ">
          <v-layout class="mh50" row wrap>
            <v-flex class="newsCommentRow" xs12 sm2><b>{{comment.comment_time}}</b></v-flex>
            <v-flex class="newsCommentRow" v-text="comment.comment_context" xs10 sm9></v-flex>
            <v-flex xs2 sm1 v-if="comment.label_news == '0'">
              <v-chip id="newsThumbs" text-color="red" label>
                <v-icon right>fas fa-thumbs-down</v-icon>
              </v-chip>
            </v-flex>
            <v-flex xs2 sm1 v-else>
              <v-chip id="newsThumbs" text-color="blue" label>
                <v-icon right>fas fa-thumbs-up</v-icon>
              </v-chip>
            </v-flex>
          </v-layout>
        </template>


      </v-list>

      <!-- paging button -->
      <v-layout class="mh50 paging" row wrap>

        <div v-if="thisPage != 1" @click="getComments(1)">처음</div>

        <div class="" v-for="i in pageList">
          <div @click="getComments(i)" class="thisPageClass pageButton" v-if="i === thisPage">{{i}}</div>
          <div @click="getComments(i)" class="pageButton" v-else>{{i}}</div>
        </div>

        <div v-model="finalPage" @click="getComments(finalPage)">마지막</div>

      </v-layout>

    </v-card>
  </v-flex>
</v-layout>
</template>

<script>
import Chart from "chart.js";
export default {
  name: "NewsDetail",
  data() {
    return {
      detailTitle: this.$route.params.detailTitle,
      detailContext: this.$route.params.detailContext,
      detailDate: this.$route.params.detailDate,
      detailNum: this.$route.params.detailNum,
      myDoughnutChart: null,
      doughnutData: null,
      comments: [],
      pageList: [],
      thisPage: 1,
      finalPage: 0,
      commentsCount: 0,
      positiveCount: 0,
      localCount: 0,
      commentTime: [],
      showLocal: true,
      commentPage: 1,
    }
  },
  created() {
    this.getComments(1);
  },
  mounted() {
    this.getCommentsInfo();
    this.getCommentsTime();

    setTimeout(() => {
      var docPNChart = document.getElementById("PNChart");
      var pnChart = new Chart(docPNChart, {
        type: "doughnut",
        data: {
          labels: ["긍정", "부정"],
          datasets: [{
            label: "# of Votes",
            data: [this.positiveCount, (this.commentsCount - this.positiveCount)],
            backgroundColor: [
              "#01A9DB",
              "#FE2E64"
            ]
          }]
        },
        options: {
          maintainAspectRatio: false
        }
      });

      var docTimeChart = document.getElementById("TimeChart").getContext("2d");
      var TimeChart = new Chart(docTimeChart, {
        type: "line",
        data: {
          labels: ["12am", "1am", "2am", "3am", "4am", "5am", "6am", "7am", "8am", "9am", "10am", "11am", "12am"],
          datasets: [{
            label: "시간대별 댓글 작성 추이",
            data: this.commentTime,
            borderColor: "#FA5882",
            backgroundColor: "#00000000",
            type: "line",
            pointRadius: 0,
            fill: false,
            lineTension: 0,
            borderWidth: 2
          }]
        },
        options: {
          scales: {
            yAxes: [{
              ticks: {
                /*    beginAtZero: true, */
              }
            }]
          }
        },
      });
    }, 300);

  },
  computed: {
    dateFormmat() {
      var dDate = this.detailDate + "";
      return dDate.substring(0, 4) + " - " + dDate.substring(4, 6) + " - " + dDate.substring(6, 8);
    }
  },

  methods: {
    // Get Comment
    getComments(page) {
      const axios = require("axios");
      let formData = new FormData();
      this.thisPage = page;
      this.getPages(this.thisPage);
      formData.append("news_num", this.detailNum);
      formData.append("page", this.thisPage);
      axios.post("http://localhost:5000/api/get/comments", formData)
        .then(res => {
          this.comments = res.data;
        })
    },

    // Get Final Page Number and Page Number List
    getPages(page) {
      const axios = require("axios");
      var self = this;
      var formData = new FormData();
      this.thisPage = page;
      formData.append("news_num", this.detailNum);
      formData.append("page", this.thisPage);
      axios.post("http://localhost:5000/api/get/page_count", formData)
        .then(res => {
          self.pageList = res.data.page_list;
          self.finalPage = res.data.final_page;
        });
    },
    //get label of Comments
    getCommentsInfo() {
      const axios = require("axios");
      let formData = new FormData();
      formData.append("news_num", this.detailNum);
      axios.post("http://localhost:5000/api/get/comments_label", formData)
        .then(res => {
          this.commentsCount = res.data[0].comment_cnt;
          this.positiveCount = res.data[0].news_positive;
          this.localCount = res.data[0].comment_cnt;
        })
    },
    // Get Chart Time
    getCommentsTime() {
      const axios = require("axios");
      let formData = new FormData();
      formData.append("news_num", this.detailNum);
      axios.post("http://localhost:5000/api/get/comments_time", formData)
        .then(res => {
          this.commentTime = res.data;
          for (var i = 0; i < res.data.length; i++) {
            this.commentTime[i] = res.data[i].hour_cnt;
          }
        })
    },
    // Show Regional sentiment
    showLocalFunc() {
      this.showLocal = !this.showLocal
    }
  }
}
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css?family=Song+Myung&display=swap");
@import url("https://fonts.googleapis.com/css?family=Noto+Serif+KR&display=swap");

.posCenter {
  margin: 0 auto;
}

.commentPN {
  height: 35px !important;
  overflow: hidden;
}

.commentPage {
  text-align: center;
  margin-top: 20px;
}

#newspaper {
  height: auto;
  background-color: #00000000;
}

#newspaperTitle {
  font-family: "Song Myung", serif;
  font-size: 50px;
  text-align: center;
}

#newspaperContent {
  font-family: "Noto Serif KR", serif;
  overflow-y: scroll;
  height: 520px;
}

#newspaperGraph {
  overflow: hidden;
  text-align: center;
}

#PNChart {
  margin: 0 auto;
  margin-top: 30px;
}

#PNChart,
#TimeChart {
  max-height: 300px;
}

::-webkit-scrollbar {
  height: 100%;
}

::-webkit-scrollbar-thumb {
  border-radius: 20px;
  height: 5px;
  background-color: #BDBDBD;
}

#newsComment {
  heigth: auto;
  min-height: 300px;
  padding: 20px;
  background-color: inherit;
}

#newsCommentList {
  background-color: inherit;
}

#newsThumbs {
  background-color: inherit;
}

.newsCommentRow {
  padding: 12px 0px;
}

.cmtRow {
  height: 35px !important;
  overflow: hidden;
}

.mh50 {
  min-height: 50px;
}


.theme--light.v-pagination .v-pagination__item--active {
  color: black !important;
  border: 1px solid blue !important;
}

@media (max-width: 600px) {
  #newspaperTitle {
    font-size: 35px;
  }

  #newsComment .v-list__tile {
    padding: 0px 0px !important;
  }
}

@media (min-width: 600px) {
  #PNChart {
    margin-left: 8%;
  }

  #newspaperContent {
    column-count: 2 !important;
    max-height: none;
    height: auto;
    overflow: visible;
  }

  .thisPageClass {
    color: black;
    font-size: 1.8rem;
    font-weight: bold;
  }

  .pageButton {
    background: -webkit-gradient(linear, left top, left bottom, color-stop(0.05, #ffffff), color-stop(1, #f6f6f6));
    background: -moz-linear-gradient(top, #ffffff 5%, #f6f6f6 100%);
    background: -webkit-linear-gradient(top, #ffffff 5%, #f6f6f6 100%);
    background: -o-linear-gradient(top, #ffffff 5%, #f6f6f6 100%);
    background: -ms-linear-gradient(top, #ffffff 5%, #f6f6f6 100%);
    background: linear-gradient(to bottom, #ffffff 5%, #f6f6f6 100%);
    filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#ffffff', endColorstr='#f6f6f6', GradientType=0);
    background-color: #ffffff;
    -moz-border-radius: 3px;
    -webkit-border-radius: 3px;
    border-radius: 3px;
    border: 2px solid #dcdcdc;
    display: inline-block;
    cursor: pointer;
    color: #826d73;
    font-family: Arial;
    font-size: 16px;
    padding: 6px 9px;
    text-decoration: none;
  }

  .pageButton:hover {
    background: -webkit-gradient(linear, left top, left bottom, color-stop(0.05, #f6f6f6), color-stop(1, #ffffff));
    background: -moz-linear-gradient(top, #f6f6f6 5%, #ffffff 100%);
    background: -webkit-linear-gradient(top, #f6f6f6 5%, #ffffff 100%);
    background: -o-linear-gradient(top, #f6f6f6 5%, #ffffff 100%);
    background: -ms-linear-gradient(top, #f6f6f6 5%, #ffffff 100%);
    background: linear-gradient(to bottom, #f6f6f6 5%, #ffffff 100%);
    filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#f6f6f6', endColorstr='#ffffff', GradientType=0);
    background-color: #f6f6f6;
  }

  .pageButton:active {
    position: relative;
    top: 1px;
  }
}
</style>
