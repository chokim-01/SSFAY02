<template>
  <v-layout row wrap>
    <v-flex class="posCenter" xs12 sm8 mb-2>
        <v-layout row wrap pb-4>
          <v-flex id="newspaperTitle" xs12 >
            {{ detailTitle }}
          </v-flex>
          <v-flex class="text-xs-center" xs12 mb-4>
            <v-chip v-for="idx in 6" :key="idx" color="red" outline> <!--  임시 -->
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
        <v-flex xs12 sm1/>
        <v-flex xs12 sm5>
          <canvas id="PNChart" width="300" height="300"/>
        </v-flex>
        <v-flex xs12 sm4 mt-5>
          <canvas id="TimeChart" width="300" height="300"/>
        </v-flex>
      </v-layout>
    </v-flex>
    <v-flex class="posCenter" xs12 sm8 mb-5>
      <v-card id="newsComment" flat>
        <h2>댓글 111개</h2>
        <v-list>
          <template v-for="tmpIdx in 5" class="cmtRow">
              <v-layout class="mh50" :key="tmpIdx+'key'" row wrap>
                <v-flex class="newsCommentRow" xs12 sm2><b>2019-09-19</b></v-flex>
                <v-flex class="newsCommentRow" v-text="tmp_comment" xs10 sm9></v-flex>
                <v-flex xs2 sm1><v-chip color="white" text-color="blue" label>
                  <v-icon left>fas fa-thumbs-up</v-icon>
                  <v-flex hidden-xs-only>긍정</v-flex>
                </v-chip></v-flex>
              </v-layout>
              <v-divider />
              <v-layout class="mh50" :key="tmpIdx+'key2'" row wrap>
                <v-flex class="newsCommentRow" xs12 sm2><b>2019-09-19</b></v-flex>
                <v-flex class="newsCommentRow" v-text="tmp_comment" xs10 sm9></v-flex>
                <v-flex xs2 sm1><v-chip color="white" text-color="red" label>
                  <v-icon left>fas fa-thumbs-down</v-icon>
                  <v-flex hidden-xs-only>부정</v-flex>
                </v-chip></v-flex>
              </v-layout>
            <v-divider />
          </template>
        </v-list>
        <div class="commentPage">
          <v-pagination
          id="newsCommentPage"
          v-model="commentPage"
          :length="5"
          color="blue"
          prev-icon="fas fa-chevron-left"
          next-icon="fas fa-chevron-right"
          ></v-pagination>
        </div>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import Chart from "chart.js";
export default {
  name: "NewsDetail",
  data () {
    return {
      detailTitle: this.$route.params.detailTitle,
      detailContext: this.$route.params.detailContext,
      detailDate: this.$route.params.detailDate,
      detailNum: this.$route.params.detailNum,
      myDoughnutChart: null,
      doughnutData: null,
      tmp_comment: "고통이 고통이라는 이유로 그 자체를 사랑하고 소유하려는 자는 없다.",
      commentPage: 1
    }
  },
  mounted() {
    var docPNChart = document.getElementById("PNChart");
    var pnChart = new Chart(docPNChart, {
      type: "doughnut",
      data: {
        labels: ["긍정", "부정"],
        datasets: [{
          label: "# of Votes",
          data: [72, 28],
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
          data: [20000, 14000, 12000, 15000, 18000, 19000, 22000,20000, 14000, 12000, 15000, 18000, 19000, 22000],
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
  },
  computed: {
    dateFormmat() {
      var dDate = this.detailDate+"";
      return dDate.substring(0,4) +" - "+dDate.substring(4,6)+" - "+dDate.substring(6,8);
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

#newspaperContent{
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

#PNChart, #TimeChart {
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
  background-color: #00000000;
}

.newsCommentRow {
  padding:12px 0px;
}

.cmtRow {
  height: 35px !important;
  overflow: hidden;
}

.mh50 {
  min-height: 50px;
}

#newsComment * {
  background-color: inherit !important;
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

  #newspaperContent{
    column-count: 2 !important;
    max-height: none;
    height: auto;
    overflow: visible;
  }
}
</style>
