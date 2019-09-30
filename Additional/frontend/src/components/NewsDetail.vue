<template>
<v-layout row wrap>
  <v-flex class="positionCenter" xs12 sm8 mb-2>
    <v-layout row wrap pb-4>
      <v-flex id="newspaperTitle" xs12>
        {{ detailTitle }}
      </v-flex>

      <!-- Get Tags -->
      <v-flex class="text-xs-center" xs12 mb-4>
        <template v-for="tag in tags">
          <v-chip color="red" outline>
            {{tag.tag_name}}
          </v-chip>
        </template>
      </v-flex>

      <v-flex class="text-xs-right" xs12 px-4>{{dateFormmat}}</v-flex>
      <v-flex id="newspaperContent" xs12 pa-3>
        {{ detailContext }}
      </v-flex>
    </v-layout>
  </v-flex>


  <!-- Comments Chart -->
  <v-flex class="positionCenter" xs12 sm8 mb-5 >
    <hr>
    <h1 id="textCenter">데이터 분석</h1>

    <v-layout row wrap>
      <v-flex xs12 sm1 />
      <v-flex xs12 sm4>
        <h2 class="chartTitle">댓글 긍/부정</h2>
        <canvas id="PNChart" width="300" height="300" />
      </v-flex>
      <v-flex xs12 sm2 />
      <v-flex xs12 sm4 >
        <h2 class="chartTitle" >시간대별 댓글 작성 추이</h2>
        <canvas id="TimeChart" width="300" height="300" />
      </v-flex>
    </v-layout>
  </v-flex>

  <!--Comments Title  -->
  <v-flex class="positionCenter" xs12 sm8 mb-5>
    <hr>
    <h1  id="textCenter">댓글 분석</h1>
    <v-card id="newsComment" flat>
      <v-layout class="mh50" row wrap>
        <v-flex xs12 sm5>
          <h2>댓글 {{commentsCount}}개 <span class="newsCommentLocal"> ( 지역감정 {{localCount}} 개 ) </span></h2>
        </v-flex>
        <v-flex xs6 sm4></v-flex>
        <v-flex xs6 sm3>
          <div class="checks etrans">
            <input type="checkbox" id="ex_chk3" @click="showLocalFunc">
            <label for="ex_chk3">지역감정 숨기기</label>
          </div>
        </v-flex>
      </v-layout>

      <!-- Show local sentiment-->
      <v-list id="newsCommentList">
        <template v-for="comment in comments" class="cmtRow" v-if="showLocal">
          <v-layout class="mh50" row wrap>
            <v-flex class="newsCommentRow" xs12 sm2><b>{{ timeChang(comment.comment_time) }}</b></v-flex>
            <v-flex :class="[ comment.label_local =='1' ? 'newsCommentRow isLocalComment' : 'newsCommentRow']" v-text="comment.comment_context" xs8 sm8></v-flex>

            <!-- 댓글 긍/부정 -->
            <v-flex v-if="comment.label_news == '0'" xs2 sm1>
              <v-chip id="newsThumbs" text-color="red" label>
                <v-icon right @click="editCommentLabelNews(comment)">fas fa-thumbs-down</v-icon>
              </v-chip>
            </v-flex>

            <v-flex v-else xs2 sm1>
              <v-chip id="newsThumbs" text-color="blue" label>
                <v-icon right @click="editCommentLabelNews(comment)">fas fa-thumbs-up</v-icon>
              </v-chip>
            </v-flex>


            <!-- 지역감정 -->
            <v-flex xs2 sm1 v-if="comment.label_local == '0'">
              <v-chip id="newsThumbs" text-color="blue" label>
                <v-icon right @click="editCommentLabelLocal(comment)">far fa-smile</v-icon>
              </v-chip>
            </v-flex>

            <v-flex v-else xs2 sm1>
              <v-chip id="newsThumbs" text-color="red" label>
                <v-icon right @click="editCommentLabelLocal(comment)">far fa-angry</v-icon>
              </v-chip>
            </v-flex>

          </v-layout>
        </template>

        <!-- Hide local sentiment-->
        <template v-for="comment in comments" class="cmtRow" v-if="!showLocal && comment.label_local =='0' ">
          <v-layout class="mh50" row wrap>
            <v-flex class="newsCommentRow" xs12 sm2><b>{{ timeChang(comment.comment_time) }}</b></v-flex>
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
        <v-flex class="text-xs-center" xs12 sm 12>
          <div>
            <div class="pageButton_text" v-if="thisPage != 1" @click="getComments(1)">처음</div>

            <div class="pageButton_text" v-for="i in pageList">
              <div class="text-xs-center thisPageClass pageButton" @click="getComments(i)" v-if="i === thisPage">{{i}}</div>
              <div class="pageButton" @click="getComments(i)" v-else>{{i}}</div>
            </div>

            <div class="pageButton_text" v-model="finalPage" @click="getComments(finalPage)">마지막</div>
          </div>
        </v-flex>
      </v-layout>

    </v-card>
  </v-flex>
</v-layout>
</template>

<script>
import Server from "../server.js"
import {
  store
} from "../store.js"

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
      tags: [],
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
    this.getCommentsTags();
  },
  mounted() {
    this.getCommentsInfo();
    this.getCommentsTime();
    this.getCommentsTags();

    // Get Chart
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
          labels: ["0am", "1am", "2am", "3am", "4am", "5am", "6am", "7am", "8am", "9am", "10am", "11am", "12pm", "1pm", "2pm", "3pm", "4pm", "5pm", "6pm", "7pm", "8pm", "9pm", "10pm", "11pm"],
          datasets: [{
            label: "시간대별 댓글 작성 추이",
            data: this.commentTime,
            borderColor: "#FA5882",
            backgroundColor: "#00000000",
            type: "line",
            pointRadius: 4,
            fill: false,
            lineTension: 0,
            borderWidth: 5
          }]
        },
      });
    }, 500);
  },

  computed: {
    dateFormmat() {
      var dDate = this.detailDate + "";
      return dDate.substring(0, 4) + " - " + dDate.substring(4, 6) + " - " + dDate.substring(6, 8);
    },
  },

  methods: {
    // Get Comment
    getComments(page) {
      let formData = new FormData();
      this.thisPage = page;
      this.getPages(this.thisPage);
      formData.append("news_num", this.detailNum);
      formData.append("page", this.thisPage);
      Server(this.$store.state.SERVER_URL).post("/api/get/comments", formData)
        .then(res => {
          this.comments = res.data;
        })
    },

    // Get Final Page Number and Page Number List
    getPages(page) {
      var self = this;
      var formData = new FormData();
      this.thisPage = page;
      formData.append("news_num", this.detailNum);
      formData.append("page", this.thisPage);
      Server(this.$store.state.SERVER_URL).post("/api/get/page_count", formData)
        .then(res => {
          self.pageList = res.data.page_list;
          self.finalPage = res.data.final_page;
        });
    },

    //get label of Comments
    getCommentsInfo() {
      let formData = new FormData();
      formData.append("news_num", this.detailNum);
      Server(this.$store.state.SERVER_URL).post("api/get/comments_label", formData)
        .then(res => {
          this.commentsCount = res.data[0].comment_cnt;
          this.positiveCount = res.data[0].news_positive;
          this.localCount = res.data[0].local_hit;
        })
    },

    // Get Chart Time
    getCommentsTime() {
      let formData = new FormData();
      formData.append("news_num", this.detailNum);
      Server(this.$store.state.SERVER_URL).post("/api/get/comments_time", formData)
        .then(res => {
          for (var i = 0; i < 24; i++) {
            this.commentTime[i] = 0
          }
          for (var i = 0; i < res.data.length; i++) {
            this.commentTime[res.data[i].hour] = res.data[i].hour_cnt;
          }
        })
    },

    // Get Tags
    getCommentsTags() {
      let formData = new FormData();
      formData.append("news_num", this.detailNum);
      Server(this.$store.state.SERVER_URL).post("/api/get/tags", formData)
        .then(res => {
          this.tags = res.data;
        })
    },

    //edit Comment Logistic
    editCommentLabelNews(comment) {
      var self = this;
      var form = new FormData();
      form.append("num", comment.comment_num);
      form.append("label_news", comment.label_news);

      Server(this.$store.state.SERVER_URL).post("/api/edit/label_news", form)
        .then(res => {
          if (comment.label_news == 0) {
            comment.label_news = 1;
          } else {
            comment.label_news = 0;
          }
        });
    },

    //edit Comment Local
    editCommentLabelLocal(comment) {
      var self = this;
      var form = new FormData();
      form.append("num", comment.comment_num);
      form.append("label_local", comment.label_local);

      Server(this.$store.state.SERVER_URL).post("/api/edit/label_local", form)
        .then(res => {
          if (comment.label_local == 0) {
            comment.label_local = 1;
          } else {
            comment.label_local = 0;
          }
        });
    },

    // Show Regional sentiment
    showLocalFunc() {
      this.showLocal = !this.showLocal
    },

    // Change Comments Time Format
    timeChang(time) {
      return time.replace('T', '\n')
    },
  }
}
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css?family=Song+Myung&display=swap");
@import url("https://fonts.googleapis.com/css?family=Noto+Serif+KR&display=swap");


.positionCenter {
  margin: 0 auto;
}

.divide{
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

#textCenter {
  text-align: center;
}

#PNChart {
  margin: 0 auto;
}

#PNChart,
#TimeChart {
  max-height: 300px;
}

.chartTitle{
  text-align: center;
  margin-top: 30px;
  margin-bottom: 15px;
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

.newsCommentLocal {
  margin-left: 10px;
  color: blue;
  font-size: 1rem;
}

.theme--light.v-pagination .v-pagination__item--active {
  color: black !important;
  border: 1px solid blue !important;
}

#newspaperContent {
  column-count: 2 !important;
  max-height: none;
  height: auto;
  overflow: visible;
}

.isLocalComment {
  color: red;
  font-weight: bold;
}

.pageButton_text {
  margin-right: 5px;
  margin-left: 5px;
  height: 30%;
  background-color: #ffffff;
  border-radius: 3px;
  border: 2px solid #dcdcdc;
  display: inline-block;
  cursor: pointer;
  color: #826d73;
  font-size: 16px;
  padding: 3px 5px;
  text-decoration: none;
  color: black;
}

.thisPageClass {
  color: black;
  font-size: 1.5rem;
  font-weight: bold;
}

.checks {
  margin-top: 15px;
  position: relative;
  display: inline-block;
  margin-left: 30px;
}

.checks input[type="checkbox"] {
  /* 실제 체크박스는 화면에서 숨김 */
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  border: 0
}

.checks input[type="checkbox"]+label {
  display: inline-block;
  position: relative;
  cursor: pointer;
}

.checks input[type="checkbox"]+label:before {
  content: ' ';
  display: inline-block;
  width: 21px;
  height: 21px;
  line-height: 21px;
  margin: -2px 8px 0 0;
  text-align: center;
  vertical-align: middle;
  background: #fafafa;
  border: 1px solid #cacece;
  border-radius: 3px;
  box-shadow: 0px 1px 2px rgba(0, 0, 0, 0.05), inset 0px -15px 10px -12px rgba(0, 0, 0, 0.05);
}

.checks input[type="checkbox"]+label:active:before,
.checks input[type="checkbox"]:checked+label:active:before {
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05), inset 0px 1px 3px rgba(0, 0, 0, 0.1);
}

.checks input[type="checkbox"]:checked+label:before {
  content: '\2714';
  color: #99a1a7;
  text-shadow: 1px 1px #fff;
  background: #e9ecee;
  border-color: #adb8c0;
  box-shadow: 0px 1px 2px rgba(0, 0, 0, 0.05), inset 0px -15px 10px -12px rgba(0, 0, 0, 0.05), inset 15px 10px -12px rgba(255, 255, 255, 0.1);
}

.checks.small input[type="checkbox"]+label {
  font-size: 12px;
}

.checks.small input[type="checkbox"]+label:before {
  width: 17px;
  height: 17px;
  line-height: 17px;
  font-size: 11px;
}

.checks.etrans input[type="checkbox"]+label {
  padding-left: 30px;
}

.checks.etrans input[type="checkbox"]+label:before {
  position: absolute;
  left: 0;
  top: 0;
  margin-top: 0;
  opacity: .6;
  box-shadow: none;
  border-color: #6cc0e5;
  -webkit-transition: all .12s, border-color .08s;
  transition: all .12s, border-color .08s;
}

.checks.etrans input[type="checkbox"]:checked+label:before {
  position: absolute;
  content: "";
  width: 10px;
  top: -5px;
  left: 5px;
  border-radius: 0;
  opacity: 1;
  background: transparent;
  border-color: transparent #6cc0e5 #6cc0e5 transparent;
  border-top-color: transparent;
  border-left-color: transparent;
  -ms-transform: rotate(45deg);
  -webkit-transform: rotate(45deg);
  transform: rotate(45deg);
}

.no-csstransforms .checks.etrans input[type="checkbox"]:checked+label:before {
  content: "\2714";
  top: 0;
  left: 0;
  width: 21px;
  line-height: 21px;
  color: #6cc0e5;
  text-align: center;
  border: 1px solid #6cc0e5;
}

.checks {
  float: right;
}



@media (max-width: 600px) {
  #newspaperTitle {
    font-size: 35px;
  }

  #newsComment .v-list__tile {
    padding: 0px 0px !important;
  }
}


</style>
