<template>
  <v-layout row wrap id="newsDetail">
    <v-flex xs12 sm8 style="margin: 0 auto;" my-5>
      <v-card id="newspaper">
        <v-layout row wrap pb-4>
          <v-flex xs12 id="newspaperTitle" my-4>조국 장관 취임 하루 만에 검찰개혁 시동 </v-flex>
          <v-flex  xs12 sm8 pa-3 id="newspaperContent">
            {{ content }}
          </v-flex>
          <v-flex  xs12 sm4 pa-3 id="newspaperGraph">
            <v-layout row wrap>
              <canvas id="myChart" width="200" height="200"/>
              <v-flex xs12 mt-5>
                <v-chip v-for="i in 6" :key="i" outline color="red"> <!--  임시 -->
                  # 블라블라
                </v-chip>
              </v-flex>
            </v-layout>
          </v-flex>
        </v-layout>
      </v-card>
    </v-flex>
    <v-flex xs12 sm8 style="margin: 0 auto;" mb-5>
      <v-card id="newsComment">
        <h2>댓글 111개</h2>
        <v-list>
          <v-list-tile
            v-for="ii in 5"
            :key="ii+'ㅇ'"
            style="height: 35px !important; overflow: hidden;"
          >
          <v-list-tile-action>
            <v-chip label color="white" text-color="blue">
              <v-icon left>fas fa-thumbs-up</v-icon>긍정
            </v-chip>
          </v-list-tile-action>

            <v-list-tile-content>
              <v-list-tile-title v-text="tmp_comment"></v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>

          <v-list-tile
            v-for="ii in 5"
            :key="ii"
            style="height: 35px !important; overflow: hidden;"
          >
          <v-list-tile-action>
            <v-chip label color="white" text-color="red">
              <v-icon left>fas fa-thumbs-down</v-icon>부정
            </v-chip>
          </v-list-tile-action>

            <v-list-tile-content>
              <v-list-tile-title v-text="tmp_comment"></v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </v-list>
        <div style="text-align: center; margin-top: 20px;">
          <v-pagination
          v-model="commentPage"
          :length="6"
          color="blue"
          prev-icon="fas fa-chevron-left"
          next-icon="fas fa-chevron-right"
          id="newsCommentPage"
          ></v-pagination>
        </div>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import Chart from 'chart.js';
  export default {
    name: "newsDetail",
    data () {
      return {
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
      var ctx = document.getElementById('myChart');
      console.log(ctx)
      var myChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: ['긍정', '부정'],
          datasets: [{
            label: '# of Votes',
            data: [72, 28],
            backgroundColor: [
              '#01A9DB',
              '#FE2E64'
            ]
          }]
        }
      });
    }
  }
</script>

<style>
@import url('https://fonts.googleapis.com/css?family=Song+Myung&display=swap');

#newsDetail {
  background-color: #D8D8D8;
}
#newspaper {
  height: auto;
}
#newspaperTitle {
  overflow: hidden;
  font-family: 'Song Myung', serif;
  font-size: 40px;
  text-align: center;
}

#newspaperContent {
  height: 400px;
  overflow-y:scroll;
}
#newspaperGraph {
  overflow: hidden;
  text-align: center;
}
::-webkit-scrollbar {
  height: 100%;  /* 가로축 스크롤바 길이 */
}
::-webkit-scrollbar-thumb {
  border-radius: 20px;
  height: 5px;
  background-color: #BDBDBD;
}
::-webkit-scrollbar-thumb:hover {
  border-radius: 20px;
  height: 5px;
  background-color: #FACC2E;
}
::-webkit-scrollbar-button {
  width: 20px;
  height: 10px;
}
::-webkit-scrollbar-button:vertical:increment {
}
::-webkit-scrollbar-button:vertical:decrement {
}
::-webkit-scrollbar-corner {
  background-color: violet; /* 우측 하단의 코너 부분 */
}
::-webkit-resizer {
  background-color: green;
}
#newsComment {
  heigth: auto;
  min-height: 300px;
  padding: 20px;
}

#newsCommentPage i {
  transform: scale(0.6);
}

@media (max-width: 600px) {
  #myChart {
    width: 70% !important;
    height: 70% !important;
    margin: 0 auto;
  }
  #newspaperGraph {
    padding-top: 40px !important;
  }
}
</style>
