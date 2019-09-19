<template>
  <v-layout row wrap>
    <v-flex class="posCenter" xs12 sm8 mb-2>
        <v-layout row wrap pb-4>
          <v-flex id="newspaperTitle" xs12 >
            {{ title }}
          </v-flex>
          <v-flex class="text-xs-center" xs12 mb-4>
            <v-chip v-for="idx in 6" :key="idx" color="red" outline> <!--  임시 -->
              # 블라블라
            </v-chip>
          </v-flex>
          <v-flex class="text-xs-right" xs12 px-4>2019-09-18 00:00:00</v-flex>
          <v-flex id="newspaperContent" xs12 pa-3>
            {{ content }}
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
              <v-layout :key="tmpIdx+'key'" class="mh50" row wrap>
                <v-flex class="newsCommentRow" xs12 sm2><b>2019-09-19</b></v-flex>
                <v-flex class="newsCommentRow" v-text="tmp_comment" xs10 sm9></v-flex>
                <v-flex xs2 sm1><v-chip color="white" text-color="blue" label>
                  <v-icon left>fas fa-thumbs-up</v-icon>
                  <v-flex hidden-xs-only>긍정</v-flex>
                </v-chip></v-flex>
              </v-layout>
              <v-divider />
              <v-layout :key="tmpIdx+'key2'" class="mh50" row wrap>
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
      title: "조국 장관 취임 하루 만에 검찰개혁 시동",
      content: '**장 의원 "사건 이후, 해도 해도 너무한 기사들이 나와도 못난 아들 둔 죄로 참고 또 참고 있었지만 이건 너무 한 것 아닙니까?"**\
      장제원(사진) 자유한국당 의원 아들인 래퍼 장용준(19·활동명 "노엘")씨가 음주운전 혐의로 경찰 수사를 받는 가운데, 사건 당시 장씨 대신 운전을 했다고 허위진술을 했던 남성 김모(27)씨가 10일 경찰에 출석해 약 3시간 동안 조사를 받았다.\
      "(장씨를) 도와주려는 생각으로 나간 것인가", "부탁은 뭐라고 받았나", "보도된 내용 중 억울하거나 잘못된 내용이 있나"라는 질문에는 답을 하지 않았다.\
      범인도피 혐의로 입건된 김씨는 피의자 신분 조사를 받기 위해 이날 오후 5시18분쯤 서울 마포경찰서에 도착했다.\
      다만 그는 "(장씨가 아버지인) 장제원 의원을 언급했나"라고 묻자 "(그런 적) 없습니다"라고 말했고, "바꿔치기 부탁 받은 적 있느냐"는 질문에는 "성실하게 조사에 임하겠다"는 대답으로 대신했다.\
      현장 경찰이 측정한 장씨의 혈중 알코올농도는 0.08% 이상으로 "면허 취소" 수준에 해당한 것으로 전해졌다.\
      장씨의 변호인인 이상민 변호사는 이날 마포경찰서에서 기자들을 만나 김씨에 대해 "의원실, 소속사 관계자 모두 아니다. 쉽게 말해 아는 형"이라고 말했다.\
      ◆대신 운전해 준 남성 "장용준, 장제원 의원 언급한 적 없다"\
      민주당 이해식 대변인은 "장씨는 만취상태에서 운전한 것도 모자라 금품으로 비위사실을 숨기려 했고 음주운전 사실 자체를 은폐하려 했다"며 "특히 자신이 운전했다고 주장한 사람이 "장 의원과 관계있는 사람"이라는 의혹이 증폭되고 있다. 수사당국은 이 모든 정황과 비위에 대해 철저히 수사해 진실을 밝혀야 한다"고 논평했다.\
      정의당 유상진 대변인은 논평을 통해 "면허취소 수준의 음주운전으로 교통사고를 일으킨 것만으로도 부족해 사건을 덮기 위한 피해자 회유 및 운전자 바꿔치기 시도가 있었다는 것은 죄질이 극히 나쁜 심각한 범죄행위"라며 "장 의원이 직접 국회의원 신분을 이용해 사건을 은폐·무마하려 한 것은 아닌지 경찰은 철저하고 엄정한 수사를 해야 한다"고 강조했다.\
      민주평화당 이승한 대변인은 "음주운전은 범죄이고 살인의도"라며 "성인이 된 아들의 무책임한 사고와 불합리한 처신을 아버지가 모두 책임질 수는 없지만 지난 조 후보자 인사청문회에서 조 후보자에게 집요하게 얘기했던 장 의원의 후보자 사퇴 얘기가 오버랩된다"고 지적했다.\
      바른미래당도 장 의원을 비판했으나, "사퇴"는 거론하지 않았다.\
      이 대변인은 "살아가면서 자식을 부모가 어떻게 할 수 없는 것도 있다 한다. 그러나 장 의원 역시 공인이자 국민의 기대를 받는 정치인으로서 상황을 더욱 무겁게 받아들이기 바란다"며 "진솔한 아버지이자 엄한 아버지이기를 바란다. 아울러 무한 책임의식을 잊지 않는 정치인이기를 바란다"고 덧붙였다.\
      김학용 한국당 의원은 9일 장씨가 음주운전 사고로 경찰에 적발된 것과 관련, "장 의원에 대한 비난으로 조국 법무부 장관 후보자가 임명될 수 있기를 바란다면 이는 손바닥으로 하늘을 가리는 격"이라며 "더 이상 국민을 우습게 보지 말고, 비열한 물타기를 중단하기 바란다"고 밝혔다.\
      그는 "노엘의 행위는 비난받아 마땅하며 아버지인 장 의원도 도의적 책임을 피할 수 없으나 조 후보자와 장 의원의 경우는 비할 수 없이 다르다"라며 "조 후보자의 케이스는 딸의 입시를 돕기 위해 부모가 부당한 스펙 만들기에 개입하고, 급기야는 상장까지 위조한 입시 부정 게이트다. 조 후보자에게 쏟아지는 실망과 비난은 딸의 잘못 탓이 아닌 부모의 잘못과 처신에서 비롯된 것"이라고 썼다.\
      ◆장제원 "내 의원실 관계자를 아들 대신 운전했다고 시킬 정도로 나쁜 사람 아니다"\
      장 의원은 10일 자신의 페이스북에 "아들이 운전자로 바꿔치기 하려 했다는 30대 남성 A씨라는 사람은 제 의원실과는 어떠한 관련도 없는 사람임을 분명히 밝힌다"고 썼다.\
      이어 "이 기사에 대해 기사 삭제 및 정정 보도를 요청할 뿐만 아니라 할 수 있는 모든 민형사상의 법적 대응을 할 것임을 분명히 밝힌다"라고 썼다.\
      그러면서 "제가 아무리, 저의 의원실 관계자를 제 아들 대신 운전을 했다고 시킬 그토록 나쁜 사람은 아니"라면서 "사건 이후, 해도 해도 너무한 기사들이 나와도 못난 아들 둔 죄로 참고 또 참고 있었지만 이건 너무 한 것 아닙니까?"라고 글을 끝맺었다.\
      hjksegye.com\
      ⓒ 세상을 보는 눈, ',
      myDoughnutChart: null,
      doughnutData: null,
      tmp_comment: "고통이 고통이라는 이유로 그 자체를 사랑하고 소유하려는 자는 없다.",
      commentPage: 1
    }
  },
  mounted() {
    var ctx = document.getElementById('PNChart');
    var myChart = new Chart(ctx, {
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

    var ctx2 = document.getElementById("TimeChart").getContext("2d");
    var chart = new Chart(ctx2, {
    type: 'line',
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
  font-family: 'Noto Serif KR', serif;
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
