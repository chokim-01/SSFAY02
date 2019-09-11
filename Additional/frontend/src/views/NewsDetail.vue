<template>
  <v-layout row wrap id="newsDetail">
    <v-flex xs12 sm8 style="margin: 0 auto;">
      <v-card id="newspaper">
        <p id="newspaperTitle">조국 장관 취임 하루 만에 검찰개혁 시동</p>
        <v-layout row wrap>
          <v-flex  xs12 sm8 pa-3>
            {{ content }}
          </v-flex>
          <v-flex  xs12 sm4 pa-3>
            그래프
          </v-flex>
        </v-layout>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
  export default {
    name: "newsDetail",
    data () {
      return {
        content: '우여곡절 끝에 임명된 조국 법무부 장관이 취임 하루 만에 "원포인트" 인사를 내고 검찰개혁 작업에 본격 시동을 걸었다.\
법무부는 10일 "이종근(50·사법연수원 28기) 차장검사가 법무부에 파견돼 검찰개혁 추진 업무를 지원할 예정"이라며 "직책은 정해진 바 없다"고 밝혔다.\
이 차장검사는 박상기 전 법무부 장관 취임 직후인 2017년 8월부터 2년간 장관 정책보좌관으로 일했다.\
지난 7월말 중간간부 정기인사에서 인천지검 2차장으로 발령난 이 차장검사는 한 달여 만에 다시 법무부 파견 근무를 하게 됐다.\
이날 인사는 수사권조정과 고위공직자범죄수사처(공수처) 설치 등 박 전 장관 재임 시기 착수한 검찰개혁 작업의 연속성을 이어가기 위한 조치로 풀이된다.\
법무부는 정책기획단 등 법무정책 관련 업무를 하는 기존 조직과 별도로 검찰개혁을 전담할 부서를 신설하는 방안도 검토 중인 것으로 알려졌다.'
      }
    },
  }
</script>

<style>
@import url('https://fonts.googleapis.com/css?family=Song+Myung&display=swap');

#newsDetail {
  background-color: #D8D8D8;
  height: 100vh;
}

#newspaper {
  height: 90vh;
  margin: 5vh auto;
}
#newspaperTitle {
  font-family: 'Song Myung', serif;
  font-size: 3vw;
  text-align: center;
}
.pa40 {
  padding: 40px;
}
</style>
